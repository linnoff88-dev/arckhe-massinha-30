#!/usr/bin/env python3
"""Massinha 30: estado verificável, provedores externos e montagem local sem IA de vídeo."""
import argparse
import base64
import hashlib
import json
import os
import re
import shlex
from pathlib import Path
import subprocess
import sys
import urllib.request


def save(path, value):
    path = Path(path)
    tmp = path.with_suffix(path.suffix + '.tmp')
    tmp.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n')
    tmp.replace(path)


def digest(story):
    return hashlib.sha256(json.dumps(story, ensure_ascii=False, sort_keys=True).encode()).hexdigest()


def load_run(folder, approved=True):
    folder = Path(folder).resolve()
    run = json.loads((folder / 'run.json').read_text())
    story = json.loads((folder / 'roteiro.json').read_text())
    if approved and run.get('aprovacao', {}).get('sha256') != digest(story):
        raise ValueError('Roteiro sem aprovação válida: obtenha resposta explícita antes de gerar.')
    return folder, run, story


def probe(path):
    p = subprocess.run(['ffprobe', '-v', 'error', '-show_streams', '-show_format', '-of', 'json', str(path)],
                       check=True, capture_output=True, text=True, timeout=30)
    return json.loads(p.stdout)


def duration(path):
    return float(probe(path)['format']['duration'])


def scene_durations(story, alignment):
    text = ''.join(alignment['characters'])
    starts, offset = [0], 0
    for i, scene in enumerate(story['cenas']):
        at = text.find(scene['texto'], offset)
        if at < 0:
            raise ValueError('Alinhamento não contém o roteiro integral; confira texto e voz.')
        if i:
            starts.append(round(alignment['character_start_times_seconds'][at] * 30))
        offset = at + len(scene['texto'])
    frames = [b-a for a, b in zip(starts, starts[1:] + [900])]
    if any(x <= 0 for x in frames):
        raise ValueError('Tempos de cenas inválidos.')
    return [x / 30 for x in frames]


def master_audio(folder):
    src = folder / 'limpo.mp4'
    analysis = subprocess.run(['ffmpeg', '-hide_banner', '-i', str(src), '-af',
        'loudnorm=I=-14:TP=-1.5:LRA=9:print_format=json', '-f', 'null', '-'],
        check=True, capture_output=True, text=True, timeout=90)
    metrics = json.loads(analysis.stderr[analysis.stderr.rfind('{'):])
    save(folder / 'master-medicao.json', metrics)
    fl = ('loudnorm=I=-14:TP=-1.5:LRA=9:measured_I=' + metrics['input_i']
          + ':measured_TP=' + metrics['input_tp'] + ':measured_LRA=' + metrics['input_lra']
          + ':measured_thresh=' + metrics['input_thresh'] + ':offset=' + metrics['target_offset'] + ':linear=true')
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', str(src), '-vn', '-af', fl,
                    '-t', '30', '-ar', '48000', '-c:a', 'aac', '-b:a', '192k', str(folder / 'master.m4a')],
                   check=True, timeout=90)
    tmp = folder / 'limpo-master.mp4'
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', str(src), '-i', str(folder / 'master.m4a'),
                    '-map', '0:v', '-map', '1:a', '-t', '30', '-c', 'copy', '-movflags', '+faststart', str(tmp)],
                   check=True, timeout=90)
    tmp.replace(src)


def timestamp(t):
    ms = round(t * 1000)
    return f'{ms//3600000:02}:{ms//60000%60:02}:{ms//1000%60:02},{ms%1000:03}'


def captions(alignment):
    chars = alignment['characters']
    starts = alignment['character_start_times_seconds']
    ends = alignment['character_end_times_seconds']
    if not chars or not (len(chars) == len(starts) == len(ends)):
        raise ValueError('Alinhamento inconsistente')
    words, word = [], ''
    for c, start, end in zip(chars + [' '], starts + [ends[-1]], ends + [ends[-1]]):
        if c.isspace():
            if word:
                words.append((word, ws, we))
                word = ''
        else:
            if not word:
                ws = start
            word += c
            we = end
    groups, group = [], []
    for w in words:
        if group and (len(group) >= 5 or len(' '.join(x[0] for x in group) + ' ' + w[0]) > 36):
            groups.append(group)
            group = []
        group.append(w)
        if w[0].endswith(('.', '!', '?', ';')):
            groups.append(group)
            group = []
    if group:
        groups.append(group)
    return '\n\n'.join(f'{i}\n{timestamp(g[0][1])} --> {timestamp(g[-1][2])}\n' + ' '.join(x[0] for x in g)
                       for i, g in enumerate(groups, 1)) + '\n'


def iniciar(args):
    story = json.loads(Path(args.roteiro).read_text())
    if len(story.get('cenas', [])) != 6 or any(not all(s.get(k) for k in ('texto', 'visual', 'movimento')) for s in story['cenas']):
        raise ValueError('Forneça seis cenas com texto, visual e movimento.')
    folder = Path(args.out).resolve()
    folder.mkdir(parents=True, exist_ok=True)
    if (folder / 'run.json').exists():
        raise ValueError('Produção já existe; retome-a sem sobrescrever.')
    save(folder / 'roteiro.json', story)
    save(folder / 'run.json', {'versao': '1.1.0', 'etapa': 'aguardando-aprovacao', 'titulo': story['titulo']})
    (folder / 'narracao.txt').write_text(' '.join(s['texto'] for s in story['cenas']))
    print(folder)


def aprovar(args):
    folder, run, story = load_run(args.pasta, False)
    if not args.evidencia.strip():
        raise ValueError('Informe a resposta real do usuário.')
    run['aprovacao'] = {'sha256': digest(story), 'evidencia': args.evidencia}
    run['etapa'] = 'aprovado'
    save(folder / 'run.json', run)
    print('Aprovação registrada para este roteiro.')


def kling(args):
    folder, run, story = load_run(args.pasta)
    if not 1 <= args.cena <= 6:
        raise ValueError('Cena deve estar entre 1 e 6.')
    image = Path(args.imagem).resolve()
    if not image.is_file():
        raise ValueError('Imagem não encontrada')
    prompt = ('Animação artesanal de massinha fosca com marcas sutis de dedos, cenário em miniatura, '
              'luz quente suave e câmera estável. Preserve identidade e cenário da imagem. '
              + story['cenas'][args.cena - 1]['movimento']
              + ' Personagens atuam em silêncio. Sem fala, narração, música, textos ou logotipos.')
    cmd = ['kling', 'image_to_video', '--model', 'kling-video-v3_0_turbo', '--image', str(image),
           '--duration', '5', '--resolution', '720p', prompt]
    if not args.enviar:
        print(json.dumps(cmd, ensure_ascii=False))
        return
    receipt = folder / f'kling-{args.cena:02}.json'
    if receipt.exists():
        raise ValueError('Recibo já existe; confira query_tasks/histórico antes de nova submissão.')
    save(receipt, {'estado': 'submissao-iniciada', 'cena': args.cena, 'prompt': prompt})
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=180)
    save(receipt, {'returncode': result.returncode, 'stdout': result.stdout, 'stderr': result.stderr, 'prompt': prompt})
    if result.returncode:
        raise ValueError(f'Kling falhou; confira {receipt.name}, sem reenviar às cegas.')
    print(receipt)


def env_values(path):
    values = dict(os.environ)
    if path:
        for line in Path(path).read_text().splitlines():
            line = line.strip()
            if not line or line.startswith('#') or '=' not in line:
                continue
            k, v = line.removeprefix('export ').split('=', 1)
            parts = shlex.split(v, comments=True)
            values.setdefault(k.strip(), parts[0].strip() if parts else '')
    return values


def voz(args):
    folder, run, story = load_run(args.pasta)
    if not 1 <= args.tomada <= 3 or not 0.85 <= args.velocidade <= 1.15:
        raise ValueError('Use tomada 1–3 e velocidade 0.85–1.15; preserve dicção natural.')
    text = ' '.join(s['texto'] for s in story['cenas'])
    if not args.enviar:
        print('Ensaio: ElevenLabs eleven_multilingual_v2,', len(text), 'caracteres. Sem chamada externa.')
        return
    marker = folder / f'voz-submissao-{args.tomada:02}.json'
    if marker.exists():
        raise ValueError('Voz já submetida; confira arquivos/histórico antes de gerar de novo.')
    env = env_values(args.env_file)
    key, voice = env.get('ELEVENLABS_API_KEY'), env.get('ELEVENLABS_VOICE_ID')
    key, voice = (key or '').strip(), (voice or '').strip()
    if not key or not voice:
        raise ValueError('Configure ELEVENLABS_API_KEY e ELEVENLABS_VOICE_ID em arquivo privado/ambiente.')
    if not re.fullmatch(r'[A-Za-z0-9_-]+', voice):
        raise ValueError('ID de voz inválido; confira o valor no arquivo privado.')
    req = urllib.request.Request('https://api.elevenlabs.io/v1/text-to-speech/' + voice + '/with-timestamps',
        data=json.dumps({'text': text, 'model_id': 'eleven_multilingual_v2',
                         'voice_settings': {'stability': 0.5, 'similarity_boost': 0.75, 'speed': args.velocidade}}).encode(),
        headers={'xi-api-key': key, 'Content-Type': 'application/json'})
    save(marker, {'estado': 'submissao-iniciada', 'texto_sha256': digest(story)})
    with urllib.request.urlopen(req, timeout=180) as response:
        result = json.load(response)
    audio = base64.b64decode(result['audio_base64'], validate=True)
    (folder / f'narracao-tomada-{args.tomada:02}.mp3').write_bytes(audio)
    (folder / 'narracao.mp3').write_bytes(audio)
    alignment = result.get('alignment') or result.get('normalized_alignment')
    if not alignment:
        raise ValueError('Áudio salvo; resposta não trouxe alinhamento para legendas.')
    save(folder / 'alinhamento.json', alignment)
    save(folder / f'alinhamento-{args.tomada:02}.json', alignment)
    (folder / 'legendas.srt').write_text(captions(alignment))
    measured = duration(folder / 'narracao.mp3')
    run['voz'] = {'provedor': 'ElevenLabs', 'duracao': measured, 'roteiro_sha256': digest(story)}
    save(folder / 'run.json', run)
    save(marker, {'estado': 'concluido', 'duracao': measured})
    print('Voz salva, duração medida:', measured)


def montar(args):
    folder, run, story = load_run(args.pasta)
    if run.get('voz', {}).get('roteiro_sha256') != digest(story):
        raise ValueError('Voz não corresponde ao roteiro aprovado.')
    voice = folder / 'narracao.mp3'
    if duration(voice) > 29.5:
        raise ValueError('Voz excede 29,5 s; ajuste a interpretação ou aprove texto mais curto.')
    if not (folder / 'legendas.srt').is_file():
        raise ValueError('Faltam legendas alinhadas à voz.')
    lengths = scene_durations(story, json.loads((folder / 'alinhamento.json').read_text())) if args.ritmo_voz else [5.0] * 6
    save(folder / 'edicao.json', {'duracoes': lengths, 'ritmo_voz': args.ritmo_voz, 'fps': 30})
    for i in range(1, 7):
        src = folder / f'{i:02}.mp4'
        if duration(src) < 4.96:
            raise ValueError(f'{src.name}: clipe menor que cinco segundos.')
        target = lengths[i - 1]
        motion = min(target, 5.75)
        vf = (f'trim=duration=5,setpts=(PTS-STARTPTS)*{motion/5:.9f},'
              'scale=720:1280:force_original_aspect_ratio=increase,crop=720:1280,setsar=1,fps=30,'
              f'tpad=stop_mode=clone:stop_duration={max(0, target-motion)+0.1:.9f}')
        subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', str(src), '-an', '-t', str(target), '-vf', vf,
                        '-c:v', 'libx264', '-threads', '2', '-preset', 'fast', '-crf', '20', '-pix_fmt', 'yuv420p',
                        str(folder / f'normal-{i:02}.mp4')], check=True, timeout=180)
    (folder / 'concat.txt').write_text(''.join(f"file 'normal-{i:02}.mp4'\n" for i in range(1, 7)))
    cmd = ['ffmpeg', '-v', 'error', '-y', '-f', 'concat', '-safe', '0', '-i', 'concat.txt', '-i', 'narracao.mp3']
    filters = ['[1:a]apad,asplit=2[v][key]'] if args.musica else ['[1:a]apad[v]']
    streams = ['[v]']
    if args.musica:
        cmd += ['-stream_loop', '-1', '-i', str(Path(args.musica).resolve())]
        filters += ['[2:a]volume=0.15[m]', '[m][key]sidechaincompress=threshold=0.03:ratio=6:attack=10:release=350[duck]']
        streams += ['[duck]']
    if args.efeitos:
        idx = 3 if args.musica else 2
        cmd += ['-i', str(Path(args.efeitos).resolve())]
        filters += [f'[{idx}:a]volume=0.35[sfx]']
        streams += ['[sfx]']
    filters += [''.join(streams) + f'amix=inputs={len(streams)}:duration=longest:normalize=0,loudnorm=I=-14:TP=-1:LRA=9,afade=t=out:st=29:d=1[a]']
    cmd += ['-filter_complex', ';'.join(filters), '-map', '0:v', '-map', '[a]', '-t', '30', '-c:v', 'copy',
            '-c:a', 'aac', '-b:a', '192k', '-movflags', '+faststart', 'limpo.mp4']
    subprocess.run(cmd, cwd=folder, check=True, timeout=180)
    master_audio(folder)
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', 'limpo.mp4', '-vf',
                    "subtitles=legendas.srt:force_style='FontName=DejaVu Sans,FontSize=15,Bold=1,PrimaryColour=&H0000FFFF,OutlineColour=&H00101010,BorderStyle=1,Outline=2,MarginV=65'",
                    '-t', '30', '-c:v', 'libx264', '-threads', '2', '-crf', '20', '-preset', 'fast', '-c:a', 'copy',
                    '-movflags', '+faststart', 'final.mp4'], cwd=folder, check=True, timeout=180)
    run['etapa'] = 'montado-aguarda-revisao'
    run['audio'] = {'musica': bool(args.musica), 'efeitos': bool(args.efeitos)}
    save(folder / 'run.json', run)
    print(folder / 'final.mp4')


def validar(args):
    info = probe(args.video)
    video = next(x for x in info['streams'] if x['codec_type'] == 'video')
    audio = next((x for x in info['streams'] if x['codec_type'] == 'audio'), {})
    n, d = map(int, video['avg_frame_rate'].split('/'))
    report = {'duracao': float(info['format']['duration']), 'largura': video['width'], 'altura': video['height'],
              'fps': n/d, 'video': video['codec_name'], 'audio': audio.get('codec_name')}
    checks = [abs(report['duracao'] - 30) <= 1/30 + 0.001, video['width'] * 16 == video['height'] * 9,
              abs(n/d - 30) < 0.001, video['codec_name'] == 'h264', audio.get('codec_name') == 'aac']
    report['aprovado_tecnicamente'] = all(checks)
    print(json.dumps(report, ensure_ascii=False))
    if not all(checks):
        raise ValueError('Arquivo fora do contrato 30s, 9:16, 30fps, H.264/AAC.')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='comando', required=True)
    p = sub.add_parser('iniciar'); p.add_argument('roteiro'); p.add_argument('--out', required=True); p.set_defaults(func=iniciar)
    p = sub.add_parser('aprovar'); p.add_argument('pasta'); p.add_argument('--evidencia', required=True); p.set_defaults(func=aprovar)
    p = sub.add_parser('kling'); p.add_argument('pasta'); p.add_argument('--cena', type=int, required=True); p.add_argument('--imagem', required=True); p.add_argument('--enviar', action='store_true'); p.set_defaults(func=kling)
    p = sub.add_parser('voz'); p.add_argument('pasta'); p.add_argument('--env-file'); p.add_argument('--tomada', type=int, default=1); p.add_argument('--velocidade', type=float, default=1.0); p.add_argument('--enviar', action='store_true'); p.set_defaults(func=voz)
    p = sub.add_parser('montar'); p.add_argument('pasta'); p.add_argument('--musica'); p.add_argument('--efeitos'); p.add_argument('--ritmo-voz', action='store_true'); p.set_defaults(func=montar)
    p = sub.add_parser('validar'); p.add_argument('video'); p.set_defaults(func=validar)
    args = parser.parse_args()
    try:
        args.func(args)
    except (ValueError, KeyError, OSError, subprocess.SubprocessError) as exc:
        print('ERRO:', exc, file=sys.stderr)
        return 1
    return 0


if __name__ == '__main__':
    sys.exit(main())
