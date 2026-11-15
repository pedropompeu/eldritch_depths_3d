# Eldritch Depths 3D — Documento de design

- [2026-11-14] (d) Escrito a partir de três rodadas de brainstorm com Pedro Pompeu, registradas no artefato "Decisões do Eldritch Depths" (claude.ai/artifact/RFRGU28gvULSbPNTmswbeN, documentos `decisoes/rodada-1`, `rodada-2` e `rodada-3`).
- [2026-11-14] (d) A rodada 4 (documento `decisoes/rodada-4`) respondeu às perguntas do revisor e fechou o §9.
- [2026-11-14] (d) **Documento aprovado por Pedro** ("perfeito! aprovado"), incluindo as escolhas do Claude marcadas com (i).
- [2026-11-14] (i) Este arquivo está na pasta do jogo 2D apenas porque o projeto 3D ainda não existe. Quando o projeto 3D for criado, o arquivo vai para lá, junto com o `context/`. ~superseded 2026-11-14 → ver linha seguinte.
- [2026-11-14] (i) O arquivo agora mora no projeto 3D; a cópia no projeto 2D é histórica.

Legenda: **(d)** decidido por Pedro · **(i)** escolha do Claude, revisável · **(e)** fato do código ou da máquina.

---

## 1. Intenção

- [2026-11-14] (d) Fazer um RPG de ação **viciante**, em que a pessoa queira evoluir e não pare de jogar. A referência é **Diablo**.
- [2026-11-14] (d) Os gráficos devem ser **mais realistas e menos quadrados** que os atuais. O visual atual do herói está vetado: "ele está todo quebrado e sem um visual".
- [2026-11-14] (d) O projeto tem dois usos: uma **demo pública na Steam** e uma peça de **portfólio**. Nos dois casos "a arte não pode ficar feia".
- [2026-11-14] (d) O tema é horror cósmico, e o eixo do jogo é a **sanidade como percepção da realidade**. Pedro disse que nunca entendeu para que servia a sanidade no jogo atual. Ela precisa ganhar história e função.

## 2. Metas, não-metas e anti-metas

**Metas**
- [2026-11-14] (d) Uma demo jogável na Steam, com **3 classes: Cavaleiro, Mago e Demônio**.
- [2026-11-14] (d) Progressão que prende: **árvore de habilidades**, **classes/builds** e **dificuldade que escala sem fim**, mais **saque enxuto**.
- [2026-11-14] (d) O primeiro bloco de trabalho é **"Tela e sensação"**: câmera, luz, herói, controle e combate parecendo bons antes de qualquer conteúdo.

**Não-metas, por enquanto**
- [2026-11-14] (d) **Congelados:** integração com Steam (conquistas e afins), ranking e mensagens/fantasmas da comunidade. O código fica, mas não é portado nem mantido agora.
- [2026-11-14] (i) Multiplayer e consoles estão fora do escopo; nada nas rodadas aponta para eles.

**Anti-metas** (o que faria o projeto fracassar mesmo funcionando)
- [2026-11-14] (d) Arte feia ou inconsistente. Exemplo: personagem que destoa do cenário.
- [2026-11-14] (d) Herói desconjuntado ou sem identidade, como o rig de peças atual.
- [2026-11-14] (i) Uma interface que ocupa a tela. Hoje o HUD cobre cerca de 1/3 da imagem; Pedro pediu HUD mínimo.
- [2026-11-14] (i) Sanidade como uma barra que só cai e incomoda. Ela precisa ser uma escolha do jogador.

## 3. Restrições

- [2026-11-14] (d) **Orçamento R$ 0.** "Investir" significa tempo e dedicação, não dinheiro. Só ferramentas, assets e serviços gratuitos.
- [2026-11-14] (d) **A arte é feita por Pedro e pelo Claude, juntos**, com geração por IA e retoque.
- [2026-11-14] (d) **Modelos 3D são originais** (gerados por IA e retocados por nós). **Animações e texturas podem vir de terceiros**, desde que sejam gratuitas e liberadas para uso comercial. Kits de cenário e corpos-base prontos ficam de fora.
- [2026-11-14] (d) **Pedro nunca usou o Blender** e confia no Claude para essa parte: "Confio nas suas habilidades".
- [2026-11-14] (i) Consequência: o Claude faz no Blender, por script, a modelagem, a limpeza, o rig e a montagem. A cada etapa ele renderiza imagens de pré-visualização, que Claude e Pedro avaliam a olho. Pedro opera, com a conta dele, os serviços online gratuitos de geração de imagem e de 3D por IA, já que o Claude não cria contas; o Claude escreve os prompts e processa o resultado.
- [2026-11-14] (d) **Sem prazo.** A demo sai quando estiver boa.
- [2026-11-14] (i) Pedro não informou quantas horas por semana tem; o plano é feito em blocos sem datas.
- [2026-11-14] (d) **PC mínimo: notebook com vídeo integrado**, como a máquina de Pedro.
- [2026-11-14] (e) Máquina de desenvolvimento: AMD Ryzen "Lucienne" com Radeon integrada (RADV RENOIR), Vulkan 1.3, 30 GB de RAM, 16 threads. Godot 4.7.2 e Blender instalados em `~/.local/bin`.
- [2026-11-14] (e) Gerar modelos 3D com IA localmente exige GPU NVIDIA, que esta máquina não tem. A geração precisa usar serviços online com cota gratuita, e a licença de cada um deve ser conferida antes de usar o resultado num produto à venda.
- [2026-11-14] (e) A Steam exige declarar o uso de conteúdo gerado por IA na página do jogo.
- [2026-11-14] (d) Agentes externos (OpenCode, Gemini) só podem ser usados com modelos ou cotas gratuitas.
- [2026-11-14] (d) Novas dependências, mudanças de arquitetura e regras de negócio passam por Pedro antes de entrar.

## 4. O jogo

### 4.1 Visual e câmera
- [2026-11-14] (d) **3D com câmera fixa inclinada**, no estilo dos Diablo atuais. Isso substitui o top-down 2D de 640×360.
- [2026-11-14] (d) Direção de arte **semi-realista pintada**: proporções reais, texturas pintadas à mão, formas um pouco exageradas, fantasia sombria.
- [2026-11-14] (d) **Luz quente ao redor do herói** num mundo escuro. Ela é o principal recurso de leitura da cena.
- [2026-11-14] (d) **Distância de câmera "como está":** enquadramento parecido com o atual, mostrando a sala em volta do herói.
- [2026-11-14] (i) Escala de referência para o construtor: em 1080p, o herói ocupa cerca de 1/8 da altura da tela, contra os ~20 px de hoje. Ajustar no protótipo. ~superseded 2026-11-14 → ver linha abaixo.
- [2026-11-14] (i) O protótipo começa no enquadramento atual (o herói ocupa cerca de 1/13 da altura da tela, com zoom 1,35) e testa uma alternativa mais próxima (cerca de 1/8). Pedro escolhe jogando, **antes** de fixar a grade do kit modular e o nível de detalhe do herói.

### 4.2 HUD
- [2026-11-14] (d) **Mínimo, estilo soulslike**: barras finas de vida, vigor e sanidade num canto, poucos atalhos de consumíveis e a barra do chefe só durante a luta.
- [2026-11-14] (i) O minimapa grande e os 4 ícones grandes de habilidade saem da tela fixa. O mapa fica numa tecla e as habilidades aparecem pequenas.

### 4.3 Combate
- [2026-11-14] (d) **Ágil e fluido.** Há base no código atual: ataque, esquiva (roll), parry, magia cósmica, postura e frascos.
- [2026-11-14] (i) Os controles de hoje (WASD, ataque, esquiva, parry, magia, frascos 1 e 2) continuam como ponto de partida. A escolha entre mirar pelo mouse e mirar pela direção do movimento fica para o protótipo. ~superseded 2026-11-14 → ver linha seguinte.
- [2026-11-14] (d) **Teclado e mouse, e também controle (gamepad), desde o início.** Steam Deck fica fora por enquanto.
- [2026-11-14] (i) No teclado e mouse a mira segue o mouse. No controle segue o analógico direito, ou a direção do movimento com ajuda de mira. Os botões mostrados na tela mudam conforme o dispositivo em uso.

### 4.4 Classes
- [2026-11-14] (d) A demo tem **Cavaleiro, Mago e Demônio**.
- [2026-11-14] (d) O **Cavaleiro** é o cavaleiro encapuzado da ilustração `assets/sprites/hero.png`: armadura escura e espada longa.
- [2026-11-14] (e) A ilustração tem só 128×128 px, pouco para guiar a modelagem.
- [2026-11-14] (i) Antes de qualquer trabalho em 3D vem um **conceito em alta resolução do Cavaleiro** (frente, lado e costas), fiel à ilustração. Pedro aprova o conceito antes da modelagem.
- [2026-11-14] (i) Papéis propostos: Cavaleiro luta corpo a corpo, com parry e postura. Mago luta à distância, com magia cósmica. O Demônio fica em aberto (ver §9). ~superseded 2026-11-14 → ver linha seguinte.
- [2026-11-14] (d) **Demônio: Senhor de lacaios.** Invoca criaturas do Véu que lutam por ele.
- [2026-11-14] (i) Papéis: o Cavaleiro luta corpo a corpo, com parry e postura; o Mago luta à distância, com magia cósmica; o Demônio é invocador.
- [2026-11-14] (i) A ordem de produção é Cavaleiro primeiro, no bloco "Tela e sensação"; Mago e Demônio vêm depois que o Cavaleiro estiver bom.

### 4.5 Mundo: o Poço sem fundo
- [2026-11-14] (d) A partir do **santuário (hub)** se desce **andar por andar**, todos **sorteados**. A cada **5 andares** há um **chefe feito à mão**. A descida é **infinita**, com dificuldade e recompensas crescentes.
- [2026-11-14] (d) Na rodada 4, Pedro marcou **demo até o andar 10, com 2 chefes**, e no comentário propôs **20 andares** com um chefe a cada 5 (andares 5, 10, 15 e 20). Depois deles vem um **chefe final impossível de vencer**, que sempre mata o herói. Em seguida aparece a mensagem "Em breve, tente de novo na versão final", com a data de lançamento do jogo completo.
- [2026-11-14] (i) Opinião do Claude: o final impossível é um bom gancho e combina com o Véu, mas a morte precisa ser claramente encenada (curta, sem perder progresso) para não parecer injusta. No lugar de uma data fixa, mostrar "Adicione à lista de desejos", já que não há prazo. O custo maior dos 20 andares está nos 4 chefes feitos à mão, não nos andares sorteados.
- [2026-11-14] (i) Recomendação, a confirmar na aprovação: fazer em duas etapas. **Etapa 1:** andares 1 a 10, 2 chefes e o chefe final impossível. **Etapa 2:** estender para 20 andares e 4 chefes antes de publicar a demo. ~superseded 2026-11-14 → ver linha seguinte.
- [2026-11-14] (d) **Demo em duas etapas, aprovada por Pedro.** Etapa 1: andares 1 a 10, 2 chefes e o chefe final impossível. Etapa 2: andares 11 a 20 e os chefes 15 e 20, antes de publicar. No fim aparece "Adicione à lista de desejos", sem data fixa.
- [2026-11-14] (e) Já existem um gerador de masmorra por grafo de salas com semente (`scripts/world/dungeon_generator.gd`), um santuário (`sanctuary_hub.gd`), um coliseu, um ciclo astral e um chefe, o Guardião dos Mil Olhos.
- [2026-11-14] (i) Os andares são montados com **peças 3D modulares** (salas e corredores pré-montados encaixados pelo gerador), não com geometria livre. Assim a arte fica consistente e o volume de trabalho fica controlado.

### 4.6 Sanidade: o Véu
- [2026-11-14] (d) **Premissa:** a mente humana é um véu que esconde o que realmente habita as profundezas. Quanto mais fino o véu, mais se vê.
- [2026-11-14] (d) **O que o Véu revela** quando a sanidade cai: **passagens e andares secretos** (atalhos no Poço, salas que antes eram parede) e **fragmentos de habilidade** (pontos extras na árvore, que só existem do outro lado do Véu).
- [2026-11-14] (d) A sanidade é **percepção da realidade**: o que o jogador vê muda conforme ela cai.
- [2026-11-14] (e) Hoje a sanidade cai 0,8 por segundo o tempo todo, cai 15 em alguns golpes, o láudano devolve 50% e há um "frenesi" abaixo de 35. Também já existe uma parede ilusória (`illusory_wall.gd`).
- [2026-11-14] (i) **Proposta a validar:** a sanidade passa a ter três faixas visíveis (por exemplo 100–60, 60–30 e 30–0). Cada faixa revela mais e cobra mais: inimigos mais fortes, alucinações (inimigos falsos, sons, HUD que mente) e, no fundo, risco real. O preço exato é regra de negócio e fica com Pedro (§9).
- [2026-11-14] (i) **Como a sanidade cai:** o mecanismo de hoje continua (queda lenta com o tempo no Poço e golpes de criaturas cósmicas). A escolha do jogador está em **quando usar o láudano ou voltar ao santuário**, ou seja, em quanto deixa o Véu afinar. No primeiro bloco basta essa queda passiva e uma tecla de depuração para testar o efeito.
- [2026-11-14] (d) **Sanidade zero = Possessão:** uma criatura nasce do herói e precisa ser derrotada; se o jogador perder, morre. Essa criatura é **um Senhor de lacaios**.
- [2026-11-14] (i) Ideia a validar: a criatura da possessão compartilha modelo e habilidades com a classe Demônio, então a arte serve aos dois. Na história, isso sugere que o Demônio é alguém que sobreviveu à própria possessão. Vencer a primeira possessão poderia desbloquear a classe.

### 4.7 Progressão e saque
- [2026-11-14] (d) **Árvore de habilidades** por classe: cada nível dá pontos, e os fragmentos do Véu dão pontos extras.
- [2026-11-14] (d) **Saque enxuto:** poucas peças por andar, com raridade e de 1 a 3 atributos. Dá motivo para a forja sem virar gestão de inventário.
- [2026-11-14] (d) Sistemas mantidos: forja e equipamentos, perks (bênçãos permanentes), códice, modo foto, criação de personagem, coliseu, santuário, ciclo astral, masmorra procedural, puzzles, mods, cosméticos, telemetria e relato de bug, login e servidor Python.
- [2026-11-14] (i) A criação de personagem vira **escolha de classe** com alguma personalização.

## 5. Pipeline de arte

- [2026-11-14] (d) A arte é feita a quatro mãos (Pedro + Claude), com IA e retoque, e R$ 0.
- [2026-11-14] (i) Fluxo proposto para personagens: conceito 2D (IA ou a ilustração existente) → modelo 3D gerado em serviço online gratuito → limpeza, retopologia e textura pintada no Blender → rig e animação. As animações podem vir de uma biblioteca gratuita de animações humanoides, se a licença permitir uso comercial. Sai em glTF para a Godot.
- [2026-11-14] (i) Fluxo proposto para cenário: kit modular de peças (paredes, pisos, portas, props) modelado no Blender por script e à mão, com texturas pintadas ou texturas CC0 repintadas para o estilo.
- [2026-11-14] (i) Um **guia de estilo curto** (paleta, valores de luz, nível de detalhe, espessura de contorno se houver) vem antes da produção em série. É o que mantém IA, Pedro e Claude coerentes entre si.
- [2026-11-14] (i) Cada asset leva origem e licença registradas no `context/` do projeto, tanto para a declaração de IA na Steam quanto para o portfólio.
- [2026-11-14] (e) Os geradores procedurais em Python (`scripts/tools/generate_*.py`) servem para texturas 2D e sons, não para modelos 3D. O gerador de áudio pode continuar a ser usado.

## 6. Arquitetura

- [2026-11-14] (d) **Projeto novo ao lado:** um projeto Godot 3D novo, que traz o código aproveitável. O projeto 2D fica intacto como referência.
- [2026-11-14] (d) **Histórico dentro do jogo:** o projeto 3D tem seu próprio `context/` (index, produto, arquitetura, decisões, achados) e é um **repositório git** desde o início.
- [2026-11-14] (i) Local e nome sugeridos: `/home/usuario/Dev/holding_agy/eldritch_depths_3d_20261114/`, seguindo o padrão de nomes da pasta.
- [2026-11-14] (e) O que pode ir quase sem mudança, porque não depende de 2D: os autoloads de áudio, autenticação, perks, diretor de combate, diálogo, banco de itens, equipamentos, telemetria, ciclo astral, registro de conteúdo, mods, códice e cosméticos (cerca de 2.300 linhas). Também `stats_component`, `blacksmith_component`, os recursos de item e arma, a máquina de estados genérica, a maior parte das telas de UI, as traduções (en_US, es_ES, pt_BR) e o backend Python.
- [2026-11-14] (e) O que precisa ser reescrito em 3D: jogador, inimigos, chefe, projéteis, hitbox, hurtbox e postura (usam Vector2 e corpos 2D), `main.gd`, minimapa, HUD, objetos de cenário e a parte espacial do gerador de masmorra.
- [2026-11-14] (i) Renderizador: escolher entre "Mobile" e "Compatibility" no protótipo, medindo na máquina de Pedro. "Forward+" só entra se sobrar desempenho. Meta: **60 fps em 1080p** no vídeo integrado, com escala de resolução se for preciso.
- [2026-11-14] (e) O addon `phantom_camera` funciona em 3D e pode ser reaproveitado para a câmera fixa. ~superseded 2026-11-14 → ver linha seguinte.
- [2026-11-14] (e) Os addons `phantom_camera` e `limboai` do projeto 2D são implementações caseiras (autor "Antigravity Team") e só funcionam em 2D (`phantom_camera_2d.gd`). Não vão para o projeto 3D: a câmera fixa e a IA são escritas do zero.
- [2026-11-14] (e) Bug no 2D: há 59 verificações `Engine.has_singleton("<Autoload>")`, e elas sempre retornam falso para autoloads (confirmado rodando a Godot 4.7.2: `has_singleton(SaveManager)=false` com o nó do autoload presente). O resultado é que bônus de perks, saves disparados por perks e outras integrações ficam desligados sem aviso. Todo código portado precisa trocar essa verificação.

## 7. Primeiro bloco: "Tela e sensação"

- [2026-11-14] (d) É o primeiro marco.
- [2026-11-14] (i) Conteúdo mínimo: o projeto 3D criado com git e `context/`; **uma sala** do kit modular; o **Cavaleiro** modelado, texturizado e animado (parado, andar, ataque, esquiva, parry, dano, morte); câmera fixa inclinada; luz ao redor do herói; **um inimigo comum**; HUD mínimo com vida, vigor e sanidade; o efeito do Véu numa parede ilusória. ~superseded 2026-11-14 → ver linha seguinte.
- [2026-11-14] (i) O bloco corre em **duas trilhas paralelas**. **Trilha de jogo:** projeto 3D com git e `context/`, uma sala em blocos cinzas, câmera fixa inclinada, luz ao redor do herói, controle (teclado, mouse e gamepad), combate com um inimigo comum, HUD mínimo e o efeito do Véu numa parede ilusória, tudo com um herói provisório. **Trilha de arte:** guia de estilo, conceito do Cavaleiro aprovado por Pedro, prova do pipeline (IA → Blender → Godot) e o Cavaleiro final com as animações (parado, andar, ataque, esquiva, parry, dano, morte), mais as peças de uma sala do kit modular. O bloco termina quando a arte substitui os provisórios.
- [2026-11-14] (i) Motivo: a arte é o maior risco (modelos originais, Pedro sem Blender). As trilhas separadas permitem acertar a sensação de jogo sem esperar pela arte.
- [2026-11-14] (i) Critério de pronto: Pedro joga e acha **bonito e gostoso de controlar**; roda a 60 fps na máquina dele; uma captura de tela serve de imagem de portfólio sem retoque.
- [2026-11-14] (i) Fora deste bloco: o Poço procedural, Mago, Demônio, saque, árvore e todos os outros sistemas.

## 8. Ordem sugerida depois do primeiro bloco

- [2026-11-14] (i) 1) Poço procedural com o kit modular e um chefe no andar 5 → 2) árvore de habilidades e níveis → 3) saque enxuto e forja → 4) Véu completo (faixas, passagens, fragmentos) → 5) Mago → 6) Demônio → 7) santuário e sistemas mantidos → 8) página da Steam e build da demo. ~superseded 2026-11-14 → ver linha seguinte.
- [2026-11-14] (i) 1) Poço procedural com o kit modular e o chefe do andar 5 → 2) árvore de habilidades e níveis → 3) saque enxuto e forja → 4) Véu completo, com faixas, passagens, fragmentos e possessão → 5) Mago → 6) Demônio (aproveitando a criatura da possessão) → 7) chefe do andar 10 e chefe final impossível (etapa 1) → 8) santuário e sistemas mantidos → 9) andares 11 a 20 e chefes 15 e 20 (etapa 2) → 10) página da Steam e build da demo.

## 9. Em aberto (decisões de Pedro)

- [2026-11-14] (i) **O Demônio:** que fantasia e que estilo de luta ele tem? Isso define modelo, animações e árvore. ~superseded 2026-11-14 → ver linha seguinte.
- [2026-11-14] (i) **O preço do Véu:** o que acontece com o jogador em cada faixa de sanidade e quando ela chega a zero. ~superseded 2026-11-14 → ver linha seguinte.
- [2026-11-14] (i) **Tamanho da demo:** até qual andar ela vai e quantos chefes tem. ~superseded 2026-11-14 → ver linha seguinte.
- [2026-11-14] (i) Resolvido na rodada 4: o Demônio está em §4.4, a sanidade zero em §4.6 e o tamanho da demo em §4.5. Continuam em aberto o efeito de cada faixa intermediária de sanidade (proposta em §4.6) e a confirmação das duas etapas da demo.

## 10. Deixado ao construtor

- [2026-11-14] (i) Estrutura de pastas e cenas do projeto 3D, organização dos autoloads, formato de save e migração do save 2D (não é necessária).
- [2026-11-14] (i) Escolha do renderizador por medição, valores de luz e névoa, configurações gráficas.
- [2026-11-14] (i) Ferramentas gratuitas específicas do pipeline de arte, desde que a licença seja conferida e registrada.
- [2026-11-14] (i) Como reaproveitar a lógica de combate 2D (portar ou reescrever) e quais testes visuais existentes (`test_visual_runner.gd`) vale manter.
