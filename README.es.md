# Massinha 30

[![Massinha 30](guia/assets/banner-es.jpg)](https://linnoff88-dev.github.io/arckhe-/guia/es/)

**🇧🇷 [Português](README.md) · 🇺🇸 [English](README.en.md) · 🇪🇸 [Español](README.es.md)**

## Qué es

Tienes una idea para una historia, pero lograr que los personajes, la voz y las escenas encajen lleva trabajo. Massinha 30 es un kit para crear narraciones cortas con aspecto de plastilina artesanal. Organiza el guion aprobado, las referencias de los personajes, los clips generados en Kling, la narración de ElevenLabs y los subtítulos. Está pensado para creadores que quieren repetir el proceso con nuevas historias. Para producir, hace falta tener acceso a los servicios de generación; la guía se puede leer gratis.

## Guía de uso

https://linnoff88-dev.github.io/arckhe-/guia/es/

Abre el proyecto en Codex y pide: “Usa skills/massinha-30/SKILL.md para crear una nueva historia de plastilina”. Lee [el flujo completo](skills/massinha-30/references/producao.md).

Python 3.10+, FFmpeg/ffprobe con libass, CLI oficial de Kling autenticada y ElevenLabs configurado. El agente genera las imágenes con image_gen mediante su suscripción. La instalación no genera videos ni hace llamadas de pago.

```bash
git clone https://github.com/linnoff88-dev/massinha-30.git
cd massinha-30
python3 -m unittest discover -s tests -v
python3 skills/massinha-30/scripts/pipeline.py iniciar exemplos/retalhos.json --out runs/retalhos
```

El ejemplo espera la aprobación explícita del guion. `voz` y `kling` solo envían solicitudes a los proveedores con `--enviar`. Las credenciales van en el entorno o en `--env-file`, nunca en el repositorio. Ningún modelo de video se ejecuta localmente.

## Estado

v1.1.0: demostración real de 30 segundos producida con Kling y ElevenLabs; ocho pruebas locales pasaron. Cortes de escena y subtítulos alineados con la voz; los archivos editables están disponibles en la Release. Fish y Agnes siguen como alternativas sin adaptador en este kit.

El montaje exporta limpo.mp4 y final.mp4 (30 s, 720×1280, 30 fps, H.264/AAC), además de legendas.srt. Se descarta el audio original de Kling; la pista musical y los efectos se incorporan como archivos separados. La comprobación técnica no sustituye ver la película con sonido.

## Licencia

MIT. No incluye licencias de música, fuentes, marcas ni las condiciones de los proveedores.
🎬 [Ver la historia](https://linnoff88-dev.github.io/arckhe-/guia/es/#video) · [MP4](https://github.com/linnoff88-dev/massinha-30/releases/download/demo-v1.1.0/massinha-30-retalhos.mp4)
