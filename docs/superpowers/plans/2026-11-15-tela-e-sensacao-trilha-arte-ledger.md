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
| B01 | Guia de estilo | arte | — | feita | claude-opus-5-5 | 2026-11-15 | f6152ae | [2026-11-15] Pedro viu a maquete das três direções (pintada, estilizada com contorno, realista sombria) e aprovou: "Podemos seguir com a opção A". Guia e paleta ficam como estão. T32 (a) segue em aberto. |
| B02 | Registro de origem e licenças | simples | — | feita | claude-opus-5-5 | 2026-11-15 | 706aa93 | OK: 131 testes; checagem em scripts/tools/assets_registry.gd (class_name AssetsRegistry); prova com arquivos falsos acusou os 2 e ignorou .import |
| B03 | Ferramentas do Blender por script | difícil | — | feita | claude-opus-5-5 | 2026-11-15 | dae8b44 | 9 testes em ~3,4 s; 4 vistas em 1024² levam ~28 s (Cycles na CPU) |
| B04 | Prova do pipeline — o braseiro | arte | B01, B02, B03 | aguarda Pedro | claude-opus-5-5 | 2026-11-15 | | [Pedro] gerar a imagem no FLUX.1 [schnell] e o modelo no TRELLIS.2 seguindo `art/prompts/braseiro.md`; salvar os dois em `art/brutos/` com os nomes do prompt |
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

- [2026-11-15] B03: o plano pede `OK: 6 testes`; a suíte tem 9. Os 3 a mais cobrem `remesh_quadriflow`, `bake_color` e `join_meshes`, funções que as tarefas B05–B14 usam e que o plano não testava. Custo se errado: três testes a apagar.
- [2026-11-15] B03: no Blender, `subdivisions=1` já é o icosaedro (20 faces); a icosfera de 20.480 triângulos é `subdivisions=6`, não 5, e a de 320 é 3, não 2. Corrigi os testes depois do RED (o RED foi pelo módulo ausente, então a correção não mascara nada). O teste de assar a cor passou a usar vermelho puro (0,8; 0; 0) com limite 0,1 nos outros canais, porque o tom antigo saía com G e B próximos de 0,2 depois da conversão de cor. Custo se errado: nenhum no código, só nos números dos testes.
