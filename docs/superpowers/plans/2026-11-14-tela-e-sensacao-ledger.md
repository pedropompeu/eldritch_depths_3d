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
| T03 | Mapa de controles | simples | T02 | feita | claude-opus-5-5 | 2026-11-14 | 8ba3f9c | OK: 5 testes; ver rulings sobre device -1 |
| T04 | context/, lint e documentos | simples | T01 | livre | | | | |
| T05 | Busca de autoload | simples | T02 | livre | | | | |
| T06 | Faixas do Véu | simples | T02 | livre | | | | |
| T07 | StatsComponent portado | médio | T05, T06 | livre | | | | |
| T08 | Máquina de estados | simples | T02 | livre | | | | |
| T09 | Matemática de movimento | simples | T02 | livre | | | | |
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
