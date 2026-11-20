# Massinha 30

<div align="center">
  <img src="capa/logo.svg" alt="Arckhé AI" height="48" />
  <p><strong>Arckhé AI</strong></p>
</div>


[![Massinha 30](guia/assets/banner.jpg)](https://inematds.github.io/massinha-30/guia/)

**ðŸ‡§ðŸ‡· [PortuguÃªs](README.md) Â· ðŸ‡ºðŸ‡¸ [English](README.en.md) Â· ðŸ‡ªðŸ‡¸ [EspaÃ±ol](README.es.md)**

## O que Ã©

VocÃª tem uma ideia de histÃ³ria, mas fazer os personagens, a voz e as cenas combinarem dÃ¡ trabalho. Massinha 30 Ã© um kit para criar narrativas curtas com aparÃªncia de massinha artesanal. Ele organiza o roteiro aprovado, as referÃªncias dos personagens, os clipes gerados no Kling, a narraÃ§Ã£o ElevenLabs e as legendas. Serve a criadores que querem repetir o processo em novas histÃ³rias. Para produzir, Ã© preciso ter acesso aos serviÃ§os de geraÃ§Ã£o; o guia pode ser lido gratuitamente.

## Guia de uso

https://inematds.github.io/massinha-30/guia/

Abra o projeto no Codex e peÃ§a: â€œUse skills/massinha-30/SKILL.md para criar uma nova histÃ³ria de massinhaâ€. Leia [o fluxo completo](skills/massinha-30/references/producao.md).

Python 3.10+, FFmpeg/ffprobe com libass, CLI Kling oficial autenticada e ElevenLabs configurado. As imagens sÃ£o geradas pelo agente com image_gen pela assinatura. A instalaÃ§Ã£o nÃ£o gera vÃ­deo nem faz chamada paga.

```bash
git clone https://github.com/inematds/massinha-30.git
cd massinha-30
python3 -m unittest discover -s tests -v
python3 skills/massinha-30/scripts/pipeline.py iniciar exemplos/retalhos.json --out runs/retalhos
```

O exemplo espera aprovaÃ§Ã£o explÃ­cita do roteiro. `voz` e `kling` sÃ³ enviam a provedores com `--enviar`. Credenciais no ambiente ou `--env-file`, nunca no repositÃ³rio. Nenhum modelo de vÃ­deo roda localmente.

## Estado

v1.1.0: demonstraÃ§Ã£o real de 30 segundos produzida com Kling e ElevenLabs; oito testes locais passaram. Cortes de cena e legendas alinhados Ã  voz, arquivos editÃ¡veis disponÃ­veis na Release. Fish e Agnes continuam como alternativas sem adaptador neste kit.

A montagem exporta limpo.mp4 e final.mp4 (30s, 720Ã—1280, 30fps, H.264/AAC), alÃ©m de legendas.srt. O Ã¡udio original do Kling Ã© descartado; trilha e efeitos entram como arquivos separados. A verificaÃ§Ã£o tÃ©cnica nÃ£o substitui assistir com som.

## LicenÃ§a

MIT. NÃ£o inclui licenÃ§as de mÃºsica, fontes, marcas ou condiÃ§Ãµes dos provedores.

ðŸŽ¬ [Assistir Ã  histÃ³ria](https://inematds.github.io/massinha-30/guia/#video) Â· [MP4](https://github.com/inematds/massinha-30/releases/download/demo-v1.1.0/massinha-30-retalhos.mp4)

---

<div align="center">
  <img src="capa/logo.svg" alt="Arckhé AI" height="32" />
  <p><strong>Arckhé AI</strong></p>
</div>