# Ledger — Bloco 1B "Tela e sensação" (trilha de arte)

Plano: `docs/superpowers/plans/2026-11-15-tela-e-sensacao-trilha-arte.md`

## Como usar
- Status possíveis: `livre`, `em andamento`, `aguarda Pedro`, `feita` e `bloqueada`.
- **Antes de começar:** confira que todas as dependências estão `feita` (portões aprovados incluídos). Marque a tarefa como `em andamento`, preenchendo modelo e data, e faça commit (`docs: start B<nn>`).
- **Passo [Pedro]:** marque `aguarda Pedro` e escreva na nota, em uma linha, o que ele precisa fazer e onde salvar.
- **Portão:** só fica `feita` com a aprovação de Pedro por escrito; cole a frase dele entre aspas na nota, com a data. Cada rodada de mudança pedida vira uma nota nova.
- **Ao terminar:** marque `feita` e preencha o hash do commit e uma nota curta se algo surpreendeu.
- **Se travar:** marque `bloqueada`, explique em uma linha na nota e registre o problema em `context/achados.md`.
- **Nunca apague uma linha.** Se uma tarefa for refeita, acrescente uma linha nova, por exemplo `B06b`.

| Tarefa | Nome | Nível | Depende de | Status | Modelo | Data | Commit | Nota |
|---|---|---|---|---|---|---|---|---|
| B01 | Guia de estilo | arte | — | livre | | | | portão: Pedro aprova |
| B02 | Registro de origem e licenças | simples | — | livre | | | | |
| B03 | Ferramentas do Blender por script | difícil | — | livre | | | | |
| B04 | Prova do pipeline — o braseiro | arte | B01, B02, B03 | livre | | | | [Pedro] gera imagem e 3D; portão |
| B05 | Conceito do Cavaleiro | arte | B01 | livre | | | | [Pedro] gera; portão |
| B06 | Cavaleiro — malha limpa | arte | B04, B05, T32 (a) | livre | | | | [Pedro] gera 3D; portão |
| B07 | Cavaleiro — textura pintada | arte | B06 | livre | | | | portão |
| B08 | Espada longa | arte | B03, B05 | livre | | | | portão |
| B09 | Cavaleiro — rig e animações | difícil | B07, B08 | livre | | | | [Pedro] confere a FAQ e opera o Mixamo |
| B10 | Cavaleiro no jogo | difícil | B09 | livre | | | | portão |
| B11 | Conceito do Cultista | arte | B01 | livre | | | | [Pedro] gera; portão |
| B12 | Cultista — malha e textura | arte | B04, B11 | livre | | | | [Pedro] gera 3D; portão |
| B13 | Cultista — rig, animações e jogo | difícil | B10, B12 | livre | | | | [Pedro] opera o Mixamo; portão |
| B14 | Kit modular — peças | arte | B04, T32 (a) | livre | | | | portão |
| B15 | Sala do kit no jogo | médio | B14 | livre | | | | |
| B16 | Luz, acabamento e fecho | arte | B10, B13, B15 | livre | | | | |
| B17 | Pedro joga e aprova | — | B16 | livre | | | | só Pedro marca |

## Rulings

(nenhum ainda)
