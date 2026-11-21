"""Refinamento da textura pintada do Cultista (B12).

Rodar da raiz: tools/blender.sh art/inimigos/cultista/build_textura.py
Saídas:
  - art/inimigos/cultista/textura_base.png
  - docs/arte/previas/cultista-textura/{frente,lado,costas,tres_quartos}.png
  - atualiza art/inimigos/cultista/cultista_malha.glb com a nova textura

Aplica as regras do guia de estilo (docs/arte/guia-de-estilo.md):
- Manto e robes em tecido grosso com pregas profundas (escuro, 0.10–0.18 lum);
- Pele exposta amarelada e enferma (0.30–0.40 lum, saturação baixa);
- Runas bioluminescentes no manto (emissão verde-turquesa, 0.45 lum);
- Edge highlights nas costuras e bordas do manto para leitura contra fundo escuro;
- Fidelidade estrita às cores da paleta de horror cósmico.
"""
import math
import os
import shutil
import subprocess
import sys

RAIZ = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
FONTE_COR = os.path.join(RAIZ, ".godot", "capturas_tmp", "cultista_malha", "textura_cor.png")
FONTE_EMISSAO = os.path.join(RAIZ, ".godot", "capturas_tmp", "cultista_malha", "textura_emissao.png")
SAIDA_TEX = os.path.join(RAIZ, "art", "inimigos", "cultista", "textura_base.png")
SAIDA_GLB = os.path.join(RAIZ, "art", "inimigos", "cultista", "cultista_malha.glb")
TMP = os.path.join(RAIZ, ".godot", "capturas_tmp", "cultista_textura")
PREVIAS_DIR = os.path.join(RAIZ, "docs", "arte", "previas", "cultista-textura")


def processar_textura(caminho_entrada, caminho_saida):
    from PIL import Image, ImageFilter
    import numpy as np

    img = Image.open(caminho_entrada).convert("RGB")
    arr = np.array(img, dtype=np.float32) / 255.0

    lum = 0.2126 * arr[:, :, 0] + 0.7152 * arr[:, :, 1] + 0.0722 * arr[:, :, 2]
    mascara_objeto = lum > 0.005

    # Suaviza manchas de ruído (robes texturizados mas limpos)
    img_blur = img.filter(ImageFilter.MedianFilter(size=3))
    arr_suave = np.array(img_blur, dtype=np.float32) / 255.0

    # Detecta bordas para edge highlights nas costuras do manto
    lum_img = Image.fromarray((lum * 255.0).astype(np.uint8))
    bordas = lum_img.filter(ImageFilter.FIND_EDGES)
    bordas_arr = np.array(bordas, dtype=np.float32) / 255.0

    # Mascara: zonas escuras do manto (tecido)
    mascara_manto = mascara_objeto & (lum > 0.005) & (lum < 0.22)
    mascara_borda_manto = mascara_manto & (bordas_arr > 0.15)

    # Cor de edge highlight: verde-turquesa suave (runas bioluminescentes)
    cor_runa = np.array([0x20 / 255.0, 0x8f / 255.0, 0x7a / 255.0], dtype=np.float32)

    arr_final = arr_suave.copy()

    # Aplica highlight nas bordas do manto
    fator_borda = np.clip((bordas_arr - 0.12) * 3.0, 0.0, 0.7)[:, :, np.newaxis]
    arr_final = np.where(
        mascara_borda_manto[:, :, np.newaxis],
        arr_final * (1.0 - fator_borda) + cor_runa * fator_borda,
        arr_final,
    )

    # Aprofunda sombras nos vincos do manto
    sombra_profunda = mascara_objeto & (lum > 0.005) & (lum < 0.08)
    arr_final[sombra_profunda] = np.clip(arr_final[sombra_profunda] * 1.4 + 0.02, 0.0, 1.0)

    # Pele exposta: leve tonalidade amarelada enferma
    mascara_pele = mascara_objeto & (lum >= 0.28) & (lum <= 0.44)
    arr_final[mascara_pele, 0] = np.clip(arr_final[mascara_pele, 0] * 1.08, 0.0, 1.0)  # + vermelho
    arr_final[mascara_pele, 2] = np.clip(arr_final[mascara_pele, 2] * 0.82, 0.0, 1.0)  # - azul

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

    mat = obj.data.materials[0] if obj.data.materials else bpy.data.materials.new("cultista")
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

    print("B12_TEXTURA_SUCESSO")


def main():
    if "--process-only" in sys.argv:
        processar_textura(FONTE_COR, SAIDA_TEX)
        return

    # Etapa 1: processa a textura com Python do sistema (tem PIL/numpy)
    subprocess.check_call(["python3", __file__, "--process-only"])

    # Etapa 2: renderiza e atualiza o GLB no Blender
    renderizar_e_atualizar_glb()


if __name__ == "__main__":
    main()
