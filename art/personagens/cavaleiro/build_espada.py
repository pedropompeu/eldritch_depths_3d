"""Espada longa do Cavaleiro (B08): modelada por script, fiel à espada do hero.png do 2D.

Rodar da raiz: tools/blender.sh art/personagens/cavaleiro/build_espada.py
Saídas: assets/models/personagens/espada.glb e as pré-visualizações em
.godot/capturas_tmp/espada/.

Peças: lâmina larga de seção losangular com sulco central e runas violeta, guarda em cruz
com as pontas viradas para a lâmina, bloco central com uma gema violeta de cada lado, cabo de
mão e meia enrolado em couro e pomo alongado em ponta. Tudo vira uma malha com um material
só, assado em 512² (guia: espada ≤ 2.000 tri, 512², 1 material).

Orientação: origem no ponto de pegada da mão direita, logo abaixo da guarda; lâmina ao longo
de +Z no Blender (+Y no glTF); faces largas da lâmina viradas para ±Y (±Z no glTF). É assim
que ela entra no osso da mão na B10.
"""
import math
import os
import sys

import bpy
import bmesh

RAIZ = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
sys.path.insert(0, os.path.join(RAIZ, "tools", "blender"))
import ed_blender as ed  # noqa: E402
import ed_modelagem as em  # noqa: E402
from ed_modelagem import ACO, ACO_ESCURO, ACO_GUME, COURO, RUNA, VEU_FUNDO  # noqa: E402

SAIDA_GLB = os.path.join(RAIZ, "assets", "models", "personagens", "espada.glb")
TMP = os.path.join(RAIZ, ".godot", "capturas_tmp", "espada")
TEX = 512
MAX_TRIS = 2000

# Medidas (m), a partir da origem na pegada.
Z_POMO = -0.25        # ponta do pomo
Z_CABO = (-0.16, 0.055)
Z_GUARDA = 0.068
Z_PONTA = 1.05        # ponta da lâmina; comprimento total 1,30 m
SULCO = 0.014         # meia largura do sulco central
RUNAS_Z = (0.15, 0.84)

# Lâmina: (z, meia largura, meia espessura). Larga no talão, afinando devagar até a ponta.
ANEIS_LAMINA = [
    (0.075, 0.066, 0.011),
    (0.13, 0.069, 0.011),
    (0.30, 0.068, 0.0105),
    (0.50, 0.066, 0.010),
    (0.70, 0.061, 0.009),
    (0.86, 0.052, 0.008),
    (0.96, 0.036, 0.006),
    (1.01, 0.018, 0.0035),
]
# Seção: (fração da meia largura, fração da meia espessura, é gume). O gume (1) vira um
# atributo de vértice que o material usa para clarear a borda.
SECAO = [
    (-1.0, 0.0, 1), (-0.72, -0.5, 0), (-0.28, -1.0, 0), (0.28, -1.0, 0), (0.72, -0.5, 0),
    (1.0, 0.0, 1), (0.72, 0.5, 0), (0.28, 1.0, 0), (-0.28, 1.0, 0), (-0.72, 0.5, 0),
]


# ---------------------------------------------------------------- geometria

def lamina():
    bm = bmesh.new()
    gume = bm.verts.layers.float.new("gume")
    aneis = []
    for z, w, t in ANEIS_LAMINA:
        anel = []
        for fx, fy, g in SECAO:
            v = bm.verts.new((fx * w, fy * t, z))
            v[gume] = float(g)
            anel.append(v)
        aneis.append(anel)
    n = len(SECAO)
    for a, b in zip(aneis, aneis[1:]):
        for k in range(n):
            bm.faces.new((a[k], a[(k + 1) % n], b[(k + 1) % n], b[k]))
    ponta = bm.verts.new((0.0, 0.0, Z_PONTA))
    ponta[gume] = 1.0
    ult = aneis[-1]
    for k in range(n):
        bm.faces.new((ult[k], ult[(k + 1) % n], ponta))
    bm.faces.new(list(reversed(aneis[0])))
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    malha = bpy.data.meshes.new("lamina")
    bm.to_mesh(malha)
    bm.free()
    # O atributo de vértice float vira cor de vértice, que o nó Color Attribute lê.
    attr = malha.attributes["gume"]
    cores = malha.color_attributes.new("gume_cor", "FLOAT_COLOR", "POINT")
    for i, d in enumerate(attr.data):
        cores.data[i].color = (d.value, d.value, d.value, 1.0)
    malha.attributes.remove(malha.attributes["gume"])
    obj = bpy.data.objects.new("lamina", malha)
    bpy.context.scene.collection.objects.link(obj)
    return obj


def bloco(nome, dims, local):
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=local)
    obj = bpy.context.view_layer.objects.active
    obj.name = nome
    obj.scale = dims
    return obj


def gema(nome, local):
    bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=1, radius=0.013, location=local)
    obj = bpy.context.view_layer.objects.active
    obj.name = nome
    obj.scale = (1.0, 0.45, 1.25)
    return obj


# ---------------------------------------------------------------- materiais (só para assar)

def _ao(nt, cor, minimo=0.55, distancia=0.03):
    """Escurece reentrâncias (oclusão pintada), como no ferro do braseiro."""
    ao = nt.nodes.new("ShaderNodeAmbientOcclusion")
    ao.inputs["Distance"].default_value = distancia
    sombra = em.rampa(nt, ao.outputs["AO"], [(0.0, (minimo, minimo, minimo, 1)), (1.0, (1, 1, 1, 1))])
    mult = nt.nodes.new("ShaderNodeMix")
    mult.data_type = "RGBA"
    mult.blend_type = "MULTIPLY"
    mult.inputs["Factor"].default_value = 1.0
    nt.links.new(cor, mult.inputs[6])
    nt.links.new(sombra.outputs["Color"], mult.inputs[7])
    return mult.outputs[2]


def _math(nt, op, a, b=None):
    no = nt.nodes.new("ShaderNodeMath")
    no.operation = op
    for i, v in enumerate((a, b)):
        if v is None:
            continue
        if isinstance(v, bpy.types.NodeSocket):
            nt.links.new(v, no.inputs[i])
        else:
            no.inputs[i].default_value = v
    return no.outputs[0]


def mat_lamina():
    """Aço escuro puxado para o violeta, gume claro, sulco central mais fundo e runas acesas
    dentro dele (linhas de Voronoi em grupos ao longo da lâmina)."""
    m, nt, bsdf = em.mat("lamina")
    largo = em.ruido(nt, 3.0, 1.5)
    base = em.rampa(nt, largo.outputs["Fac"], [(0.35, em.rgba(ACO_ESCURO)), (0.65, em.rgba(ACO))])
    cor = em.mistura(nt, 0.45, base.outputs["Color"], em.rgba(VEU_FUNDO))

    attr = nt.nodes.new("ShaderNodeVertexColor")
    attr.layer_name = "gume_cor"
    gume = em.rampa(nt, attr.outputs["Color"], [(0.45, (0, 0, 0, 1)), (0.8, (1, 1, 1, 1))])
    cor = em.mistura(nt, gume.outputs["Color"], cor, em.rgba(ACO_GUME))

    coord = nt.nodes.new("ShaderNodeTexCoord")
    sep = nt.nodes.new("ShaderNodeSeparateXYZ")
    nt.links.new(coord.outputs["Object"], sep.inputs["Vector"])
    ax = _math(nt, "ABSOLUTE", sep.outputs["X"])
    no_trecho = _math(nt, "MULTIPLY",
                      _math(nt, "GREATER_THAN", sep.outputs["Z"], RUNAS_Z[0] - 0.03),
                      _math(nt, "LESS_THAN", sep.outputs["Z"], RUNAS_Z[1] + 0.03))
    sulco = _math(nt, "MULTIPLY", _math(nt, "LESS_THAN", ax, SULCO), no_trecho)
    cor = em.mistura(nt, _math(nt, "MULTIPLY", sulco, 0.55), cor, em.rgba("#0c0b12"))

    # Runas: bordas de células de Voronoi no plano XZ, só dentro do sulco, em grupos.
    plano = nt.nodes.new("ShaderNodeCombineXYZ")
    nt.links.new(sep.outputs["X"], plano.inputs["X"])
    nt.links.new(sep.outputs["Z"], plano.inputs["Y"])
    vor = nt.nodes.new("ShaderNodeTexVoronoi")
    vor.feature = "DISTANCE_TO_EDGE"
    vor.inputs["Scale"].default_value = 70.0
    vor.inputs["Randomness"].default_value = 0.6
    nt.links.new(plano.outputs["Vector"], vor.inputs["Vector"])
    linha = _math(nt, "LESS_THAN", vor.outputs["Distance"], 0.1)
    grupos = _math(nt, "GREATER_THAN",
                   _math(nt, "SINE", _math(nt, "MULTIPLY", sep.outputs["Z"], 2 * math.pi / 0.06)), -0.35)
    faixa = _math(nt, "MULTIPLY",
                  _math(nt, "LESS_THAN", ax, SULCO * 0.8),
                  _math(nt, "MULTIPLY",
                        _math(nt, "GREATER_THAN", sep.outputs["Z"], RUNAS_Z[0]),
                        _math(nt, "LESS_THAN", sep.outputs["Z"], RUNAS_Z[1])))
    runa = _math(nt, "MULTIPLY", _math(nt, "MULTIPLY", linha, grupos), faixa)

    cor = em.mistura(nt, runa, _ao(nt, cor), em.rgba(RUNA))
    nt.links.new(cor, bsdf.inputs["Base Color"])
    emis = em.mistura(nt, runa, (0, 0, 0, 1), em.rgba(RUNA))
    nt.links.new(emis, bsdf.inputs["Emission Color"])
    bsdf.inputs["Emission Strength"].default_value = 1.0
    return m


def mat_metal():
    """Guarda, bloco e pomo: aço com pinceladas largas e oclusão pintada."""
    m, nt, bsdf = em.mat("metal")
    largo = em.ruido(nt, 6.0, 1.5)
    base = em.rampa(nt, largo.outputs["Fac"], [(0.3, em.rgba(ACO_ESCURO)), (0.7, em.rgba(ACO))])
    nt.links.new(_ao(nt, base.outputs["Color"], 0.5, 0.02), bsdf.inputs["Base Color"])
    return m


def mat_cabo():
    """Couro enrolado: faixas em espiral com junta escura entre elas."""
    m, nt, bsdf = em.mat("cabo")
    coord = nt.nodes.new("ShaderNodeTexCoord")
    onda = nt.nodes.new("ShaderNodeTexWave")
    onda.wave_type = "BANDS"
    onda.bands_direction = "DIAGONAL"
    onda.inputs["Scale"].default_value = 18.0
    onda.inputs["Distortion"].default_value = 0.5
    nt.links.new(coord.outputs["Object"], onda.inputs["Vector"])
    junta = em.rampa(nt, onda.outputs["Fac"], [(0.08, (1, 1, 1, 1)), (0.2, (0, 0, 0, 1))])
    cor = em.mistura(nt, junta.outputs["Color"], em.rgba(COURO), em.rgba("#140c0c"))
    nt.links.new(_ao(nt, cor, 0.6, 0.01), bsdf.inputs["Base Color"])
    return m


def mat_gema():
    m, nt, bsdf = em.mat("gema")
    bsdf.inputs["Base Color"].default_value = em.rgba(RUNA)
    bsdf.inputs["Emission Color"].default_value = em.rgba(RUNA)
    bsdf.inputs["Emission Strength"].default_value = 1.0
    return m


# ---------------------------------------------------------------- montagem

def montar():
    lam, metal, cabo, pedra = mat_lamina(), mat_metal(), mat_cabo(), mat_gema()
    partes = [em.usar(lamina(), lam)]

    # Guarda em cruz: barra quadrada com as pontas subindo para a lâmina, como no 2D.
    pts = [(-0.17, 0, 0.105), (-0.125, 0, 0.078), (-0.05, 0, Z_GUARDA), (0.05, 0, Z_GUARDA),
           (0.125, 0, 0.078), (0.17, 0, 0.105)]
    partes.append(em.usar(em.barra("guarda", pts, 0.016, resolucao=4), metal))
    partes.append(em.usar(bloco("guarda_bloco", (0.08, 0.042, 0.036), (0, 0, Z_GUARDA)), metal))
    for i, y in enumerate((-0.021, 0.021)):
        partes.append(em.usar(gema(f"gema{i}", (0, y, Z_GUARDA)), pedra))

    # Cabo de mão e meia (21,5 cm) e anel de metal junto da guarda.
    z0, z1 = Z_CABO
    partes.append(em.usar(em.torno("cabo", [
        (0.0, z0), (0.0165, z0), (0.0175, -0.11), (0.0155, -0.05), (0.0165, 0.0),
        (0.0155, z1), (0.0, z1),
    ], 8), cabo))
    partes.append(em.usar(em.torno("virola", [
        (0.0, 0.04), (0.02, 0.04), (0.021, 0.052), (0.0, 0.052),
    ], 8), metal))

    # Pomo alongado em ponta.
    partes.append(em.usar(em.torno("pomo", [
        (0.0, -0.152), (0.02, -0.155), (0.029, -0.175), (0.027, -0.198), (0.017, -0.222),
        (0.007, -0.24), (0.0, Z_POMO),
    ], 8), metal))
    return partes


def main():
    ed.reset_scene()
    partes = montar()
    obj = ed.join_meshes(partes, "espada")
    ed.apply_transforms(obj)
    tris = ed.decimate_to(obj, MAX_TRIS)
    ed._select([obj], obj)
    bpy.ops.object.shade_smooth_by_angle(angle=math.radians(35))
    ed.smart_uv(obj, margin=0.02)
    em.assar(obj, "espada", TEX, TMP, metalico=0.35, rugosidade=0.45)
    # O gume já está na textura; sem isto o GLB levaria cor de vértice, que a Godot usaria
    # como albedo.
    for ca in list(obj.data.color_attributes):
        obj.data.color_attributes.remove(ca)
    # A origem fica onde está (0, 0, 0 = pegada); não vai para os pés como nos props.
    ed.render_turnaround([obj], TMP)
    ed.export_glb([obj], SAIDA_GLB)
    print("TRIS", tris)
    print("RELATORIO", ed.report([obj]))


main()
