# Prompt — conceito do Cavaleiro (B05)

Folha de conceito do herói em três vistas (frente, lado, costas), corpo inteiro, em pose A e sem a espada. É ela que o gerador 3D (B06) e o auto-rig do Mixamo (B09) vão receber, então a pose e o fundo importam tanto quanto o desenho.

**Referência:** `art/referencias/cavaleiro-2d-1024.png`, o `hero.png` do 2D (128 px) ampliado para 1024 px sobre cinza liso. Use esse arquivo, não o original de 128 px.

**O que o 2D mostra e o conceito mantém:** capuz marrom fundo com máscara de osso em forma de caveira na sombra, gema violeta na testa e no peito; ombreiras e manoplas de placa de aço escuro; casaco longo de couro marrom aberto na frente, com cravos violeta na barra; tabardo central cinza-prata com padrão rúnico; cinto de couro com fivela e bolsas; capa escura esfarrapada pendendo das costas; grevas e botas de placa.

## 1. Caminho principal: Qwen-Image-Edit (uma geração por vista)

**Serviço:** Space `Qwen/Qwen-Image-Edit` — https://huggingface.co/spaces/Qwen/Qwen-Image-Edit (Apache 2.0; ver `context/assets.md`).

**Configurações (as três vistas):**
- Imagem de entrada: `art/referencias/cavaleiro-2d-1024.png`. A saída sai quadrada, 1024 × 1024, o que já dá a altura mínima de 1024 px.
- Se houver opção de reescrever o prompt (*rewrite prompt* / *prompt enhance*), **desligue**: ela troca as instruções de pose e fundo.
- Demais campos no padrão. Seed aleatória; gere de 3 a 4 por vista e fique com a melhor.
- Faça a **frente primeiro**. Se o Space aceitar mais de uma imagem de entrada, mande a frente escolhida junto com a referência ao gerar o lado e as costas: ajuda a manter as mesmas roupas e proporções.

### Frente

```
Redraw this exact character as a clean full-body character turnaround view, FRONT view, facing the viewer. Same outfit, same colors, same proportions: deep brown hood casting shadow over a pale bone skull mask, small violet gem on the forehead and one on the chest, dark steel plate pauldrons and gauntlets, long open brown leather coat with small violet studs along the hem, central silver-grey tabard with an engraved runic pattern, leather belt with buckle and pouches, tattered dark cape hanging behind, steel greaves and armored boots. Standing straight in an A-pose: arms held straight down and out at 45 degrees from the body, hands open and empty, palms facing the thighs, feet shoulder-width apart, head looking straight ahead. Remove the sword completely. Whole body visible from the top of the hood to the soles of the boots, centered, nothing cropped. Plain flat medium grey background, even soft studio lighting, no cast shadow, no floor, no particles, no glow effects, no text. Semi-realistic painterly dark fantasy style.
```

### Lado

```
Redraw this exact character as a clean full-body character turnaround view, SIDE view in strict profile, facing to the right of the image. Same outfit, same colors, same proportions: deep brown hood casting shadow over a pale bone skull mask, dark steel plate pauldrons and gauntlets, long open brown leather coat with small violet studs along the hem, silver-grey tabard, leather belt with pouches, tattered dark cape hanging behind the back, steel greaves and armored boots. Standing straight in an A-pose: arms held straight down and out at 45 degrees from the body, hands open and empty, feet shoulder-width apart. Remove the sword completely. Whole body visible from the top of the hood to the soles of the boots, centered, nothing cropped. Plain flat medium grey background, even soft studio lighting, no cast shadow, no floor, no particles, no glow effects, no text. Semi-realistic painterly dark fantasy style.
```

### Costas

```
Redraw this exact character as a clean full-body character turnaround view, BACK view, seen from directly behind, face not visible. Same outfit, same colors, same proportions: back of the deep brown hood, dark steel plate pauldrons, long tattered dark cape hanging from the shoulders down to the calves, brown leather coat visible at the sides, leather belt, steel greaves and armored boots. Standing straight in an A-pose: arms held straight down and out at 45 degrees from the body, hands open and empty, feet shoulder-width apart. Remove the sword completely. Whole body visible from the top of the hood to the soles of the boots, centered, nothing cropped. Plain flat medium grey background, even soft studio lighting, no cast shadow, no floor, no particles, no glow effects, no text. Semi-realistic painterly dark fantasy style.
```

**Salvar como** (mantendo a extensão que a página entregar, `.png` ou `.webp`), com a data do dia da geração:
- `art/brutos/AAAA-MM-DD-qwen-cavaleiro-frente.png`
- `art/brutos/AAAA-MM-DD-qwen-cavaleiro-lado.png`
- `art/brutos/AAAA-MM-DD-qwen-cavaleiro-costas.png`

## 2. Reserva: FLUX.1 [schnell], só texto

Use se o Qwen-Image-Edit estiver fora do ar ou insistir em manter a espada ou a pose do 2D depois de 3 tentativas por vista.

**Serviço:** Space `black-forest-labs/FLUX.1-schnell` — https://huggingface.co/spaces/black-forest-labs/FLUX.1-schnell (Apache 2.0). Largura 1536, altura 1024 se a página deixar (senão 1024 × 1024), 4 passos, seed aleatória, de 4 a 6 imagens.

```
Character turnaround reference sheet of one dark fantasy knight, three full-body views side by side at the same scale: front view, side profile view facing right, back view. Deep brown hood shadowing a pale bone skull mask, small violet gem on the forehead and chest, dark steel plate pauldrons and gauntlets, long open brown leather coat with violet studs along the hem, silver-grey tabard with engraved runes, leather belt with pouches, tattered dark cape, steel greaves and armored boots. A-pose in every view: arms straight down and out at 45 degrees, hands open and empty, feet shoulder-width apart, no weapon. Plain flat medium grey background, even soft lighting, no cast shadow, no floor, no text, no labels. Semi-realistic painterly style, muted colors, dark steel, brown leather, violet only as small accents.
```

**Salvar como:** `art/brutos/AAAA-MM-DD-flux-cavaleiro-folha.png`. O Claude recorta as três vistas.

## Conferir antes de mandar ao Claude

- [ ] As três vistas são do mesmo personagem: mesmas roupas, mesmas cores, mesmo tamanho de capuz e capa.
- [ ] Pose A nas três: braços retos a uns 45°, mãos abertas e vazias, pernas um pouco afastadas. Nada de mão no cabo, braço dobrado ou capa cobrindo os braços.
- [ ] Nenhuma espada (nem bainha) em lugar nenhum.
- [ ] Corpo inteiro, do topo do capuz à sola da bota, sem corte.
- [ ] Fundo cinza liso, sem chão, sombra no chão, partículas, brilho violeta solto ou texto.
- [ ] Rosto: máscara de caveira na sombra do capuz, como no 2D. Se preferir só sombra, sem máscara, diga ao Claude antes de gerar.

## Depois

Avise o Claude com os nomes dos arquivos. Ele registra os brutos em `context/assets.md` (operador Pedro), monta `docs/arte/cavaleiro-conceito.png` com as três vistas lado a lado na mesma altura e mostra a folha para você aprovar.
