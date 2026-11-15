# Tela e sensação — Trilha de jogo (Bloco 1A) Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Um projeto Godot 3D novo em que um herói provisório anda, mira, ataca, esquiva e apara contra um inimigo comum numa sala de blocos cinzas, com câmera fixa inclinada, luz quente no herói, HUD mínimo e uma parede ilusória que só se abre quando o Véu afina, rodando a 60 fps em 1080p na máquina de Pedro.

**Architecture:** Projeto novo em `/home/usuario/Dev/holding_agy/eldritch_depths_3d_20261114/`, com git e `context/` próprios. A lógica testável (movimento, mira, distância de câmera, faixas do Véu, janelas de combate) fica em funções puras e componentes sem nó 3D, testadas por um runner caseiro em `tests/`. As cenas 3D só ligam essas peças. Do 2D vêm apenas `StatsComponent` e a máquina de estados, generalizados. O resto é escrito do zero.

**Tech Stack:** Godot 4.7.2 (`/home/usuario/.local/bin/godot`), GDScript, renderizador Mobile (Compatibility como alternativa medida na T31), git. Nenhuma dependência nova.

**Spec:** `docs/superpowers/specs/2026-11-14-eldritch-depths-3d-design.md`. A T04 copia o arquivo do projeto 2D para o 3D. Antes de começar, ler §3, §4.1–4.3, §4.6, §6 e §7.

**Ledger:** `docs/superpowers/plans/2026-11-14-tela-e-sensacao-ledger.md` diz qual tarefa está livre, em andamento ou feita, e por qual modelo.

**Fora deste plano:** a trilha de arte (Bloco 1B: guia de estilo, conceito do Cavaleiro, pipeline IA → Blender → Godot, Cavaleiro final, kit modular). Ela terá plano próprio, porque depende de aprovações visuais de Pedro a cada etapa.

---

## Como trabalhar neste plano (vários modelos, vários dias)

Cada tarefa (T01 a T32) foi feita para caber numa sessão e ser executada por um modelo que **não viu nenhuma conversa anterior**. Tudo o que ele precisa está aqui, no ledger e no repositório.

**Ao começar uma sessão:**
1. Ler, nesta ordem: este cabeçalho até o fim de "Review Focus", a linha da tarefa no ledger e a tarefa inteira. Não precisa ler as outras tarefas: o bloco **Interfaces** de cada uma diz o que ela usa das anteriores.
2. Conferir no ledger que **todas as dependências** ("Depende de") estão `feita`. Se alguma não estiver, pare e escolha outra tarefa livre.
3. Marcar a tarefa como `em andamento`, com o modelo e a data, e fazer commit só do ledger: `docs: start T<nn>`.
4. Rodar `tools/test.sh` (a partir da T02). Ele precisa passar **antes** de você mexer em qualquer coisa. Se falhar, a tarefa anterior deixou um problema: registre em `context/achados.md` e pare.

**Durante a tarefa:**
- Siga os passos na ordem: teste que falha, implementação, teste passando.
- Os nomes, assinaturas e valores do bloco **Interfaces** são contrato. Não troque. Se um contrato estiver errado ou impossível, pare. Registre o problema em `context/achados.md` e deixe a tarefa como `bloqueada` no ledger, com uma linha explicando. Não invente um contrato novo por conta própria.
- Não mexa em arquivos de outras tarefas, a não ser os listados em **Files → Modify**.
- Não adiante trabalho de tarefas futuras.

**Ao terminar:**
1. `tools/test.sh` passa, e `python lint.py` passa se você mexeu em `context/`.
2. Todos os itens de **Pronto quando** estão verdadeiros.
3. Marcar a tarefa como `feita` no ledger, com o modelo, a data e o hash do commit, mais uma linha de nota se algo surpreendeu.
4. Um commit só para a tarefa, mais o do ledger (pode ser o mesmo).

**Nível de cada tarefa** (para escolher o modelo):
- `simples`: mecânica, qualquer modelo.
- `médio`: exige cuidado com a API da Godot.
- `difícil`: física, tempo e cenas interligadas. Usar o modelo mais capaz disponível.

Agentes externos (OpenCode, Gemini) só com modelos ou cotas gratuitas.

**Tarefas humanas:** a T32 é de Pedro. Nenhum modelo a marca como feita sozinho.

---

## Global Constraints

- **Orçamento R$ 0.** Nenhuma ferramenta, asset ou serviço pago.
- **Nenhum addon novo:** nem GUT, nem phantom_camera, nem limboai. Toda dependência nova passa por Pedro antes e é registrada como (d).
- **Godot 4.7.2.** Renderizador inicial `mobile`.
- **Meta de desempenho:** 60 fps em 1080p no vídeo integrado (AMD RADV RENOIR), usando escala de resolução se for preciso.
- **Controles:** teclado e mouse **e** gamepad desde o início. Steam Deck fica fora.
- **HUD mínimo, estilo soulslike:** barras finas de vida, vigor e sanidade num canto e poucos atalhos de consumíveis. Sem minimapa e sem ícones grandes de habilidade na tela fixa.
- **Proibido `Engine.has_singleton("<Autoload>")`**, porque sempre retorna falso para autoloads. Usar `Autoloads.get_autoload(&"Nome")` (T05).
- **Unidades:** 1 m equivale a 27 px do 2D. Valores convertidos: andar 5,0 m/s; esquiva 10,4 m/s; inimigo 2,4 m/s; alcance de ataque do inimigo 1,5 m; detecção 6,7 m.
- **Idioma:** código e comentários em português do Brasil, como no 2D; identificadores em inglês.
- **Commits:** Conventional Commits em inglês, **sem `Co-Authored-By` nem qualquer menção à IA**.
- **Push:** `git push` só com ordem explícita de Pedro.
- **Fatos em `context/`:** cada um leva a data do dia (`[YYYY-MM-DD]`) e a procedência `(d)`, `(i)` ou `(e)`.
  - Nada se apaga: usar `~superseded YYYY-MM-DD` apontando para o fato novo.
  - Uma `(i)` nunca sustenta outra `(i)`.
  - Rodar `python lint.py` depois de mexer em `context/`.
- **Testes:** um único comando para todas as tarefas, `tools/test.sh` (criado na T02). A última linha de sucesso é `OK: <n> testes`, com código de saída 0.
- **Testes com nós na árvore:** depois de adicionar `Area3D` ou corpos, esperar 2 frames de física (`await tree.physics_frame` duas vezes) antes de checar sobreposições. Liberar com `queue_free()` no fim de cada teste.
- **Pasta temporária:** capturas de tela e quadros vão para `/tmp/claude-1001/-home-usuario-Dev-Suporte/00369e3d-1515-4469-bd6e-f0b40f59328c/scratchpad/`. Se essa pasta não existir na sua sessão, use a pasta temporária da sua sessão, nunca o repositório.

## Review Focus

1. **Troca de dispositivo no meio do jogo e controle desconectado:**
   - Mexer o mouse depois de usar o controle, ou o contrário, troca o modo de mira e os botões mostrados no mesmo frame.
   - O drift do analógico abaixo da deadzone (0,2) **não** conta como uso do controle.
   - Se o controle for desconectado em modo PAD, o jogo volta para KBM.
   - Testes na T10.
2. **Raio do mouse que não acerta o chão** (mouse acima do horizonte, ou raio paralelo ao plano):
   - A mira cai para a direção do movimento e, sem movimento, para a última mira válida.
   - Ela nunca é `NaN` nem zero.
   - Testes na T11.
3. **Travada de frame** (delta de 0,25 a 0,3 s): a janela ativa do golpe e a invencibilidade da esquiva não são puladas.
   - Testes na T14, T18 e T19.
4. **Herói dentro da parede ilusória quando a sanidade volta acima de 60:**
   - A parede só fica sólida de novo quando nenhum corpo está dentro dela.
   - O herói nunca fica preso.
   - Teste na T26.
5. **Telas que não são 16:9** (2560×1080 e 1280×800): o HUD continua no canto, legível e sem cortes, ocupando menos de 6% da área.
   - Teste na T29.

---

## Mapa das tarefas

| Fase | Tarefas | O que entrega |
|---|---|---|
| 0. Fundação | T01–T04 | Projeto abre, testes rodam, controles mapeados, `context/` montado |
| 1. Núcleo sem 3D | T05–T11 | Atributos, Véu, máquina de estados, movimento, modo de entrada, mira |
| 2. Câmera e herói | T12–T21 | Câmera fixa, janelas de tempo, hitbox, herói que anda, ataca, esquiva, apara, sofre e morre |
| 3. Inimigo | T22–T24 | Inimigo que persegue, avisa, bate, atordoa e morre |
| 4. Mundo | T25–T27 | Sala cinza com luz e névoa, parede do Véu, vinheta de sanidade |
| 5. HUD | T28–T29 | Barras finas e botões por dispositivo |
| 6. Medição e teste | T30–T32 | fps medido, renderizador escolhido, Pedro joga e escolhe a câmera |

Tarefas que podem correr em paralelo, depois das dependências delas:
- T05, T06, T08, T09 e T11;
- T12 e T14;
- T15 e T16;
- T28 e qualquer tarefa da fase 3.

## Estrutura de arquivos

```
eldritch_depths_3d_20261114/
  project.godot  .gitignore  lint.py
  tools/test.sh  tools/measure_fps.sh
  context/{index,produto,arquitetura,decisoes,achados}.md
  docs/superpowers/specs/  docs/superpowers/plans/  docs/capturas/
  tests/run_tests.gd  tests/test_case.gd  tests/test_*.gd
  scripts/core/autoloads.gd  scripts/core/input_mode.gd
  scripts/components/stats_component.gd  scripts/components/veil.gd
  scripts/state_machine/state.gd  scripts/state_machine/state_machine.gd
  scripts/player/player_motion.gd  scripts/player/aim_resolver.gd  scripts/player/player_3d.gd
  scripts/player/states/{idle,move,attack,roll,parry,hurt,dead}.gd
  scripts/combat/action_timeline.gd  hitbox_3d.gd  hurtbox_3d.gd  posture_component.gd
  scripts/camera/camera_rig_3d.gd
  scripts/enemies/enemy_common.gd  scripts/enemies/states/{idle,chase,telegraph,attack,cooldown,stunned,dead}.gd
  scripts/world/veil_wall.gd  scripts/main.gd
  scripts/ui/hud_minimal.gd  scripts/ui/input_prompt.gd
  shaders/veil_vignette.gdshader
  scenes/main.tscn  scenes/player/player_3d.tscn  scenes/camera/camera_rig_3d.tscn
  scenes/enemies/enemy_common.tscn  scenes/world/{greybox_room,veil_wall}.tscn  scenes/ui/hud_minimal.tscn
```

**Camadas de colisão** (todas as tarefas usam esta tabela):

| Camada | Uso |
|---|---|
| 1 | mundo |
| 2 | corpo do herói |
| 3 | corpo dos inimigos |
| 4 | hitbox do herói |
| 5 | hitbox dos inimigos |
| 6 | hurtbox do herói |
| 7 | hurtbox dos inimigos |

**Máscaras das hitboxes:**
- A hitbox do herói (4) detecta a camada 7.
- A hitbox dos inimigos (5) detecta a camada 6.

---

# Fase 0 — Fundação

### T01: Pasta, git e `project.godot` mínimo
**Nível:** simples · **Depende de:** nada

**Files:** Create `project.godot`, `.gitignore`

- [ ] **Passo 1:** `mkdir -p /home/usuario/Dev/holding_agy/eldritch_depths_3d_20261114 && cd /home/usuario/Dev/holding_agy/eldritch_depths_3d_20261114 && git init -b main`. A saída esperada é `Initialized empty Git repository`.
- [ ] **Passo 2:** Escrever `project.godot` com estes valores:
  - `config/name="Eldritch Depths"` e `config/features=PackedStringArray("4.7")`;
  - `rendering/renderer/rendering_method="mobile"`;
  - `display/window/size/viewport_width=1920` e `display/window/size/viewport_height=1080`;
  - `display/window/stretch/mode="canvas_items"` e `display/window/stretch/aspect="expand"`;
  - `physics/common/physics_ticks_per_second=60`;
  - `run/main_scene` vazio, que a T25 preenche.
- [ ] **Passo 3:** Escrever o `.gitignore` com as linhas `.godot/`, `/build/` e `*.tmp`. Os arquivos `*.import` **são** versionados.
- [ ] **Passo 4:** Rodar `godot --headless --path . --import`. A saída esperada é código 0, sem `ERROR`. (Não use `--quit`: sem cena principal ele tenta rodar o jogo e sai com erro.)
- [ ] **Passo 5:** Criar o ledger: copiar `/home/usuario/Dev/holding_agy/eldritch_depths_20260912/docs/superpowers/plans/2026-11-14-tela-e-sensacao-ledger.md` para `docs/superpowers/plans/` e marcar a T01.
- [ ] **Passo 6:** Commit `chore: create godot 3d project skeleton`.

**Pronto quando:** o projeto abre headless sem erro e o ledger existe no repositório.

---

### T02: Runner de testes e `tools/test.sh`
**Nível:** médio · **Depende de:** T01

**Files:** Create `tests/test_case.gd`, `tests/run_tests.gd`, `tests/test_harness.gd`, `tools/test.sh`

**Interfaces — Produces:**
- `tests/test_case.gd`, declarado como `class_name TestCase extends RefCounted`.
  - Guarda as falhas em `var failures: Array[String]` e oferece os asserts abaixo.
  - Uma falha entra na lista e **não** aborta o teste.

  | Assert | Assinatura |
  |---|---|
  | igualdade | `assert_eq(a, b, msg := "")` |
  | número próximo | `assert_near(a: float, b: float, eps := 0.001, msg := "")` |
  | verdadeiro | `assert_true(c: bool, msg := "")` |
  | falso | `assert_false(c: bool, msg := "")` |
  | vetor próximo | `assert_vec_near(a: Vector3, b: Vector3, eps := 0.001, msg := "")` |

- `tests/run_tests.gd`, que estende `SceneTree`. No `_initialize`:
  1. faz `await process_frame` uma vez;
  2. carrega cada `res://tests/test_*.gd` em ordem alfabética e instancia o script;
  3. para cada método que começa com `test_`, em ordem alfabética:
     - se `get_method_argument_count` for 1, faz `await obj.call(m, self)`, passando a árvore;
     - senão, faz `await obj.call(m)`;
     - depois, move as falhas do objeto para o relatório;
  4. imprime `FAIL <arquivo>::<método>: <mensagem>` para cada falha;
  5. termina com `OK: <n> testes` e `quit(0)`, ou com `FALHOU: <f> de <n>` e `quit(1)`.
- `tools/test.sh` (executável) roda `godot --headless --path . --import`, para registrar as classes novas, e depois `godot --headless --path . -s res://tests/run_tests.gd`. O script sai com o código do segundo comando.

**Passos:**
- [ ] **Passo 1:** Escrever `tests/test_harness.gd`, que estende `TestCase`, com dois testes:
  - `test_assert_near_tolera_epsilon`: depois de `assert_near(1.0, 1.0005)`, a lista `failures` está vazia.
  - `test_assert_eq_registra_falha`: cria `var t := TestCase.new()`, chama `t.assert_eq(1, 2)` e confere `assert_eq(t.failures.size(), 1)`.
- [ ] **Passo 2:** Rodar `tools/test.sh` antes do runner existir. O esperado é uma falha.
- [ ] **Passo 3:** Implementar `test_case.gd`, `run_tests.gd` e `test.sh`, e dar `chmod +x tools/test.sh`.
- [ ] **Passo 4:** Rodar `tools/test.sh`. O esperado é `OK: 2 testes` e `echo $?` igual a `0`.
- [ ] **Passo 5:** Prova de que o runner detecta falha:
  1. mudar temporariamente o `1.0005` do primeiro teste para `1.5`;
  2. rodar e conferir `FALHOU: 1 de 2` com código 1;
  3. desfazer a mudança.
- [ ] **Passo 6:** Commit `test: add in-house godot test runner`.

**Pronto quando:** `tools/test.sh` passa com 2 testes e reprova quando um assert falha.

---

### T03: Mapa de controles
**Nível:** simples · **Depende de:** T02

**Files:** Modify `project.godot` (seção `[input]`) · Test `tests/test_input_map.gd`

Tabela (deadzone 0,2 em todas as ações de eixo):

| Ação | Teclado e mouse | Gamepad |
|---|---|---|
| move_up / move_down / move_left / move_right | W / S / A / D | eixo 1 − / eixo 1 + / eixo 0 − / eixo 0 + |
| aim_up / aim_down / aim_left / aim_right | — | eixo 3 − / eixo 3 + / eixo 2 − / eixo 2 + |
| attack | botão esquerdo do mouse | botão 2 (X do Xbox, Quadrado) |
| roll | Espaço | botão 0 (A, X do PlayStation) |
| parry | botão direito do mouse | eixo 4 + (gatilho esquerdo) |
| spell_cosmic | Q | botão 3 (Y, Triângulo) |
| use_blood_flask | 1 | botão 12 (direcional para baixo) |
| use_laudanum | 2 | botão 11 (direcional para cima) |
| interact | E | botão 1 (B, Círculo) |
| debug_sanity_drop | F9 | — |
| debug_camera_preset | F7 | — |

- [ ] **Passo 1:** Escrever `test_todas_as_acoes_existem`: para cada nome da tabela, `assert_true(InputMap.has_action(nome), nome)`.
- [ ] **Passo 2:** Escrever `test_acoes_de_jogo_tem_teclado_e_pad`: as ações move_*, attack, roll, parry, spell_cosmic, use_blood_flask, use_laudanum e interact têm pelo menos um evento de teclado ou mouse **e** um de joypad.
- [ ] **Passo 3:** Escrever `test_deadzone`: `InputMap.action_get_deadzone(&"move_up")` ≈ 0,2.
- [ ] **Passo 4:** Rodar `tools/test.sh`. O esperado é falha.
- [ ] **Passo 5:** Escrever a seção `[input]`. Dica: é mais seguro criar as ações pelo editor (`godot --path . -e`, depois Projeto → Configurações → Mapa de Entrada) do que escrever o formato serializado à mão.
- [ ] **Passo 6:** Rodar `tools/test.sh`. O esperado é passar.
- [ ] **Passo 7:** Commit `feat: add keyboard, mouse and gamepad input map`.

**Pronto quando:** os três testes passam.

---

### T04: `context/`, lint e documentos copiados
**Nível:** simples · **Depende de:** T01

**Files:** Create `lint.py`, `context/{index,produto,arquitetura,decisoes,achados}.md` · Copy a spec e este plano para `docs/superpowers/`

- [ ] **Passo 1:** Copiar `/home/usuario/Dev/Suporte_agy/lint.py` para a raiz e ajustar só a constante de data da convenção para `2026-11-14`.
- [ ] **Passo 2:** Copiar dois arquivos da pasta `/home/usuario/Dev/holding_agy/eldritch_depths_20260912/docs/superpowers/` para o mesmo caminho dentro do projeto 3D:
  - `specs/2026-11-14-eldritch-depths-3d-design.md`;
  - `plans/2026-11-14-tela-e-sensacao-trilha-jogo.md`.
- [ ] **Passo 3:** Na spec copiada, marcar a linha 6 com `~superseded 2026-11-14 → ver linha seguinte` e acrescentar: `- [2026-11-14] (i) O arquivo agora mora no projeto 3D; a cópia no projeto 2D é histórica.`
- [ ] **Passo 4:** Criar os arquivos de `context/`. Todos levam frontmatter com `tipo`, `descricao`, `estado: estavel` e `criado: 2026-11-14`, e todas as linhas têm data e procedência.

  | Arquivo | Conteúdo |
  |---|---|
  | `index.md` | O que há em cada arquivo e quando carregá-lo: código pede `arquitetura` + `achados`; regras pedem `produto`; decisões pedem `decisoes`. |
  | `produto.md` | Resumo de §1, §2 e §4 da spec, com as linhas `(d)`/`(i)` originais e um ponteiro para a spec. |
  | `arquitetura.md` | Stack, estrutura de pastas e camadas de colisão (as duas tabelas deste plano), runner de testes, renderizador `mobile` provisório e a regra do `has_singleton`. |
  | `decisoes.md` | As `(d)` das rodadas 1 a 4 (spec §1–§7) e mais três `(i)`. Cada uma no formato `- [2026-11-14] (d)/(i) **<Decisão>.** Por quê: … Fecha: … Descartado: …`. |
  | `achados.md` | Os dois itens descritos abaixo. |

  As três decisões `(i)` de `decisoes.md`:
  - runner caseiro em vez de GUT, para evitar dependência nova;
  - 1 m = 27 px;
  - pasta `eldritch_depths_3d_20261114`.

  Os dois itens de `achados.md`:
  - **Bug do `has_singleton`.** Severidade alta. Repro: com a Godot 4.7.2, um script `--headless` que imprime `Engine.has_singleton("SaveManager")` dá `false` enquanto o nó `/root/SaveManager` existe. Fix: `Autoloads.get_autoload`.
  - **Risco de arte.** Severidade alta: modelos originais, e Pedro nunca usou o Blender.
- [ ] **Passo 5:** Rodar `python lint.py`. O esperado é nenhum achado e código 0.
- [ ] **Passo 6:** Commit `docs: add project context, lint and design documents`.

**Pronto quando:** o lint passa e os quatro documentos estão versionados.

---

# Fase 1 — Núcleo sem 3D

### T05: Busca de autoload por nome
**Nível:** simples · **Depende de:** T02

**Files:** Create `scripts/core/autoloads.gd` · Modify `project.godot` (seção `[autoload]`) · Test `tests/test_autoloads.gd`

**Interfaces — Produces:** autoload `Autoloads` com `func get_autoload(name: StringName) -> Node`. A função devolve `get_tree().root.get_node_or_null(NodePath(name))`, ou seja, `null` sem erro quando o autoload não existe.

- [ ] **Passo 1:** Escrever `test_get_autoload(tree)`:
  - `tree.root.get_node("Autoloads").get_autoload(&"Autoloads")` não é nulo;
  - `get_autoload(&"Inexistente")` é nulo.
- [ ] **Passo 2:** Rodar e ver falhar.
- [ ] **Passo 3:** Implementar e registrar como autoload.
- [ ] **Passo 4:** Rodar e ver passar.
- [ ] **Passo 5:** Commit `feat: add autoload lookup replacing has_singleton`.

**Pronto quando:** o teste passa.

---

### T06: Faixas do Véu
**Nível:** simples · **Depende de:** T02

**Files:** Create `scripts/components/veil.gd` · Test `tests/test_veil.gd`

**Interfaces — Produces:** `class_name Veil` (estende `RefCounted`) com:
- `enum Band { CLARO, FINO, RASGADO }`, nesta ordem, para valer `CLARO < FINO < RASGADO`;
- `const THRESHOLD_FINO := 60.0` e `const THRESHOLD_RASGADO := 30.0`;
- `static func band_for(sanity: float) -> Band`, que devolve:
  - `CLARO` quando a sanidade é ≥ 60;
  - `FINO` quando é ≥ 30 e < 60;
  - `RASGADO` quando é < 30.

**Passos:**
- [ ] **Passo 1:** Escrever o teste:
```gdscript
func test_faixas_nos_limites():
    assert_eq(Veil.band_for(100.0), Veil.Band.CLARO)
    assert_eq(Veil.band_for(60.0), Veil.Band.CLARO)
    assert_eq(Veil.band_for(59.9), Veil.Band.FINO)
    assert_eq(Veil.band_for(30.0), Veil.Band.FINO)
    assert_eq(Veil.band_for(29.9), Veil.Band.RASGADO)
    assert_eq(Veil.band_for(0.0), Veil.Band.RASGADO)
```
- [ ] **Passo 2:** Rodar e ver falhar.
- [ ] **Passo 3:** Implementar.
- [ ] **Passo 4:** Rodar e ver passar.
- [ ] **Passo 5:** Em `context/decisoes.md`, registrar a `(i)`: faixas 60/30 provisórias; o efeito de cada faixa segue em aberto com Pedro (spec §9).
- [ ] **Passo 6:** Rodar `python lint.py`.
- [ ] **Passo 7:** Commit `feat: add veil sanity bands`.

**Pronto quando:** o teste e o lint passam.

---

### T07: StatsComponent portado
**Nível:** médio · **Depende de:** T05, T06

**Files:** Create `scripts/components/stats_component.gd` · Source `/home/usuario/Dev/holding_agy/eldritch_depths_20260912/scripts/components/stats_component.gd` (236 linhas) · Test `tests/test_stats.gd`

**Interfaces — Produces:** `class_name StatsComponent extends Node`.
- Mantém os mesmos sinais, exports e métodos do 2D:

  | Grupo | O que vem do 2D |
  |---|---|
  | Sinais | `health_changed`, `died`, `stamina_changed`, `sanity_changed`, `xp_changed`, `leveled_up`, `flasks_changed`, `exhaustion_changed` |
  | Vida e vigor | `take_damage(amount)`, `heal(amount)`, `consume_stamina(cost) -> bool`, `recover_stamina(amount)` |
  | Sanidade | `drain_sanity(amount)`, `restore_sanity(amount)` |
  | Progressão | `gain_xp(amount)` |
  | Frascos | `use_blood_flask() -> bool`, `use_laudanum_flask() -> bool`, `refill_flasks()` |
  | Estado | `is_alive() -> bool` |

- Os padrões numéricos ficam iguais aos do 2D:
  - vida 100;
  - vigor 100, com regeneração de 25/s, exaustão de 1,0 s e atraso de 0,5 s;
  - sanidade 100;
  - 3 frascos de sangue (curam 40%) e 2 de láudano (restauram 50% do máximo);
  - XP: o primeiro nível pede 80 e cada nível multiplica por 1,45.
- Novidades em relação ao 2D:
  - `signal veil_band_changed(band: Veil.Band)`;
  - `@export var ambient_sanity_drain: float = 0.0`, em unidades por segundo;
  - `func get_veil_band() -> Veil.Band`.

**Passos:**
- [ ] **Passo 1:** Escrever os testes. Cada teste cria `StatsComponent.new()`, chama `_ready()` à mão e avança com `_process(delta)`.

  | Teste | Ação | Esperado |
  |---|---|---|
  | `test_dreno_ambiente` | `ambient_sanity_drain = 0.8` e 10 chamadas de `_process(1.0)` | `current_sanity` ≈ 92,0 |
  | `test_sinal_de_faixa_so_na_troca` | conectar `veil_band_changed`, depois `drain_sanity(39)`, `drain_sanity(2)` e `drain_sanity(1)` | 0 emissões após a primeira chamada; 1 emissão com `FINO` após a segunda; ainda 1 após a terceira |
  | `test_laudano_restaura_metade` | `drain_sanity(80)`, depois `use_laudanum_flask()` | retorna `true`; sanidade 70; `current_laudanum_flasks` igual a 1 |
  | `test_laudano_reabre_faixa` | `drain_sanity(50)`, depois `use_laudanum_flask()` | emite `veil_band_changed(CLARO)` |
  | `test_vigor_exausto_nao_regenera` | `consume_stamina(100)`, `_process(0.9)` e depois `_process(0.7)` | vigor 0 após o primeiro passo; vigor > 0 após o segundo |
  | `test_sem_perks_manager_nao_quebra` | `consume_stamina(50)`, `_process(0.6)` e depois `_process(1.0)` | vigor ≈ 75 depois do segundo passo (regeneração de 25/s) |
  | `test_nivel` | `gain_xp(80)` | `level` 2, `max_health` 115, `max_stamina` 110, `xp_to_next` 116 |
- [ ] **Passo 2:** Rodar e ver falhar.
- [ ] **Passo 3:** Copiar o arquivo do 2D e fazer exatamente estas mudanças:
  - **(a)** Trocar `Engine.has_singleton("PerksManager")` por:
    ```gdscript
    var perks := Autoloads.get_autoload(&"PerksManager")
    if perks and perks.has_method("get_stamina_regen_multiplier"):
    ```
  - **(b)** Remover o bloco de `StatusEffectComponent` e deixar no lugar um comentário `# TODO porte: penalidade de StatusEffectComponent (ver 2D)`.
  - **(c)** No `_process`, chamar `drain_sanity(ambient_sanity_drain * delta)` quando `ambient_sanity_drain > 0`.
  - **(d)** Em `drain_sanity` e `restore_sanity`, guardar a faixa de antes e emitir `veil_band_changed` quando a de depois for diferente.
- [ ] **Passo 4:** Rodar e ver passar.
- [ ] **Passo 5:** Rodar `rtk proxy grep -rn has_singleton scripts/`. O esperado é nenhuma linha.
- [ ] **Passo 6:** Commit `feat: port stats component with veil band signal`.

**Pronto quando:** os 7 testes passam e não há nenhum `has_singleton` em `scripts/`.

---

### T08: Máquina de estados generalizada
**Nível:** simples · **Depende de:** T02

**Files:** Create `scripts/state_machine/state.gd`, `scripts/state_machine/state_machine.gd` · Source `/home/usuario/Dev/holding_agy/eldritch_depths_20260912/scripts/state_machine/` · Test `tests/test_state_machine.gd`

**Interfaces — Produces:**
- `class_name State extends Node`, com `var state_machine` e `var actor: Node` (no 2D era `CharacterBody2D`), e os métodos `enter()`, `exit()`, `process_input(event)`, `process_frame(delta)` e `process_physics(delta)`.
- `class_name StateMachine extends Node`, com:
  - `func init(actor: Node)`, que entra no **primeiro** estado filho;
  - `func change_state(key: StringName)`, em que a chave é o nome do nó em minúsculas;
  - `var current_state: State`;
  - `process_input`, `process_frame` e `process_physics`, que repassam a chamada ao estado atual.

**Passos:**
- [ ] **Passo 1:** Escrever `test_init_com_node3d`:
  - criar uma máquina com dois estados de teste, `A` e `B`, que contam quantas vezes `enter` e `exit` foram chamados;
  - chamar `init(Node3D.new())` → `current_state` é `A`, com 1 `enter`;
  - chamar `change_state(&"b")` → `A` tem 1 `exit` e `B` tem 1 `enter`.
- [ ] **Passo 2:** Escrever `test_chave_inexistente_nao_troca`: `change_state(&"zzz")` mantém o estado atual e não dá erro fatal.
- [ ] **Passo 3:** Rodar e ver falhar.
- [ ] **Passo 4:** Portar os dois arquivos do 2D, trocando o tipo de `actor`.
- [ ] **Passo 5:** Rodar e ver passar.
- [ ] **Passo 6:** Commit `refactor: generalize state machine actor to Node`.

**Pronto quando:** os 2 testes passam.

---

### T09: Matemática de movimento
**Nível:** simples · **Depende de:** T02

**Files:** Create `scripts/player/player_motion.gd` · Test `tests/test_motion.gd`

**Interfaces — Produces:** `class_name PlayerMotion`, com estas constantes e funções estáticas:
- Constantes: `WALK_SPEED := 5.0`, `ACCEL := 40.0` e `DECEL := 60.0`.
- `static func input_to_world(input: Vector2, cam_yaw: float) -> Vector3`:
  - recebe a direção na tela, com x para a direita e y para baixo;
  - devolve a direção no plano XZ, girada pelo yaw da câmera em torno de `Vector3.UP`, com comprimento no máximo 1.
- `static func compute_velocity(current: Vector3, wish: Vector3, max_speed: float, accel: float, delta: float) -> Vector3`:
  - aproxima `current` de `wish * max_speed` com `move_toward`, avançando `accel * delta` por passo;
  - quem chama passa `DECEL` quando `wish` é zero.

**Passos:**
- [ ] **Passo 1:** Escrever os testes:

  | Teste | Ação | Esperado |
  |---|---|---|
  | `test_frente_com_yaw_zero` | `input_to_world(Vector2(0, -1), 0.0)` | ≈ `Vector3(0, 0, -1)` |
  | `test_yaw_45` | `input_to_world(Vector2(0, -1), deg_to_rad(45))` | ≈ `Vector3(-0.7071, 0, -0.7071)` |
  | `test_diagonal_normalizada` | `input_to_world(Vector2(1, 1), 0.0).length()` | ≈ 1,0 |
  | `test_acelera_ate_velocidade` | 30 passos de `compute_velocity(v, Vector3(1, 0, 0), 5.0, 40.0, 1.0 / 60)` | `v.x` ≈ 5,0 e nunca acima disso |
  | `test_desacelera_ao_soltar` | partir de `Vector3(5, 0, 0)` com `wish` zero e `DECEL` | para em até 6 frames de 1/60 |
- [ ] **Passo 2:** Rodar e ver falhar.
- [ ] **Passo 3:** Implementar.
- [ ] **Passo 4:** Rodar e ver passar.
- [ ] **Passo 5:** Commit `feat: add camera-relative motion math`.

**Pronto quando:** os 5 testes passam.

---

### T10: Modo de entrada (teclado e mouse ou controle)
**Nível:** médio · **Depende de:** T03, T05

**Files:** Create `scripts/core/input_mode.gd` · Modify `project.godot` (autoload `InputMode`, depois de `Autoloads`) · Test `tests/test_input_mode.gd`

**Interfaces — Produces:** autoload `InputMode` com:
- `enum Mode { KBM, PAD }`, `var mode: Mode = Mode.KBM` e `signal mode_changed(mode: Mode)`;
- `const STICK_DEADZONE := 0.2`;
- `func handle_event(event: InputEvent) -> void`, chamada por `_input`, com estas regras:

  | Evento | Efeito |
  |---|---|
  | `InputEventJoypadButton` pressionado | vai para PAD |
  | `InputEventJoypadMotion` com `abs(axis_value) > STICK_DEADZONE` | vai para PAD |
  | `InputEventMouseMotion` com `relative.length() > 2.0` | vai para KBM |
  | `InputEventMouseButton` | vai para KBM |
  | `InputEventKey` pressionado | vai para KBM |

- O sinal `mode_changed` só é emitido quando o modo muda de fato.
- `func _on_joy_connection_changed(device: int, connected: bool)` volta para KBM quando `connected` é falso e não sobra nenhum controle (`Input.get_connected_joypads().is_empty()`). No `_ready`, essa função é conectada a `Input.joy_connection_changed`.

**Passos:**
- [ ] **Passo 1:** Escrever os testes. Cada teste instancia o próprio objeto com `load("res://scripts/core/input_mode.gd").new()` e não usa o autoload global.

  | Teste | Ação | Esperado |
  |---|---|---|
  | `test_comeca_em_kbm` | nenhuma | modo KBM |
  | `test_stick_acima_deadzone_vira_pad` | eixo 0 com valor 0,5 | PAD e 1 emissão |
  | `test_drift_nao_troca` | eixo com valor 0,15 | KBM e 0 emissões |
  | `test_mouse_volta_kbm` | depois de PAD, `InputEventMouseMotion` com `relative = Vector2(4, 0)` | KBM |
  | `test_mouse_tremido_nao_troca` | em PAD, `relative = Vector2(1, 0)` | continua PAD |
  | `test_botao_do_pad_vira_pad` | botão do controle pressionado | PAD |
  | `test_sem_reemissao` | dois eventos de PAD seguidos | 1 emissão |
  | `test_desconexao_volta_kbm` | em PAD, `_on_joy_connection_changed(0, false)` sem controle conectado na máquina de teste | KBM |
- [ ] **Passo 2:** Rodar e ver falhar.
- [ ] **Passo 3:** Implementar e registrar como autoload.
- [ ] **Passo 4:** Rodar e ver passar.
- [ ] **Passo 5:** Commit `feat: add input mode autoload with device hot-switch`.

**Pronto quando:** os 8 testes passam.

---

### T11: Mira
**Nível:** médio · **Depende de:** T02

**Files:** Create `scripts/player/aim_resolver.gd` · Test `tests/test_aim.gd`

**Interfaces — Produces:** `class_name AimResolver`, com duas funções estáticas.
- `static func ground_point(origin: Vector3, dir: Vector3, plane_y: float) -> Variant`:
  - devolve o ponto em que o raio cruza o plano horizontal na altura `plane_y`, como `Vector3`;
  - devolve `null` quando `abs(dir.y) < 0.0001` (raio quase paralelo ao plano) ou quando o ponto fica atrás da origem.
- `static func resolve(is_pad: bool, actor_pos: Vector3, mouse_ground: Variant, right_stick_world: Vector3, move_dir: Vector3, last_aim: Vector3) -> Vector3`:
  - devolve uma direção no plano XZ, com y = 0 e comprimento 1;
  - testa as fontes na ordem abaixo e usa a primeira que servir:
    1. em KBM: o ponto do mouse, se não for nulo e estiver a mais de 0,1 m do herói;
    2. em PAD: o analógico direito, se o comprimento passar de 0,2;
    3. a direção do movimento, se não for zero;
    4. `last_aim`, se não for zero;
    5. `Vector3.FORWARD`.
  - O resultado nunca é zero nem NaN.

**Passos:**
- [ ] **Passo 1:** Escrever os testes:

  | Teste | Ação | Esperado |
  |---|---|---|
  | `test_raio_acerta_chao` | `ground_point(Vector3(0, 10, 0), Vector3(0, -1, 1).normalized(), 0.0)` | ≈ `Vector3(0, 0, 10)` |
  | `test_raio_acima_do_horizonte_e_null` | `dir = Vector3(0, 0.2, 1)` | `null` |
  | `test_raio_paralelo_e_null` | `dir = Vector3(0, 0, 1)` | `null` |
  | `test_kbm_mira_no_mouse` | KBM, herói na origem, mouse em `(3, 0, 0)` | `(1, 0, 0)` |
  | `test_kbm_sem_chao_cai_no_movimento` | KBM, mouse `null`, movimento `(1, 0, 0)` | `(1, 0, 0)` |
  | `test_parado_sem_chao_mantem_ultima` | sem mouse, stick e movimento; `last_aim = (0, 0, 1)` | `(0, 0, 1)` |
  | `test_pad_stick_ganha_do_movimento` | stick `(0, 0, -1)` e movimento `(1, 0, 0)` | `(0, 0, -1)` |
  | `test_pad_drift_usa_movimento` | stick `(0.1, 0, 0)` e movimento `(0, 0, 1)` | `(0, 0, 1)` |
  | `test_nunca_zero` | todas as fontes zero ou nulas, inclusive `last_aim` | comprimento 1 e nenhum componente NaN |
- [ ] **Passo 2:** Rodar e ver falhar.
- [ ] **Passo 3:** Implementar.
- [ ] **Passo 4:** Rodar e ver passar.
- [ ] **Passo 5:** Commit `feat: add aim resolver with fallbacks`.

**Pronto quando:** os 9 testes passam.

---

# Fase 2 — Câmera e herói

### T12: Rig de câmera: distância e seguimento
**Nível:** médio · **Depende de:** T02

**Files:** Create `scripts/camera/camera_rig_3d.gd`, `scenes/camera/camera_rig_3d.tscn` · Test `tests/test_camera.gd`

**Interfaces — Produces:** `class_name CameraRig3D extends Node3D`.
- **Exports:** `target: Node3D`, `pitch_deg := 55.0`, `yaw_deg := 45.0`, `fov_deg := 40.0` e `follow_sharpness := 8.0`.
- **Constante e variável:** `const HERO_HEIGHT := 1.8` e `var distance: float`.
- **Funções:**
  - `func get_yaw() -> float`, em radianos;
  - `func step(delta: float)`, que faz o trabalho do `_process` e pode ser chamada pelos testes;
  - `static func distance_for_fraction(h: float, f: float, fov_deg: float) -> float`, que calcula `h / (f * 2.0 * tan(deg_to_rad(fov_deg) / 2.0))`.
- **Montagem da cena:** a raiz `CameraRig3D` tem um único filho, `Camera3D`, com `fov = fov_deg`.
  - O rig gira `yaw_deg` em Y.
  - A câmera fica recuada `distance` ao longo do eixo inclinado `pitch_deg` e olha para a origem do rig.
- **Seguimento:** `position = position.lerp(target.global_position, 1.0 - exp(-follow_sharpness * delta))`, o que não depende do fps.

**Passos:**
- [ ] **Passo 1:** Escrever os testes:

  | Teste | Ação | Esperado |
  |---|---|---|
  | `test_distancia_proxima` | `distance_for_fraction(1.8, 1.0 / 8.0, 40.0)` | ≈ 19,78 (eps 0,05) |
  | `test_distancia_atual` | `distance_for_fraction(1.8, 1.0 / 13.0, 40.0)` | ≈ 32,15 (eps 0,05) |
  | `test_seguimento_independe_do_fps(tree)` | alvo em `(10, 0, 0)`; o rig A recebe 60 passos de 1/60 e o rig B, 30 passos de 1/30 | posições finais iguais (eps 0,01) |
  | `test_alvo_projeta_no_centro(tree)` | `SubViewport` de 1920×1080 e 120 passos | `camera.unproject_position(target.global_position)` a menos de 2% do centro |
- [ ] **Passo 2:** Rodar e ver falhar.
- [ ] **Passo 3:** Implementar o script e a cena.
- [ ] **Passo 4:** Rodar e ver passar.
- [ ] **Passo 5:** Commit `feat: add tilted fixed camera rig`.

**Pronto quando:** os 4 testes passam.

---

### T13: Enquadramentos "atual" e "próxima"
**Nível:** simples · **Depende de:** T03, T12

**Files:** Modify `scripts/camera/camera_rig_3d.gd` · Test `tests/test_camera_presets.gd`

**Interfaces — Produces** (o que entra em `CameraRig3D`):
- `enum Preset { ATUAL, PROXIMA }`;
- `const FRACTION := { Preset.ATUAL: 1.0 / 13.0, Preset.PROXIMA: 1.0 / 8.0 }`;
- `@export var preset: Preset = Preset.ATUAL`;
- `func set_preset(p: Preset)`, que só define a distância-alvo;
- `func toggle_preset()`, que alterna entre os dois.

A distância atual vai até a distância-alvo pelo mesmo lerp do seguimento. A ação `debug_camera_preset` (F7) chama `toggle_preset()`.

**Passos:**
- [ ] **Passo 1:** Escrever os testes:
  - `test_preset_inicial`: depois de 300 passos de 1/60, `distance` ≈ 32,15.
  - `test_troca_suave`: chamar `set_preset(PROXIMA)` e dar 1 passo → `distance` fica entre 19,78 e 32,15. Depois de 300 passos → ≈ 19,78.
  - `test_toggle`: dois `toggle_preset()` voltam a `ATUAL`.
- [ ] **Passo 2:** Rodar e ver falhar.
- [ ] **Passo 3:** Implementar.
- [ ] **Passo 4:** Rodar e ver passar.
- [ ] **Passo 5:** Commit `feat: add camera framing presets with F7 toggle`.

**Pronto quando:** os 3 testes passam.

---

### T14: Linha do tempo de ações
**Nível:** médio · **Depende de:** T02

**Files:** Create `scripts/combat/action_timeline.gd` · Test `tests/test_timeline.gd`

**Interfaces — Produces:** `class_name ActionTimeline extends RefCounted`.
- `func _init(phases: Array)`: cada fase é um dicionário `{name: StringName, duration: float}`.
- `func advance(delta: float) -> Array[StringName]`: devolve **todas** as fases tocadas no intervalo, em ordem, inclusive as atravessadas inteiras num delta grande.
- `func current() -> StringName`: devolve `&""` quando a linha do tempo terminou.
- `func finished() -> bool`, `func elapsed() -> float` e `func reset()`.
- `func is_in(name: StringName, from_t: float, to_t: float) -> bool`: diz se a janela da fase cruza o intervalo de tempo `[from_t, to_t]`. A esquiva usa isso para a invencibilidade.

**Passos:**
- [ ] **Passo 1:** Escrever os testes. As fases do ataque são `windup 0.08`, `active 0.18` e `recovery 0.14`.

  | Teste | Ação | Esperado |
  |---|---|---|
  | `test_fases_em_ordem` | `advance(0.05)` e depois `advance(0.05)` | `[windup]` e depois `[windup, active]` |
  | `test_delta_grande_nao_pula_active` | `advance(0.3)` a partir do zero | o resultado contém `active` |
  | `test_termina` | `advance(0.5)` | `finished()` verdadeiro e `current()` igual a `&""` |
  | `test_reset` | `reset()` depois de terminar | `elapsed()` 0 e `current()` igual a `windup` |
- [ ] **Passo 2:** Rodar e ver falhar.
- [ ] **Passo 3:** Implementar.
- [ ] **Passo 4:** Rodar e ver passar.
- [ ] **Passo 5:** Commit `feat: add action timeline robust to frame hitches`.

**Pronto quando:** os 4 testes passam.

---

### T15: Hitbox e hurtbox 3D
**Nível:** difícil · **Depende de:** T02

**Files:** Create `scripts/combat/hitbox_3d.gd`, `scripts/combat/hurtbox_3d.gd` · Test `tests/test_hitbox.gd`

**Interfaces — Produces:**
- `class_name Hitbox3D extends Area3D`
  - Exports: `damage: float = 20.0`, `posture_damage: float = 20.0` e `sanity_damage: float = 0.0`.
  - Estado: `var active := false` e `var source: Node`, que é quem bate.
  - `signal hit_landed(hurtbox: Hurtbox3D)`.
  - `func activate()`:
    1. marca `active` e limpa a lista de quem já foi atingido;
    2. **na mesma chamada**, consulta as sobreposições com `get_world_3d().direct_space_state.intersect_shape` usando a própria forma e máscara;
    3. atinge cada hurtbox encontrada.
  - Enquanto ativa, também atinge quem entrar por `area_entered`.
  - Cada hurtbox é atingida **no máximo uma vez** por ativação.
  - `func deactivate()`.
- `class_name Hurtbox3D extends Area3D`
  - `signal hurt(hitbox: Hitbox3D)`.
  - Estado: `var invulnerable := false` e `var parrying := false`.
  - `func receive(hitbox: Hitbox3D) -> void`: não faz nada se `invulnerable`. Senão, emite `hurt`. Quem trata o parry é o dono da hurtbox, ao receber o sinal.
- Camadas e máscaras seguem a tabela do cabeçalho. As duas classes têm `@export var team: int` (0 herói, 1 inimigo), que define camada e máscara no `_ready`.

**Passos:**
- [ ] **Passo 1:** Escrever os testes (todos com a árvore; esperar 2 frames de física depois de montar):

  | Teste | Montagem | Esperado |
  |---|---|---|
  | `test_acerta_ao_ativar_sobreposto` | hitbox do herói e hurtbox de inimigo na mesma posição; `activate()` | 1 `hurt` **sem** esperar outro frame |
  | `test_uma_vez_por_ativacao` | ativa e espera 5 frames de física | 1 `hurt` |
  | `test_reativar_acerta_de_novo` | `deactivate()` e `activate()` | 2 `hurt` |
  | `test_mesmo_time_nao_acerta` | hitbox e hurtbox do herói | 0 `hurt` |
  | `test_invulneravel` | `invulnerable = true` | 0 `hurt` |
- [ ] **Passo 2:** Rodar e ver falhar.
- [ ] **Passo 3:** Implementar.
- [ ] **Passo 4:** Rodar e ver passar.
- [ ] **Passo 5:** Commit `feat: add 3d hitbox and hurtbox with immediate overlap check`.

**Pronto quando:** os 5 testes passam.

---

### T16: Postura
**Nível:** simples · **Depende de:** T02

**Files:** Create `scripts/combat/posture_component.gd` · Source `/home/usuario/Dev/holding_agy/eldritch_depths_20260912/scripts/components/posture_component.gd` · Test `tests/test_posture.gd`

**Interfaces — Produces:** `class_name PostureComponent extends Node`.
- Sinais: `posture_changed(current, max_val)`, `posture_broken` e `posture_recovered`. O sinal `riposted` do 2D não entra neste bloco.
- Valores: `max_posture := 100.0`, `stagger_duration := 3.0` e `recovery_rate := 14.0` (por segundo).
- Estado: `var current := 0.0` e `var is_broken := false`.
- Funções: `func damage_posture(amount: float)` e `func step(delta: float)`.
- **Quebra:** quando `current` chega ao máximo, emite `posture_broken`, e a postura fica quebrada por `stagger_duration`. Depois, zera e emite `posture_recovered`.
- **Recuperação:** fora da quebra, a postura volta a 0 a 14 por segundo.

**Passos:**
- [ ] **Passo 1:** Escrever os testes:
  - `test_quebra_no_maximo`: `damage_posture(100)` → 1 `posture_broken` e `is_broken` verdadeiro.
  - `test_recupera_apos_3s`: depois de quebrar, `step(2.9)` → ainda quebrada; `step(0.2)` → `posture_recovered` e `current` 0.
  - `test_recuperacao_gradual`: `damage_posture(50)` e `step(1.0)` → `current` ≈ 36.
- [ ] **Passo 2:** Rodar e ver falhar.
- [ ] **Passo 3:** Implementar.
- [ ] **Passo 4:** Rodar e ver passar.
- [ ] **Passo 5:** Commit `feat: port posture component`.

**Pronto quando:** os 3 testes passam.

---

### T17: Herói provisório: cena, parado e andar
**Nível:** difícil · **Depende de:** T07, T08, T09, T10, T11, T13, T15, T16

**Files:** Create `scripts/player/player_3d.gd`, `scripts/player/states/idle.gd`, `scripts/player/states/move.gd`, `scenes/player/player_3d.tscn` · Test `tests/test_player_move.gd`

**Interfaces — Produces:** `class_name Player3D extends CharacterBody3D`.
- **Exports:** `camera_rig: CameraRig3D` e `base_damage := 20.0`.
- **Variáveis:**
  - `var aim_dir: Vector3 = Vector3.FORWARD` e `var move_dir: Vector3`;
  - `var input_source: Callable`. O padrão lê `Input` e `InputMode`. Os testes injetam um `Callable` que devolve o dicionário de entrada.
- **Dicionário de entrada:** `{move: Vector2, aim: Vector2, attack: bool, roll: bool, parry: bool, flask: bool, laudanum: bool}`. Os botões chegam como `just_pressed`.
- **Funções:**
  - `func read_input() -> Dictionary`;
  - `func step(delta: float)`, que faz o trabalho do `_physics_process` e pode ser chamada pelos testes.
- **Filhos da cena, com estes nomes exatos:**
  - `Stats` (`StatsComponent`) e `Posture` (`PostureComponent`);
  - `StateMachine`, com os estados `Idle` e `Move` (a partir da T18, também `Attack`, `Roll`, `Parry`, `Hurt` e `Dead`);
  - `Sword` (`Hitbox3D`, time 0, uma caixa de 1,2 × 1 × 1,2 m a 0,9 m à frente);
  - `Hurtbox` (`Hurtbox3D`, time 0, uma cápsula);
  - `Body` (`MeshInstance3D` com uma cápsula de 1,8 m) e `AimArrow` (`MeshInstance3D` com um cone fino no chão, apontando para `aim_dir`);
  - `CollisionShape3D`, uma cápsula de raio 0,35 m e altura 1,8 m.
- **Regras:**
  - O movimento usa `PlayerMotion.input_to_world(move, camera_rig.get_yaw())` e depois `compute_velocity`, com `DECEL` quando a entrada é zero.
  - A cada passo, `aim_dir` vem de `AimResolver.resolve`. Em KBM, o raio sai de `camera.project_ray_origin` e `project_ray_normal` na posição do mouse.
  - O corpo gira com `look_at` na direção do movimento quando anda, e na de `aim_dir` durante ataque e parry (T18 e T20).
  - O estado é `idle` com velocidade zero e `move` com entrada.
  - Gravidade fixa de 20 m/s² e `move_and_slide()`.

**Passos:**
- [ ] **Passo 1:** Escrever os testes. Todos montam `player_3d.tscn` com um `CameraRig3D` e um piso `StaticBody3D`.

  | Teste | Ação | Esperado |
  |---|---|---|
  | `test_parado_e_idle` | 10 passos sem entrada | estado `idle` e velocidade ≈ 0 |
  | `test_anda_e_move` | `move = (1, 0)` por 30 passos de 1/60 | estado `move` e velocidade horizontal ≈ 5,0 |
  | `test_movimento_relativo_a_camera` | rig com yaw 45° e `move = (0, -1)` por 30 passos | velocidade ≈ `(-3.54, 0, -3.54)` |
  | `test_mira_segue_movimento_no_pad` | modo PAD, sem stick e `move = (1, 0)` | `aim_dir` ≈ a direção do movimento no mundo |
- [ ] **Passo 2:** Rodar e ver falhar.
- [ ] **Passo 3:** Implementar o script, os dois estados e a cena.
- [ ] **Passo 4:** Rodar e ver passar.
- [ ] **Passo 5:** Commit `feat: add placeholder hero with camera-relative movement`.

**Pronto quando:** os 4 testes passam e a cena abre no editor sem avisos de nó faltando.

---

### T18: Ataque em dois golpes
**Nível:** difícil · **Depende de:** T14, T17

**Files:** Create `scripts/player/states/attack.gd` · Modify `scenes/player/player_3d.tscn` (acrescentar o estado `Attack`) · Test `tests/test_player_attack.gd`

**Interfaces — Produces:** o estado `attack`.
- **Linha do tempo:** fases `windup 0.08`, `active 0.18` e `recovery 0.14`, numa `ActionTimeline`.
- **Vigor:** 18 no primeiro golpe e 22 no segundo. Sem vigor, o ataque não sai e o estado não muda.
- **Hitbox:** `Sword` ativa ao entrar em `active` e desativa ao sair. O dano é `base_damage`, e a hitbox tem `source = self`.
- **Combo:** uma entrada `attack` durante `recovery` encadeia o golpe 2. Depois do golpe 2, o próximo volta ao golpe 1.
- **Movimento e mira:** no ataque, a velocidade cai a 20% da caminhada, e o corpo encara `aim_dir`.
- **Fim:** ao terminar a linha do tempo, volta a `idle` ou `move`.

**Passos:**
- [ ] **Passo 1:** Escrever os testes. Todos montam o herói e um `Hurtbox3D` de inimigo (time 1) a 1 m à frente.

  | Teste | Ação | Esperado |
  |---|---|---|
  | `test_ataque_gasta_vigor_e_acerta_uma_vez` | `attack` por 1 frame e depois 0,4 s | vigor 82 logo após o comando; ao fim, exatamente 1 `hurt` na hurtbox de teste |
  | `test_combo_segundo_golpe` | `attack` de novo durante a recovery | vigor 60 logo após o segundo golpe, antes dos 0,5 s de atraso da regeneração; 2 acertos ao fim |
  | `test_ataque_com_travada` | `attack` e depois um único `step(0.3)` | 1 `hurt` |
  | `test_sem_vigor_nao_ataca` | vigor 10 e `attack` | estado inalterado |
- [ ] **Passo 2:** Rodar e ver falhar.
- [ ] **Passo 3:** Implementar.
- [ ] **Passo 4:** Rodar e ver passar.
- [ ] **Passo 5:** Commit `feat: add two-hit attack combo`.

**Pronto quando:** os 4 testes passam.

---

### T19: Esquiva
**Nível:** difícil · **Depende de:** T14, T17

**Files:** Create `scripts/player/states/roll.gd` · Modify `scenes/player/player_3d.tscn` · Test `tests/test_player_roll.gd`

**Interfaces — Produces:** o estado `roll`.
- **Custo e duração:** 20 de vigor e 0,34 s.
- **Velocidade:** 10,4 m/s na direção do movimento, ou de `aim_dir` se o herói estiver parado.
- **Invencibilidade:** `Hurtbox.invulnerable` é verdadeira enquanto o tempo da esquiva está entre 0,04 e 0,26 s.
  - O teste de travada usa `ActionTimeline.is_in` com o intervalo do frame.
  - A hurtbox é atualizada **antes** de processar os golpes recebidos naquele frame.
- **Interrupção:** a esquiva não pode ser interrompida por ataque.
- **Fim:** depois dela, volta a `idle` ou `move`.

**Passos:**
- [ ] **Passo 1:** Escrever os testes:

  | Teste | Ação | Esperado |
  |---|---|---|
  | `test_esquiva_desloca` | `roll` com `move = (1, 0)` e 0,34 s | deslocamento ≈ 3,5 m (eps 0,3) |
  | `test_esquiva_invencivel_com_travada` | `roll`, um passo de 0,02 s e depois um único passo de 0,22 s, com uma `Hitbox3D` inimiga ativa sobre o herói o tempo todo | vida continua 100 e o estado ainda é `roll` |
  | `test_vulneravel_depois` | depois de 0,3 s de esquiva | `Hurtbox.invulnerable` é falso |
  | `test_esquiva_sem_vigor_nao_sai` | vigor 10 e `roll` | estado inalterado |
- [ ] **Passo 2:** Rodar e ver falhar.
- [ ] **Passo 3:** Implementar.
- [ ] **Passo 4:** Rodar e ver passar.
- [ ] **Passo 5:** Commit `feat: add roll with invulnerability window`.

**Pronto quando:** os 4 testes passam.

---

### T20: Parry
**Nível:** médio · **Depende de:** T17

**Files:** Create `scripts/player/states/parry.gd` · Modify `scenes/player/player_3d.tscn`, `scripts/player/player_3d.gd` (handler de `Hurtbox.hurt`) · Test `tests/test_player_parry.gd`

**Interfaces — Produces:** o estado `parry`.
- **Custo e tempos:** 15 de vigor, janela de 0,22 s com `Hurtbox.parrying = true` e recovery de 0,18 s.
- **Dano recebido**, tratado em `Player3D._on_hurt(hitbox)`:
  - se `parrying` for verdadeiro: o herói não recebe dano, e o `PostureComponent` do `hitbox.source` (quando existir) recebe 50. Esse valor é `(i)`, ajustável no teste de Pedro;
  - senão: `Stats.take_damage(hitbox.damage)`, `Stats.drain_sanity(hitbox.sanity_damage)` e troca para o estado `hurt` (T21).
- **Arquivo `player_3d.gd`:** `@export var shield_mitigation := 0.5` fica declarado e **sem uso**, porque não há bloqueio neste bloco.

**Passos:**
- [ ] **Passo 1:** Escrever os testes. Usam um nó atacante de teste com `PostureComponent` e uma `Hitbox3D` de inimigo com `source` igual a ele.

  | Teste | Ação | Esperado |
  |---|---|---|
  | `test_parry_quebra_postura` | o golpe chega 0,1 s depois do `parry` | herói sem dano e postura do atacante 50 |
  | `test_parry_atrasado_toma_dano` | o golpe chega 0,3 s depois | dano recebido |
  | `test_golpe_cosmico_tira_sanidade` | sem parry, `sanity_damage = 15` | sanidade do herói 85 |
- [ ] **Passo 2:** Rodar e ver falhar.
- [ ] **Passo 3:** Implementar.
- [ ] **Passo 4:** Rodar e ver passar.
- [ ] **Passo 5:** Commit `feat: add parry with posture damage to attacker`.

**Pronto quando:** os 3 testes passam.

---

### T21: Dano, morte e frascos
**Nível:** médio · **Depende de:** T20

**Files:** Create `scripts/player/states/hurt.gd`, `scripts/player/states/dead.gd` · Modify `scenes/player/player_3d.tscn`, `scripts/player/player_3d.gd` · Test `tests/test_player_hurt.gd`

**Interfaces — Produces:**
- **Estado `hurt`:** dura 0,3 s, ignora entradas e empurra o herói 0,5 m para longe de quem bateu.
- **Estado `dead`:** começa com o sinal `Stats.died`. O herói fica parado, ignora entradas para sempre e emite `Player3D.signal hero_died`.
- **Frascos:** fora de `hurt` e `dead`, a entrada `flask` chama `Stats.use_blood_flask()` e `laudanum` chama `Stats.use_laudanum_flask()`.

**Passos:**
- [ ] **Passo 1:** Escrever os testes:

  | Teste | Ação | Esperado |
  |---|---|---|
  | `test_dano_entra_em_hurt` | 1 golpe | estado `hurt`; depois de 0,35 s, `idle` |
  | `test_morte` | `Stats.take_damage(100)` | estado `dead`, 1 `hero_died`; uma entrada `attack` depois disso não muda o estado |
  | `test_frasco_de_sangue` | vida 50 e `flask` | vida 90 |
  | `test_laudano` | sanidade 20 e `laudanum` | sanidade 70 |
- [ ] **Passo 2:** Rodar e ver falhar.
- [ ] **Passo 3:** Implementar.
- [ ] **Passo 4:** Rodar e ver passar.
- [ ] **Passo 5:** Commit `feat: add hurt, death and flask use to hero`.

**Pronto quando:** os 4 testes passam.

---

# Fase 3 — Inimigo

### T22: Inimigo: cena, parado e perseguição
**Nível:** médio · **Depende de:** T07, T08, T15, T16

**Files:** Create `scripts/enemies/enemy_common.gd`, `scripts/enemies/states/idle.gd`, `scripts/enemies/states/chase.gd`, `scenes/enemies/enemy_common.tscn` · Test `tests/test_enemy_chase.gd`

**Interfaces — Produces:** `class_name EnemyCommon extends CharacterBody3D`.
- **Exports:** `target: Node3D`, `is_cosmic := true`, `move_speed := 2.4`, `detection_range := 6.7` e `attack_range := 1.5`.
- **Função:** `func step(delta: float)`.
- **Filhos da cena:**
  - `Stats` (`StatsComponent` com `max_health = 60`) e `Posture`;
  - `StateMachine` com os estados `Idle` e `Chase`;
  - `Claw` (`Hitbox3D`, time 1, `damage = 15`) e `Hurtbox` (`Hurtbox3D`, time 1);
  - `Body` (cápsula escura de 1,6 m, com material próprio para a T23 poder trocar a cor);
  - `CollisionShape3D`.
- **Comportamento:**
  - Sem alvo, ou com o alvo além da detecção: fica em `idle`.
  - Dentro da detecção: `chase`, andando em linha reta até o alvo com `move_and_slide` (sem `NavigationAgent3D` neste bloco).
  - Dentro do alcance: para e fica no estado `chase`. A T23 troca isso por `telegraph`.

**Passos:**
- [ ] **Passo 1:** Escrever os testes:

  | Teste | Montagem | Esperado |
  |---|---|---|
  | `test_parado_fora_da_deteccao` | alvo a 8 m e 60 passos | `idle` |
  | `test_persegue_dentro_da_deteccao` | alvo a 5 m | `chase` e velocidade ≈ 2,4 |
  | `test_para_no_alcance` | alvo a 1,2 m | velocidade horizontal ≈ 0 |
- [ ] **Passo 2:** Rodar e ver falhar.
- [ ] **Passo 3:** Implementar.
- [ ] **Passo 4:** Rodar e ver passar.
- [ ] **Passo 5:** Commit `feat: add common enemy with chase`.

**Pronto quando:** os 3 testes passam.

---

### T23: Inimigo: aviso, golpe e recarga
**Nível:** médio · **Depende de:** T14, T22

**Files:** Create `scripts/enemies/states/{telegraph,attack,cooldown}.gd` · Modify `scenes/enemies/enemy_common.tscn`, `scripts/enemies/states/chase.gd` · Test `tests/test_enemy_attack.gd`

**Interfaces — Produces:**
- **Ciclo:** dentro do alcance, `chase` vai para `telegraph` (0,4 s), depois `attack` (0,25 s) e depois `cooldown` (0,6 s). Ao fim, volta a `chase`.
- **Aviso visual:** durante `telegraph`, o material de `Body` fica vermelho emissivo (`emission = #ff2020`, energia 2). Ao sair, volta ao normal.
- **Golpe:** `Claw` fica ativa durante `attack`, com `sanity_damage = 15` se `is_cosmic` e 0 se não.
- **Direção:** o inimigo encara o alvo no início do `telegraph` e não gira depois disso, para que a esquiva para o lado funcione.

**Passos:**
- [ ] **Passo 1:** Escrever os testes. O alvo é um `Node3D` com `Hurtbox3D` (time 0) e um `StatsComponent`, ligado como no `Player3D._on_hurt`.

  | Teste | Montagem | Esperado |
  |---|---|---|
  | `test_telegrafa_antes_de_bater` | alvo a 1 m | estado `telegraph`; nenhum dano nos primeiros 0,39 s; 15 de dano até 0,7 s |
  | `test_golpe_cosmico_tira_sanidade` | depois do golpe | sanidade do alvo 85 |
  | `test_nao_cosmico_nao_tira` | `is_cosmic = false` | sanidade 100 |
  | `test_recarga` | depois do golpe | nenhum novo dano antes de 0,6 s |
- [ ] **Passo 2:** Rodar e ver falhar.
- [ ] **Passo 3:** Implementar.
- [ ] **Passo 4:** Rodar e ver passar.
- [ ] **Passo 5:** Commit `feat: add enemy telegraph, attack and cooldown`.

**Pronto quando:** os 4 testes passam.

---

### T24: Inimigo: atordoado, crítico e morte
**Nível:** médio · **Depende de:** T23

**Files:** Create `scripts/enemies/states/{stunned,dead}.gd` · Modify `scenes/enemies/enemy_common.tscn`, `scripts/enemies/enemy_common.gd` · Test `tests/test_enemy_stun.gd`

**Interfaces — Produces:**
- **Atordoado:** `Posture.posture_broken` leva ao estado `stunned`, que dura 1,5 s. Esse tempo é o atordoamento do inimigo no 2D e prevalece sobre os 3,0 s do componente: o `stunned` chama `Posture` para recuperar ao sair.
- **Crítico:** o dano recebido em `stunned` é dobrado.
- **Morte:** `Stats.died` leva ao estado `dead`. O inimigo:
  - desliga as colisões e a hurtbox;
  - dá 35 de XP ao `Stats` do alvo, se o alvo tiver um;
  - emite `signal enemy_died`;
  - se apaga em 1 s com `queue_free`.
- **Função:** `func _on_hurt(hitbox)` aplica `hitbox.damage` (× 2 se atordoado) e `hitbox.posture_damage` na postura.

**Passos:**
- [ ] **Passo 1:** Escrever os testes:

  | Teste | Ação | Esperado |
  |---|---|---|
  | `test_postura_quebrada_atordoa` | `Posture.damage_posture(100)` | `stunned`; depois de 1,6 s, sai de `stunned` |
  | `test_critico_atordoado` | golpe de 20 em `stunned` | vida 20 |
  | `test_morte_da_xp` | 60 de dano | estado `dead`; XP do alvo 35; 1 `enemy_died` |
- [ ] **Passo 2:** Rodar e ver falhar.
- [ ] **Passo 3:** Implementar.
- [ ] **Passo 4:** Rodar e ver passar.
- [ ] **Passo 5:** Commit `feat: add enemy stagger, crits and death`.

**Pronto quando:** os 3 testes passam.

---

# Fase 4 — Mundo

### T25: Sala cinza, luz e cena principal
**Nível:** médio · **Depende de:** T21, T24

**Files:** Create `scenes/world/greybox_room.tscn`, `scenes/main.tscn`, `scripts/main.gd` · Modify `project.godot` (`run/main_scene="res://scenes/main.tscn"`) · Test `tests/test_main_scene.gd`

**Interfaces — Produces:**
- **`greybox_room.tscn`:**
  - Geometria em `CSGBox3D` com `use_collision = true`, na camada 1:
    - um piso de 16 × 16 m e paredes de 3 m de altura;
    - uma coluna de 1 × 1 m no centro-leste;
    - uma abertura de porta de 2 m na parede norte, levando a uma saleta de 4 × 4 m.
  - O nó `DoorSlot` (`Marker3D`) marca o centro da abertura (T26).
  - Material: cinza-escuro `#3a3a40`, com roughness 0,9.
- **`WorldEnvironment`:**
  - fundo `#05060a`, ambiente `#202430` com energia 0,05;
  - névoa de profundidade com densidade 0,03 e cor `#0b0d12`;
  - tonemap ACES e glow ligado com intensidade 0,4.
  - Nenhuma `DirectionalLight3D`.
- **Luz do herói:** `OmniLight3D` com o nome `HeroLight`, filha do `Player3D` (acrescentar na cena do herói):
  - posição a 2,2 m de altura;
  - cor `#ffb36b`, energia 2,5, alcance 7 m;
  - sombra ligada.
- **`main.tscn`:** contém a sala, o `Player3D` no centro-sul, o `CameraRig3D` com `target` igual ao herói, e o `EnemyCommon` a 6 m do herói com `target` igual ao herói.
- **`main.gd`:**
  - põe `ambient_sanity_drain = 0.8` no `Stats` do herói;
  - liga `hero_died` a um `get_tree().reload_current_scene()` com 2 s de atraso.

**Passos:**
- [ ] **Passo 1:** Escrever os testes:
  - `test_main_carrega(tree)`: instanciar `main.tscn` não gera erros. A cena tem `Player3D`, `EnemyCommon`, `CameraRig3D` e `HeroLight`.
  - `test_drena_sanidade`: 10 s de passos → sanidade do herói ≈ 92.
- [ ] **Passo 2:** Rodar e ver falhar.
- [ ] **Passo 3:** Implementar.
- [ ] **Passo 4:** Rodar e ver passar.
- [ ] **Passo 5:** Rodar a captura: `godot --path . --write-movie <pasta temporária>/sala/f.png --fixed-fps 30 --quit-after 90`. Abrir o último quadro e conferir três coisas:
  - o herói se lê pela luz quente;
  - a sala aparece até a névoa;
  - o inimigo é visível.
- [ ] **Passo 6:** Descrever em uma linha no ledger o que se vê no quadro.
- [ ] **Passo 7:** Commit `feat: add greybox room, hero light and main scene`.

**Pronto quando:** os testes passam e a captura mostra herói, sala e inimigo.

---

### T26: Parede do Véu
**Nível:** difícil · **Depende de:** T06, T25

**Files:** Create `scripts/world/veil_wall.gd`, `scenes/world/veil_wall.tscn` · Modify `scenes/main.tscn` (parede em `DoorSlot`), `scripts/main.gd` · Test `tests/test_veil_wall.gd`

**Interfaces — Produces:** `class_name VeilWall extends StaticBody3D`, no grupo `veil_walls`.
- **Export e funções:** `@export var opens_at: Veil.Band = Veil.Band.FINO`, `func set_band(b: Veil.Band)` e `func is_solid() -> bool`.
- **Filhos:** `CollisionShape3D` de 2 × 3 × 0,4 m, `Mesh` com um material de dissolução (parâmetro `dissolve` de 0 a 1) e `Inside` (`Area3D` do mesmo tamanho, que detecta as camadas 2 e 3).
- **Regras:**
  - **Abrir:** quando `band >= opens_at`, desliga a colisão na hora e anima `dissolve` até 1 em 0,6 s.
  - **Fechar:** quando a faixa volta abaixo de `opens_at` **e** `Inside` está vazia, religa a colisão e anima `dissolve` até 0.
  - **Com alguém dentro:** se `Inside` não estiver vazia, a parede marca o fechamento como pendente e fecha no primeiro frame de física em que esvaziar.
- **`main.gd`:** liga `Stats.veil_band_changed` do herói ao `set_band` de cada nó do grupo `veil_walls`.

**Passos:**
- [ ] **Passo 1:** Escrever os testes (todos com a árvore):

  | Teste | Ação | Esperado |
  |---|---|---|
  | `test_solida_no_claro` | parede nova | `is_solid()` verdadeiro |
  | `test_abre_no_fino` | `set_band(FINO)` | `is_solid()` falso no mesmo frame |
  | `test_abre_no_rasgado` | `set_band(RASGADO)` | aberta |
  | `test_nao_fecha_com_corpo_dentro` | aberta, um `CharacterBody3D` na camada 2 dentro de `Inside`, 2 frames de física e `set_band(CLARO)` | continua aberta; depois de tirar o corpo e esperar 2 frames, fica sólida |
  | `test_main_queda_abre_parede` | em `main.tscn`, `drain_sanity(45)` no herói | a parede fica não sólida no mesmo frame |
- [ ] **Passo 2:** Rodar e ver falhar.
- [ ] **Passo 3:** Implementar.
- [ ] **Passo 4:** Rodar e ver passar.
- [ ] **Passo 5:** Commit `feat: add veil wall that opens with low sanity`.

**Pronto quando:** os 5 testes passam.

---

### T27: Vinheta da sanidade e tecla de depuração
**Nível:** médio · **Depende de:** T26

**Files:** Create `shaders/veil_vignette.gdshader` · Modify `scenes/main.tscn` (`CanvasLayer` com `ColorRect`), `scripts/main.gd` · Test `tests/test_vignette.gd`

**Interfaces — Produces:**
- **Shader:** `canvas_item` com `uniform float intensity : hint_range(0, 1)`.
  - Desenha uma borda escura arroxeada (`#1a0f24`) que se fecha conforme a intensidade sobe.
  - Mesmo com `intensity = 1`, o raio interno sem efeito é de pelo menos 0,35 da meia-diagonal.
  - Com `intensity = 0`, o shader fica totalmente transparente.
- **Na cena:** um `ColorRect` chamado `Vignette`, em tela cheia, com `mouse_filter = IGNORE`.
- **`main.gd`:**
  - `static func vignette_intensity(sanity: float) -> float` devolve `clamp((60.0 - sanity) / 60.0, 0.0, 1.0)`;
  - ao receber `sanity_changed`, atualiza o uniform;
  - a ação `debug_sanity_drop` (F9) chama `drain_sanity(20)` só quando `OS.is_debug_build()`.

**Passos:**
- [ ] **Passo 1:** Escrever os testes:
  - `test_intensidade`: 100 → 0; 60 → 0; 30 → 0,5; 0 → 1.
  - `test_vinheta_existe(tree)`: em `main.tscn`, o nó `Vignette` existe e o shader carrega sem erro.
- [ ] **Passo 2:** Rodar e ver falhar.
- [ ] **Passo 3:** Implementar.
- [ ] **Passo 4:** Rodar e ver passar.
- [ ] **Passo 5:** Rodar a captura com a sanidade em 20, ajustada à mão em `main.gd` por um argumento `-- --sanity=20`. Conferir que a borda está fechada e o centro está limpo.
- [ ] **Passo 6:** Commit `feat: add sanity vignette and debug sanity key`.

**Pronto quando:** os testes passam e a captura confere.

---

# Fase 5 — HUD

### T28: Rótulos de botão por dispositivo
**Nível:** simples · **Depende de:** T10

**Files:** Create `scripts/ui/input_prompt.gd` · Test `tests/test_prompts.gd`

**Interfaces — Produces:** `class_name InputPrompt`, com `static func label_for(action: StringName, is_pad: bool) -> String`. Os rótulos são texto, sem ícones neste bloco:

| Ação | KBM | PAD |
|---|---|---|
| `use_blood_flask` | `"1"` | `"↓"` |
| `use_laudanum` | `"2"` | `"↑"` |
| `interact` | `"E"` | `"B"` |
| qualquer outra | `""` | `""` |

**Passos:**
- [ ] **Passo 1:** Escrever um teste por linha da tabela.
- [ ] **Passo 2:** Rodar e ver falhar.
- [ ] **Passo 3:** Implementar.
- [ ] **Passo 4:** Rodar e ver passar.
- [ ] **Passo 5:** Commit `feat: add device-aware input prompt labels`.

**Pronto quando:** os testes passam.

---

### T29: HUD mínimo
**Nível:** médio · **Depende de:** T25, T28

**Files:** Create `scripts/ui/hud_minimal.gd`, `scenes/ui/hud_minimal.tscn` · Modify `scenes/main.tscn` (o HUD num `CanvasLayer` acima da vinheta), `scripts/main.gd` (`hud.bind(hero.get_node("Stats"))`) · Test `tests/test_hud.gd`

**Interfaces — Produces:** `class_name HudMinimal extends Control`.
- **Funções:**
  - `func bind(stats: StatsComponent)`, que conecta `health_changed`, `stamina_changed`, `sanity_changed` e `flasks_changed`, além de `InputMode.mode_changed`;
  - `func hud_rect() -> Rect2`, que devolve a união dos retângulos visíveis.
- **Posição e escala:** canto superior esquerdo. A escala é `altura_da_tela / 1080`, com margem de 24 px em 1080p.
- **Barras:** três barras finas, cada uma com 6 px de altura em 1080p, 4 px entre elas e largura de 2,4 px por ponto do máximo, limitada a 360 px.

  | Barra | Cor |
  |---|---|
  | vida | `#9b2226` |
  | vigor | `#c9a227` |
  | sanidade | `#6a4c93` |

  A barra de sanidade tem marcas de 1 px em 60 e 30.
- **Contadores:** abaixo das barras, dois contadores (sangue e láudano) em fonte de 16 px em 1080p, no formato `<rótulo> ×<quantidade>`, usando `InputPrompt.label_for`.
- **Restrição:** nada no centro nem na parte de baixo da tela.

**Passos:**
- [ ] **Passo 1:** Escrever os testes. Todos rodam num `SubViewport`, com o HUD ligado a um `StatsComponent`.

  | Teste | Ação | Esperado |
  |---|---|---|
  | `test_area_menor_que_6_por_cento` | para cada tamanho: 1920×1080, 2560×1080 e 1280×800 | área de `hud_rect()` menor que 6% da tela e o retângulo inteiro dentro da tela |
  | `test_barra_segue_vida` | `take_damage(50)` | a parte preenchida da barra de vida tem metade da largura total (eps 1 px) |
  | `test_prompt_troca_com_modo` | emitir `mode_changed(PAD)` | rótulo do frasco de sangue começa com `"↓"` |
  | `test_contador_frasco` | `use_blood_flask()` com vida 50 | contador `×2` |
- [ ] **Passo 2:** Rodar e ver falhar.
- [ ] **Passo 3:** Implementar.
- [ ] **Passo 4:** Rodar e ver passar.
- [ ] **Passo 5:** Rodar a captura em 1080p e conferir que o HUD está no canto e que o centro da tela está livre.
- [ ] **Passo 6:** Commit `feat: add minimal soulslike hud`.

**Pronto quando:** os 4 testes passam e a captura confere.

---

# Fase 6 — Medição e teste

### T30: Modo automático e script de fps
**Nível:** médio · **Depende de:** T29

**Files:** Create `tools/measure_fps.sh`, `scripts/autoplay_input.gd` · Modify `scripts/main.gd` · Test `tests/test_autoplay.gd`

**Interfaces — Produces:**
- **`scripts/autoplay_input.gd`:** `static func make(start_ms: int) -> Callable`, que devolve um `Callable` de entrada com este comportamento:
  - `move` gira em círculo, com período de 4 s;
  - `attack` pulsa a cada 0,8 s;
  - `roll` pulsa a cada 3 s.
- **`main.gd`:** com `-- --autoplay` em `OS.get_cmdline_user_args()`, injeta esse `Callable` no `Player3D.input_source` e põe o inimigo para reaparecer 2 s depois de morrer.
- **`tools/measure_fps.sh <mobile|gl_compatibility>`:**
  - roda `godot --path . --rendering-method $1 --resolution 1920x1080 --print-fps --quit-after 1800 -- --autoplay`;
  - lê as linhas `Project FPS: N`, descarta os primeiros 5 s e imprime `renderer=<r> media=<x> minimo=<y>`.

**Passos:**
- [ ] **Passo 1:** Escrever `test_autoplay_varia`: amostrar o `Callable` em 0, 1, 2 e 3 s → as quatro direções de `move` são diferentes, e `attack` é verdadeiro em pelo menos uma amostra.
- [ ] **Passo 2:** Rodar e ver falhar.
- [ ] **Passo 3:** Implementar.
- [ ] **Passo 4:** Rodar e ver passar.
- [ ] **Passo 5:** Rodar `tools/measure_fps.sh mobile`. O esperado é uma linha no formato `renderer=mobile media=… minimo=…`.
- [ ] **Passo 6:** Commit `chore: add autoplay mode and fps measurement script`.

**Pronto quando:** o teste passa e o script imprime a linha de medição.

---

### T31: Escolher o renderizador e fazer a captura provisória
**Nível:** simples · **Depende de:** T30

**Files:** Modify `project.godot`, `context/decisoes.md`, `context/arquitetura.md` · Create `docs/capturas/2026-11-14-greybox.png` (ou a data do dia)

- [ ] **Passo 1:** Medir os dois renderizadores: `tools/measure_fps.sh mobile` e `tools/measure_fps.sh gl_compatibility`.
- [ ] **Passo 2:** Se nenhum chegar a média 60 com mínimo ≥ 50:
  1. pôr `rendering/scaling_3d/scale = 0.75` e `rendering/scaling_3d/mode = "fsr"`, e medir de novo;
  2. se ainda não chegar, desligar a sombra de `HeroLight` e medir de novo.

  Anotar cada medição.
- [ ] **Passo 3:** Fixar no `project.godot` o renderizador com melhor média que cumpra a meta. Registrar como `(i)` em `context/decisoes.md`, com todos os números medidos, e atualizar `context/arquitetura.md`.
- [ ] **Passo 4:** Fazer uma captura em 1080p com `--write-movie` e escolher o quadro mais legível. Salvá-lo em `docs/capturas/`.
- [ ] **Passo 5:** Rodar `tools/test.sh` e `python lint.py`.
- [ ] **Passo 6:** Commit `chore: pick renderer by measurement`.

**Pronto quando:** a decisão está registrada com os números e os testes e o lint passam.

Se nenhuma combinação chegar a 60 fps, registrar o melhor resultado em `context/achados.md` com severidade alta e deixar a T32 seguir mesmo assim, para Pedro decidir.

---

### T32: Pedro joga e escolhe a câmera (tarefa humana)
**Nível:** humano · **Depende de:** T31

- [ ] **Passo 1:** Pedro roda `godot --path /home/usuario/Dev/holding_agy/eldritch_depths_3d_20261114`.
  - Joga pelo menos 5 minutos com teclado e mouse e 5 minutos com o controle.
  - Alterna o enquadramento com F7 e afina o Véu com F9.
- [ ] **Passo 2:** O modelo que acompanha faz três perguntas e anota as respostas:
  - **(a)** Qual enquadramento: "atual" ou "próxima"?
  - **(b)** O que está ruim de controlar? (uma queixa por linha)
  - **(c)** A luz e a parede do Véu passam a ideia?
- [ ] **Passo 3:** Registrar:
  - a escolha da câmera como `(d)` em `context/decisoes.md`;
  - cada queixa como achado em `context/achados.md`, com severidade e a tarefa de origem (por exemplo, "esquiva curta demais → T19").
- [ ] **Passo 4:** Fixar o preset escolhido como padrão em `camera_rig_3d.gd` e ajustar o teste `test_preset_inicial` da T13.
- [ ] **Passo 5:** Rodar `tools/test.sh` e `python lint.py`.
- [ ] **Passo 6:** Commit `chore: lock camera framing chosen by playtest`.

**Pronto quando:** Pedro aprova o controle, a escolha está registrada como (d), e os testes e o lint passam.

As queixas viram tarefas novas no ledger (T33 em diante) antes de seguir.

---

**Fim do Bloco 1A.** O bloco está pronto quando os testes passam, a média chega a 60 fps em 1080p na máquina de Pedro e Pedro aprova o controle. O critério "bonito" e a captura definitiva de portfólio dependem da trilha de arte (Bloco 1B).
