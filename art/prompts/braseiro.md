# Prompt — braseiro (B04)

Primeira peça do Bloco 1B: prova o caminho IA → Blender → Godot com um prop pequeno antes do Cavaleiro. São duas gerações, nesta ordem: a imagem e depois o modelo 3D a partir dela.

**[2026-11-15] Pela API (decisão de Pedro):** o Claude roda as duas etapas por script, `tools/ia.sh flux.py art/prompts/braseiro.md .godot/capturas_tmp/ia/braseiro <seeds…>` para a imagem, e copia só a escolhida para `art/brutos/`. As configurações abaixo valem para os dois caminhos; o passo a passo pela página fica de reserva.

## 1. Imagem (FLUX.1 [schnell])

**Serviço:** Space `black-forest-labs/FLUX.1-schnell` — https://huggingface.co/spaces/black-forest-labs/FLUX.1-schnell (Apache 2.0, uso comercial liberado; ver `context/assets.md`).

**Prompt** (colar inteiro, em inglês):

```
A single standing iron brazier, game asset concept, isolated on a plain flat medium grey background. Hand-forged dark wrought iron bowl on three tall curved legs joined by a ring, riveted bands and small spikes along the rim, worn and slightly rusted. The bowl is filled with glowing orange embers and a low flame. Three-quarter view from slightly above, full object visible and centered, nothing cropped. Semi-realistic painterly dark fantasy style, broad soft brushstrokes, muted colors, dark grey-blue iron, warm orange glow only on the embers. Even soft studio lighting, no cast shadow on the floor, no text, no scenery.
```

O FLUX.1 [schnell] não tem campo de prompt negativo; o que ele não deve fazer já está no fim do prompt ("no cast shadow… no text, no scenery").

**Configurações:**
- Largura 1024, altura 1024.
- Passos (*inference steps*): 4, o padrão.
- Seed aleatória. Gere de 4 a 6 imagens e fique com a melhor.

**Salvar como:** `art/brutos/AAAA-MM-DD-flux-braseiro.png`, com a data do dia da geração (ex.: `2026-11-16-flux-braseiro.png`).

**Conferir antes de seguir:**
- [ ] O braseiro aparece inteiro, sem nada cortado, e sozinho no fundo cinza liso.
- [ ] Três pés e uma bacia legíveis; nenhum pé fundido no outro.
- [ ] Sem chão, parede, mesa, texto nem marca d'água.
- [ ] Cor perto do guia: ferro escuro azulado, laranja só nas brasas.

## 2. Modelo 3D (TRELLIS.2)

**Serviço:** Space `microsoft/TRELLIS.2` — https://huggingface.co/spaces/microsoft/TRELLIS.2 (MIT; ver `context/assets.md`).

**Como:**
1. Envie a imagem escolhida acima.
2. Deixe as configurações no padrão. Se o Space oferecer remover o fundo, deixe ligado.
3. Gere e olhe o modelo girando na pré-visualização. Se os pés saírem grudados ou a bacia furada, gere de novo com outra seed (até 3 vezes).
4. Na exportação para GLB, se houver opção de simplificação ou tamanho de textura, deixe o padrão: o Claude reduz a malha para o orçamento (≤ 3.000 triângulos) e refaz a textura no Blender.

**Salvar como:** `art/brutos/AAAA-MM-DD-trellis2-braseiro.glb`, com a mesma data da imagem.

**Conferir antes de mandar ao Claude:**
- [ ] O arquivo é `.glb` e abre na pré-visualização com cor (não só cinza).
- [ ] Três pés separados e a bacia fechada por baixo.
- [ ] Nada do fundo cinza virou parte do modelo (placa ou parede atrás).

## Se o TRELLIS.2 falhar

Se a malha sair inútil depois de 3 tentativas ou o Space ficar fora do ar por mais de um dia, use o Meshy grátis (imagem → 3D) com a mesma imagem e salve como `art/brutos/AAAA-MM-DD-meshy-braseiro.glb`. A saída do plano grátis é CC BY 4.0: a atribuição entra nos créditos do jogo, e o Claude anota o desvio no ledger.

## Depois

Avise o Claude com os nomes dos dois arquivos. Ele registra os brutos em `context/assets.md` (operador Pedro), roda `art/props/braseiro/build.py` e mostra as quatro pré-visualizações sob a luz do jogo para você aprovar.
