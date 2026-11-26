ï»¿# Massinha 30

<div align="center">
  <img src="capa/logo.svg" alt="Arckhé AI" height="48" />
  <p><strong>Arckhé AI</strong></p>
</div>


[![Massinha 30](guia/assets/banner.jpg)](https://inematds.github.io/massinha-30/guia/)

**ê°Å¸â¡Â§ê°Å¸â¡Â· [PortuguêÂªs](README.md) êÂ· ê°Å¸â¡Âºê°Å¸â¡Â¸ [English](README.en.md) êÂ· ê°Å¸â¡Âªê°Å¸â¡Â¸ [EspaêÂ±ol](README.es.md)**

## O que êÂ©

VocêÂª tem uma ideia de histêÂ³ria, mas fazer os personagens, a voz e as cenas combinarem dêÂ¡ trabalho. Massinha 30 êÂ© um kit para criar narrativas curtas com aparêÂªncia de massinha artesanal. Ele organiza o roteiro aprovado, as referêÂªncias dos personagens, os clipes gerados no Kling, a narraêÂ§êÂ£o ElevenLabs e as legendas. Serve a criadores que querem repetir o processo em novas histêÂ³rias. Para produzir, êÂ© preciso ter acesso aos serviêÂ§os de geraêÂ§êÂ£o; o guia pode ser lido gratuitamente.

## Guia de uso

https://inematds.github.io/massinha-30/guia/

Abra o projeto no Codex e peêÂ§a: ê¢â¬ÅUse skills/massinha-30/SKILL.md para criar uma nova histêÂ³ria de massinhaê¢â¬Â. Leia [o fluxo completo](skills/massinha-30/references/producao.md).

Python 3.10+, FFmpeg/ffprobe com libass, CLI Kling oficial autenticada e ElevenLabs configurado. As imagens sêÂ£o geradas pelo agente com image_gen pela assinatura. A instalaêÂ§êÂ£o nêÂ£o gera vêÂ­deo nem faz chamada paga.

```bash
git clone https://github.com/inematds/massinha-30.git
cd massinha-30
python3 -m unittest discover -s tests -v
python3 skills/massinha-30/scripts/pipeline.py iniciar exemplos/retalhos.json --out runs/retalhos
```

O exemplo espera aprovaêÂ§êÂ£o explêÂ­cita do roteiro. `voz` e `kling` sêÂ³ enviam a provedores com `--enviar`. Credenciais no ambiente ou `--env-file`, nunca no repositêÂ³rio. Nenhum modelo de vêÂ­deo roda localmente.

## Estado

v1.1.0: demonstraêÂ§êÂ£o real de 30 segundos produzida com Kling e ElevenLabs; oito testes locais passaram. Cortes de cena e legendas alinhados êÂ  voz, arquivos editêÂ¡veis disponêÂ­veis na Release. Fish e Agnes continuam como alternativas sem adaptador neste kit.

A montagem exporta limpo.mp4 e final.mp4 (30s, 720êâ1280, 30fps, H.264/AAC), alêÂ©m de legendas.srt. O êÂ¡udio original do Kling êÂ© descartado; trilha e efeitos entram como arquivos separados. A verificaêÂ§êÂ£o têÂ©cnica nêÂ£o substitui assistir com som.

## LicenêÂ§a

MIT. NêÂ£o inclui licenêÂ§as de mêÂºsica, fontes, marcas ou condiêÂ§êÂµes dos provedores.

ê°Å¸Å½Â¬ [Assistir êÂ  histêÂ³ria](https://inematds.github.io/massinha-30/guia/#video) êÂ· [MP4](https://github.com/inematds/massinha-30/releases/download/demo-v1.1.0/massinha-30-retalhos.mp4)

---

<div align="center">
  <img src="capa/logo.svg" alt="Arckhé AI" height="32" />
  <p><strong>Arckhé AI</strong></p>
</div>