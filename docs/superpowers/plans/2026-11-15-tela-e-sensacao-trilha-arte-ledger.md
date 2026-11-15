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
| B04 | Prova do pipeline — o braseiro | arte | B01, B02, B03 | feita | claude-opus-5-5 | 2026-11-15 | | [2026-11-15] geração passou para a API (Pedro: "aprovamdo"); a cota anônima de ZeroGPU está zerada. [Pedro] salvar um token de leitura do Hugging Face em `~/.cache/huggingface/token`; depois o Claude roda `tools/ia.sh flux.py` e segue. [2026-11-15] A conta do Hugging Face falhou ao ser criada (erro do servidor), mas Pedro gerou a imagem pela página → `art/brutos/2026-11-15-flux-braseiro.webp`, aprovada pelo Claude (4 pés em vez de 3 e sombra no chão; aceitável). ~superseded 2026-11-15: Pedro disse que o TRELLIS.2 "não está mais funcionando" e perguntou se o Claude faz o trabalho. [2026-11-15] Braseiro modelado por script (`art/props/braseiro/build.py`, 2.144 tri, 1 material, 1,14 m), `scenes/props/brazier.tscn`, dois na parede sul; 133 testes OK. Prancha para Pedro: https://claude.ai/artifact/NfKVQy1Zd7Uyh63BFGnE15. [Pedro] aprovar ou pedir ajustes; aprovado → copiar as prévias para `docs/arte/previas/braseiro/` ~superseded 2026-11-15: Pedro aprovou ("perfeito, pode seguir"); prévias e o recorte do jogo em `docs/arte/previas/braseiro/` |
| B05 | Conceito do Cavaleiro | arte | B01 | em andamento | claude-opus-5-5 | 2026-11-15 | 4268c92 | [Pedro] gera; portão. [2026-11-15] Prompts em `art/prompts/cavaleiro-conceito.md` (Qwen-Image-Edit, uma vista por geração; FLUX de reserva) e referência ampliada `art/referencias/cavaleiro-2d-1024.png`. [Pedro] gerar as três vistas pela página e salvar em `art/brutos/`. |
| B06 | Cavaleiro — malha limpa | arte | B04, B05, T32 (a) | livre | | | | [Pedro] gera 3D; portão |
| B07 | Cavaleiro — textura pintada | arte | B06 | livre | | | | portão |
| B08 | Espada longa | arte | B03, B05 | feita | claude-opus-5-5 | 2026-11-15 | | portão. [2026-11-15] `art/personagens/cavaleiro/build_espada.py` → `assets/models/personagens/espada.glb`: 558 tri, 1,30 m, 1 material 512², runas violeta emissivas no sulco; `test_espada` RED→GREEN; 134 testes OK. [Pedro] aprovar ou pedir ajustes ~superseded 2026-11-15: Pedro aprovou ("aprovado"); prévias em `docs/arte/previas/espada/`; commits 20e62c5..aa44231 |
| B09 | Cavaleiro — rig e animações | difícil | B07, B08 | livre | | | | [Pedro] confere a FAQ e opera o Mixamo |
| B10 | Cavaleiro no jogo | difícil | B09 | livre | | | | portão |
| B11 | Conceito do Cultista | arte | B01 | em andamento | claude-opus-5-5 | 2026-11-15 | 4268c92 | [Pedro] gera; portão. [2026-11-15] Prompts em `art/prompts/cultista-conceito.md` e referência `art/referencias/cultista-2d-1024.png`. [Pedro] gerar as três vistas pela página e salvar em `art/brutos/`. |
| B12 | Cultista — malha e textura | arte | B04, B11 | livre | | | | [Pedro] gera 3D; portão |
| B13 | Cultista — rig, animações e jogo | difícil | B10, B12 | livre | | | | [Pedro] opera o Mixamo; portão |
| B14 | Kit modular — peças | arte | B04, T32 (a) | livre | | | | portão |
| B15 | Sala do kit no jogo | médio | B14 | livre | | | | |
| B16 | Luz, acabamento e fecho | arte | B10, B13, B15 | livre | | | | |
| B17 | Pedro joga e aprova | — | B16 | livre | | | | só Pedro marca |

## Rulings

- [2026-11-15] B03: o plano pede `OK: 6 testes`; a suíte tem 9. Os 3 a mais cobrem `remesh_quadriflow`, `bake_color` e `join_meshes`, funções que as tarefas B05–B14 usam e que o plano não testava. Custo se errado: três testes a apagar.
- [2026-11-15] B03: no Blender, `subdivisions=1` já é o icosaedro (20 faces); a icosfera de 20.480 triângulos é `subdivisions=6`, não 5, e a de 320 é 3, não 2. Corrigi os testes depois do RED (o RED foi pelo módulo ausente, então a correção não mascara nada). O teste de assar a cor passou a usar vermelho puro (0,8; 0; 0) com limite 0,1 nos outros canais, porque o tom antigo saía com G e B próximos de 0,2 depois da conversão de cor. Custo se errado: nenhum no código, só nos números dos testes.
- [2026-11-15] B04: o Passo 2 era [Pedro] (gerar nos Spaces pela página); Pedro aprovou que o Claude gere pela API (`tools/ia/`, `gradio_client`), e o passo passa a ser do Claude, com Pedro só no portão. Os scripts de `tools/ia/` não têm teste automático porque só chamam um serviço externo e copiam o arquivo; a verificação é rodar e olhar a saída. Custo se errado: escrever um teste de leitura do prompt.
- [2026-11-15] B04: Ruling: o braseiro foi modelado por script no Blender (bacia em torno, pés em curva, materiais procedurais assados numa textura de cor e numa de brilho), com a imagem do FLUX só como referência, em vez de passar pelo TRELLIS.2 — o Space falhava e a cota grátis não existe sem conta, e Pedro perguntou se o Claude podia fazer — custo se errado: a prova da B04 não testou imagem → 3D por IA, que continua sem prova para os personagens (B06, B12); sugerir a Pedro testar a mesma imagem no Meshy grátis antes da B06.
- [2026-11-15] B04: Ruling: commit do braseiro antes do portão, com as prévias em `docs/arte/previas/braseiro/` só depois da aprovação — o trabalho tem testes verdes e vários modelos usam o repositório; deixar sem commit arrisca perder — custo se errado: um commit de ajuste se Pedro pedir mudanças.
- [2026-11-15] B04: Ruling: teste extra `test_cena_braseiro` (StaticBody3D na camada 1, cilindro de colisão, `FlameLight` na cor brasa e sem sombra), que o plano não pedia — prende o Produces da cena — custo se errado: nenhum.
- [2026-11-15] B05/B11: Ruling: o `hero.png` e o `cultist.png` têm 128 px; o Qwen-Image-Edit recebe uma ampliação Lanczos para 1024 px sobre cinza liso (`art/referencias/`), não o original — referência pequena demais perde capuz, máscara e runas — custo se errado: Pedro manda o original e compara.
- [2026-11-15] B05: Ruling: o prompt mantém a máscara de osso em forma de caveira que o `hero.png` mostra sob o capuz; o plano dizia "rosto na sombra". Fidelidade ao 2D manda (guia de estilo); o checklist do prompt deixa Pedro trocar antes de gerar — custo se errado: gerar a frente de novo.
- [2026-11-15] B08: Ruling: a espada foi feita antes da folha da B05 ser aprovada — a folha exclui a espada de propósito e a referência é a espada do `hero.png`, então nada da B05 muda a B08 — custo se errado: refazer proporções no script (minutos).
- [2026-11-15] B08: Ruling: o teste pede "origem dentro do AABB do cabo", mas o GLB é uma malha só, sem cabo separado; `test_espada` prende o mesmo contrato por fora: pomo entre 10 e 30 cm abaixo da origem e centro da caixa no eixo X/Z da origem (±2 cm) — custo se errado: uma espada com a origem fora do cabo mas dentro dessas folgas passaria.
- [2026-11-15] B08: Ruling: os ajudantes de geometria e de material do braseiro foram para `tools/blender/ed_modelagem.py`, usados pelo braseiro e pela espada; o braseiro reconstruído saiu byte a byte igual (mesmo sha256) — custo se errado: nenhum.
- [2026-11-15] B08: Ruling: commit antes do portão, como na B04 — custo se errado: um commit de ajuste.
