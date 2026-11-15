---
tipo: contexto
projeto: eldritch-depths-3d
descricao: Visão, metas, restrições e regras do jogo, resumidas da spec aprovada.
estado: estavel
criado: 2026-11-14
---

# Produto

> Resumo dos §1, §2 e §4 da spec `docs/superpowers/specs/2026-11-14-eldritch-depths-3d-design.md`. Em caso de dúvida, **a spec vale**. Decisões com motivo e alternativas descartadas ficam em [[decisoes]].

## Intenção {#intencao}

- [2026-11-14] (d) RPG de ação **viciante**, referência **Diablo**: a pessoa quer evoluir e não para de jogar.
- [2026-11-14] (d) Gráficos **mais realistas e menos quadrados** que o 2D; o herói atual ("todo quebrado e sem um visual") está vetado.
- [2026-11-14] (d) Dois usos: **demo pública na Steam** e **portfólio**. "A arte não pode ficar feia."
- [2026-11-14] (d) Horror cósmico com a **sanidade como percepção da realidade**; ela precisa ganhar história e função.

## Metas e limites {#metas}

- [2026-11-14] (d) Demo com **3 classes: Cavaleiro, Mago e Demônio**.
- [2026-11-14] (d) Progressão: árvore de habilidades, classes/builds, dificuldade que escala sem fim e **saque enxuto**.
- [2026-11-14] (d) Primeiro bloco: **"Tela e sensação"** — câmera, luz, herói, controle e combate bons antes de qualquer conteúdo.
- [2026-11-14] (d) **Congelados:** integração com Steam, ranking e mensagens da comunidade.
- [2026-11-14] (i) Multiplayer e consoles fora do escopo.
- [2026-11-14] (d) Anti-metas: arte feia ou inconsistente; herói desconjuntado ou sem identidade.
- [2026-11-14] (i) Anti-metas: interface que ocupa a tela; sanidade como barra que só cai e incomoda.

## Restrições {#restricoes}

- [2026-11-14] (d) **Orçamento R$ 0.** Só ferramentas, assets e serviços gratuitos.
- [2026-11-14] (d) Modelos 3D **originais** (IA + retoque). Animações e texturas de terceiros só se gratuitas e liberadas para uso comercial.
- [2026-11-14] (d) **Sem prazo.** **PC mínimo: notebook com vídeo integrado.**
- [2026-11-14] (e) Máquina de desenvolvimento: Ryzen com Radeon integrada (RADV RENOIR), Vulkan 1.3, 30 GB de RAM.
- [2026-11-14] (e) A Steam exige declarar conteúdo gerado por IA.

## O jogo {#jogo}

- [2026-11-14] (d) **3D com câmera fixa inclinada**, estilo dos Diablo atuais; arte **semi-realista pintada**; **luz quente ao redor do herói** num mundo escuro.
- [2026-11-14] (i) Enquadramento: começa no atual (herói ≈ 1/13 da altura da tela) e testa um mais próximo (≈ 1/8); Pedro escolhe jogando.
- [2026-11-14] (d) **HUD mínimo, estilo soulslike:** barras finas de vida, vigor e sanidade num canto, poucos atalhos e barra do chefe só na luta.
- [2026-11-14] (d) Combate **ágil e fluido**: ataque, esquiva, parry, magia cósmica, postura e frascos.
- [2026-11-14] (d) **Teclado e mouse e gamepad desde o início**; Steam Deck fora por enquanto.
- [2026-11-14] (i) Mira: mouse no teclado; analógico direito ou direção do movimento no controle. Os botões mostrados mudam com o dispositivo.
- [2026-11-14] (d) Classes: **Cavaleiro** (o encapuzado de armadura escura e espada longa), **Mago** e **Demônio = Senhor de lacaios** (invocador).
- [2026-11-14] (d) **O Poço sem fundo:** do santuário se desce andar por andar, sorteados, com chefe feito à mão a cada 5 andares, descida infinita.
- [2026-11-14] (d) Demo em **duas etapas**: andares 1–10 com 2 chefes e o chefe final impossível; depois andares 11–20 com os chefes 15 e 20. No fim, "Adicione à lista de desejos", sem data.

## O Véu (sanidade) {#veu}

- [2026-11-14] (d) A mente é um véu que esconde o que habita as profundezas: quanto mais fino, mais se vê.
- [2026-11-14] (d) O Véu revela **passagens e andares secretos** e **fragmentos de habilidade** (pontos extras na árvore).
- [2026-11-14] (d) **Sanidade zero = Possessão:** nasce do herói um Senhor de lacaios que precisa ser derrotado; perder é morrer.
- [2026-11-14] (i) Proposta: três faixas (100–60, 60–30, 30–0), cada uma revelando e cobrando mais. **O efeito de cada faixa segue em aberto com Pedro.**
- [2026-11-14] (i) A sanidade cai devagar no Poço e com golpes cósmicos; a escolha do jogador é quando usar o láudano ou voltar ao santuário.

## História {#historia}

- [2026-11-15] (d) **Cada jogador dá o nome ao próprio personagem**; o texto da história não nomeia o herói.
- [2026-11-15] (d) A história pode ser **criada** (a spec só tinha a premissa), **com nomes novos** de lugares e personagens, que Pedro aprova junto com o texto.
- [2026-11-15] (d) O que move o herói: a **esperança de salvar o mundo e a Princesa**, "à la Mario Bros".
- [2026-11-15] (d) Linguagem em **português arcaico** (tratamento por "tu").
- [2026-11-15] (d) As **classes** entram na história **já agora**, mesmo antes de Mago e Demônio existirem no jogo.
- [2026-11-15] (d) **O Demônio é alguém que sobreviveu à própria possessão** — promove a ideia `(i)` da spec §4.4/§4.6.
- [2026-11-15] (d) **História aprovada por Pedro** ("perfeito"), em seis parágrafos, no `README.md` (seção "A história"): o Reino de Solvéria; na noite da Maré Astral o chão do Santuário das Cinzas se fende e abre o Poço sem fundo; Oth-Ysael, Aquele Que Sonha Sob o Poço, arrasta para as trevas a Princesa Aurélia, derradeira herdeira; o andarilho sem nome fixo desce abençoado por Illyria, a Guardiã das Cinzas; o juízo é o que os olhos alcançam e o Véu revela passagens, andares e fragmentos de poder; o juízo a zero faz nascer do herói um Senhor de lacaios; descem o Cavaleiro, o Mago ("lê nas estrelas o que o Poço esconde") e o Demônio (sobrevivente da própria possessão).
- [2026-11-15] (d) **Nomes aprovados:** Reino de Solvéria, Princesa Aurélia, Oth-Ysael (Aquele Que Sonha Sob o Poço) e Santuário das Cinzas, criados agora; Illyria, a Guardiã das Cinzas, e a Maré Astral, vindos do 2D. O Guardião dos Mil Olhos fica fora da história por ora.
