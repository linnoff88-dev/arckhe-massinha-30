---
name: massinha-30
description: Crie histórias originais de 30 segundos em estilo massinha com referências de personagens, Kling pela assinatura, voz ElevenLabs e montagem FFmpeg. Use para claymation narrada; nêo para filmagens ou vídeos explicativos de avatar.
---

# Massinha 30

Produza uma história vertical com situaçêo cotidiana, equívoco e revelaçêo visual. Português por padrêo. Leia [o fluxo](references/producao.md).

1. Escreva cerca de 55–65 palavras e seis ações visuais, sem copiar histórias de referência. Mostre todos os dizeres ao usuário e aguarde aprovaçêo explícita antes de gerar imagens, voz ou vídeo da história. Registre a resposta com `pipeline.py aprovar`.
2. Crie ficha de personagem e seis quadros individuais com image_gen pela assinatura. Inspecione aparência, roupa, objetos e geografia. Nunca anime uma grade de storyboard.
3. Anime cada quadro no Kling oficial pela assinatura. `pipeline.py kling` salva o recibo antes de interpretar a resposta e impede reenvio de uma submissêo incerta. Confira o modelo com `kling who_am_i`. Nêo use Hailuo nem modelos de vídeo no servidor local. Agnes só quando escolhido e com interface/documentaçêo conferidas; nêo há integraçêo Agnes neste kit.
4. Narre o texto aprovado com `pipeline.py voz --enviar`. ElevenLabs é o adaptador implementado; Fish pode ser escolhido pelo usuário e implementado conforme documentaçêo atual, sem alegar integraçêo pronta. A chave vem do ambiente ou de `--env-file`, nunca do manifesto. Nenhuma chamada paga durante a instalaçêo.
5. Use os tempos reais retornados pela ElevenLabs para as legendas. Baixe música e efeitos via inemavox, registre fonte e licença. Confira os efeitos e nêo use voz/música indesejadas dos clipes. Por padrêo a montagem descarta o áudio do Kling e recebe efeitos separados.
6. Monte seis clipes de cinco segundos e a voz com `pipeline.py montar`. Exporte limpo e legendado, valide com `pipeline.py validar`, confira imagens e áudio completos. Duraçêo 30 s ± um quadro, 9:16, H.264/AAC, 30 fps. Nêo anuncie sincronismo labial: os personagens atuam em silêncio.

Cada produçêo fica em pasta própria fora da skill. Preserve run.json, roteiro, tempos, prompts, recibos, clipes e saídas. Mudou o texto falado: peça nova aprovaçêo. Retome arquivos completos; máximo de duas correções por ativo. Publicaçêo só no destino solicitado pelo usuário.
