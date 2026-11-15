---
tipo: indice
projeto: eldritch-depths-3d
descricao: Roteamento do contexto do Eldritch Depths 3D — o que cada arquivo tem e quando carregar.
estado: estavel
criado: 2026-11-14
---

# Contexto — Eldritch Depths 3D

RPG de ação 3D (Godot 4.7.2) de horror cósmico em que a sanidade é o Véu da percepção. Demo pública na Steam e peça de portfólio.

## Quando carregar o quê

| Tarefa | Carregar |
|---|---|
| Mexer em código ou inspecionar estrutura | [[arquitetura]] + [[achados]] |
| Regras do jogo, visão e escopo | [[produto]] |
| Antes de reabrir ou tomar uma decisão | [[decisoes]] |
| Antes de dizer que algo está pronto | [[achados]] |

## Fora de `context/`

- [2026-11-14] (e) Design aprovado (autoridade do produto): `docs/superpowers/specs/2026-11-14-eldritch-depths-3d-design.md`.
- [2026-11-14] (e) Plano do Bloco 1A (trilha de jogo): `docs/superpowers/plans/2026-11-14-tela-e-sensacao-trilha-jogo.md`.
- [2026-11-14] (e) Ledger do Bloco 1A (quem faz qual tarefa, status, rulings): `docs/superpowers/plans/2026-11-14-tela-e-sensacao-ledger.md`.
- [2026-11-14] (e) Projeto 2D de referência (intacto, só leitura): `/home/usuario/Dev/holding_agy/eldritch_depths_20260912/`.

## Regras

- [2026-11-14] (d) Todo fato leva `[YYYY-MM-DD]` e procedência: `(d)` dito por Pedro, `(i)` inferido pela IA, `(e)` externo (código, máquina, documentos).
- [2026-11-14] (d) Fato nunca se apaga: marcar `~superseded YYYY-MM-DD` apontando para o novo. Uma `(i)` nunca sustenta outra `(i)`.
- [2026-11-14] (d) Rodar `python lint.py` depois de mexer em `context/`.
