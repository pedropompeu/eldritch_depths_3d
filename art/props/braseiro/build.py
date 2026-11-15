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
import bmesh
from mathutils import Matrix, Vector

RAIZ = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
sys.path.insert(0, os.path.join(RAIZ, "tools", "blender"))
import ed_blender as ed  # noqa: E402

SAIDA_GLB = os.path.join(RAIZ, "assets", "models", "props", "braseiro.glb")
TMP = os.path.join(RAIZ, ".godot", "capturas_tmp", "braseiro")
TEX = 1024
MAX_TRIS = 3000

# Paleta do guia (docs/arte/guia-de-estilo.md)
ACO_ESCURO = "#1e1f26"
ACO = "#3c3e4a"
ACO_GUME = "#8a8c96"
COURO = "#3c2a28"
BRASA = "#ff8a3d"
LUZ_HEROI = "#ffb36b"
BREU = "#05060a"


def rgba(hexcor, a=1.0):
    return (*ed._linear(hexcor), a)


# ---------------------------------------------------------------- geometria

def torno(nome, perfil, segmentos, torcao=0.0):
    """Sólido de revolução em torno de Z. `perfil` = [(raio, z)]; raio 0 vira um vértice só.
    `torcao` gira cada anel (rad por anel), para as chamas."""
    bm = bmesh.new()
    aneis = []
    for i, (r, z) in enumerate(perfil):
        if r <= 1e-6:
            aneis.append([bm.verts.new((0, 0, z))])
            continue
        fase = torcao * i
        aneis.append([bm.verts.new((r * math.cos(2 * math.pi * k / segmentos + fase),
                                    r * math.sin(2 * math.pi * k / segmentos + fase), z))
                      for k in range(segmentos)])
    for a, b in zip(aneis, aneis[1:]):
        if len(a) == 1 and len(b) == 1:
            continue
        if len(a) == 1 or len(b) == 1:
            centro, anel = (a[0], b) if len(a) == 1 else (b[0], a)
            for k in range(segmentos):
                v1, v2 = anel[k], anel[(k + 1) % segmentos]
                bm.faces.new((centro, v1, v2) if len(a) == 1 else (v1, v2, centro))
            continue
        for k in range(segmentos):
            bm.faces.new((a[k], a[(k + 1) % segmentos], b[(k + 1) % segmentos], b[k]))
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    malha = bpy.data.meshes.new(nome)
    bm.to_mesh(malha)
    bm.free()
    obj = bpy.data.objects.new(nome, malha)
    bpy.context.scene.collection.objects.link(obj)
    return obj


def barra(nome, pontos, espessura, resolucao=5):
    """Barra de seção quadrada seguindo uma NURBS pelos pontos (x, y, z)."""
    curva = bpy.data.curves.new(nome, "CURVE")
    curva.dimensions = "3D"
    curva.bevel_depth = espessura
    curva.bevel_resolution = 0
    curva.use_fill_caps = True
    curva.resolution_u = resolucao
    sp = curva.splines.new("NURBS")
    sp.points.add(len(pontos) - 1)
    for p, xyz in zip(sp.points, pontos):
        p.co = (*xyz, 1.0)
    sp.order_u = 3
    sp.use_endpoint_u = True
    obj = bpy.data.objects.new(nome, curva)
    bpy.context.scene.collection.objects.link(obj)
    ed._select([obj], obj)
    bpy.ops.object.convert(target="MESH")
    return bpy.context.view_layer.objects.active


def anel(nome, raio, espessura, seg, seg_menor, local, rotacao=(0, 0, 0)):
    bpy.ops.mesh.primitive_torus_add(major_radius=raio, minor_radius=espessura,
                                     major_segments=seg, minor_segments=seg_menor,
                                     location=local, rotation=rotacao)
    obj = bpy.context.view_layer.objects.active
    obj.name = nome
    return obj


def tora(nome, comprimento, raio, local, rotacao):
    bpy.ops.mesh.primitive_cylinder_add(vertices=6, radius=raio, depth=comprimento,
                                        location=local, rotation=rotacao)
    obj = bpy.context.view_layer.objects.active
    obj.name = nome
    return obj


# ---------------------------------------------------------------- materiais (só para assar)

def _mat(nome):
    m = bpy.data.materials.new(nome)
    m.use_nodes = True
    nt = m.node_tree
    bsdf = nt.nodes["Principled BSDF"]
    return m, nt, bsdf


def _ruido(nt, escala, detalhe=2.0):
    coord = nt.nodes.new("ShaderNodeTexCoord")
    ruido = nt.nodes.new("ShaderNodeTexNoise")
    ruido.inputs["Scale"].default_value = escala
    ruido.inputs["Detail"].default_value = detalhe
    nt.links.new(coord.outputs["Object"], ruido.inputs["Vector"])
    return ruido


def _rampa(nt, entrada, paradas):
    rampa = nt.nodes.new("ShaderNodeValToRGB")
    els = rampa.color_ramp.elements
    els[0].position, els[0].color = paradas[0]
    els[1].position, els[1].color = paradas[-1]
    for pos, cor in paradas[1:-1]:
        e = els.new(pos)
        e.color = cor
    nt.links.new(entrada, rampa.inputs["Fac"])
    return rampa


def _mistura(nt, fac, a, b):
    mix = nt.nodes.new("ShaderNodeMix")
    mix.data_type = "RGBA"
    for entrada, valor in (("Factor", fac), ("A", a), ("B", b)):
        alvo = mix.inputs[entrada] if entrada == "Factor" else mix.inputs[6 if entrada == "A" else 7]
        if isinstance(valor, bpy.types.NodeSocket):
            nt.links.new(valor, alvo)
        else:
            alvo.default_value = valor
    return mix.outputs[2]


def mat_ferro():
    """Ferro batido: pinceladas largas entre aço-escuro e aço, ferrugem em manchas,
    quinas claras (pointiness) e oclusão leve pintada."""
    m, nt, bsdf = _mat("ferro")
    largo = _ruido(nt, 2.5, 1.5)
    base = _rampa(nt, largo.outputs["Fac"], [(0.35, rgba(ACO_ESCURO)), (0.65, rgba(ACO))])
    mancha = _ruido(nt, 6.0, 3.0)
    ferrugem = _rampa(nt, mancha.outputs["Fac"], [(0.58, (0, 0, 0, 1)), (0.68, (1, 1, 1, 1))])
    cor = _mistura(nt, ferrugem.outputs["Color"], base.outputs["Color"], rgba(COURO))
    geo = nt.nodes.new("ShaderNodeNewGeometry")
    quina = _rampa(nt, geo.outputs["Pointiness"], [(0.56, (0, 0, 0, 1)), (0.66, (0.3, 0.3, 0.3, 1))])
    cor = _mistura(nt, quina.outputs["Color"], cor, rgba(ACO_GUME))
    ao = nt.nodes.new("ShaderNodeAmbientOcclusion")
    ao.inputs["Distance"].default_value = 0.08
    sombra = _rampa(nt, ao.outputs["AO"], [(0.0, (0.55, 0.55, 0.55, 1)), (1.0, (1, 1, 1, 1))])
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
    m, nt, bsdf = _mat("interior")
    coord = nt.nodes.new("ShaderNodeTexCoord")
    sep = nt.nodes.new("ShaderNodeSeparateXYZ")
    nt.links.new(coord.outputs["Object"], sep.inputs["Vector"])
    altura = _rampa(nt, sep.outputs["Z"], [(0.86, rgba("#5a2a14")), (0.93, rgba("#1a1414"))])
    nt.links.new(altura.outputs["Color"], bsdf.inputs["Base Color"])
    brilho = _rampa(nt, sep.outputs["Z"], [(0.86, rgba("#6a2a0c")), (0.91, rgba(BREU))])
    nt.links.new(brilho.outputs["Color"], bsdf.inputs["Emission Color"])
    bsdf.inputs["Emission Strength"].default_value = 1.0
    return m


def mat_brasa():
    """Brasas e tições: carvão escuro com rachaduras finas de brasa (Voronoi), acesas só onde
    um ruído largo deixa, para não virar uma rede regular."""
    m, nt, bsdf = _mat("brasa")
    coord = nt.nodes.new("ShaderNodeTexCoord")
    torto = _ruido(nt, 4.0, 2.0)
    desvio = nt.nodes.new("ShaderNodeMix")
    desvio.data_type = "VECTOR"
    desvio.inputs["Factor"].default_value = 0.25
    nt.links.new(coord.outputs["Object"], desvio.inputs[4])
    nt.links.new(torto.outputs["Color"], desvio.inputs[5])
    vor = nt.nodes.new("ShaderNodeTexVoronoi")
    vor.feature = "DISTANCE_TO_EDGE"
    vor.inputs["Scale"].default_value = 9.0
    nt.links.new(desvio.outputs[1], vor.inputs["Vector"])
    racha = _rampa(nt, vor.outputs["Distance"], [(0.0, (1, 1, 1, 1)), (0.06, (0, 0, 0, 1))])
    acesa = _rampa(nt, _ruido(nt, 3.0, 1.0).outputs["Fac"], [(0.42, (0, 0, 0, 1)), (0.6, (1, 1, 1, 1))])
    mascara = nt.nodes.new("ShaderNodeMix")
    mascara.data_type = "RGBA"
    mascara.blend_type = "MULTIPLY"
    mascara.inputs["Factor"].default_value = 1.0
    nt.links.new(racha.outputs["Color"], mascara.inputs[6])
    nt.links.new(acesa.outputs["Color"], mascara.inputs[7])
    fac = mascara.outputs[2]
    cor = _mistura(nt, fac, rgba("#1c1412"), rgba(BRASA))
    nt.links.new(cor, bsdf.inputs["Base Color"])
    emis = _mistura(nt, fac, rgba(BREU), rgba(BRASA))
    nt.links.new(emis, bsdf.inputs["Emission Color"])
    bsdf.inputs["Emission Strength"].default_value = 1.0
    return m


def mat_chama():
    """Chama: brasa na base, luz quente na ponta; toda emissiva."""
    m, nt, bsdf = _mat("chama")
    coord = nt.nodes.new("ShaderNodeTexCoord")
    sep = nt.nodes.new("ShaderNodeSeparateXYZ")
    nt.links.new(coord.outputs["Object"], sep.inputs["Vector"])
    grad = _rampa(nt, sep.outputs["Z"], [(0.92, rgba(BRASA)), (1.1, rgba(LUZ_HEROI))])
    nt.links.new(grad.outputs["Color"], bsdf.inputs["Base Color"])
    nt.links.new(grad.outputs["Color"], bsdf.inputs["Emission Color"])
    bsdf.inputs["Emission Strength"].default_value = 1.0
    return m


def usar(obj, mat):
    obj.data.materials.clear()
    obj.data.materials.append(mat)
    return obj


# ---------------------------------------------------------------- montagem

def montar():
    ferro, interior, brasa, chama = mat_ferro(), mat_interior(), mat_brasa(), mat_chama()
    partes = []

    # Bacia: casca externa e borda (ferro) + parede interna (interior). Medidas do conceito,
    # com a borda a 1,0 m do chão.
    partes.append(usar(torno("bacia", [
        (0.0, 0.735), (0.13, 0.742), (0.25, 0.77), (0.335, 0.82), (0.39, 0.88),
        (0.418, 0.945), (0.428, 0.99), (0.43, 1.0), (0.405, 1.0),
    ], 24), ferro))
    partes.append(usar(torno("bacia_dentro", [
        (0.405, 1.0), (0.393, 0.95), (0.365, 0.895), (0.33, 0.865), (0.0, 0.855),
    ], 24), interior))

    # Monte de brasas e três tições cruzados.
    partes.append(usar(torno("brasas", [(0.34, 0.868), (0.22, 0.892), (0.0, 0.905)], 12), brasa))
    for i, (ang, inc) in enumerate(((0.3, 0.25), (2.2, -0.2), (4.1, 0.15))):
        partes.append(usar(tora(f"ticao{i}", 0.3, 0.032,
                                (0.05 * math.cos(ang), 0.05 * math.sin(ang), 0.93),
                                (math.pi / 2 + inc, 0, ang)), brasa))

    # Três chamas torcidas, alturas diferentes.
    for i, (dx, dy, alt, gir) in enumerate(((0.0, 0.0, 0.24, 0.0), (0.09, -0.04, 0.16, 1.3), (-0.07, 0.06, 0.12, 2.5))):
        c = usar(torno(f"chama{i}", [
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
        partes.append(usar(barra(f"pe{i}", pts, 0.017), ferro))

    partes.append(usar(anel("anel_meio", 0.205, 0.014, 24, 4, (0, 0, 0.47)), ferro))

    # Duas argolas encostadas na bacia, viradas para fora (frente e costas).
    for i, ang in enumerate((-math.pi / 2, math.pi / 2)):
        r = 0.405
        partes.append(usar(anel(f"argola{i}", 0.07, 0.011, 12, 4,
                                (r * math.cos(ang), r * math.sin(ang), 0.86),
                                (math.pi / 2, 0, ang + math.pi / 2)), ferro))
    return partes


def assar(obj):
    """Assa cor e emissão de todos os materiais na UV de `obj` e troca por um material só."""
    ed._cycles_cpu(16)
    os.makedirs(TMP, exist_ok=True)
    imagens = {}
    for tipo in ("cor", "emissao"):
        img = bpy.data.images.new(f"braseiro_{tipo}", TEX, TEX, alpha=False)
        for mat in obj.data.materials:
            no = mat.node_tree.nodes.new("ShaderNodeTexImage")
            no.image = img
            mat.node_tree.nodes.active = no
        ed._select([obj], obj)
        if tipo == "cor":
            bpy.ops.object.bake(type="DIFFUSE", pass_filter={"COLOR"}, margin=8)
        else:
            bpy.ops.object.bake(type="EMIT", margin=8)
        img.filepath_raw = os.path.join(TMP, f"textura_{tipo}.png")
        img.file_format = "PNG"
        img.save()
        imagens[tipo] = img

    final = bpy.data.materials.new("braseiro")
    final.use_nodes = True
    nt = final.node_tree
    bsdf = nt.nodes["Principled BSDF"]
    for tipo, entrada in (("cor", "Base Color"), ("emissao", "Emission Color")):
        no = nt.nodes.new("ShaderNodeTexImage")
        no.image = imagens[tipo]
        nt.links.new(no.outputs["Color"], bsdf.inputs[entrada])
    bsdf.inputs["Emission Strength"].default_value = 1.0
    bsdf.inputs["Metallic"].default_value = 0.2
    bsdf.inputs["Roughness"].default_value = 0.65
    obj.data.materials.clear()
    obj.data.materials.append(final)
    for p in obj.data.polygons:
        p.material_index = 0


def main():
    ed.reset_scene()
    partes = montar()
    obj = ed.join_meshes(partes, "braseiro")
    ed.apply_transforms(obj)
    tris = ed.decimate_to(obj, MAX_TRIS)
    ed._select([obj], obj)
    bpy.ops.object.shade_smooth_by_angle(angle=math.radians(40))
    ed.smart_uv(obj, margin=0.01)
    assar(obj)
    ed.set_origin_to_feet(obj)
    ed.render_turnaround([obj], TMP)
    ed.export_glb([obj], SAIDA_GLB)
    print("TRIS", tris)
    print("RELATORIO", ed.report([obj]))


main()
