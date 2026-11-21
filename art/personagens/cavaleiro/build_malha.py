"""Malha limpa do Cavaleiro (B06): unificação, decimate (≤ 20.000 tri), smart UV, bake e exportação GLB.

Rodar da raiz: tools/blender.sh art/personagens/cavaleiro/build_malha.py
Saídas:
  - art/personagens/cavaleiro/cavaleiro_malha.glb
  - .godot/capturas_tmp/cavaleiro_malha/{frente,lado,costas,tres_quartos}.png
  - .godot/capturas_tmp/cavaleiro_malha/{textura_cor,textura_emissao}.png

Baseado no conceito 3D realista aprovado (B05b) em `build_conceito.py`.
Produz malha única em pose A (braços a 45°), altura de 1,80 m, pés em z = 0,
olhando para −Y do Blender (+Z no glTF), com contagem poligonal dentro do teto
(≤ 20.000 triângulos) e textura assada em 2048².
"""
import math
import os
import sys

import bpy

RAIZ = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
sys.path.insert(0, os.path.join(RAIZ, "tools", "blender"))
sys.path.insert(0, os.path.join(RAIZ, "art", "personagens", "cavaleiro"))

import ed_blender as ed  # noqa: E402
import ed_modelagem as em  # noqa: E402
import build_conceito as bc  # noqa: E402

SAIDA_GLB = os.path.join(RAIZ, "art", "personagens", "cavaleiro", "cavaleiro_malha.glb")
TMP = os.path.join(RAIZ, ".godot", "capturas_tmp", "cavaleiro_malha")
TEX = 2048
MAX_TRIS = 20000


def main():
    ed.reset_scene()
    M = bc.materiais()

    # 1. Gera todas as partes procedurais da versão 3 realista aprovada
    partes = bc.corpo(M) + bc.bracos(M) + bc.cabeca(M) + bc.roupa(M)

    # 2. Junta tudo em um único objeto de malha
    obj = ed.join_meshes(partes, "cavaleiro")
    ed.apply_transforms(obj)

    # 3. Escala para exatamente 1,80 m e alinha origem aos pés (z = 0)
    ed.scale_to_height(obj, 1.80)
    ed.set_origin_to_feet(obj)

    # 4. Decimate para caber no orçamento de 20.000 triângulos
    tris = ed.decimate_to(obj, MAX_TRIS)

    # 5. Suavização normal das quinas
    ed._select([obj], obj)
    bpy.ops.object.shade_smooth_by_angle(angle=math.radians(45))

    # 6. Mapeamento UV limpo
    ed.smart_uv(obj, margin=0.01)

    # 7. Assa cor difusa e emissão em 2048²
    em.assar(obj, "cavaleiro", TEX, TMP, metalico=0.35, rugosidade=0.6, emissao=1.0)

    # 8. Renderiza as 4 vistas de turnaround sob a iluminação de teste
    ed.render_turnaround([obj], TMP, size=1024)

    # 9. Exporta GLB com a malha limpa unificada
    ed.export_glb([obj], SAIDA_GLB)

    rep = ed.report([obj])
    print("B06_SUCESSO")
    print("TRIS:", tris)
    print("RELATORIO:", rep)
    print("ARQUIVO_GLB:", SAIDA_GLB)


if __name__ == "__main__":
    main()
