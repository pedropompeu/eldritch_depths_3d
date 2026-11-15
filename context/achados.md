---
tipo: contexto
projeto: eldritch-depths-3d
descricao: Bugs, riscos e dívidas do Eldritch Depths 3D, com severidade, local, reprodução e fix.
estado: estavel
criado: 2026-11-14
relacionado:
  - context/arquitetura.md
---

# Achados

> Ler **antes de dizer que algo está pronto** ou de mexer em área crítica. Todo achado leva severidade (justificada pela consequência), onde, reprodução e fix. Achado resolvido não se apaga: ganha uma linha `Resolvido` com data.

## A01 · Verificação de autoload que sempre falha desliga integrações sem aviso {#has-singleton}

- [2026-11-14] (e) **Severidade:** alto — bônus de perks, saves disparados por perks e outras integrações ficam desligados em silêncio, e o jogador nunca recebe o que o jogo promete.
- [2026-11-14] (e) **Onde:** projeto 2D, 59 ocorrências de `Engine.has_singleton("<Autoload>")`; por exemplo `scripts/components/stats_component.gd:91` (`PerksManager`). Afeta todo código portado.
- [2026-11-14] (e) **Reprodução:** com a Godot 4.7.2, um script `--headless` que imprime `Engine.has_singleton("SaveManager")` dá `false` enquanto o nó `/root/SaveManager` existe.
- [2026-11-14] (i) **Fix:** no 3D, usar `Autoloads.get_autoload(&"Nome")` (T05 do plano) e checar `has_method` antes de chamar. `grep -rn has_singleton scripts/` deve voltar vazio.

## A02 · A arte pode não chegar ao nível da Steam e do portfólio {#risco-arte}

- [2026-11-14] (i) **Severidade:** alto — arte feia é anti-meta declarada por Pedro; se o pipeline falhar, o jogo funciona mas não serve a nenhum dos dois usos.
- [2026-11-14] (e) **Onde:** trilha de arte (Bloco 1B, plano próprio a escrever).
- [2026-11-14] (e) **Reprodução:** não é bug; vem das restrições — modelos 3D originais, Pedro nunca usou Blender, geração 3D por IA local exige NVIDIA (ausente nesta máquina), orçamento R$ 0.
- [2026-11-14] (i) **Fix / mitigação:** guia de estilo antes da produção em série; conceito do Cavaleiro aprovado por Pedro antes de modelar; prova do pipeline IA → Blender → Godot com uma peça pequena; pré-visualizações renderizadas a cada etapa. A trilha de jogo segue com provisórios para não esperar a arte.

## A03 · Teste que quebrava passava como aprovado {#runner-silencioso}

- [2026-11-14] (e) **Severidade:** alto — com vários modelos escrevendo testes, um teste com erro de script contava como aprovado e um script com erro de sintaxe travava a suíte para sempre; o `OK` deixava de significar alguma coisa.
- [2026-11-14] (e) **Onde:** `tests/run_tests.gd` (versão do commit `85efc13`, T02).
- [2026-11-14] (e) **Reprodução:** um `test_*.gd` com `var n = null; n.metodo()` dava `OK: 6 testes`; um com `func test_x(:` travava o runner (o `load` devolve o script, o `new()` falha e a função do runner aborta sem chamar `quit`).
- [2026-11-14] (i) **Fix:** `Logger` que converte erro da engine em falha, checagem `can_instantiate()` e vigia de 30 s por teste. Resolvido em 2026-11-14 — conferido com quatro testes temporários (erro de script, `push_error`, sintaxe, `await` eterno), todos reprovados; `push_warning` passou.

## A04 · Herói e câmera tremiam um contra o outro acima de 60 Hz {#interpolacao-fisica}

- [2026-11-15] (e) **Severidade:** médio — num monitor de 120 ou 144 Hz o herói treme contra o cenário a cada frame; é a primeira coisa que um jogador da demo vê.
- [2026-11-15] (e) **Onde:** `scripts/player/player_3d.gd` (anda no passo de física), `scripts/camera/camera_rig_3d.gd` (seguia em `_process`), `project.godot` (sem `physics/common/physics_interpolation`).
- [2026-11-15] (e) **Reprodução:** apontado pela revisão final do branch (intervalo `aebf5f5..9dd7507`); com física a 60 ticks/s e desenho a 144 Hz, o herói fica parado em 2 de cada 3 frames enquanto a câmera anda.
- [2026-11-15] (i) **Fix:** interpolação de física ligada e câmera no passo de física; o inimigo que reaparece chama `reset_physics_interpolation()`. Resolvido em 2026-11-15 (commit `2d0c524`, `test_camera.gd::test_interpolacao_de_fisica`). Não foi conferido num monitor acima de 60 Hz — fica para a T32.

## A05 · Suíte falhava com controle plugado {#teste-controle-plugado}

- [2026-11-15] (e) **Severidade:** médio — a T32 roda a suíte depois de jogar com controle; um teste vermelho por causa do hardware faz o `OK` deixar de significar alguma coisa (ver [A03](#runner-silencioso)).
- [2026-11-15] (e) **Onde:** `tests/test_input_mode.gd::test_desconexao_volta_kbm` exigia `Input.get_connected_joypads()` vazio.
- [2026-11-15] (e) **Reprodução:** rodar `tools/test.sh` com qualquer controle conectado.
- [2026-11-15] (i) **Fix:** `InputMode.connected_joypads` (Callable injetável, padrão `Input.get_connected_joypads`). Resolvido em 2026-11-15 (commit `8dcc9fe`).

## A06 · Travada no fim da esquiva ou do parry deixava o golpe passar {#travada-protecao}

- [2026-11-15] (e) **Severidade:** médio — num engasgo (carregamento, troca de janela), uma esquiva ou parry feitos no tempo certo levam o golpe mesmo assim; o jogador sente o jogo trapaceando.
- [2026-11-15] (e) **Onde:** `scripts/player/states/roll.gd` e `parry.gd`: o `exit()` desligava `invulnerable`/`parrying` no mesmo passo em que a ação terminava, antes de o frame processar os golpes.
- [2026-11-15] (e) **Reprodução:** `step(0.1)` e depois `step(0.3)` (esquiva) ou `step(0.35)` (parry) e um golpe ativado em seguida: o golpe entrava.
- [2026-11-15] (i) **Fix:** `Player3D.release_guard_next_step()`; a proteção desliga no começo do passo seguinte. Resolvido em 2026-11-15 (commit `af6e18c`, `test_travada_que_termina_a_esquiva`, `test_travada_que_termina_o_parry`).
