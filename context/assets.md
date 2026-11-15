---
tipo: registro
projeto: eldritch-depths-3d
descricao: Origem e licença de cada ferramenta e de cada arquivo de arte do jogo (modelos, texturas, brutos dos serviços de IA).
estado: estavel
criado: 2026-11-15
---

# Registro de origem e licenças

Todo arquivo em `assets/models/` e em `art/brutos/` precisa de uma linha na tabela de [Assets](#assets) **antes do commit**; o teste `test_assets_registrados` (`tests/test_assets_registry.gd`) reprova o que faltar. Serve também de base para a declaração de conteúdo gerado por IA da Steam.

## Ferramentas e serviços {#ferramentas}

- [2026-11-15] (e) **TRELLIS.2** (imagem → modelo 3D): o cartão do modelo diz "released under the MIT License"; uso pelo Space `microsoft/TRELLIS.2`, porque rodar local exige placa NVIDIA. https://huggingface.co/microsoft/TRELLIS.2-4B
- [2026-11-15] (e) **Qwen-Image-Edit** (edição de imagem com 1 a 3 referências): Apache 2.0; Space `Qwen/Qwen-Image-Edit`. https://huggingface.co/Qwen/Qwen-Image-Edit-2509
- [2026-11-15] (e) **FLUX.1 [schnell]** (texto → imagem): Apache 2.0, "personal, scientific, and commercial purposes"; Space `black-forest-labs/FLUX.1-schnell`. https://huggingface.co/black-forest-labs/FLUX.1-schnell
- [2026-11-15] (e) **Meshy, plano grátis** (reserva do TRELLIS.2): 100 créditos por mês, saída sob CC BY 4.0, uso comercial com atribuição, "You own the output". Se for usado, a atribuição entra nos créditos do jogo. https://docs.meshy.ai/en/webapp/pricing
- [2026-11-15] (e) **Mixamo** (auto-rig e animações sobre o nosso modelo): segundo a FAQ da Adobe, lida por busca porque a página recusou leitura automática, personagens e animações são royalty-free para projetos pessoais, comerciais e sem fins lucrativos, jogos incluídos, com Adobe ID grátis. Pedro confere a FAQ no navegador antes da B09 e a confirmação entra aqui como (d). https://helpx.adobe.com/creative-cloud/faq/mixamo-faq.html ~superseded 2026-11-15 → linha seguinte
- [2026-11-15] (d) **Mixamo conferido por Pedro.** Pedro leu a FAQ da Adobe no navegador e respondeu "Confirmado que terminou o FAQ", sem objeção ao uso; o Mixamo fica liberado para o auto-rig e as animações da B09 e da B13, com origem `mixamo` em cada arquivo. https://helpx.adobe.com/creative-cloud/faq/mixamo-faq.html
- [2026-11-15] (e) **Hunyuan3D — excluído:** a licença comunitária não vale na União Europeia, no Reino Unido nem na Coreia do Sul, onde a demo será vendida. https://huggingface.co/tencent/Hunyuan3D-2/blob/main/LICENSE
- [2026-11-15] (e) **Blender 4.5.15 LTS:** GPL; o que se cria com ele pertence a quem cria. https://www.blender.org/about/license/
- [2026-11-15] (e) **gradio_client 2.7.2** (cliente da API dos Spaces): Apache 2.0. Os Spaces ZeroGPU dão cota diária de GPU por conta; a cota anônima desta rede estava zerada na primeira chamada ("You have exceeded your ZeroGPU quota (90s requested vs. 0s left)"), então as chamadas usam o token da conta grátis de Pedro. https://github.com/gradio-app/gradio/tree/main/client/python
- [2026-11-15] (d) Pedro aprovou gerar pela API em vez da página ("aprovamdo"): o Claude opera os Spaces por script e o operador dos brutos passa a ser `claude (api, conta de Pedro)`; ver [[decisoes]].
- [2026-11-15] (i) **`art/referencias/`** guarda as ampliações de 128 para 1024 px (Lanczos, sobre cinza `#808080`, feitas com Pillow) dos sprites `hero.png` e `cultist.png` do 2D, arte própria do projeto; servem só de entrada para o Qwen-Image-Edit nas B05 e B11 e não vão para o jogo.
- [2026-11-15] (d) Ferramentas acima confirmadas por Pedro ("o que voce indicar"), ver [[decisoes]].

## Assets {#assets}

Uma linha por arquivo. `arquivo` é o caminho relativo à raiz do repositório; `tipo` é `bruto`, `modelo` ou `textura`; `origem` é `ia`, `script`, `mixamo` ou `terceiro`; `prompt` aponta para o arquivo em `art/prompts/`; `sha256` é o do arquivo como está no repositório (ou só no disco, para brutos grandes).

| arquivo | tipo | origem | ferramenta e modelo | licença | operador | data | prompt | sha256 |
|---|---|---|---|---|---|---|---|---|
| art/brutos/2026-11-15-flux-braseiro.webp | bruto | ia | FLUX.1 [schnell], Space black-forest-labs/FLUX.1-schnell, 1024×1024, 4 passos | Apache 2.0 | pedro (página do Space) | 2026-11-15 | art/prompts/braseiro.md | 3c1f89d9367fbbf4787ecfb303807110024212f0909a930ad2c6ce77b89edf44 |
| assets/models/props/braseiro.glb | modelo | script | Blender 4.5.15 LTS, `art/props/braseiro/build.py` (modelado por script; conceito `art/brutos/2026-11-15-flux-braseiro.webp` só como referência visual) | própria | claude (script Blender) | 2026-11-15 | art/prompts/braseiro.md | 5c52683bb8d50314f037b7aabeeb70aa35e35b61f173497b8410eb04299a581a |
| assets/models/props/braseiro_textura_cor.png | textura | script | assada pelo `art/props/braseiro/build.py`; o Godot a extrai do GLB ao importar | própria | claude (script Blender) | 2026-11-15 | art/prompts/braseiro.md | a28652a831c3b017ec760cf24fea845d3659f05b11db8187a7c94d5072aa218c |
| assets/models/props/braseiro_textura_emissao.png | textura | script | assada pelo `art/props/braseiro/build.py`; o Godot a extrai do GLB ao importar | própria | claude (script Blender) | 2026-11-15 | art/prompts/braseiro.md | 7971ce2f1a696229619399e9fdd87b80f3eab76a17dddf8de4a90dcdc78e56e2 |
| assets/models/personagens/espada.glb | modelo | script | Blender 4.5.15 LTS, `art/personagens/cavaleiro/build_espada.py` (modelado por script; referência visual: a espada do `hero.png` do 2D) | própria | claude (script Blender) | 2026-11-15 | — | 7786fe5b2d8fbad2ba4248ec493390b5d8792c5feb612eb1855034593d0fd881 |
| assets/models/personagens/espada_textura_cor.png | textura | script | assada pelo `art/personagens/cavaleiro/build_espada.py`; o Godot a extrai do GLB ao importar | própria | claude (script Blender) | 2026-11-15 | — | c85a8c7d2bf81ba7f6ae288d5b6a0e277b8a8212eeb60c116e457e40218e5e94 |
| assets/models/personagens/espada_textura_emissao.png | textura | script | assada pelo `art/personagens/cavaleiro/build_espada.py`; o Godot a extrai do GLB ao importar | própria | claude (script Blender) | 2026-11-15 | — | 353173f9122b845d76a536a7894a943b1f03878e487d03b824192478547376ab |
| docs/arte/cavaleiro-conceito.png | bruto | script | Blender 4.5.15 LTS, `art/personagens/cavaleiro/build_conceito.py` (blockout 3D por script, Cycles, vistas ortográficas; refeita em 2026-11-15 com a paleta e o acabamento do guia; versão 3 realista em 2026-11-15 com relevo de material) + `tools/folha_conceito.py` (Pillow); sem geração por IA | própria | claude (script Blender) | 2026-11-15 | art/prompts/cavaleiro-conceito.md (só como descrição) | a356f881398a0313d6707a0dea1e8d38b8a762623e184079e6833cb1bf28ab75 |
| docs/arte/cultista-conceito.png | bruto | script | Blender 4.5.15 LTS, `art/inimigos/cultista/build_conceito.py` (blockout 3D por script, Cycles, vistas ortográficas; refeita em 2026-11-15 com a paleta e o acabamento do guia; versão 3 realista em 2026-11-15 com relevo de material) + `tools/folha_conceito.py` (Pillow); sem geração por IA | própria | claude (script Blender) | 2026-11-15 | art/prompts/cultista-conceito.md (só como descrição) | d7be17c4b4be4f01ec4ebd06741fc513d41ca3fe1da654eb391dc39f5d322f05 |
