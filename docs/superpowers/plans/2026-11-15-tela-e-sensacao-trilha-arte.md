# Tela e sensação — Trilha de arte (Bloco 1B) Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Trocar os provisórios do Bloco 1A (cápsulas e blocos cinzas) por arte original: o Cavaleiro modelado, pintado e animado, o inimigo comum (o Cultista) e uma sala do kit modular, com um guia de estilo que mantém tudo coerente e o registro de origem e licença de cada peça.

**Architecture:** Pedro opera, com a conta dele, os serviços gratuitos de IA (imagem e 3D) e o Mixamo; o Claude escreve os prompts e faz todo o resto no Blender **por script**, sem mexer à mão: cada modelo sai de um `build.py` reproduzível que lê o arquivo bruto em `art/brutos/` e grava o `.glb` em `assets/models/`. A cada etapa visual, o script renderiza pré-visualizações que Pedro aprova. No jogo, um componente `CharacterVisual` liga a máquina de estados às animações, sem tocar em nenhum valor de jogabilidade.

**Tech Stack:** Blender 4.5.15 LTS sem janela (`/home/usuario/.local/bin/blender -b`, Python embutido), Godot 4.7.2, GDScript. Serviços online gratuitos operados por Pedro: Qwen-Image-Edit e FLUX.1 [schnell] (Spaces do Hugging Face), TRELLIS.2 (Space `microsoft/TRELLIS.2`), Meshy (plano grátis, só como reserva) e Mixamo (Adobe ID grátis). Nenhum addon novo na Godot e nenhum pacote Python novo.

**Spec:** `docs/superpowers/specs/2026-11-14-eldritch-depths-3d-design.md`. Ler §3, §4.1, §5, §7 e §10 antes de começar.

**Ledger:** `docs/superpowers/plans/2026-11-15-tela-e-sensacao-trilha-arte-ledger.md`.

**Relação com o Bloco 1A:** a trilha de jogo (`2026-11-14-tela-e-sensacao-trilha-jogo.md`) está pronta, menos a T32 (Pedro joga). Duas tarefas daqui (B06 e B14) esperam a resposta **(a)** da T32, o enquadramento escolhido, porque ele fixa o nível de detalhe do herói e do cenário (spec §4.1).

---

## Como trabalhar neste plano (vários modelos, vários dias)

As regras de sessão do plano do Bloco 1A valem aqui sem mudança (ler a seção "Como trabalhar neste plano" de lá): ler o cabeçalho, a linha no ledger e a tarefa; conferir dependências; marcar `em andamento` com commit `docs: start B<nn>`; `tools/test.sh` verde antes e depois; Interfaces são contrato; não adiantar tarefas futuras.

O que muda nesta trilha:

- **Tarefas com Pedro.** Os passos marcados **[Pedro]** são dele: rodar um serviço online, escolher animações no Mixamo, aprovar uma imagem. O modelo prepara tudo para esse passo (prompt, link, configurações, onde salvar), avisa Pedro e marca a tarefa como `aguarda Pedro` no ledger, com uma linha dizendo o que falta. Nunca cria conta, nunca opera um serviço no lugar dele.
- **Portões de aprovação.** Um passo **[Portão]** só passa com a aprovação de Pedro por escrito. O ledger guarda a frase dele entre aspas e a data. Sem aprovação, a tarefa não fica `feita`, e nenhuma tarefa que dependa dela começa. Se Pedro pedir mudanças, a tarefa volta ao passo indicado; cada rodada vira uma linha nas notas.
- **Nada à mão no Blender.** Todo arquivo em `assets/models/` precisa sair de novo, igual, rodando o `build.py` dele. Pedro nunca usou o Blender (spec §3); um retoque que só existe num `.blend` salvo à mão se perde.
- **Status extra no ledger:** `aguarda Pedro`.
- **Nível `arte`:** julgamento visual. Usar o modelo mais capaz disponível e, nas pré-visualizações, olhar a imagem de verdade (ferramenta de leitura de imagem), nunca só o relatório numérico.

---

## Global Constraints

- **Orçamento R$ 0.** Nenhuma ferramenta, asset ou serviço pago. Se a cota grátis de um serviço acabar, espera-se a cota renovar.
- **Modelos 3D originais**, gerados por IA e retocados por nós. **Animações e texturas de terceiros** só se forem gratuitas e liberadas para uso comercial. **Proibidos:** kits de cenário prontos, corpos-base prontos e os personagens prontos do Mixamo. O auto-rig do Mixamo sobre o **nosso** modelo é permitido.
- **Hunyuan3D proibido:** a licença dele exclui União Europeia, Reino Unido e Coreia do Sul, e a demo na Steam é vendida nesses lugares.
- **Registro antes do commit.** Nenhum arquivo entra em `art/brutos/` ou `assets/models/` sem a linha dele em `context/assets.md` (B02). O teste `test_assets_registrados` reprova o que faltar.
- **Steam:** todo uso de IA fica registrado para a declaração de conteúdo gerado por IA (rascunho na B16).
- **Desempenho:** 60 fps em 1080p no vídeo integrado (AMD RADV RENOIR), medido com `tools/measure_fps.sh mobile`. Orçamentos de triângulos e texturas no guia de estilo (B01).
- **Jogabilidade intocada.** A arte não muda nenhum valor de jogo: formas e camadas de colisão, velocidades, durações de estado, alcances. As 129 asserções da suíte atual continuam passando; um teste antigo só muda quando um nó que ele lê é trocado (B10 e B13 dizem quais).
- **Escala:** 1 unidade da Godot = 1 m. Herói com 1,80 m (a cápsula de colisão), paredes com 3 m, sala de 16 × 16 m.
- **Orientação:** o `Player3D` e o `EnemyCommon` olham para −Z (usam `look_at`). Modelos glTF importados olham para +Z, então o nó `Visual` gira 180° em Y.
- **Pastas:**
  - `art/` (com `.gdignore`): fontes da arte. `art/prompts/` (prompts escritos pelo Claude), `art/brutos/` (saída crua dos serviços, nome `YYYY-MM-DD-<serviço>-<assunto>.<ext>`), `art/<categoria>/<nome>/build.py`.
  - `assets/models/<categoria>/<nome>.glb`: o que o jogo carrega.
  - `docs/arte/` (com `.gdignore`): guia de estilo e as pré-visualizações **aprovadas** (`docs/arte/previas/<nome>/`).
  - Material bruto de arte fica em `art/brutos/`, não em `fontes/`: são insumos de produção registrados em `context/assets.md`, não documentos a interpretar.
- **Arquivos grandes:** bruto acima de 50 MB não vai para o git. Fica em `art/brutos/` local (padrão `art/brutos/*.grande.*` no `.gitignore`), com SHA-256 e tamanho registrados em `context/assets.md`.
- **Temporários** (renders de trabalho, quadros de captura): `.godot/capturas_tmp/`, ignorada pelo git.
- **Commits:** Conventional Commits em inglês, sem `Co-Authored-By` nem menção à IA. **Push só com ordem de Pedro.**
- **Fatos em `context/`:** data `[YYYY-MM-DD]` e procedência `(d)`/`(i)`/`(e)`; nada se apaga (`~superseded`); `python lint.py` depois de mexer em `context/`.
- **Testes:** `tools/test.sh` (Godot, última linha `OK: <n> testes`) e, a partir da B03, `tools/test_blender.sh` (mesmo formato de saída).

## Review Focus

1. **Modelo virado, flutuando ou afundado:** o rosto do Cavaleiro e do Cultista aponta para onde o corpo anda e mira, e os pés tocam o chão (y = 0, tolerância 3 cm) parado e andando. Testes na B09, B10 e B13.
2. **Animação que não cabe no estado:** um ataque de 0,40 s com um clipe de 1,2 s seria cortado no meio, e um clipe curto congelaria. Cada clipe de ação toca na duração exata do estado do jogo. Testes na B10 e B13.
3. **Root motion:** um rolamento do Mixamo que anda sozinho tiraria o modelo de cima da colisão. Os quadris não andam no plano XZ em nenhum clipe (até 5 cm). Testes na B09 e B13.
4. **Brilho de aviso compartilhado:** com o modelo novo, o vermelho do aviso de um inimigo não pode acender outro (hoje isso é garantido pelo material único por instância). Teste na B13.
5. **Asset sem origem registrada:** todo arquivo em `assets/models/` e `art/brutos/` tem linha em `context/assets.md`. Teste na B02, que vale para todas as tarefas seguintes.

---

## Mapa das tarefas

| Fase | Tarefas | O que entrega |
|---|---|---|
| 0. Base | B01–B03 | Guia de estilo aprovado, registro de licenças, ferramentas do Blender por script |
| 1. Prova do pipeline | B04 | Um braseiro feito por IA → Blender → Godot, aceso na sala cinza |
| 2. Cavaleiro | B05–B10 | Conceito aprovado, malha, textura, espada, rig e animações, herói novo no jogo |
| 3. Cultista | B11–B13 | Conceito, modelo e animações, inimigo novo no jogo |
| 4. Cenário | B14–B15 | Peças do kit e a sala montada com elas, parede do Véu incluída |
| 5. Fecho | B16–B17 | Luz, captura de portfólio, fps, README, declaração de IA; Pedro joga e aprova |

Paralelo depois das dependências: B01, B02 e B03 entre si; o ramo do Cultista (B11–B12) e o do kit (B14) correm ao lado do Cavaleiro.

---

### B01: Guia de estilo
**Nível:** arte · **Depende de:** —

**Files:** Create `docs/arte/guia-de-estilo.md`, `docs/arte/paleta.svg`, `docs/arte/.gdignore`, `art/.gdignore`

**Interfaces — Produces:** os valores que todas as tarefas seguintes citam. O guia tem estas seções, nesta ordem:
- **Direção:** semi-realista pintada, proporções reais, formas um pouco exageradas, fantasia sombria (spec §4.1). Sem contorno (outline): a leitura vem da luz quente no herói.
- **Paleta:** no máximo 16 cores com hex e uso. Partir das cores já no jogo (luz do herói `#ffb36b`, fundo `#05060a`, névoa `#0b0d12`, aviso `#ff2020`, violeta do Véu da `veil_wall.tscn`) e das ilustrações 2D `hero.png` e `cultist.png` do projeto 2D (`assets/sprites/`). `paleta.svg` mostra as amostras com o hex embaixo.
- **Valores de luz:** o valor (claro/escuro) de cada material sob a luz do herói: armadura escura mas com borda que pega luz, pedra do cenário mais escura que o herói, violeta só como acento.
- **Orçamentos** (cada um é um limite que os testes conferem): Cavaleiro ≤ 20.000 triângulos, textura base 2048²; espada ≤ 2.000, 512²; Cultista ≤ 12.000, 1024²; peça do kit ≤ 1.500, texturas compartilhadas de 1024²; prop ≤ 3.000, 1024². No máximo 2 materiais por personagem.
- **Escala e grade:** 1 unidade = 1 m; herói 1,80 m; Cultista até 1,95 m; paredes 3 m de altura e 0,4 m de espessura; grade do kit de 2 m (a sala de 16 × 16 m, a porta de 2 m e a saleta de 4 × 4 m do 1A cabem nela).
- **Nomes:** pastas e arquivos em português sem acento e em minúsculas; clipes de animação em inglês (lista na B09).
- **Luz das pré-visualizações:** a mesma da B03 (luz principal `#ffb36b`, contraluz `#3a4a6a`, fundo `#05060a`), para Pedro aprovar a peça sob a luz do jogo.

**Passos:**
- [ ] **Passo 1:** Ler as duas ilustrações 2D e as cenas do 1A, escrever o guia e o SVG.
- [ ] **Passo 2:** Criar `art/.gdignore` e `docs/arte/.gdignore` (vazios). Rodar `tools/test.sh`. Esperado: `OK: 129 testes`.
- [ ] **Passo 3:** Commit `docs: add art style guide`.
- [ ] **Passo 4 [Portão]:** Mostrar a Pedro o guia e a paleta. Registrar a aprovação no ledger; mudanças pedidas voltam ao Passo 1 e ganham novo commit.

**Pronto quando:** Pedro aprovou o guia por escrito.

---

### B02: Registro de origem e licenças
**Nível:** simples · **Depende de:** —

**Files:** Create `context/assets.md`, `tests/test_assets_registry.gd` · Modify `context/index.md` (uma linha na tabela), `.gitignore` (`art/brutos/*.grande.*`)

**Interfaces — Produces:**
- `context/assets.md` (frontmatter `tipo: registro`, `descricao`, `estado: estavel`) com duas seções:
  - **`## Ferramentas e serviços {#ferramentas}`:** uma linha (e) por ferramenta, com licença, URL conferida e data. Conferir de novo cada uma na página oficial no dia da tarefa, não copiar daqui. Ponto de partida, conferido em 2026-11-15:
    - TRELLIS.2: licença MIT no cartão do modelo `huggingface.co/microsoft/TRELLIS.2-4B`; Space `microsoft/TRELLIS.2`.
    - Qwen-Image-Edit: Apache 2.0 (`huggingface.co/Qwen/Qwen-Image-Edit-2509`); Space `Qwen/Qwen-Image-Edit`.
    - FLUX.1 [schnell]: Apache 2.0 (`huggingface.co/black-forest-labs/FLUX.1-schnell`).
    - Meshy, plano grátis (reserva): CC BY 4.0, uso comercial com atribuição, 100 créditos por mês (`docs.meshy.ai/en/webapp/pricing`). Se for usado, a atribuição entra nos créditos do jogo.
    - Mixamo: personagens e animações royalty-free para projetos comerciais, jogos incluídos, com Adobe ID grátis (FAQ da Adobe, `helpx.adobe.com/creative-cloud/faq/mixamo-faq.html`). A página bloqueou leitura automática em 2026-11-15: Pedro confere a FAQ no navegador antes da B09 e a linha é registrada como (d).
    - Hunyuan3D: excluído (licença sem validade em UE, Reino Unido e Coreia do Sul).
    - Blender 4.5.15 LTS: GPL; o que se cria com ele é nosso.
  - **`## Assets {#assets}`:** uma tabela, uma linha por arquivo: `| arquivo | tipo | origem | ferramenta e modelo | licença | operador | data | prompt | sha256 |`. `tipo` é `bruto`, `modelo` ou `textura`; `origem` é `ia`, `script`, `mixamo` ou `terceiro`.
- `test_assets_registrados`: varre `res://assets/models/` (recursivo, só `.glb`, `.png`, `.jpg`) e lê `art/brutos/` por caminho absoluto do projeto (`ProjectSettings.globalize_path("res://art/brutos")`, pulando `.gdignore`); todo caminho relativo à raiz tem de aparecer na coluna `arquivo` de `context/assets.md`. Pastas que ainda não existem contam como vazias.

**Passos:**
- [ ] **Passo 1:** Escrever `test_assets_registrados` e um segundo teste, `test_registro_acusa_falta`, que chama a função de checagem com uma lista falsa de arquivos e um registro sem eles e espera a lista dos faltantes.
- [ ] **Passo 2:** Rodar `tools/test.sh`. Esperado: FAIL em `test_registro_acusa_falta` (função inexistente).
- [ ] **Passo 3:** Implementar a checagem (`static func missing_entries(files: PackedStringArray, registry_text: String) -> PackedStringArray` no próprio arquivo de teste ou em `scripts/tools/assets_registry.gd`) e criar `context/assets.md`.
- [ ] **Passo 4:** `tools/test.sh` → `OK: 131 testes`; `python lint.py` → `nada a reportar.`
- [ ] **Passo 5:** Commit `feat: add asset origin and license registry`.

**Pronto quando:** os dois testes passam e o lint está limpo.

---

### B03: Ferramentas do Blender por script
**Nível:** difícil · **Depende de:** —

**Files:** Create `tools/blender.sh`, `tools/test_blender.sh`, `tools/blender/.gdignore`, `tools/blender/ed_blender.py`, `tools/blender/report.py`, `tools/blender/tests/test_ed_blender.py` · Modify `context/arquitetura.md` (pastas `art/`, `assets/models/`, `tools/blender/` e o fluxo)

**Interfaces — Produces:**
- `tools/blender.sh <script.py> [args…]`: roda `"${BLENDER:-blender}" -b --factory-startup --python-exit-code 1 --python <script> -- <args>` a partir da raiz do repositório e devolve o código do Blender.
- `tools/test_blender.sh`: roda `tools/blender/tests/test_ed_blender.py`; última linha `OK: <n> testes` (código 0) ou `FALHOU: <x> de <n>` (código 1), como o runner da Godot.
- Módulo `ed_blender` (importável por qualquer `build.py` com `sys.path` apontando para `tools/blender/`):
  - `reset_scene() -> None` — cena vazia, unidades métricas, escala 1.
  - `import_any(path: str) -> list` — `.glb`/`.gltf`/`.fbx`/`.obj` pela extensão; devolve os objetos novos.
  - `join_meshes(objs: list, name: str) -> Object`
  - `apply_transforms(obj) -> None`
  - `scale_to_height(obj, height_m: float) -> None` — escala uniforme pela altura em Z.
  - `set_origin_to_feet(obj) -> None` — origem no centro XY da base, base em z = 0.
  - `decimate_to(obj, max_tris: int) -> int` — devolve os triângulos finais (≤ `max_tris`).
  - `remesh_quadriflow(obj, target_faces: int) -> Object` — malha nova, limpa; a original fica.
  - `smart_uv(obj, margin: float = 0.01) -> None`
  - `bake_color(src, dst, size: int, out_png: str) -> str` — Cycles na CPU, cor difusa de `src` para a UV de `dst`.
  - `render_turnaround(objs: list, out_dir: str, size: int = 1024) -> list[str]` — quatro PNGs (`frente`, `lado`, `costas`, `tres_quartos`), Cycles na CPU com 32 amostras, luz do guia (B01).
  - `export_glb(objs: list, path: str, animations: bool = False) -> None` — glTF binário, Y para cima, modificadores aplicados.
  - `report(objs: list) -> dict` — chaves `tris`, `dims` ([x, y, z] em m), `min_z`, `materials`, `has_uv`, `bones`, `actions`.
- `tools/blender/report.py <arquivo>`: importa e imprime uma linha `RELATORIO <json do report>`.

**Passos:**
- [ ] **Passo 1:** Escrever `test_ed_blender.py` (funções `test_*`, um runner mínimo no fim do arquivo que conta, imprime e sai com o código certo):
  - `test_escala_altura`: cubo de 2 m, `scale_to_height(1.8)` → `dims[2]` ≈ 1,8 (±0,001).
  - `test_origem_nos_pes`: cubo deslocado → `set_origin_to_feet` → `min_z` ≈ 0 e centro XY ≈ 0.
  - `test_decimate`: icosfera com 5 subdivisões (20.480 triângulos), `decimate_to(…, 5000)` → entre 4.000 e 5.000.
  - `test_exporta_e_reimporta`: `export_glb` de uma icosfera para `.godot/capturas_tmp/`, `reset_scene`, `import_any` → mesmos triângulos.
  - `test_turnaround`: `render_turnaround` de um cubo com `size=128` → quatro PNGs de 128 × 128.
  - `test_relatorio`: `report.py` de um `.glb` imprime uma linha que começa com `RELATORIO ` e cujo JSON tem as sete chaves.
- [ ] **Passo 2:** Rodar `tools/test_blender.sh`. Esperado: FALHOU, módulo inexistente.
- [ ] **Passo 3:** Implementar o módulo, `report.py` e os dois `.sh`.
- [ ] **Passo 4:** `tools/test_blender.sh` → `OK: 6 testes`. Anotar no ledger o tempo do `test_turnaround` (Cycles na CPU desta máquina).
- [ ] **Passo 5:** Atualizar `arquitetura.md`; `python lint.py`; commit `feat: add headless blender toolkit`.

**Pronto quando:** `OK: 6 testes` e o lint limpo.

---

### B04: Prova do pipeline — o braseiro
**Nível:** arte · **Depende de:** B01 (aprovada), B02, B03

**Por quê:** spec §7 e achado A02: provar IA → Blender → Godot com uma peça pequena antes de arriscar o Cavaleiro. Um braseiro de ferro serve à sala e à luz quente.

**Files:** Create `art/prompts/braseiro.md`, `art/brutos/<data>-flux-braseiro.png` e `art/brutos/<data>-trellis2-braseiro.glb` (por Pedro), `art/props/braseiro/build.py`, `assets/models/props/braseiro.glb`, `scenes/props/brazier.tscn`, `tests/test_art_props.gd`, `docs/arte/previas/braseiro/*.png` · Modify `scenes/main.tscn` (dois braseiros), `context/assets.md`, `context/achados.md` (A02: o que a prova mostrou)

**Interfaces — Produces:**
- `art/prompts/<nome>.md` (modelo para todas as tarefas com IA): serviço e link do Space, prompt, prompt negativo, configurações, nome do arquivo para salvar em `art/brutos/` e o que conferir antes de mandar ao Claude.
- `build.py` de cada peça segue o mesmo esqueleto: `reset_scene` → `import_any(bruto)` → limpeza → orçamento → textura → `set_origin_to_feet` → `render_turnaround` para `.godot/capturas_tmp/<nome>/` → `export_glb` → imprime `report`. Rodar: `tools/blender.sh art/<categoria>/<nome>/build.py`.
- `brazier.tscn`: `StaticBody3D` (camada 1) com o modelo, colisão em cilindro e uma `OmniLight3D` `FlameLight` (cor e energia do guia, sombra desligada por desempenho).

**Passos:**
- [ ] **Passo 1:** Escrever `art/prompts/braseiro.md`: imagem pelo FLUX.1 [schnell] (braseiro de ferro forjado sobre três pés, brasas, peça isolada em fundo cinza liso, vista 3/4, pintura semi-realista), depois a imagem no TRELLIS.2.
- [ ] **Passo 2 [Pedro]:** gerar a imagem e o modelo nos Spaces e salvar os dois em `art/brutos/` com os nomes do prompt. Registrar os dois em `context/assets.md` (operador Pedro).
- [ ] **Passo 3:** Escrever `test_braseiro` em `tests/test_art_props.gd`: carregar `res://assets/models/props/braseiro.glb` → triângulos ≤ 3.000, altura entre 0,8 e 1,2 m, base em y ≈ 0 (±0,03). Rodar `tools/test.sh`: FAIL (arquivo inexistente).
- [ ] **Passo 4:** Escrever `build.py` (decimate para ≤ 3.000; cor assada e ajustada à paleta), rodar e **olhar** as quatro pré-visualizações.
- [ ] **Passo 5:** `brazier.tscn` e dois braseiros em `main.tscn` (cantos da parede sul, longe do caminho do inimigo). `tools/test.sh` → todos passam.
- [ ] **Passo 6:** Captura como na T31 (`--fullscreen --write-movie .godot/capturas_tmp/b04/f.png --fixed-fps 30 --quit-after 90 -- --autoplay`), olhar o último quadro.
- [ ] **Passo 7 [Portão]:** mostrar a Pedro as pré-visualizações e a captura. Aprovado, copiar as pré-visualizações para `docs/arte/previas/braseiro/`.
- [ ] **Passo 8:** Registrar em `achados.md` (A02, linha nova) o que a prova mostrou: qualidade da malha do TRELLIS.2, tempo de cada etapa, o que precisou de reserva. Commit `feat: add brazier prop through the ai to godot pipeline`.

**Pronto quando:** o braseiro aprovado está na sala, os testes passam e o A02 diz o que a prova ensinou.

**Se o TRELLIS.2 falhar** (malha inútil ou Space fora do ar por mais de um dia): repetir o Passo 2 no Meshy grátis, registrar a atribuição CC BY 4.0 e anotar o ruling no ledger.

---

### B05: Conceito do Cavaleiro
**Nível:** arte · **Depende de:** B01 (aprovada)

**Files:** Create `art/prompts/cavaleiro-conceito.md`, brutos em `art/brutos/`, `docs/arte/cavaleiro-conceito.png` · Modify `context/assets.md`

**Requisitos do conceito** (spec §7): fiel ao `hero.png` do 2D (capuz, rosto na sombra, armadura de placas escura, capa, acentos violeta rúnicos); três vistas — frente, lado e costas — na mesma escala; corpo inteiro em **pose A** (braços a 45°), sem a espada na mão (ela é modelada à parte na B08); fundo cinza liso e luz uniforme; pelo menos 1024 px de altura por vista. A pose A e o fundo liso são o que o gerador 3D e o auto-rig do Mixamo pedem.

**Passos:**
- [ ] **Passo 1:** Escrever o prompt: Qwen-Image-Edit com o `hero.png` como referência (uma geração por vista); FLUX.1 [schnell] como reserva só por texto.
- [ ] **Passo 2 [Pedro]:** gerar, escolher as melhores e salvar em `art/brutos/`. Registrar.
- [ ] **Passo 3:** Montar `docs/arte/cavaleiro-conceito.png` (as três vistas lado a lado, mesma altura) com um script Blender pequeno (plano com as imagens, render ortográfico) ou GIMP em lote; registrar a ferramenta usada.
- [ ] **Passo 4 [Portão]:** Pedro aprova a folha. Commit `docs: add approved knight concept sheet`.

**Pronto quando:** a folha aprovada está no repositório e registrada.

---

### B06: Cavaleiro — malha limpa
**Nível:** arte · **Depende de:** B04, B05, resposta (a) da T32

**Files:** Create `art/prompts/cavaleiro-3d.md`, bruto do TRELLIS.2 em `art/brutos/`, `art/personagens/cavaleiro/build_malha.py` · Modify `context/assets.md`

**Interfaces — Produces:** `build_malha.py` grava `art/personagens/cavaleiro/cavaleiro_malha.glb` (intermediário, registrado) com: uma malha só, pose A, 1,80 m, pés em z = 0, olhando para −Y do Blender (frente na exportação glTF = +Z), ≤ 20.000 triângulos, UV nova e a cor do bruto assada nela em 2048².

O enquadramento da T32 decide o detalhe: no "próxima" (herói ≈ 1/8 da tela) o rosto, as placas e a capa precisam de forma própria; no "atual" (≈ 1/13) a silhueta manda e o orçamento pode ficar abaixo do teto.

**Passos:**
- [ ] **Passo 1:** Prompt para o TRELLIS.2 com a vista de frente aprovada (e a de 3/4, se o Space aceitar várias). **[Pedro]** gera e salva o bruto. Registrar.
- [ ] **Passo 2:** `build_malha.py`: juntar, `remesh_quadriflow` (malha limpa, simétrica onde der), `decimate_to(20000)`, `smart_uv`, `bake_color` do bruto para a malha nova, escala e origem. Rodar e olhar as pré-visualizações ao lado da folha de conceito.
- [ ] **Passo 3 [Portão]:** Pedro compara as pré-visualizações com o conceito. Aprovado, copiar para `docs/arte/previas/cavaleiro-malha/` e commit `feat: add knight base mesh`.

**Pronto quando:** a malha aprovada sai do `build_malha.py` dentro do orçamento.

---

### B07: Cavaleiro — textura pintada
**Nível:** arte · **Depende de:** B06

**Files:** Create `art/personagens/cavaleiro/build_textura.py`, `art/personagens/cavaleiro/textura_base.png` · Modify `context/assets.md`

A cor assada do gerador vem com luz e sombra embutidas e ruído. A textura final é **pintada**: valores do guia (B01), sombras embutidas suavizadas, bordas das placas clareadas para pegar a luz do herói, acentos violeta nas runas, ruído removido. O script faz o grosso (correção de valor e matiz para a paleta, máscara de bordas por curvatura assada, limpeza). Pedro pode retocar a imagem no GIMP se quiser; nesse caso, o arquivo retocado entra em `art/` como fonte nova, registrado, e o script passa a partir dele.

**Passos:**
- [ ] **Passo 1:** `build_textura.py` e render de pré-visualização com a luz do jogo.
- [ ] **Passo 2 [Portão]:** Pedro aprova (ou retoca e aprova). Pré-visualizações em `docs/arte/previas/cavaleiro-textura/`. Commit `feat: add knight painted texture`.

---

### B08: Espada longa
**Nível:** arte · **Depende de:** B03, B05

**Files:** Create `art/personagens/cavaleiro/build_espada.py`, `assets/models/personagens/espada.glb` · Modify `context/assets.md`, `tests/test_art_props.gd`

Modelada por script (lâmina larga, guarda em cruz, cabo para uma mão e meia, runas violeta pintadas na lâmina), fiel à espada do `hero.png`. ≤ 2.000 triângulos, 512². Origem no ponto de pegada do cabo, lâmina ao longo de +Y local, para ir no osso da mão direita na B10.

**Passos:**
- [ ] **Passo 1:** `test_espada` em `test_art_props.gd`: triângulos ≤ 2.000; comprimento total entre 1,1 e 1,4 m; origem dentro do cabo (AABB do cabo contém a origem). Rodar: FAIL.
- [ ] **Passo 2:** `build_espada.py`, rodar, olhar as pré-visualizações. `tools/test.sh` → passa.
- [ ] **Passo 3 [Portão]:** Pedro aprova. Commit `feat: add knight longsword`.

---

### B09: Cavaleiro — rig e animações
**Nível:** difícil · **Depende de:** B07, B08

**Files:** Create `art/personagens/cavaleiro/build_para_mixamo.py`, `art/personagens/cavaleiro/build_final.py`, `art/prompts/cavaleiro-mixamo.md`, `assets/models/personagens/cavaleiro.glb`, `tests/test_art_knight.gd` · Modify `context/assets.md`

**Interfaces — Produces:** `cavaleiro.glb` com uma `Skeleton3D`, uma malha e um `AnimationPlayer` com exatamente estes clipes, todos **no lugar** (sem andar sozinhos):

| Clipe | Uso no jogo | Busca sugerida no Mixamo |
|---|---|---|
| `idle` | parado | great sword idle |
| `walk` | andar | great sword walk |
| `attack_1` | 1º golpe do combo | great sword slash |
| `attack_2` | 2º golpe do combo | outra great sword slash |
| `roll` | esquiva | sword and shield roll / stand to roll |
| `parry` | parry | great sword block / parry |
| `hurt` | dano | great sword impact / hit reaction |
| `death` | morte | great sword death / dying |

A spec lista "ataque" no singular; são dois clipes porque o ataque é um combo de dois golpes (T18 do 1A).

**Passos:**
- [ ] **Passo 1 [Pedro]:** conferir a FAQ do Mixamo no navegador (licença, ver B02) e dizer ao Claude o que leu; registrar como (d).
- [ ] **Passo 2:** `build_para_mixamo.py` exporta um `.fbx` com a malha texturizada em pose A. `cavaleiro-mixamo.md` explica a Pedro: subir o FBX, marcar os pontos do auto-rig (queixo, pulsos, cotovelos, joelhos, virilha), escolher cada clipe da tabela olhando o preview, baixar em FBX binário, 30 fps, o primeiro "With Skin" e os outros "Without Skin", "In Place" marcado quando o clipe oferecer.
- [ ] **Passo 3 [Pedro]:** fazer o auto-rig, baixar os oito clipes e salvar em `art/brutos/` com o nome do clipe no arquivo. Registrar cada um (origem `mixamo`).
- [ ] **Passo 4:** Escrever os testes em `test_art_knight.gd`:
  - `test_cavaleiro_estrutura`: há `Skeleton3D` e `AnimationPlayer`; os nomes dos clipes são exatamente os oito da tabela; triângulos ≤ 20.000; materiais ≤ 2.
  - `test_cavaleiro_escala`: AABB da malha na pose de repouso com altura entre 1,75 e 1,85 m e base em y ≈ 0 (±0,03).
  - `test_sem_root_motion`: em cada clipe, a trilha de posição do osso dos quadris (nome que contém `Hips`) varia no máximo 0,05 m em X e em Z.
  - Rodar: FAIL (arquivo inexistente).
- [ ] **Passo 5:** `build_final.py`: importa o FBX com malha e os clipes, junta tudo numa armadura, renomeia as actions para os nomes da tabela, zera X e Z dos quadris onde o clipe ainda anda, reaplica a textura pintada e exporta com `animations=True`. Rodar e conferir o relatório (`bones`, `actions`).
- [ ] **Passo 6:** `tools/test.sh` → passa. Render de uma folha com um quadro do meio de cada clipe; olhar e mostrar a Pedro junto com o próximo portão (B10).
- [ ] **Passo 7:** Commit `feat: add rigged and animated knight`.

---

### B10: Cavaleiro no jogo
**Nível:** difícil · **Depende de:** B09

**Files:** Create `scripts/visual/character_visual.gd`, `tests/test_character_visual.gd` · Modify `scripts/state_machine/state_machine.gd`, `scripts/player/player_3d.gd`, `scripts/player/states/attack.gd`, `scenes/player/player_3d.tscn`, `tests/test_state_machine.gd`

**Interfaces:**
- **Consumes:** `cavaleiro.glb` e `espada.glb` (B08, B09); `StateMachine.change_state(key)`; durações do 1A: ataque 0,40 s por golpe (0,08 + 0,18 + 0,14), esquiva 0,34 s (0,04 + 0,22 + 0,08), parry 0,40 s (0,22 + 0,18), dano 0,30 s; `PlayerMotion.WALK_SPEED = 5.0`.
- **Produces:**
  - `StateMachine`: `signal state_changed(key: StringName)`, emitido depois de cada `enter()`, inclusive o do estado inicial no `init`.
  - `Player3D`: `signal attack_swing(index: int)`, emitido no início de cada golpe do combo (0 e 1).
  - `class_name CharacterVisual extends Node3D` em `scripts/visual/character_visual.gd`:
    - `@export var anim_map: Dictionary` — estado (StringName) → clipe (StringName).
    - `@export var fit_durations: Dictionary` — clipe → duração em s em que ele deve tocar inteiro.
    - `@export var looping: Array[StringName] = [&"idle", &"walk"]`
    - `@export var walk_anim: StringName = &"walk"` e `@export var walk_reference_speed: float = 5.0`
    - `func bind(machine: StateMachine) -> void` — liga ao `state_changed`.
    - `func play_clip(clip: StringName) -> void` — toca com `speed_scale = duração do clipe / fit_durations[clip]` quando houver; sem `fit_durations`, velocidade 1. O clipe `death` para no último quadro.
    - `func set_move_speed(speed: float) -> void` — no `walk`, `speed_scale = speed / walk_reference_speed` (mínimo 0,3).
    - `func current_clip() -> StringName` e `func current_speed_scale() -> float`
    - Acha o `AnimationPlayer` dentro do modelo instanciado; marca os clipes de `looping` com `LOOP_LINEAR` no `_ready`.
  - `player_3d.tscn`: o `MeshInstance3D` `Body` (cápsula) sai; entra `Visual` (`CharacterVisual`, rotação Y de 180°) com `cavaleiro.glb` instanciado e um `BoneAttachment3D` na mão direita segurando `espada.glb`. Mapa: `idle→idle`, `move→walk`, `roll→roll`, `parry→parry`, `hurt→hurt`, `dead→death`; o ataque toca `attack_1`/`attack_2` pelo `attack_swing`. `fit_durations`: `attack_1` e `attack_2` 0,40, `roll` 0,34, `parry` 0,40, `hurt` 0,30. A `AimArrow` e a `HeroLight` ficam.

**Passos:**
- [ ] **Passo 1:** Testes:
  - em `test_state_machine.gd`: `test_emite_state_changed` (init emite o inicial; `change_state(&"b")` emite `&"b"`).
  - em `test_character_visual.gd`, montando o `Player3D` como os testes do 1A:
    - `test_toca_clipe_do_estado`: forçar cada estado → `current_clip()` igual ao mapa.
    - `test_ataque_cabe_no_golpe`: atacar → `attack_1` com `current_speed_scale()` ≈ duração do clipe / 0,40 (±0,01); o segundo golpe toca `attack_2`.
    - `test_esquiva_cabe`: idem para `roll` com 0,34.
    - `test_andar_escala`: `set_move_speed(2.5)` → escala 0,5; `set_move_speed(0.0)` → 0,3.
    - `test_modelo_olha_para_frente`: o +Z global do modelo importado ≈ −Z global do `Player3D` (produto escalar > 0,99) depois de mirar em três direções.
    - `test_pes_no_chao`: herói parado e andando 1 s → menor y da AABB da malha esfolada entre −0,03 e 0,03 m em relação ao `Player3D`.
    - `test_morte_para_no_fim`: morrer e avançar 3 s → `death` no último quadro, sem repetir.
- [ ] **Passo 2:** Rodar e ver falhar.
- [ ] **Passo 3:** Implementar. Testes antigos que leem a cápsula do herói (procurar `Body` em `tests/`) passam a ler o `Visual`; nenhuma asserção de jogo muda.
- [ ] **Passo 4:** `tools/test.sh` → tudo passa.
- [ ] **Passo 5:** Captura como na B04, 20 s de `--autoplay`, e olhar quadros de andar, atacar e esquivar.
- [ ] **Passo 6 [Portão]:** Pedro vê a folha de clipes (B09) e a captura. Commit `feat: replace hero capsule with animated knight`.

---

### B11: Conceito do Cultista
**Nível:** arte · **Depende de:** B01 (aprovada)

Igual à B05, a partir do `cultist.png` do 2D (capuz vermelho e violeta, manto, lâmina curva, tentáculos na barra do manto). Pose A, sem a lâmina na mão, três vistas. Os tentáculos ficam como forma do manto, não como membros com osso. Folha em `docs/arte/cultista-conceito.png`. **[Pedro]** gera; **[Portão]** Pedro aprova. Commit `docs: add approved cultist concept sheet`.

---

### B12: Cultista — malha e textura
**Nível:** arte · **Depende de:** B04, B11

Igual à B06 + B07, numa tarefa só (peça menor): `art/inimigos/cultista/build_malha.py` e `build_textura.py`, ≤ 12.000 triângulos, 1024², altura até 1,95 m. A lâmina curva é modelada por script como a espada (B08), ≤ 1.000 triângulos, em `assets/models/inimigos/lamina.glb`. **[Pedro]** gera o bruto no TRELLIS.2; **[Portão]** Pedro aprova as pré-visualizações. Commit `feat: add cultist mesh and texture`.

---

### B13: Cultista — rig, animações e jogo
**Nível:** difícil · **Depende de:** B10, B12

**Files:** Create `art/inimigos/cultista/build_final.py`, `assets/models/inimigos/cultista.glb`, `tests/test_art_cultist.gd` · Modify `scenes/enemies/enemy_common.tscn`, `scripts/enemies/enemy_common.gd`, `tests/test_enemy_attack.gd`, `tests/test_enemy_chase.gd`, `context/assets.md`

**Interfaces:**
- **Consumes:** `CharacterVisual` e `state_changed` (B10); durações do inimigo no 1A: aviso 0,40 s, golpe 0,25 s, atordoado 1,5 s, morte 1,0 s; velocidade 2,4 m/s.
- **Produces:**
  - `cultista.glb` com os clipes `idle`, `walk`, `telegraph`, `attack`, `stunned`, `death`, todos no lugar (mesmo fluxo Mixamo da B09; o Passo 1 da B09 não se repete).
  - Mapa: `idle→idle`, `chase→walk`, `telegraph→telegraph`, `attack→attack`, `cooldown→idle`, `stunned→stunned`, `dead→death`; `fit_durations`: `telegraph` 0,40, `attack` 0,25, `stunned` 1,5, `death` 1,0; `walk_reference_speed` 2,4.
  - O `MeshInstance3D` `Body` sai; entra `Visual` com o modelo e a lâmina na mão direita.
  - `EnemyCommon.set_telegraph_glow(on)` passa a pôr, em cada `MeshInstance3D` do `Visual`, um `material_overlay` próprio da instância (`StandardMaterial3D`, emissão `#ff2020`, energia 2,0, mistura aditiva); `on = false` tira o overlay. `var telegraph_overlay: StandardMaterial3D` exposto para os testes.

**Passos:**
- [ ] **Passo 1:** Testes em `test_art_cultist.gd` (estrutura, escala até 1,95 m, sem root motion, como na B09) e no `CharacterVisual` do inimigo (`test_aviso_cabe` com 0,40 s, `test_cultista_olha_para_frente`). Reescrever as asserções de brilho de `test_enemy_attack.gd` (linhas 84–91) para ler `telegraph_overlay` e o `material_overlay` das malhas, com os mesmos valores (`#ff2020`, 2,0, liga no aviso, desliga ao sair), e a de `test_enemy_chase.gd` (linhas 90–91) para comparar os `telegraph_overlay` de dois inimigos: instâncias diferentes, e acender um não acende o outro.
- [ ] **Passo 2:** Rodar e ver falhar.
- [ ] **Passo 3 [Pedro]:** auto-rig e os seis clipes no Mixamo, como na B09.
- [ ] **Passo 4:** Implementar `build_final.py`, a cena e o overlay.
- [ ] **Passo 5:** `tools/test.sh` → passa. Captura de 20 s de `--autoplay`.
- [ ] **Passo 6 [Portão]:** Pedro vê a captura. Commit `feat: replace enemy capsule with animated cultist`.

---

### B14: Kit modular — peças
**Nível:** arte · **Depende de:** B04, resposta (a) da T32

**Files:** Create `art/kit/build_kit.py`, `art/kit/texturas/` (fontes), `assets/models/kit/*.glb`, `tests/test_art_kit.gd` · Modify `context/assets.md`

**Interfaces — Produces:** peças na grade de 2 m (B01), cada uma com origem no canto de grade e base em y = 0:

| Arquivo | Peça | Medidas |
|---|---|---|
| `piso.glb` | piso de lajes | 2 × 2 m |
| `parede.glb` | parede de pedra | 2 m × 3 m × 0,4 m |
| `parede_porta.glb` | parede com abertura | 2 m × 3 m, vão de 2 m de largura × 2,4 m de altura |
| `canto.glb` | pilar de canto | 0,4 × 0,4 × 3 m |
| `coluna.glb` | coluna | 1 × 1 × 3 m |

Modeladas por script (blocos de pedra com chanfro, juntas, alguma irregularidade aleatória com semente fixa para o resultado se repetir). Texturas: pintadas por script ou CC0 repintadas; cada fonte CC0 conferida e registrada (ambientCG, por exemplo, declara CC0 na página de cada material). No "próxima", mais irregularidade e juntas modeladas; no "atual", o desenho das juntas fica na textura.

**Passos:**
- [ ] **Passo 1:** `test_pecas_do_kit`: os cinco arquivos existem; AABB de cada um bate com a tabela (±0,02 m); triângulos ≤ 1.500 por peça; base em y ≈ 0. Rodar: FAIL.
- [ ] **Passo 2:** `build_kit.py`, rodar, render de uma folha com as cinco peças e de um trecho de 3 × 3 peças montado. Olhar.
- [ ] **Passo 3:** `tools/test.sh` → passa.
- [ ] **Passo 4 [Portão]:** Pedro aprova. Commit `feat: add modular dungeon kit pieces`.

---

### B15: Sala do kit no jogo
**Nível:** médio · **Depende de:** B14

**Files:** Create `scenes/world/kit/*.tscn` (uma cena por peça: `StaticBody3D` na camada 1, `BoxShape3D` com as medidas da peça), `scenes/world/kit_room.tscn` · Modify `scenes/main.tscn` (sala nova no lugar da `greybox_room`), `scenes/world/veil_wall.tscn`, `tests/test_main_scene.gd`

**Interfaces:**
- **Consumes:** peças da B14; layout do 1A: piso 16 × 16 m, paredes de 3 m, coluna 1 × 1 m no centro-leste, porta de 2 m na parede norte com o `DoorSlot` no centro, saleta de 4 × 4 m; `WorldEnvironment` como está; a `VeilWall` no `DoorSlot`.
- **Produces:** `kit_room.tscn` com o mesmo layout, o mesmo `DoorSlot` e o mesmo `WorldEnvironment`. A `greybox_room.tscn` fica no repositório como referência. Na `veil_wall.tscn`, o nó `Mesh` passa a usar a malha de `parede.glb` com o shader `veil_dissolve` (parâmetro `dissolve` igual) e a textura da pedra como cor; nomes de nós e colisão não mudam.

**Passos:**
- [ ] **Passo 1:** Em `test_main_scene.gd`, `test_sala_do_kit`: `main.tscn` tem `KitRoom` e não tem `GreyboxRoom`; um raio para baixo em 25 pontos de uma grade sobre o piso acerta a camada 1 em y ≈ 0; um raio horizontal do centro para cada parede externa acerta a 8 m (±0,3); o `DoorSlot` está no mesmo lugar da sala cinza. Rodar: FAIL.
- [ ] **Passo 2:** Montar as cenas. `tools/test.sh` → tudo passa, inclusive `test_veil_wall.gd` sem mudança.
- [ ] **Passo 3:** Captura de 20 s de `--autoplay`, olhar costuras entre peças e a parede do Véu dissolvendo com F9 (build de depuração).
- [ ] **Passo 4:** Commit `feat: build the room from the modular kit`.

---

### B16: Luz, acabamento e fecho
**Nível:** arte · **Depende de:** B10, B13, B15

**Files:** Modify `scenes/main.tscn` e `scenes/world/kit_room.tscn` (luzes e névoa, se o guia pedir), `README.md` ("Estado atual" e captura nova), `context/assets.md` (seção `## Declaração de IA para a Steam (rascunho) {#steam-ia}`), `context/arquitetura.md`, `context/achados.md` (A02 com o resultado) · Create `docs/capturas/<data>-bloco-1.png`

**Passos:**
- [ ] **Passo 1:** Ajustar luz do herói, braseiros e névoa só pelos valores do guia (B01), conferindo a leitura do herói contra o cenário em capturas.
- [ ] **Passo 2:** `tools/measure_fps.sh mobile`. Esperado: `media` ≥ 59 e `minimo` ≥ 50. Se não, cortar na ordem: sombras dos braseiros, triângulos do kit, resolução das texturas; registrar no ledger o que saiu.
- [ ] **Passo 3:** Captura de portfólio (`--fullscreen`, como na T31): um quadro em que herói, inimigo, braseiro e a parede do Véu aparecem, sem HUD cortado. Salvar em `docs/capturas/`.
- [ ] **Passo 4:** Rascunho da declaração de IA: o que foi gerado por IA (conceitos, malhas brutas), com quais ferramentas, e o que foi retrabalhado por nós; animações do Mixamo; nada de IA em tempo de execução.
- [ ] **Passo 5:** README e `context/`; `python lint.py`; `tools/test.sh` e `tools/test_blender.sh` → passam. Commit `docs: close art track with capture and ai disclosure draft`.

---

### B17: Pedro joga e aprova (tarefa de Pedro)
**Nível:** — · **Depende de:** B16

Pedro joga o build e responde: (a) está **bonito e gostoso de controlar**? (b) a captura serve de imagem de portfólio sem retoque? (c) o que incomoda? Cada incômodo vira uma tarefa nova (B18 em diante). Nenhum modelo marca esta tarefa como feita. Com (a) e (b) "sim" e a T32 feita, o Bloco 1 termina (spec §7).
