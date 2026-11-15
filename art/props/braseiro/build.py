"""Braseiro (B04): modelado por script a partir do conceito art/brutos/2026-11-15-flux-braseiro.webp.

Rodar da raiz: tools/blender.sh art/props/braseiro/build.py
Saídas: assets/models/props/braseiro.glb e as pré-visualizações em .godot/capturas_tmp/braseiro/.

Peças: bacia de ferro (torno), interior queimado, monte de brasas e tições, três chamas,
quatro pés de barra quadrada em curva, anel do meio e duas argolas. Cada peça recebe um
material procedural; tudo é juntado numa malha, desdobrado e assado numa textura de cor e
numa de emissão (1024²), e a malha final tem um material só (guia: prop ≤ 3.000 tri, 1 material).
"""
import math
import os
import sys

import bpy

RAIZ = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
sys.path.insert(0, os.path.join(RAIZ, "tools", "blender"))
import ed_blender as ed  # noqa: E402
import ed_modelagem as em  # noqa: E402
from ed_modelagem import ACO, ACO_ESCURO, ACO_GUME, BRASA, BREU, COURO, LUZ_HEROI  # noqa: E402

SAIDA_GLB = os.path.join(RAIZ, "assets", "models", "props", "braseiro.glb")
TMP = os.path.join(RAIZ, ".godot", "capturas_tmp", "braseiro")
TEX = 1024
MAX_TRIS = 3000


# ---------------------------------------------------------------- materiais (só para assar)

def mat_ferro():
    """Ferro batido: pinceladas largas entre aço-escuro e aço, ferrugem em manchas,
    quinas claras (pointiness) e oclusão leve pintada."""
    m, nt, bsdf = em.mat("ferro")
    largo = em.ruido(nt, 2.5, 1.5)
    base = em.rampa(nt, largo.outputs["Fac"], [(0.35, em.rgba(ACO_ESCURO)), (0.65, em.rgba(ACO))])
    mancha = em.ruido(nt, 6.0, 3.0)
    ferrugem = em.rampa(nt, mancha.outputs["Fac"], [(0.58, (0, 0, 0, 1)), (0.68, (1, 1, 1, 1))])
    cor = em.mistura(nt, ferrugem.outputs["Color"], base.outputs["Color"], em.rgba(COURO))
    geo = nt.nodes.new("ShaderNodeNewGeometry")
    quina = em.rampa(nt, geo.outputs["Pointiness"], [(0.56, (0, 0, 0, 1)), (0.66, (0.3, 0.3, 0.3, 1))])
    cor = em.mistura(nt, quina.outputs["Color"], cor, em.rgba(ACO_GUME))
    ao = nt.nodes.new("ShaderNodeAmbientOcclusion")
    ao.inputs["Distance"].default_value = 0.08
    sombra = em.rampa(nt, ao.outputs["AO"], [(0.0, (0.55, 0.55, 0.55, 1)), (1.0, (1, 1, 1, 1))])
    mult = nt.nodes.new("ShaderNodeMix")
    mult.data_type = "RGBA"
    mult.blend_type = "MULTIPLY"
    mult.inputs["Factor"].default_value = 1.0
    nt.links.new(cor, mult.inputs[6])
    nt.links.new(sombra.outputs["Color"], mult.inputs[7])
    nt.links.new(mult.outputs[2], bsdf.inputs["Base Color"])
    return m


def mat_interior():
    """Dentro da bacia: fuligem escura que esquenta para brasa perto do fundo."""
    m, nt, bsdf = em.mat("interior")
    coord = nt.nodes.new("ShaderNodeTexCoord")
    sep = nt.nodes.new("ShaderNodeSeparateXYZ")
    nt.links.new(coord.outputs["Object"], sep.inputs["Vector"])
    altura = em.rampa(nt, sep.outputs["Z"], [(0.86, em.rgba("#5a2a14")), (0.93, em.rgba("#1a1414"))])
    nt.links.new(altura.outputs["Color"], bsdf.inputs["Base Color"])
    brilho = em.rampa(nt, sep.outputs["Z"], [(0.86, em.rgba("#6a2a0c")), (0.91, em.rgba(BREU))])
    nt.links.new(brilho.outputs["Color"], bsdf.inputs["Emission Color"])
    bsdf.inputs["Emission Strength"].default_value = 1.0
    return m


def mat_brasa():
    """Brasas e tições: carvão escuro com rachaduras finas de brasa (Voronoi), acesas só onde
    um ruído largo deixa, para não virar uma rede regular."""
    m, nt, bsdf = em.mat("brasa")
    coord = nt.nodes.new("ShaderNodeTexCoord")
    torto = em.ruido(nt, 4.0, 2.0)
    desvio = nt.nodes.new("ShaderNodeMix")
    desvio.data_type = "VECTOR"
    desvio.inputs["Factor"].default_value = 0.25
    nt.links.new(coord.outputs["Object"], desvio.inputs[4])
    nt.links.new(torto.outputs["Color"], desvio.inputs[5])
    vor = nt.nodes.new("ShaderNodeTexVoronoi")
    vor.feature = "DISTANCE_TO_EDGE"
    vor.inputs["Scale"].default_value = 9.0
    nt.links.new(desvio.outputs[1], vor.inputs["Vector"])
    racha = em.rampa(nt, vor.outputs["Distance"], [(0.0, (1, 1, 1, 1)), (0.06, (0, 0, 0, 1))])
    acesa = em.rampa(nt, em.ruido(nt, 3.0, 1.0).outputs["Fac"], [(0.42, (0, 0, 0, 1)), (0.6, (1, 1, 1, 1))])
    mascara = nt.nodes.new("ShaderNodeMix")
    mascara.data_type = "RGBA"
    mascara.blend_type = "MULTIPLY"
    mascara.inputs["Factor"].default_value = 1.0
    nt.links.new(racha.outputs["Color"], mascara.inputs[6])
    nt.links.new(acesa.outputs["Color"], mascara.inputs[7])
    fac = mascara.outputs[2]
    cor = em.mistura(nt, fac, em.rgba("#1c1412"), em.rgba(BRASA))
    nt.links.new(cor, bsdf.inputs["Base Color"])
    emis = em.mistura(nt, fac, em.rgba(BREU), em.rgba(BRASA))
    nt.links.new(emis, bsdf.inputs["Emission Color"])
    bsdf.inputs["Emission Strength"].default_value = 1.0
    return m


def mat_chama():
    """Chama: brasa na base, luz quente na ponta; toda emissiva."""
    m, nt, bsdf = em.mat("chama")
    coord = nt.nodes.new("ShaderNodeTexCoord")
    sep = nt.nodes.new("ShaderNodeSeparateXYZ")
    nt.links.new(coord.outputs["Object"], sep.inputs["Vector"])
    grad = em.rampa(nt, sep.outputs["Z"], [(0.92, em.rgba(BRASA)), (1.1, em.rgba(LUZ_HEROI))])
    nt.links.new(grad.outputs["Color"], bsdf.inputs["Base Color"])
    nt.links.new(grad.outputs["Color"], bsdf.inputs["Emission Color"])
    bsdf.inputs["Emission Strength"].default_value = 1.0
    return m


# ---------------------------------------------------------------- montagem

def montar():
    ferro, interior, brasa, chama = mat_ferro(), mat_interior(), mat_brasa(), mat_chama()
    partes = []

    # Bacia: casca externa e borda (ferro) + parede interna (interior). Medidas do conceito,
    # com a borda a 1,0 m do chão.
    partes.append(em.usar(em.torno("bacia", [
        (0.0, 0.735), (0.13, 0.742), (0.25, 0.77), (0.335, 0.82), (0.39, 0.88),
        (0.418, 0.945), (0.428, 0.99), (0.43, 1.0), (0.405, 1.0),
    ], 24), ferro))
    partes.append(em.usar(em.torno("bacia_dentro", [
        (0.405, 1.0), (0.393, 0.95), (0.365, 0.895), (0.33, 0.865), (0.0, 0.855),
    ], 24), interior))

    # Monte de brasas e três tições cruzados.
    partes.append(em.usar(em.torno("brasas", [(0.34, 0.868), (0.22, 0.892), (0.0, 0.905)], 12), brasa))
    for i, (ang, inc) in enumerate(((0.3, 0.25), (2.2, -0.2), (4.1, 0.15))):
        partes.append(em.usar(em.tora(f"ticao{i}", 0.3, 0.032,
                                (0.05 * math.cos(ang), 0.05 * math.sin(ang), 0.93),
                                (math.pi / 2 + inc, 0, ang)), brasa))

    # Três chamas torcidas, alturas diferentes.
    for i, (dx, dy, alt, gir) in enumerate(((0.0, 0.0, 0.24, 0.0), (0.09, -0.04, 0.16, 1.3), (-0.07, 0.06, 0.12, 2.5))):
        c = em.usar(em.torno(f"chama{i}", [
            (0.0, 0.0), (0.065, 0.03), (0.07, alt * 0.25), (0.055, alt * 0.5), (0.03, alt * 0.78), (0.0, alt),
        ], 8, torcao=0.2), chama)
        c.location = (dx, dy, 0.9)
        c.rotation_euler = (0, 0, gir)
        partes.append(c)

    # Quatro pés de barra quadrada: saem de baixo da bacia, encostam no anel do meio e
    # abrem para fora, com o pé virado na ponta.
    perfil_pe = [(0.31, 0.83), (0.27, 0.69), (0.205, 0.47), (0.29, 0.24),
                 (0.45, 0.05), (0.54, 0.012), (0.575, 0.03)]
    for i in range(4):
        ang = math.radians(45 + 90 * i)
        pts = [(r * math.cos(ang), r * math.sin(ang), z) for r, z in perfil_pe]
        partes.append(em.usar(em.barra(f"pe{i}", pts, 0.017), ferro))

    partes.append(em.usar(em.anel("anel_meio", 0.205, 0.014, 24, 4, (0, 0, 0.47)), ferro))

    # Duas argolas encostadas na bacia, viradas para fora (frente e costas).
    for i, ang in enumerate((-math.pi / 2, math.pi / 2)):
        r = 0.405
        partes.append(em.usar(em.anel(f"argola{i}", 0.07, 0.011, 12, 4,
                                (r * math.cos(ang), r * math.sin(ang), 0.86),
                                (math.pi / 2, 0, ang + math.pi / 2)), ferro))
    return partes


def main():
    ed.reset_scene()
    partes = montar()
    obj = ed.join_meshes(partes, "braseiro")
    ed.apply_transforms(obj)
    tris = ed.decimate_to(obj, MAX_TRIS)
    ed._select([obj], obj)
    bpy.ops.object.shade_smooth_by_angle(angle=math.radians(40))
    ed.smart_uv(obj, margin=0.01)
    em.assar(obj, "braseiro", TEX, TMP, metalico=0.2, rugosidade=0.65)
    ed.set_origin_to_feet(obj)
    ed.render_turnaround([obj], TMP)
    ed.export_glb([obj], SAIDA_GLB)
    print("TRIS", tris)
    print("RELATORIO", ed.report([obj]))


main()
