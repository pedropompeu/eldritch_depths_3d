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
| T10 | Modo de entrada | médio | T03, T05 | livre | | | | |
| T11 | Mira | médio | T02 | livre | | | | |
| T12 | Câmera: distância e seguimento | médio | T02 | livre | | | | |
| T13 | Enquadramentos | simples | T03, T12 | livre | | | | |
| T14 | Linha do tempo de ações | médio | T02 | livre | | | | |
| T15 | Hitbox e hurtbox 3D | difícil | T02 | livre | | | | |
| T16 | Postura | simples | T02 | livre | | | | |
| T17 | Herói: cena, parado e andar | difícil | T07–T11, T13, T15, T16 | livre | | | | |
| T18 | Ataque em dois golpes | difícil | T14, T17 | livre | | | | |
| T19 | Esquiva | difícil | T14, T17 | livre | | | | |
| T20 | Parry | médio | T17 | livre | | | | |
| T21 | Dano, morte e frascos | médio | T20 | livre | | | | |
| T22 | Inimigo: perseguição | médio | T07, T08, T15, T16 | livre | | | | |
| T23 | Inimigo: aviso, golpe e recarga | médio | T14, T22 | livre | | | | |
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
