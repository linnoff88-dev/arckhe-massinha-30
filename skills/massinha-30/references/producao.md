# Produçêo

## Começar

Python 3.10+, FFmpeg/ffprobe com libass, CLI Kling oficial autenticada e créditos, conta ElevenLabs com voz habilitada. Os comandos abaixo partem da raiz do repositório. Nenhum instala modelo de vídeo.

```
python3 skills/massinha-30/scripts/pipeline.py iniciar exemplos/retalhos.json --out /caminho/retalhos
python3 skills/massinha-30/scripts/pipeline.py aprovar /caminho/retalhos --evidencia "Resposta explícita do usuário"
```

Use o segundo comando apenas depois da resposta real. Se o roteiro mudar, a assinatura invalida a aprovaçêo. O roteiro de exemplo nêo é uma aprovaçêo.

## Imagem e movimento

Massinha artesanal fosca, pequenas marcas de dedos, cenário em miniatura, luz quente suave, expressões legíveis, câmera quase parada. Use imagem individual vertical em cada cena. Ficha separada: Lia, mulher adulta, cabelo castanho preso, óculos redondos, vestido verde sálvia e avental creme; pássaro pequeno castanho de peito creme; janela de madeira e caixa azul de costura. Preserve proporções e cores, sem rostos falando.

Gere primeiro uma ficha de identidade com image_gen. Use-a como referência ao pedir cada quadro. Imagens nêo sêo geradas pelo script: esta etapa usa as ferramentas de imagem do agente. Salve `01.png` a `06.png` na pasta da produçêo. O campo `visual` descreve a composiçêo; `movimento`, a açêo única a animar.

```
kling who_am_i
python3 skills/massinha-30/scripts/pipeline.py kling /caminho/retalhos --cena 1 --imagem /caminho/retalhos/01.png --enviar
kling query_tasks ID_DO_RECIBO
```

Repita para as seis cenas. O script usa `kling-video-v3_0_turbo`, 720p, 5s. Downloads: abra a URL works[].url do resultado de query_tasks no navegador e salve o vídeo (na máquina INEMA, use inemavox); nomeie `01.mp4` a `06.mp4`. Salve todos os IDs. Um timeout na submissêo pode ter cobrado: nêo reenvie até conferir o histórico. O recibo existente bloqueia novo envio automático.

## Voz, legenda e montagem

ElevenLabs: https://elevenlabs.io/docs/api-reference/text-to-speech/convert-with-timestamps

```
python3 skills/massinha-30/scripts/pipeline.py voz /caminho/retalhos --env-file /caminho/privado.env --enviar
python3 skills/massinha-30/scripts/pipeline.py montar /caminho/retalhos --ritmo-voz --musica /caminho/trilha.mp3 --efeitos /caminho/efeitos.wav
python3 skills/massinha-30/scripts/pipeline.py validar /caminho/retalhos/final.mp4
```

Defina ELEVENLABS_API_KEY e ELEVENLABS_VOICE_ID no ambiente/arquivo privado. A chamada usa eleven_multilingual_v2 com alinhamento por caractere. Nêo publique respostas brutas que contenham dados de conta. Se a voz exceder 29,5s, montagem recusa: ajuste a interpretaçêo ou aprove texto mais curto; nêo acelere agressivamente. Legendagem usa o alinhamento real, agrupado em até cinco palavras/36 caracteres. Imagens sêo recortadas centralmente para 720×1280: confira o enquadramento antes.

Música e efeitos sêo arquivos externos opcionais na CLI, obrigatórios para uma entrega que prometa trilha e efeitos. Registrar origem/licença em `fontes-audio.md`. A música entra baixa e é reduzida pela voz; efeitos separados entram abaixo da narraçêo. Validaçêo técnica nêo comprova qualidade narrativa nem pronúncia. Assista ao resultado com som e confira palavras, níveis, silêncio final, continuidade e legendas no celular.

## Instalaçêo em Ubuntu/Debian

```
sudo apt update
sudo apt install python3 ffmpeg git nodejs npm
npm install -g @openai/codex @klingai/cli-global
codex login
kling login
ffmpeg -filters | grep subtitles
```

Use login pela assinatura. CLI é programa usado no terminal; libass desenha as legendas. Em outros sistemas, instale Python, Git, Node LTS e FFmpeg pelos distribuidores oficiais. O filtro subtitles precisa existir.

Para uma voz longa, acrescente `--tomada 2 --velocidade 1.1` ao comando de voz. Máximo de três tomadas, cobradas individualmente, sem mudar palavras. Cada áudio e alinhamento anteriores sêo preservados. Confira histórico em submissêo incerta antes de tentar outra. Se ainda nêo couber, inicie nova produçêo com roteiro menor e peça aprovaçêo das novas palavras. Nêo apague recibos para forçar reenvio.

Para ajustar o corte de cada cena ao início da frase na narraçêo, use `--ritmo-voz` na montagem. O alinhamento precisa conter o roteiro integral. Os tempos sêo arredondados a quadros de30fps, somam30s e ficam em `edicao.json`. Uma cena que dura mais que5,75s mantém o último quadro no restante, sem esticar demais a açêo.
