# Prompt — conceito do Cultista (B11)

Folha de conceito do inimigo em três vistas (frente, lado, costas), corpo inteiro, em pose A e sem a lâmina. Mesmo processo da B05 (`cavaleiro-conceito.md`).

**Referência:** `art/referencias/cultista-2d-1024.png`, o `cultist.png` do 2D (128 px) ampliado para 1024 px sobre cinza liso. Use esse arquivo, não o original de 128 px.

**O que o 2D mostra e o conceito mantém:** capuz pontudo carmim com o rosto em breu e dois olhos violeta brilhando; manto vinho e carmim aberto em sino, esfarrapado, com bordas laranja-ferrugem; sobremanto com padrão rúnico violeta e azul; contas violeta brilhando no peito; cinto de couro com medalhão violeta; tentáculos roxo-escuros com ventosas saindo por baixo da barra do manto. **Fica de fora:** a adaga curva serrilhada (vira a lâmina da B12) e a chama violeta na mão (efeito de jogo, não modelo).

**Os tentáculos** são forma do manto: grossos, curtos, curvados no chão em volta dos pés, sem articulação nem osso. No 3D eles vão junto da barra; o rig da B13 não os anima.

## 1. Caminho principal: Qwen-Image-Edit (uma geração por vista)

**Serviço:** Space `Qwen/Qwen-Image-Edit` — https://huggingface.co/spaces/Qwen/Qwen-Image-Edit (Apache 2.0; ver `context/assets.md`).

**Configurações:** as mesmas da B05. Entrada `art/referencias/cultista-2d-1024.png`; reescrita de prompt desligada; seed aleatória, de 3 a 4 por vista; frente primeiro e, se o Space aceitar várias imagens, a frente escolhida junto com a referência para o lado e as costas.

### Frente

```
Redraw this exact character as a clean full-body character turnaround view, FRONT view, facing the viewer. Same outfit, same colors, same proportions: tall pointed crimson hood with a pitch-black face and two glowing violet eyes, open bell-shaped wine-red and crimson robe with tattered rust-orange edges, inner robe with a violet and blue runic pattern, a row of glowing violet beads on the chest, leather belt with a violet medallion, thick dark purple tentacles with pale suckers curling out from under the robe hem onto the ground around the feet. Standing straight in an A-pose: arms held straight down and out at 45 degrees from the body, sleeves hanging, hands open and empty. Remove the curved dagger and remove the violet flame from the hand. Whole body visible from the tip of the hood to the tentacles on the ground, centered, nothing cropped. Plain flat medium grey background, even soft studio lighting, no cast shadow, no floor, no puddle, no particles, no text. Semi-realistic painterly dark fantasy style.
```

### Lado

```
Redraw this exact character as a clean full-body character turnaround view, SIDE view in strict profile, facing to the right of the image. Same outfit, same colors, same proportions: tall pointed crimson hood with a pitch-black face and one glowing violet eye visible, open bell-shaped wine-red and crimson robe with tattered rust-orange edges flaring out at the bottom, leather belt, thick dark purple tentacles with pale suckers curling out from under the robe hem onto the ground. Standing straight in an A-pose: arms held straight down and out at 45 degrees from the body, sleeves hanging, hands open and empty. No dagger, no flame, nothing in the hands. Whole body visible from the tip of the hood to the tentacles on the ground, centered, nothing cropped. Plain flat medium grey background, even soft studio lighting, no cast shadow, no floor, no puddle, no particles, no text. Semi-realistic painterly dark fantasy style.
```

### Costas

```
Redraw this exact character as a clean full-body character turnaround view, BACK view, seen from directly behind, face not visible. Same outfit, same colors, same proportions: back of the tall pointed crimson hood, wide bell-shaped wine-red and crimson robe with tattered rust-orange edges reaching the ground, thick dark purple tentacles with pale suckers curling out from under the robe hem onto the ground. Standing straight in an A-pose: arms held straight down and out at 45 degrees from the body, sleeves hanging, hands open and empty. No dagger, no flame. Whole body visible from the tip of the hood to the tentacles on the ground, centered, nothing cropped. Plain flat medium grey background, even soft studio lighting, no cast shadow, no floor, no puddle, no particles, no text. Semi-realistic painterly dark fantasy style.
```

**Salvar como** (mantendo a extensão que a página entregar), com a data do dia da geração:
- `art/brutos/AAAA-MM-DD-qwen-cultista-frente.png`
- `art/brutos/AAAA-MM-DD-qwen-cultista-lado.png`
- `art/brutos/AAAA-MM-DD-qwen-cultista-costas.png`

## 2. Reserva: FLUX.1 [schnell], só texto

Mesmas condições da B05 (Qwen fora do ar, ou 3 tentativas por vista sem tirar a lâmina ou acertar a pose). Largura 1536, altura 1024 se a página deixar, 4 passos, de 4 a 6 imagens.

```
Character turnaround reference sheet of one hooded eldritch cultist, three full-body views side by side at the same scale: front view, side profile view facing right, back view. Tall pointed crimson hood with a pitch-black face and two glowing violet eyes, open bell-shaped wine-red and crimson robe with tattered rust-orange edges, inner robe with violet and blue runes, glowing violet beads on the chest, leather belt with a violet medallion, thick dark purple tentacles with pale suckers curling out from under the robe hem onto the ground. A-pose in every view: arms straight down and out at 45 degrees, hands open and empty, no weapon, no magic. Plain flat medium grey background, even soft lighting, no cast shadow, no floor, no text, no labels. Semi-realistic painterly style, dark wine and crimson cloth, violet only as small glowing accents.
```

**Salvar como:** `art/brutos/AAAA-MM-DD-flux-cultista-folha.png`.

## Conferir antes de mandar ao Claude

- [ ] As três vistas são do mesmo personagem: mesmo capuz, mesmas cores, mesma largura de manto.
- [ ] Pose A nas três, mãos vazias; nem adaga, nem chama, nem fumaça violeta solta.
- [ ] Tentáculos saindo da barra, encostados no chão, sem virar pernas: os pés (ou a barra) continuam lá.
- [ ] Corpo inteiro, da ponta do capuz aos tentáculos, sem corte.
- [ ] Fundo cinza liso, sem poça, chão, sombra no chão ou texto.

## Depois

Avise o Claude com os nomes dos arquivos. Ele registra os brutos em `context/assets.md` (operador Pedro), monta `docs/arte/cultista-conceito.png` e mostra a folha para você aprovar.
