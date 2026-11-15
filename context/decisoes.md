---
tipo: contexto
projeto: eldritch-depths-3d
descricao: Log de decisões fechadas do Eldritch Depths 3D, com razão, escopo e alternativas descartadas.
estado: estavel
criado: 2026-11-14
---

# Decisões

> **Ler antes de reabrir qualquer discussão.** As `(d)` vêm das quatro rodadas de brainstorm com Pedro (artefato "Decisões do Eldritch Depths", documentos `decisoes/rodada-1` a `rodada-4`) e da aprovação da spec. As `(i)` são escolhas técnicas da IA, revisáveis.

## Produto {#produto}

- [2026-11-14] (d) **RPG de ação viciante no estilo Diablo.** Por quê: Pedro quer que a pessoa queira evoluir e não pare de jogar. Fecha: gênero e referência. Descartado: manter o jogo como estava.
- [2026-11-14] (d) **Demo pública na Steam e peça de portfólio.** Por quê: os dois usos de Pedro; "a arte não pode ficar feia". Fecha: público e padrão de qualidade. Descartado: protótipo só interno.
- [2026-11-14] (d) **Três classes: Cavaleiro, Mago e Demônio (Senhor de lacaios).** Por quê: escolha de Pedro nas rodadas 1 e 4. Fecha: elenco da demo. Descartado: classe única; Demônio corpo a corpo.
- [2026-11-14] (d) **Progressão por árvore de habilidades e saque enxuto.** Por quê: dá motivo para evoluir sem virar gestão de inventário. Fecha: eixo de progressão. Descartado: saque abundante estilo planilha.
- [2026-11-14] (d) **Sanidade é o Véu: revela passagens secretas e fragmentos de habilidade; zero é possessão.** Por quê: Pedro nunca entendeu para que servia a sanidade; ela precisa de história e função. Fecha: papel da sanidade. Descartado: barra que só cai e pune.
- [2026-11-14] (d) **Demo em duas etapas (andares 1–10, depois 11–20), terminando em "Adicione à lista de desejos".** Por quê: entrega algo jogável antes dos quatro chefes feitos à mão. Fecha: tamanho da demo. Descartado: data fixa de lançamento na tela final.
- [2026-11-14] (d) **Congelar integração Steam, ranking e mensagens da comunidade.** Por quê: não ajudam o bloco atual. Fecha: escopo inicial. Descartado: portar tudo do 2D.

## Visual e controle {#visual}

- [2026-11-14] (d) **3D com câmera fixa inclinada e arte semi-realista pintada.** Por quê: "mais realista e menos quadrado"; referência Diablo atual. Fecha: dimensão e direção de arte. Descartado: top-down 2D de 640×360; pixel art; câmera livre.
- [2026-11-14] (d) **Luz quente ao redor do herói num mundo escuro.** Por quê: é o principal recurso de leitura da cena. Fecha: linguagem de luz. Descartado: cena toda iluminada.
- [2026-11-14] (d) **HUD mínimo estilo soulslike.** Por quê: o HUD do 2D cobre cerca de 1/3 da tela. Fecha: interface fixa. Descartado: minimapa grande e ícones grandes de habilidade.
- [2026-11-14] (d) **Teclado e mouse e gamepad desde o início, sem Steam Deck.** Por quê: público de PC na Steam. Fecha: dispositivos. Descartado: só teclado; suporte a Steam Deck agora.

## Restrições e arte {#restricoes}

- [2026-11-14] (d) **Orçamento R$ 0.** Por quê: "investir" é tempo e dedicação. Fecha: ferramentas, assets e serviços. Descartado: qualquer pago.
- [2026-11-14] (d) **Modelos 3D originais; só animações e texturas de terceiros.** Por quê: identidade própria e portfólio. Fecha: origem dos assets. Descartado: kits de cenário e corpos-base prontos.
- [2026-11-14] (d) **O Claude faz a parte de Blender; Pedro nunca usou.** Por quê: "Confio nas suas habilidades". Fecha: divisão do trabalho de arte. Descartado: Pedro aprender Blender agora.
- [2026-11-14] (d) **Sem prazo; PC mínimo é notebook com vídeo integrado.** Por quê: a demo sai quando estiver boa e precisa rodar na máquina de Pedro. Fecha: cronograma e piso de hardware. Descartado: data fixa; exigir placa dedicada.

## Arquitetura {#arquitetura}

- [2026-11-14] (d) **Projeto Godot 3D novo ao lado do 2D, com `context/` e git próprios.** Por quê: o 2D fica intacto como referência e o histórico mora dentro do jogo. Fecha: onde o 3D vive. Descartado: converter o projeto 2D no lugar.
- [2026-11-14] (d) **Nenhuma dependência nova sem Pedro.** Por quê: regra da holding. Fecha: addons e bibliotecas. Descartado: adotar addons por conveniência.
- [2026-11-14] (i) **Runner de testes caseiro em vez de GUT.** Por quê: evita dependência nova; o necessário (asserts, descoberta de `test_*`, saída e código de retorno) cabe em dois arquivos pequenos. Fecha: ferramenta de testes do Bloco 1A. Descartado: GUT; gdUnit4.
- [2026-11-14] (i) **1 m = 27 px do 2D.** Por quê: uma escala única converte velocidades e alcances do 2D mantendo a proporção entre eles; ajuste fino fica para o teste de Pedro (T32). Fecha: conversão de unidades. Descartado: recalibrar todos os valores do zero.
- [2026-11-14] (i) **Pasta `eldritch_depths_3d_20261114`.** Por quê: segue o padrão `<nome>_<data>` da `holding_agy`. Fecha: caminho do projeto. Descartado: renomear o projeto 2D.
- [2026-11-14] (i) **Plano do Bloco 1A em 32 tarefas pequenas com ledger.** Por quê: Pedro vai usar vários modelos de IA ao longo de dias; cada tarefa precisa caber numa sessão sem conversa anterior. Fecha: forma de execução do Bloco 1A. Descartado: 9 tarefas grandes.
- [2026-11-14] (i) **Mapa de entrada com tecla física e `device = -1`.** Por quê: WASD fica no lugar em qualquer layout e qualquer controle funciona. Fecha: formato do `[input]`. Descartado: `keycode` lógico; dispositivo 0.
- [2026-11-14] (i) **Faixas do Véu provisórias em 60 e 30 (CLARO ≥ 60, FINO ≥ 30, RASGADO < 30).** Por quê: a spec propõe três faixas (100–60, 60–30, 30–0) e o código precisa de limites para a parede e a vinheta do Bloco 1A. Fecha: só os limites usados em `Veil.band_for`. Descartado: limites finais agora — o efeito de cada faixa segue em aberto com Pedro (spec §9).
- [2026-11-14] (i) **Renderizador `mobile` (Forward Mobile, Vulkan) fixado por medição na T31.** Por quê: na GPU integrada desta máquina (AMD Radeon Graphics, RADV Renoir; Godot 4.7.2), com o herói em `--autoplay` e os 5 primeiros segundos descartados, os dois renderizadores cumprem a meta (média 60, mínimo ≥ 50) presos ao vsync — `tools/measure_fps.sh mobile` → média 60,0 mínimo 60 (de novo na T30: mínimo 59); `tools/measure_fps.sh gl_compatibility` → média 60,0 mínimo 60 — e sem vsync, em tela cheia 1920×1080, o `mobile` tem mais folga: média 403,7 mínimo 364 contra média 387,2 mínimo 341 do `gl_compatibility`. Os passos de FSR 0,75 e de tirar a sombra da HeroLight não foram necessários. Fecha: `rendering/renderer/rendering_method` do Bloco 1A. Descartado: `gl_compatibility` (menos folga e sem os recursos do Forward Mobile).
- [2026-11-14] (d) **README em português do Brasil.** Por quê: Pedro confirmou ("pode ser em portugues mesmo") ao receber as tarefas T33–T34. Fecha: idioma do `README.md`. Descartado: inglês; versão bilíngue.
- [2026-11-15] (i) **Interpolação de física ligada; câmera segue no passo de física.** Por quê: o herói anda no passo de física e a câmera seguia no frame de desenho, o que treme acima de 60 Hz (achado A04, revisão final do Bloco 1A). Fecha: `physics/common/physics_interpolation` e o laço da câmera. Descartado: interpolar à mão só o visual do herói; subir os ticks de física.
- [2026-11-15] (d) **História do jogo fixada no README.** Por quê: Pedro aprovou o rascunho 2 ("perfeito") depois de responder às perguntas da T34 (nome dado pelo jogador, salvar o mundo e a Princesa, português arcaico, classes já na história, Demônio sobrevivente da possessão). Fecha: texto da seção "A história" e os nomes em `produto.md#historia`. Descartado: rascunho 1 (sem motivação nem nomes); herói com nome fixo; incluir o Guardião dos Mil Olhos.
- [2026-11-15] (i) **Plano do Bloco 1B em 17 tarefas (B01–B17) com ledger e portões de aprovação de Pedro.** Por quê: o plano do 1A reservou a arte para um plano próprio porque cada etapa visual depende de aprovação de Pedro; o prefixo B evita colisão com os achados A01–A06. Fecha: forma de execução da trilha de arte. Descartado: anexar a arte ao plano do 1A; tarefas grandes por personagem.
- [2026-11-15] (i) **Ferramentas propostas para a trilha de arte, a confirmar com Pedro:** Qwen-Image-Edit e FLUX.1 [schnell] (Apache 2.0) para conceitos; TRELLIS.2 (MIT) para malhas, com o Meshy grátis (CC BY 4.0, com atribuição) só de reserva; Mixamo para rig e animações sobre o nosso modelo; Blender 4.5 sem janela, por script. Por quê: licenças conferidas em 2026-11-15 permitem uso comercial, custo zero, e a máquina não tem NVIDIA para rodar geração 3D localmente (spec §10 deixa a escolha ao construtor com licença registrada). Fecha: ferramentas iniciais do Bloco 1B, sujeitas ao veto de Pedro. Descartado: Hunyuan3D (licença exclui UE, Reino Unido e Coreia do Sul); Tripo (termos do plano grátis contraditórios); personagens prontos do Mixamo (corpo-base, vetado pela spec). ~superseded 2026-11-15 → linha seguinte
- [2026-11-15] (i) **Material bruto de arte em `art/brutos/`, não em `fontes/`.** Por quê: são insumos de produção registrados em `context/assets.md` com licença e SHA-256, não documentos a interpretar; o lint cobra ingestão de tudo em `fontes/`. Fecha: onde vivem as saídas cruas dos serviços de IA. Descartado: `fontes/`; fora do repositório.
- [2026-11-15] (d) **Plano do Bloco 1B aceito, execução nativa e ferramentas propostas confirmadas.** Pedro respondeu "o que voce indicar" à pergunta sobre o plano, o modo de execução e o veto das ferramentas. Fecha: Qwen-Image-Edit/FLUX.1 [schnell], TRELLIS.2 (Meshy de reserva), Mixamo sobre o nosso modelo e Blender por script; execução nativa com revisão final única. Descartado: subagente por tarefa; Hunyuan3D; Tripo.
- [2026-11-15] (d) **Direção de arte A, semi-realista pintada; guia de estilo B01 aprovado como está.** Pedro viu a maquete em Blender com a câmera do jogo comparando três tratamentos da mesma sala e respondeu "Podemos seguir com a opção A". Fecha: direção de arte do Bloco 1B, `docs/arte/guia-de-estilo.md` e `docs/arte/paleta.svg`. Descartado: estilizada com sombra em faixas e contorno; realista sombria dessaturada.
- [2026-11-15] (d) **Geração de arte pela API dos Spaces, operada pelo Claude.** Pedro perguntou "e se usarmos via API ?" e, depois da proposta (cliente `gradio_client` num venv isolado, Claude operando FLUX.1 [schnell] e TRELLIS.2 por script, token da conta grátis dele só se a cota anônima acabar), respondeu "aprovamdo". Pedro segue aprovando cada peça nos portões. Fecha: quem opera os serviços de IA no Bloco 1B (a spec §3 dizia que era Pedro) e a dependência nova `gradio_client`, só de ferramenta. Descartado: Pedro gerar e salvar à mão pela página; chamar a API HTTP crua com curl (as etapas do TRELLIS.2 guardam estado na sessão, o que o cliente já resolve).
- [2026-11-15] (i) **Braseiro modelado por script no Blender, com a imagem do FLUX como referência.** Por quê: o Space do TRELLIS.2 falhou (cota anônima zerada, conta não criada, Space parado) e Pedro perguntou "nao existe outra, ou voce pode fazer esse trabalho"; as alternativas grátis de imagem → 3D também dependem de ZeroGPU ou têm licença problemática. Fecha: origem do modelo da B04. Descartado: esperar o TRELLIS.2; Meshy só para o braseiro (gasta créditos e exige atribuição numa peça que o script resolve).
- [2026-11-15] (d) **Braseiro da B04 aprovado.** Pedro viu a prancha (conceito, quatro vistas e captura no jogo) e respondeu "perfeito, pode seguir". Fecha: modelo `assets/models/props/braseiro.glb` e a cena `scenes/props/brazier.tscn`; prévias em `docs/arte/previas/braseiro/`. Descartado: refazer pelo TRELLIS.2.
