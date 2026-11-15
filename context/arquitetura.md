---
tipo: contexto
projeto: eldritch-depths-3d
descricao: Stack, estrutura de pastas, camadas de colisão, testes e regras técnicas do projeto 3D.
estado: estavel
criado: 2026-11-14
relacionado:
  - context/achados.md
---

# Arquitetura

## Stack {#stack}

- [2026-11-14] (e) Godot **4.7.2** (`/home/usuario/.local/bin/godot`), GDScript, git (branch `main`).
- [2026-11-14] (i) Renderizador **`mobile` provisório**; a T31 do plano mede `mobile` contra `gl_compatibility` e fixa o melhor. Meta: 60 fps em 1080p no vídeo integrado. ~superseded 2026-11-14 → `decisoes.md`: `mobile` fixado por medição na T31.
- [2026-11-14] (i) Renderizador **`mobile`** fixado por medição (T31; números em `decisoes.md`): média 60 com vsync nos dois renderizadores, `mobile` com mais folga sem vsync (403,7 contra 387,2 fps). Captura provisória em `docs/capturas/2026-11-14-greybox.png`.
- [2026-11-14] (e) Janela base 1920×1080, stretch `canvas_items` / `expand`, física a 60 ticks/s.
- [2026-11-15] (e) Interpolação de física ligada (`physics/common/physics_interpolation=true`); herói, inimigo e câmera andam no passo de física. Nó teletransportado chama `reset_physics_interpolation()` depois de mudar a posição.
- [2026-11-14] (d) Remoto `origin` em https://github.com/pedropompeu/eldritch_depths_3d (branch `main`), criado por Pedro; primeiro push em 2026-11-14 por ordem dele.
- [2026-11-14] (d) **Nenhum addon.** Toda dependência nova passa por Pedro antes. Os addons `phantom_camera` e `limboai` do 2D só funcionam em 2D e não vêm.
- [2026-11-14] (i) Do 2D vêm só `StatsComponent`, `PostureComponent` e a máquina de estados, generalizados; jogador, inimigo, câmera e mundo são escritos do zero.

## Estrutura de pastas {#pastas}

- [2026-11-14] (i) Estrutura prevista pelo plano do Bloco 1A:

```
project.godot  .gitignore  lint.py
tools/test.sh  tools/measure_fps.sh
context/  docs/superpowers/{specs,plans}/  docs/capturas/
tests/run_tests.gd  tests/test_case.gd  tests/test_*.gd
scripts/core/        autoloads.gd, input_mode.gd
scripts/components/  stats_component.gd, veil.gd
scripts/state_machine/  state.gd, state_machine.gd
scripts/player/      player_motion.gd, aim_resolver.gd, player_3d.gd, states/
scripts/combat/      action_timeline.gd, hitbox_3d.gd, hurtbox_3d.gd, posture_component.gd
scripts/camera/      camera_rig_3d.gd
scripts/enemies/     enemy_common.gd, states/
scripts/world/       veil_wall.gd
scripts/ui/          hud_minimal.gd, input_prompt.gd
scripts/main.gd  scripts/autoplay_input.gd  shaders/veil_vignette.gdshader  shaders/veil_dissolve.gdshader
scenes/              main.tscn, player/, camera/, enemies/, world/, ui/
```
- [2026-11-15] (e) `README.md` na raiz (T33), em português do Brasil: o que é o jogo, estado, requisitos, como rodar, controles, depuração, testes e onde está a documentação. A seção da história é um marcador `<!-- história: T34 -->` até a T34.

## Camadas de colisão {#colisao}

- [2026-11-14] (i) Tabela usada por todas as cenas:

| Camada | Uso |
|---|---|
| 1 | mundo |
| 2 | corpo do herói |
| 3 | corpo dos inimigos |
| 4 | hitbox do herói (detecta 7) |
| 5 | hitbox dos inimigos (detecta 6) |
| 6 | hurtbox do herói |
| 7 | hurtbox dos inimigos |

## Unidades {#unidades}

- [2026-11-14] (i) **1 m = 27 px do 2D.** Andar 5,0 m/s; esquiva 10,4 m/s; inimigo 2,4 m/s; alcance do inimigo 1,5 m; detecção 6,7 m.

## Controles {#controles}

- [2026-11-14] (e) Mapa de entrada em `project.godot` `[input]`: move_*, aim_*, attack, roll, parry, spell_cosmic, use_blood_flask, use_laudanum, interact, debug_sanity_drop (F9), debug_camera_preset (F7). Deadzone 0,2 em todas.
- [2026-11-14] (i) Teclas por `physical_keycode` (WASD fica no lugar em qualquer layout, ABNT2 incluso) e todo evento com `device = -1` (qualquer controle).

## Testes {#testes}

- [2026-11-14] (i) Runner caseiro, sem GUT: `tools/test.sh` importa o projeto e roda `res://tests/run_tests.gd`. Sucesso termina em `OK: <n> testes`, código 0; falha imprime `FAIL <arquivo>::<método>: <msg>` e `FALHOU: <f> de <n>`, código 1.
- [2026-11-14] (i) Cada `tests/test_*.gd` estende `TestCase` (`assert_eq`, `assert_near`, `assert_true`, `assert_false`, `assert_vec_near`); método `test_*` com 1 argumento recebe a `SceneTree`.
- [2026-11-14] (i) O runner conta como falha todo erro da engine logado durante o teste (via `Logger` em `OS.add_logger`; `push_warning` não conta), reprova script que não instancia e interrompe a suíte se um teste passar de 30 s. `tools/test.sh` ainda tem `timeout 900` como última rede.
- [2026-11-14] (e) `godot --headless --path . --quit` sai com código 1 quando não há cena principal; para só abrir o projeto, usar `--import`.

## Regras técnicas {#regras}

- [2026-11-14] (e) **Proibido `Engine.has_singleton("<Autoload>")`**: sempre retorna falso para autoloads (ver [[achados#has-singleton]]). Usar `Autoloads.get_autoload(&"Nome")`.
- [2026-11-14] (d) Código e comentários em português do Brasil; identificadores em inglês.
- [2026-11-14] (d) Commits em Conventional Commits, em inglês, sem `Co-Authored-By` nem menção à IA; `git push` só com ordem explícita de Pedro.
