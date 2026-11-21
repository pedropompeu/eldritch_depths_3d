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
scenes/              main.tscn, player/, camera/, enemies/, world/, ui/, props/ (brazier.tscn)
```
- [2026-11-15] (e) `README.md` na raiz (T33), em português do Brasil: o que é o jogo, estado, requisitos, como rodar, controles, depuração, testes e onde está a documentação. A seção da história é um marcador `<!-- história: T34 -->` até a T34.

- [2026-11-20] (i) KitRoom (B15): `scenes/world/kit_room.tscn` (16 × 16, sala de 4 × 4 atrás da porta, coluna em (4, 0)); `scenes/world/kit/*.tscn`; `tools/gerar_kit_room.py`; `veil_wall.gd` pega a malha de `parede.glb` no `_ready()`; captura: `.godot/capturas_tmp/diag*`.

- [2026-11-15] (i) Trilha de arte (Bloco 1B, B03): `art/brutos/` guarda o material bruto das IAs (fora do Godot por `.gdignore`; arquivos `*.grande.*` fora do git); `assets/models/` guarda os `.glb` prontos que o Godot importa; `docs/arte/` tem o guia de estilo e a paleta; `tools/blender/` tem o kit `ed_blender.py`, o `report.py` e os testes (fora do Godot por `.gdignore`). Registro de origem e licença em `context/assets.md`.
- [2026-11-15] (i) Fluxo de uma peça: bruto em `art/brutos/<peça>/` → `build.py` da peça roda no Blender sem janela (`tools/blender.sh <script> -- <args>`) usando `ed_blender` (importar, juntar, remesh/decimate até o orçamento, UV, assar a cor, escala e origem nos pés) → `.glb` em `assets/models/` + quatro PNGs de pré-visualização → `report.py` confere orçamento e escala → linha nova em `context/assets.md`.
- [2026-11-15] (i) Geração por API (B04): `tools/ia/` tem os scripts que chamam os Spaces do Hugging Face pelo `gradio_client` (`flux.py`; fora do Godot por `.gdignore`), rodados por `tools/ia.sh <script> <args>` num venv isolado em `tools/ia/.venv/` (fora do git). Candidatos vão para `.godot/capturas_tmp/ia/<peça>/`; só o escolhido é copiado para `art/brutos/`. Token do Hugging Face: o salvo em `~/.cache/huggingface/token`, nunca no repositório.
- [2026-11-15] (i) Props modelados por script (B04): `art/props/<nome>/build.py` monta a peça no Blender sem bruto de IA (torno, curvas, primitivas), dá materiais procedurais por parte, junta, faz UV e assa cor e brilho numa malha de um material só; o conceito em `art/brutos/` fica como referência. O Godot extrai as texturas do `.glb` para `assets/models/props/<nome>_textura_*.png`, que também entram no `context/assets.md`. A cena do prop fica em `scenes/props/` (`StaticBody3D` + modelo + colisão + luz).
- [2026-11-15] (i) Acessórios e modelagem comum (B08): `tools/blender/ed_modelagem.py` reúne a geometria (torno, barra, anel, tora), os ajudantes de nós de material e `assar` (cor + brilho num material só), usados pelos scripts de props e de acessórios. Peças de personagem ficam em `art/personagens/<nome>/` (a espada: `art/personagens/cavaleiro/build_espada.py`) e saem em `assets/models/personagens/`. `art/referencias/` guarda as ampliações dos sprites 2D usadas como entrada dos geradores de imagem.
- [2026-11-15] (i) Folhas de conceito por blockout (B05/B11): `tools/blender/ed_conceito.py` tem as peças de blockout (segmento, casca aberta, grade com UV, espessura, materiais simples e de runas) e `render` (frente, lado, costas ortográficas e ¾ em perspectiva, fundo transparente, contorno Freestyle). Cada personagem tem seu `build_conceito.py` (`art/personagens/cavaleiro/`, `art/inimigos/cultista/`); renders em `.godot/capturas_tmp/<nome>_conceito/`; `tools/folha_conceito.py` (Python do sistema + Pillow) junta as vistas em `docs/arte/<nome>-conceito.png`. Inimigos ficam em `art/inimigos/<nome>/`. ~superseded 2026-11-15 → linha seguinte
- [2026-11-15] (i) Folhas de conceito por blockout, segunda versão (B05/B11): `tools/blender/ed_conceito.py` ganhou `acabamento` (pincelada larga, oclusão fria e realce de borda no lugar do contorno, que o guia não usa), `mao` (palma e dedos com falanges), `liso` (subdivisão) e pregas em `casca`/`manto`; `mat_runas` aceita `cor_barra` para deixar só as runas com brilho. `render` faz as vistas sem contorno e uma prova com a luz do jogo (fundo em breu, luz quente por cima e fio violeta atrás) em `jogo_frente.png` e `jogo_tres_quartos.png`. O resto do fluxo segue igual. ~superseded 2026-11-15 → linha seguinte
- [2026-11-15] (i) Folhas de conceito por blockout, terceira versão (B05b/B11b, realismo): `tools/blender/ed_conceito.py` ganhou `relevo` (mapa de normal e rugosidade procedurais por tipo: `couro`, `aco`, `pano`, `pele`, `osso`), o parâmetro `superficie` em `material` e `mat_runas` (este também com `faixas` e `sujeira`), pele com subsuperfície e película (`Coat`), `amassar` (subdivisão + deslocamento por nuvens, para dobras irregulares no pano), `booleana` (solver EXACT, usada no crânio do Cavaleiro) e `aplicar`. `render` usa céu em gradiente para os reflexos do metal (desligado na prova com a luz do jogo) e AgX "Medium High Contrast". O resto do fluxo segue igual.

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
- [2026-11-15] (e) Blender **4.5.15 LTS** (`/home/usuario/.local/bin/blender`; outro binário pela variável `BLENDER`). `tools/test_blender.sh` roda `tools/blender/tests/test_ed_blender.py` sem janela, no mesmo formato do runner do Godot (`OK: <n> testes` ou `FAIL ...` + `FALHOU: <x> de <n>`). Suíte de 9 testes em ~3,4 s; uma pré-visualização completa (4 vistas em 1024², Cycles na CPU, 32 amostras) leva ~28 s nesta máquina.
- [2026-11-15] (e) `gradio_client` **2.7.2** (Apache 2.0) no venv `tools/ia/.venv/`, Python 3.12; ferramenta de produção de arte, não entra no build do jogo. Recriar: `python3 -m venv tools/ia/.venv && tools/ia/.venv/bin/pip install gradio_client`.
- [2026-11-14] (e) `godot --headless --path . --quit` sai com código 1 quando não há cena principal; para só abrir o projeto, usar `--import`.

## Regras técnicas {#regras}

- [2026-11-14] (e) **Proibido `Engine.has_singleton("<Autoload>")`**: sempre retorna falso para autoloads (ver [[achados#has-singleton]]). Usar `Autoloads.get_autoload(&"Nome")`.
- [2026-11-14] (d) Código e comentários em português do Brasil; identificadores em inglês.
- [2026-11-14] (d) Commits em Conventional Commits, em inglês, sem `Co-Authored-By` nem menção à IA; `git push` só com ordem explícita de Pedro.
