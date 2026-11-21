# Prompt e Especificação 3D — Cavaleiro (B06)

Instruções para geração da malha base limpa 3D do Cavaleiro (herói) em pose A, fiel à folha de conceito aprovada (`docs/arte/cavaleiro-conceito.png`), com altura de 1,80 m, pés em z = 0, voltado para −Y no Blender (+Z no glTF) e orçamento ≤ 20.000 triângulos com UV e textura assada em 2048².

## 1. Referência Visual Aprovada

- **Folha de conceito:** `docs/arte/cavaleiro-conceito.png` (vistas ortográficas: frente, lado, costas).
- **Prévias adicionais:** `docs/arte/previas/cavaleiro/` (¾ com iluminação dramática do jogo).
- **Características obrigatórias:**
  - Capuz marrom escuro fundo em couro;
  - Máscara de osso em formato de caveira na sombra do capuz, com dentes e arcada detalhados;
  - Gema violeta rúnica na testa e gema no peito sobre o tabardo;
  - Ombreiras de placas de aço escuro com friso rolado;
  - Casaco longo de couro marrom aberto na frente, cravos violeta na barra;
  - Tabardo cinza com relevo rúnico;
  - Cinto de couro com fivela e bolsas laterais;
  - Capa esfarrapada escura pendendo das costas;
  - Grevas, joelheiras e sabatões de placas metálicas articuladas;
  - Manoplas de aço articuladas em pose A (braços a 45°).

## 2. Geração Externa (TRELLIS.2 / Meshy - Reserva)

Caso opte por gerar uma malha bruta externa via Space Hugging Face:
- **Serviço principal:** Space `microsoft/TRELLIS.2` (MIT) — https://huggingface.co/spaces/microsoft/TRELLIS.2
- **Entrada:** recorte da vista frontal de `docs/arte/cavaleiro-conceito.png` (fundo cinza neutro).
- **Configurações:** manter resolução e exportar `.glb`.
- **Salvar em:** `art/brutos/AAAA-MM-DD-trellis2-cavaleiro.glb`.

## 3. Geração Direta por Script (Caminho Oficial / Reproduzível)

Devido às restrições de cota dos Spaces e para garantir 100% de consistência com os materiais aprovados:
- **Script:** `tools/blender.sh art/personagens/cavaleiro/build_malha.py`
- **Operação:**
  1. Constrói a geometria de alta definição a partir das partes validadas em `build_conceito.py` (~163k triângulos);
  2. Unifica em malha única (`join_meshes`);
  3. Aplica escala exata para 1,80 m de altura e alinha origem aos pés (z = 0);
  4. Reduz a contagem poligonal via decimate para caber no teto de 20.000 triângulos (resultando em ~19.400 tris);
  5. Aplica normal smoothing adequado (`shade_smooth_by_angle(45°)`);
  6. Gera mapeamento UV (`smart_uv`);
  7. Assa as cores e emissão procedural em textura 2048²;
  8. Exporta `art/personagens/cavaleiro/cavaleiro_malha.glb` e renderiza as prévias de turnaround em 1024².
