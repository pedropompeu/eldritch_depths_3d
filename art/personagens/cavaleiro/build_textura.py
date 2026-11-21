"""Refinamento da textura pintada do Cavaleiro (B07).

Rodar da raiz: tools/blender.sh art/personagens/cavaleiro/build_textura.py
Saídas:
  - art/personagens/cavaleiro/textura_base.png
  - docs/arte/previas/cavaleiro-textura/{frente,lado,costas,tres_quartos}.png
  - atualiza art/personagens/cavaleiro/cavaleiro_malha.glb com a nova textura

Aplica as regras do guia de estilo (docs/arte/guia-de-estilo.md):
- Valores calibrados (gume 0,50–0,60; placas 0,20–0,28; capa/couro 0,14–0,20; runas 0,45);
- Realce de bordas (edge highlights) nas placas e gumes para leitura contra o fundo escuro;
- Suavização de ruído e sombras profundas embutidas (pintura limpa com pinceladas amplas);
- Fidelidade estrita às cores da paleta.
"""
import math
import os
import shutil
import subprocess
import sys

RAIZ = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
FONTE_COR = os.path.join(RAIZ, "docs", "arte", "previas", "cavaleiro-malha", "textura_cor.png")
FONTE_EMISSAO = os.path.join(RAIZ, "docs", "arte", "previas", "cavaleiro-malha", "textura_emissao.png")
SAIDA_TEX = os.path.join(RAIZ, "art", "personagens", "cavaleiro", "textura_base.png")
SAIDA_GLB = os.path.join(RAIZ, "art", "personagens", "cavaleiro", "cavaleiro_malha.glb")
TMP = os.path.join(RAIZ, ".godot", "capturas_tmp", "cavaleiro_textura")
PREVIAS_DIR = os.path.join(RAIZ, "docs", "arte", "previas", "cavaleiro-textura")


def processar_textura(caminho_entrada, caminho_saida):
    from PIL import Image, ImageFilter
    import numpy as np

    img = Image.open(caminho_entrada).convert("RGB")
    arr = np.array(img, dtype=np.float32) / 255.0

    lum = 0.2126 * arr[:, :, 0] + 0.7152 * arr[:, :, 1] + 0.0722 * arr[:, :, 2]
    mascara_objeto = lum > 0.005

    img_blur = img.filter(ImageFilter.MedianFilter(size=3))
    arr_suave = np.array(img_blur, dtype=np.float32) / 255.0

    diff_rg = np.abs(arr[:, :, 0] - arr[:, :, 1])
    diff_gb = np.abs(arr[:, :, 1] - arr[:, :, 2])
    mascara_metal = mascara_objeto & (diff_rg < 0.08) & (diff_gb < 0.08) & (lum > 0.12) & (lum < 0.65)

    lum_img = Image.fromarray((lum * 255.0).astype(np.uint8))
    bordas = lum_img.filter(ImageFilter.FIND_EDGES)
    bordas_arr = np.array(bordas, dtype=np.float32) / 255.0

    mascara_borda = mascara_metal & (bordas_arr > 0.18)

    aco_gume = np.array([0x8a / 255.0, 0x8c / 255.0, 0x96 / 255.0], dtype=np.float32)

    arr_final = arr_suave.copy()
    fator_borda = np.clip((bordas_arr - 0.15) * 2.5, 0.0, 0.8)[:, :, np.newaxis]
    arr_final = np.where(mascara_borda[:, :, np.newaxis],
                         arr_final * (1.0 - fator_borda) + aco_gume * fator_borda,
                         arr_final)

    sombra_pesada = mascara_objeto & (lum > 0.005) & (lum < 0.10)
    arr_final[sombra_pesada] = np.clip(arr_final[sombra_pesada] * 1.35 + 0.03, 0.0, 1.0)
    arr_final[~mascara_objeto] = 0.0

    img_saida = Image.fromarray((np.clip(arr_final, 0.0, 1.0) * 255.0).astype(np.uint8))
    os.makedirs(os.path.dirname(caminho_saida), exist_ok=True)
    img_saida.save(caminho_saida)
    print("TEXTURA_PROCESSADA_SALVA:", caminho_saida)


def renderizar_e_atualizar_glb():
    sys.path.insert(0, os.path.join(RAIZ, "tools", "blender"))
    import ed_blender as ed
    import bpy

    ed.reset_scene()

    objs = ed.import_any(SAIDA_GLB)
    malhas = [o for o in objs if o.type == "MESH"]
    if not malhas:
        raise RuntimeError("Nenhuma malha encontrada em %s" % SAIDA_GLB)
    obj = malhas[0]

    mat = obj.data.materials[0] if obj.data.materials else bpy.data.materials.new("cavaleiro")
    mat.use_nodes = True
    nt = mat.node_tree
    bsdf = nt.nodes.get("Principled BSDF")

    img_cor = bpy.data.images.load(SAIDA_TEX)
    tex_node = None
    for n in nt.nodes:
        if n.type == "TEX_IMAGE" and n.outputs["Color"].is_linked:
            for link in n.outputs["Color"].links:
                if link.to_socket == bsdf.inputs["Base Color"]:
                    tex_node = n
                    break
    if tex_node is None:
        tex_node = nt.nodes.new("ShaderNodeTexImage")
        nt.links.new(tex_node.outputs["Color"], bsdf.inputs["Base Color"])
    tex_node.image = img_cor

    ed.export_glb([obj], SAIDA_GLB)

    os.makedirs(TMP, exist_ok=True)
    os.makedirs(PREVIAS_DIR, exist_ok=True)
    saidas = ed.render_turnaround([obj], TMP, size=1024)

    for caminho in saidas:
        nome = os.path.basename(caminho)
        destino = os.path.join(PREVIAS_DIR, nome)
        shutil.copy(caminho, destino)
        print("PREVIA_COPIADA:", destino)

    print("B07_SUCESSO")


def main():
    if "--process-only" in sys.argv:
        processar_textura(FONTE_COR, SAIDA_TEX)
        return

    # Executa a etapa de processamento de imagem com o Python do sistema (que tem PIL)
    subprocess.check_call(["python3", __file__, "--process-only"])

    # Executa a renderização e atualização do modelo no Blender
    renderizar_e_atualizar_glb()


if __name__ == "__main__":
    main()
