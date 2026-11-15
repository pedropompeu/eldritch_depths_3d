# Guia de estilo — Eldritch Depths 3D

Referência de toda peça de arte do Bloco 1B em diante. Quando uma tarefa do plano cita "o guia", é este arquivo. Mudança aqui passa por Pedro.

## Direção

- **Semi-realista pintada.** Proporções reais, formas um pouco exageradas para ler de cima (ombreiras, capuz, lâmina), fantasia sombria (spec §4.1).
- **A luz conta a história.** O mundo é escuro; o herói anda numa poça de luz quente e é ela que separa as formas. Por isso **não há contorno** (outline) nem efeito de desenho animado: a leitura vem do valor (claro contra escuro) e da borda que pega luz.
- **Pintura, não foto.** Texturas com pinceladas largas e variação de cor suave, sem ruído fino de foto nem detalhe que some a 10 m de câmera. Sombras de oclusão leves pintadas na textura; nada de luz direcional embutida (a luz vem da cena).
- **Silhueta primeiro.** Cada personagem precisa ser reconhecido só pela silhueta em 1/13 da altura da tela: o Cavaleiro pelo capuz, ombreiras e espada longa; o Cultista pelo capuz pontudo, manto aberto em sino e tentáculos na barra.
- **Fidelidade ao 2D.** O Cavaleiro e o Cultista seguem as ilustrações `hero.png` e `cultist.png` do projeto 2D (`/home/usuario/Dev/holding_agy/eldritch_depths_20260912/assets/sprites/`): mesmo desenho de roupa, mesmas cores, versão 3D.

## Paleta

No máximo 16 cores no mundo 3D. Uma textura pode variar em torno delas (mais clara, mais escura, um pouco mais quente ou mais fria), mas o matiz de cada material sai daqui. Amostras em [`paleta.svg`](paleta.svg).

| Nome | Hex | Uso |
|---|---|---|
| `breu` | `#05060a` | fundo e vazio; nada do mundo é mais escuro |
| `nevoa` | `#0b0d12` | névoa de profundidade |
| `pedra-sombra` | `#1c1c22` | juntas e reentrâncias da pedra |
| `pedra` | `#3a3a40` | face da pedra do cenário |
| `pedra-gasta` | `#5c5852` | quinas gastas da pedra, só onde a luz bate |
| `aco-escuro` | `#1e1f26` | placas da armadura na sombra |
| `aco` | `#3c3e4a` | placas da armadura sob luz |
| `aco-gume` | `#8a8c96` | bordas das placas e gume da espada |
| `couro` | `#3c2a28` | capa, cintos, luvas |
| `veu-fundo` | `#29193a` | massa da parede do Véu, sombras violeta |
| `runa` | `#9e59ff` | runas, borda do Véu; só acento |
| `manto-vinho` | `#3a0f1e` | manto do Cultista na sombra |
| `manto-carmim` | `#6c1f34` | manto do Cultista sob luz |
| `luz-heroi` | `#ffb36b` | luz do herói (HeroLight) |
| `brasa` | `#ff8a3d` | braseiros e chamas |
| `aviso` | `#ff2020` | brilho de aviso do inimigo; só jogabilidade |

Origem: `breu`, `nevoa`, `pedra`, `luz-heroi` e `aviso` são os valores que já estão no jogo (`greybox_room.tscn`, `player_3d.tscn`, `enemy_common.gd`); `veu-fundo` e `runa` são o `albedo` e o `edge_color` do `veil_dissolve.gdshader`; aço, couro e mantos vêm das cores dominantes de `hero.png` e `cultist.png`.

As cores do HUD (vida `#9b2226`, vigor `#c9a227`, sanidade `#6a4c93`, texto `#d9d1c7`) são da interface e não entram nos materiais do mundo.

**Regras de uso:**
- `runa` e `aviso` são acentos: no máximo uns 5% da área visível de uma peça. `aviso` é reservado ao jogo (o golpe que vem); nenhuma textura usa esse vermelho.
- `brasa` e `luz-heroi` são cores de luz; nas texturas aparecem só em brasas, chamas e reflexos pintados.

## Valores de luz

Valor = claridade da cor do material (albedo), de 0 (preto) a 1 (branco), medida como luminância dos valores sRGB (0,2126 R + 0,7152 G + 0,0722 B). Sob a luz do jogo, a ordem do mais claro ao mais escuro precisa ficar assim:

| Material | Valor do albedo | Por quê |
|---|---|---|
| Gume e bordas das placas | 0,50–0,60 | pegam a luz e desenham o herói |
| Placas da armadura | 0,20–0,28 | escuras, mas legíveis na poça de luz |
| Capa e couro | 0,14–0,20 | massa escura atrás do metal |
| Manto do Cultista | 0,08–0,22 | vermelho sombrio; o brilho de aviso precisa saltar por cima |
| Pedra do cenário | 0,18–0,26 na face, 0,30–0,36 nas quinas | sempre um degrau abaixo do herói na mesma luz |
| Runas | 0,45 com emissão fraca (≤ 0,5) | acento violeta que se vê no escuro |

Nenhum albedo passa de 0,65: o que for mais claro estoura sob a `HeroLight` (energia 2,5).

## Orçamentos

Cada número é um limite que os testes conferem (`tools/test.sh`).

| Peça | Triângulos | Textura base | Materiais |
|---|---|---|---|
| Cavaleiro | ≤ 20.000 | 2048² | ≤ 2 |
| Espada longa | ≤ 2.000 | 512² | 1 |
| Cultista | ≤ 12.000 | 1024² | ≤ 2 |
| Lâmina do Cultista | ≤ 1.000 | 512² | 1 |
| Peça do kit modular | ≤ 1.500 | 1024², compartilhada entre as peças | 1 |
| Prop (braseiro, baú, altar) | ≤ 3.000 | 1024² | 1 |

Texturas além da cor (normal, rugosidade) só se a peça precisar e couberem no mesmo tamanho. Meta de desempenho: 60 fps em 1080p no vídeo integrado (`tools/measure_fps.sh mobile`).

## Escala e grade

- 1 unidade da Godot = 1 m. Modelos exportados já na escala certa, sem escala no nó.
- Herói: 1,80 m (altura da cápsula de colisão). Cultista: até 1,95 m.
- Paredes: 3 m de altura, 0,4 m de espessura. Porta: 2 m de largura, 2,4 m de altura.
- **Grade do kit: 2 m.** A sala de 16 × 16 m, a porta de 2 m e a saleta de 4 × 4 m do Bloco 1A cabem nela.
- Origem: personagens e props com a origem no chão, no centro da base; peças do kit com a origem num canto de grade, base em y = 0.
- Frente: personagens olham para +Z no glTF exportado (−Y no Blender); o nó `Visual` gira 180° porque o jogo mira em −Z.

## Nomes

- Pastas e arquivos em português, sem acento, minúsculas, palavras com `_` nos modelos (`parede_porta.glb`) e `-` nos prompts e pré-visualizações (`cavaleiro-conceito.png`).
- Clipes de animação em inglês: `idle`, `walk`, `attack_1`, `attack_2`, `roll`, `parry`, `hurt`, `death` (herói); `telegraph`, `attack`, `stunned` (inimigo).
- Brutos dos serviços: `art/brutos/YYYY-MM-DD-<servico>-<assunto>.<ext>`.

## Luz das pré-visualizações

Toda pré-visualização renderizada para aprovação (`render_turnaround`, B03) usa a mesma luz, perto da do jogo:

- Fundo `breu` `#05060a`.
- Luz principal `luz-heroi` `#ffb36b`, pontual, acima e à frente da peça, como a `HeroLight`.
- Contraluz fria `#3a4a6a`, fraca, atrás e acima, para mostrar a silhueta.
- Câmera ortográfica nas vistas de frente, lado e costas, e em perspectiva na de três quartos, de cima a uns 55° como a câmera do jogo.

Assim Pedro aprova a peça sob a luz em que ela vai aparecer.
