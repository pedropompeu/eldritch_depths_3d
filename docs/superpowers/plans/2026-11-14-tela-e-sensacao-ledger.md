# Ledger — Bloco 1A "Tela e sensação" (trilha de jogo)

Plano: `docs/superpowers/plans/2026-11-14-tela-e-sensacao-trilha-jogo.md`

## Como usar
- Status possíveis: `livre`, `em andamento`, `feita` e `bloqueada`.
- **Antes de começar:** confira que todas as dependências estão `feita`. Marque a tarefa como `em andamento`, preenchendo modelo e data, e faça commit (`docs: start T<nn>`).
- **Ao terminar:** marque `feita` e preencha o hash do commit e uma nota curta se algo surpreendeu.
- **Se travar:** marque `bloqueada`, explique em uma linha na nota e registre o problema em `context/achados.md`.
- **Nunca apague uma linha.** Se uma tarefa for refeita, acrescente uma linha nova, por exemplo `T19b`.

| Tarefa | Nome | Nível | Depende de | Status | Modelo | Data | Commit | Nota |
|---|---|---|---|---|---|---|---|---|
| T01 | Pasta, git e project.godot | simples | — | feita | claude-opus-5-5 | 2026-11-14 | aebf5f5 | verificação via --import (ver rulings) |
| T02 | Runner de testes | médio | T01 | feita | claude-opus-5-5 | 2026-11-14 | 85efc13 | OK: 2 testes; prova de falha deu FALHOU: 1 de 2, código 1 |
| T02b | Runner reprova erro da engine e teste travado | médio | T02 | feita | claude-opus-5-5 | 2026-11-14 | 291fc4f | achado A03 |
| T03 | Mapa de controles | simples | T02 | feita | claude-opus-5-5 | 2026-11-14 | 8ba3f9c | OK: 5 testes; ver rulings sobre device -1 |
| T04 | context/, lint e documentos | simples | T01 | feita | claude-opus-5-5 | 2026-11-14 | 8ff2f4c | lint limpo; decisoes.md ganhou 2 (i) extras: plano em 32 tarefas e formato do [input] |
| T05 | Busca de autoload | simples | T02 | feita | claude-opus-5-5 | 2026-11-14 | 95426d6 | OK: 6 testes; teste usa get_node_or_null em vez de get_node (ver rulings) |
| T06 | Faixas do Véu | simples | T02 | feita | claude-opus-5-5 | 2026-11-14 | 862f575 | OK: 13 testes; teste extra da ordem das faixas |
| T07 | StatsComponent portado | médio | T05, T06 | feita | claude-opus-5-5 | 2026-11-14 | c2c80af | OK: 22 testes; esperado de test_sem_perks corrigido de 75 para 90 (ver rulings) |
| T08 | Máquina de estados | simples | T02 | feita | claude-opus-5-5 | 2026-11-14 | b1dbbd1 | OK: 15 testes; chave inexistente dá push_warning |
| T09 | Matemática de movimento | simples | T02 | feita | claude-opus-5-5 | 2026-11-14 | 7d0e957 | OK: 11 testes (5 novos) |
| T10 | Modo de entrada | médio | T03, T05 | feita | claude-opus-5-5 | 2026-11-14 | 0f7a176 | OK: 31 testes; 1 teste extra (tecla e clique voltam a KBM) |
| T11 | Mira | médio | T02 | feita | claude-opus-5-5 | 2026-11-14 | 4da0630 | OK: 43 testes; 3 testes extras (mouse sobre o herói, altura diferente, NaN) |
| T12 | Câmera: distância e seguimento | médio | T02 | feita | claude-opus-5-5 | 2026-11-14 | 6213f30 | OK: 47 testes; rig nasce em cima do alvo (ver rulings) |
| T13 | Enquadramentos | simples | T03, T12 | feita | claude-opus-5-5 | 2026-11-14 | 8bb36c3 | OK: 51 testes; teste extra do F7 via _unhandled_input |
| T14 | Linha do tempo de ações | médio | T02 | feita | claude-opus-5-5 | 2026-11-14 | a73da6d | OK: 56 testes; teste extra de is_in |
| T15 | Hitbox e hurtbox 3D | difícil | T02 | feita | claude-opus-5-5 | 2026-11-14 | 8fba6d9 | OK: 67 testes; 3 testes extras (inimigo acerta herói, entrar ativa, entrar inativa) |
| T16 | Postura | simples | T02 | feita | claude-opus-5-5 | 2026-11-14 | 4453290 | OK: 59 testes; escala invertida e sem espera de 2,2 s em relação ao 2D (ver rulings) |
| T17 | Herói: cena, parado e andar | difícil | T07–T11, T13, T15, T16 | feita | claude-opus-5-5 | 2026-11-14 | 5b521c9 | 4 testes; cena roda sem avisos |
| T18 | Ataque em dois golpes | difícil | T14, T17 | feita | claude-opus-5-5 | 2026-11-14 | d77e066 | 4 testes; suíte 75 |
| T19 | Esquiva | difícil | T14, T17 | feita | claude-opus-5-5 | 2026-11-14 | 9b13cb5 | 4 testes; suíte 79 |
| T20 | Parry | médio | T17 | feita | claude-opus-5-5 | 2026-11-14 | 5ec3a2a | 3 testes; suíte 82 |
| T21 | Dano, morte e frascos | médio | T20 | feita | claude-opus-5-5 | 2026-11-14 | cf08433 | OK: 86 testes |
| T22 | Inimigo: perseguição | médio | T07, T08, T15, T16 | feita | claude-opus-5-5 | 2026-11-14 | 5a1caf8 | OK: 91 testes |
| T23 | Inimigo: aviso, golpe e recarga | médio | T14, T22 | feita | claude-opus-5-5 | 2026-11-14 | 59cd72c | OK: 97 testes |
| T24 | Inimigo: atordoado e morte | médio | T23 | livre | | | | |
| T25 | Sala cinza, luz e main | médio | T21, T24 | livre | | | | |
| T26 | Parede do Véu | difícil | T06, T25 | livre | | | | |
| T27 | Vinheta e tecla de depuração | médio | T26 | livre | | | | |
| T28 | Rótulos de botão | simples | T10 | livre | | | | |
| T29 | HUD mínimo | médio | T25, T28 | livre | | | | |
| T30 | Modo automático e fps | médio | T29 | livre | | | | |
| T31 | Renderizador e captura | simples | T30 | livre | | | | |
| T32 | Pedro joga e escolhe a câmera | humano | T31 | livre | | | | |

## Decisões de execução (rulings)
Formato: `- [data] T<nn> · modelo · <o que foi decidido> — <por quê> — <custo se estiver errado>`

- [2026-11-14] T01 · claude-opus-5-5 · Verificação trocada de `--quit` para `--import` (plano corrigido) — sem cena principal, `--quit` tenta rodar o jogo e sai com código 1 — nenhum.
- [2026-11-14] T01–T04 · claude-opus-5-5 · Sem commits `docs: start T<nn>` — as quatro tarefas rodaram em sequência numa sessão só, sem outro modelo em paralelo — nenhum.
- [2026-11-14] T03 · claude-opus-5-5 · `[input]` gerado por script com `ProjectSettings.save()`, com `device = -1` em todo evento, e teclas por `physical_keycode` — escrever à mão é frágil; sem `-1` o controle só valeria no dispositivo 0; tecla física deixa WASD no lugar em qualquer layout (ABNT2 incluso) — se alguém editar no editor, o editor mantém o formato.
- [2026-11-14] T03 · claude-opus-5-5 · Ao salvar, a Godot removeu `run/main_scene=""` e `physics/common/physics_ticks_per_second=60` por serem o padrão — comportamento idêntico; a T25 grava `run/main_scene` — nenhum.
- [2026-11-14] T04 · claude-opus-5-5 · `context/decisoes.md` recebeu duas `(i)` além das três pedidas (plano em 32 tarefas com ledger; mapa de entrada com tecla física e `device = -1`) — são decisões técnicas já tomadas que um modelo novo precisa achar em `context/` — nenhum.
- [2026-11-14] T04 · claude-opus-5-5 · A partir daqui, a cópia canônica do plano, da spec e do ledger é a do projeto 3D; as do projeto 2D são históricas — evita duas versões vivas — se alguém editar a do 2D, a mudança se perde.
- [2026-11-14] T02b · claude-opus-5-5 · Runner endurecido depois da T04 (commit 291fc4f): erro da engine durante o teste vira falha, script que não instancia reprova na carga, vigia de 30 s por teste — sem isso um teste quebrado passava e um erro de sintaxe travava a suíte (achado A03) — teste que usa `push_error` de propósito agora reprova; usar `push_warning`.
- [2026-11-14] T05 · claude-opus-5-5 · O teste busca `/root/Autoloads` com `get_node_or_null` e checa nulo antes, em vez do `get_node` do plano — com `get_node`, a ausência do autoload virava erro de script e o teste parava antes do assert; agora falha com mensagem clara — nenhum.
- [2026-11-14] T05 e T09 · claude-opus-5-5 · Sem commits `docs: start T<nn>` — feitas em sequência numa sessão só, sem outro modelo em paralelo — nenhum.
- [2026-11-14] T08 · claude-opus-5-5 · `transition_to(String)` do 2D virou `change_state(StringName)` (contrato da T08) e o `@export var initial_state` do 2D ficou como opcional: sem ele, `init` entra no primeiro estado filho — mantém o contrato e deixa a cena escolher outro estado inicial sem código — se alguém preencher `initial_state` por engano, a máquina começa em outro estado.
- [2026-11-14] T06–T16 · claude-opus-5-5 · Sem commits `docs: start T<nn>` — feitas em sequência numa sessão só, sem outro modelo em paralelo — nenhum.
- [2026-11-14] T07 · claude-opus-5-5 · Em `test_sem_perks_manager_nao_quebra`, o esperado virou 90 em vez de 75 (plano corrigido) — o código do 2D, que a T07 manda portar sem mudar padrões, desconta o atraso e regenera no mesmo frame com o delta inteiro: 50 + 25 × 0,6 + 25 × 1,0 = 90; 75 só sairia mudando a regra de regeneração — se Pedro quiser que o atraso "coma" o frame, é uma mudança de comportamento a decidir com ele (diferença de no máximo um frame de regeneração a 60 fps).
- [2026-11-14] T12 · claude-opus-5-5 · No `_ready`, o rig salta para a posição do alvo e `distance` começa no enquadramento 1/13 — sem isso, a câmera faria uma varredura desde a origem ao abrir a cena; a T13 troca a distância inicial pelo preset — se Pedro quiser uma entrada animada da câmera, é só tirar o salto.
- [2026-11-14] T16 · claude-opus-5-5 · Postura segue o contrato da T16, não o 2D: começa em 0 e enche até quebrar (no 2D começava cheia e caía), recupera sem a espera de 2,2 s depois do dano e volta a 0 depois da quebra (no 2D voltava a 65%); retícula visual e som do `AudioManager` ficaram de fora — as tarefas do inimigo (T22–T24) consomem esse contrato; a retícula é visual de outro bloco — sem a espera, a postura do inimigo esvazia logo entre golpes e quebrá-la exige pressão contínua; Pedro ajusta jogando na T32.
- [2026-11-14] T15 · claude-opus-5-5 · Hurtbox invulnerável no momento do contato entra na lista de atingidas da ativação, e `hit_landed` só sai quando o golpe pega de fato — assim a esquiva escapa do golpe inteiro, e não só do começo dele, e o dono da hitbox não conta acerto em quem desviou — se Pedro quiser que um golpe longo pegue quem sai da esquiva no meio, é tirar o `append` antes do teste de invulnerabilidade.
- [2026-11-14] T15 · claude-opus-5-5 · Hitbox fica sempre com `monitoring = true` e filtra por `active`; hurtbox tem `monitoring = false` e `collision_mask = 0` — ligar e desligar `monitoring` exige `set_deferred` e faria perder o contato do mesmo frame — nenhum.
- [2026-11-14] T17 · claude-opus-5-5 · `move` só volta a `idle` quando a velocidade horizontal zera (< 0,01 m/s); a frenagem acontece em `move` — é a leitura literal de "idle com velocidade zero" — custo se errado: troca de uma condição em `move.gd`.
- [2026-11-14] T17 · claude-opus-5-5 · Além do contrato, o `Player3D` expõe `input` (entrada do passo), `walk(delta)`, `face(dir)`, `horizontal_speed()` e `is_pad()` para os estados da T18–T20; campos ausentes no dicionário injetado caem no valor vazio — evita cada estado repetir a física e os testes de montar o dicionário inteiro — custo se errado: renomear helpers.
- [2026-11-14] T17 · claude-opus-5-5 · Valores que o plano não fixa: raio do mouse sai da câmera atual da viewport (no jogo, a do rig); hurtbox cápsula r 0,4 m × 1,8 m; espada e corpo centrados a 0,9 m de altura; seta de mira cone de 0,6 m a 0,9 m dos pés — custo se errado: ajuste na cena, sem código.
- [2026-11-14] T18 · claude-opus-5-5 · Quem decide se o ataque sai é o próprio estado (`attack.try_begin()`, chamado por `idle`/`move` via `Player3D.try_attack()`): gasta o vigor antes de trocar de estado, então sem vigor nada muda — mantém custo e combo num arquivo só — custo se errado: mover a checagem.
- [2026-11-14] T18 · claude-opus-5-5 · A janela de combo é só a recuperação, sem guardar o aperto feito no preparo ou na fase ativa; apertar na recuperação do golpe 2 encadeia o golpe 1 (18 de vigor) — leitura literal do plano — custo se errado: se o combo parecer duro no teste de Pedro (T32), acrescentar um buffer de entrada.
- [2026-11-14] T19 · claude-opus-5-5 · O teste de travada conta os sinais `Hurtbox.hurt` (0 durante a esquiva) e tem um controle (o mesmo golpe acerta o herói parado), porque "vida continua 100" passaria sem esquiva nenhuma: até a T20 nada aplica dano no herói. O golpe é ativado logo depois do passo de 0,22 s, que é a ordem do frame no jogo (o herói marca a invencibilidade antes de os golpes chegarem) — custo se errado: nenhum no código; só o teste é mais exigente que o plano.
- [2026-11-14] T19 · claude-opus-5-5 · A esquiva sai só de `idle` e `move` (não cancela o ataque), tem direção fixa ao começar e mantém 10,4 m/s até o fim, sem frear; ao sair, `move`/`idle` freiam com `DECEL` — o plano não fala em cancelar ataque nem em curva de velocidade — custo se errado: se Pedro quiser cancelar a recuperação do ataque com esquiva (comum em soulslike), é uma checagem em `attack.gd`.
- [2026-11-14] T20 · claude-opus-5-5 · A janela do parry segue o mesmo esquema da esquiva: `parrying` liga já no `enter` (vale golpe no frame do aperto) e, a cada passo, é marcado pelo intervalo do frame inteiro antes de os golpes chegarem; no parry o herói freia até parar e encara a mira — o plano não diz se o herói anda no parry — custo se errado: trocar o `walk(delta, 0.0)` por outra escala.
- [2026-11-14] T20 · claude-opus-5-5 · O `PostureComponent` de quem bateu é o primeiro filho desse tipo em `hitbox.source`; a troca para `hurt` só acontece se o estado existir e o herói ainda estiver vivo, para não gerar aviso até a T21 e não disputar com `dead` — custo se errado: a T21 pode trocar a busca por um campo explícito.
- [2026-11-14] T20 · claude-opus-5-5 · `test_esquiva_invencivel_com_travada` (T19) passou a comparar a vida com a de logo antes da esquiva, porque o golpe de controle agora tira 20 de vida de verdade — o que o teste prova (nenhum golpe novo na invencibilidade) não muda — custo se errado: nenhum.
- [2026-11-14] T21 · claude-opus-5-5 · Empurrão do `hurt` em velocidade constante (0,5 m / 0,3 s = 1,67 m/s), direção de `hitbox.source` (ou da própria hitbox) até o herói; um golpe novo no meio recomeça o `hurt` — o brief só fixa distância e duração — custo se errado: troca da curva do empurrão, só em `hurt.gd`.
- [2026-11-14] T21 · claude-opus-5-5 · Frascos valem em idle, move, attack, roll e parry (só `hurt` e `dead` bloqueiam), consumidos em `step()` antes da máquina de estados — o brief diz "fora de hurt e dead" — custo se errado: o teste de Pedro (T32) pode pedir bloqueio no ataque/esquiva; ajuste de uma linha em `_use_flasks`.
- [2026-11-14] T21 · claude-opus-5-5 · Golpe em herói morto é ignorado em `_on_hurt` (nem dano, nem sanidade); `hero_died` é emitido por `Stats.died`, que só dispara uma vez — custo se errado: nenhum visível na demo.
- [2026-11-14] T21 · claude-opus-5-5 · Teste da T19 (`test_esquiva_invencivel_com_travada`) espera 0,35 s depois do golpe de controle, porque o `hurt` ignora a entrada — custo se errado: nenhum, só o teste.
- [2026-11-14] T22 · claude-opus-5-5 · Corpo do inimigo na camada 3 com máscara só do mundo (1), como o herói: não se empurram fisicamente — o brief não fixa — custo se errado: inimigo e herói se atravessam; trocar a máscara para 1|2 na cena.
- [2026-11-14] T22 · claude-opus-5-5 · Perseguição sem aceleração (velocidade = `move_speed` já no primeiro passo), inimigo vira para o alvo também parado no alcance; `chase` volta a `idle` quando o alvo sai da detecção; distância medida no plano XZ — o brief só pede "≈ 2,4" e "linha reta" — custo se errado: sensação de arranque seco; ajuste em `chase.gd`.
- [2026-11-14] T22 · claude-opus-5-5 · Material do corpo dentro da `CapsuleMesh`, com malha e material `resource_local_to_scene` (cada instância tem o seu), e não em `surface_material_override`, que dá erro no renderizador vazio do modo headless — custo se errado: nenhum; teste extra `test_material_proprio_por_inimigo` (verificado quebrando a cena) e `test_sem_alvo_fica_parado` além dos 3 do brief.
- [2026-11-14] T22 · claude-opus-5-5 · Valores não fixados: cápsula r0,35 / h1,6 (hurtbox r0,4), garra caixa 1×1×1,2 a 0,8 m à frente e 0,8 m de altura, cor (0,12; 0,1; 0,16) — custo se errado: só ajuste visual/alcance na T23.
- [2026-11-14] T23 · claude-opus-5-5 · Garra ativada na entrada do `attack` (acerta na hora quem já está sobreposto) e desligada na saída; durações contadas por soma de `delta` com folga de 0,0001 s; inimigo parado (velocidade horizontal zero) em `telegraph`, `attack` e `cooldown` — o brief só fixa as durações — custo se errado: golpe sem avanço; ajuste nos estados.
- [2026-11-14] T23 · claude-opus-5-5 · O ciclo começa dois passos depois do alvo entrar no alcance partindo de `idle` (idle→chase→telegraph): a máquina de estados troca um estado por passo; os testes usam `_ate_avisar` — custo se errado: 1/60 s de atraso, invisível.
- [2026-11-14] T23 · claude-opus-5-5 · `test_para_no_alcance` (T22) passa a esperar `Telegraph` em vez de `Chase`, como a própria T23 anuncia; testes extras `test_aviso_brilha_vermelho` e `test_nao_gira_depois_do_aviso` além dos 4 do brief — custo se errado: nenhum, só testes.
- [2026-11-14] T23 · claude-opus-5-5 · O brilho do aviso só liga/desliga `emission_enabled` no material local do corpo (cor e energia ficam gravadas depois do primeiro aviso) — custo se errado: nenhum visível.
