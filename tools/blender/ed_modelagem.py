"""Peças e materiais procedurais para props e acessórios modelados por script (B04, B08).

Geometria (torno, barra, anel, tora), ajudantes de nós para materiais que só existem para
serem assados (mat, ruido, rampa, mistura) e `assar`, que leva todos os materiais de uma
malha para uma textura de cor e uma de emissão e deixa um material só.
Escala: 1 unidade = 1 m, Z para cima.
"""
import math
import os

import bpy
import bmesh

import ed_blender as ed

# Paleta do guia (docs/arte/guia-de-estilo.md)
ACO_ESCURO = "#1e1f26"
ACO = "#3c3e4a"
ACO_GUME = "#8a8c96"
COURO = "#3c2a28"
VEU_FUNDO = "#29193a"
RUNA = "#9e59ff"
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

def mat(nome):
    m = bpy.data.materials.new(nome)
    m.use_nodes = True
    nt = m.node_tree
    bsdf = nt.nodes["Principled BSDF"]
    return m, nt, bsdf


def ruido(nt, escala, detalhe=2.0):
    coord = nt.nodes.new("ShaderNodeTexCoord")
    ruido = nt.nodes.new("ShaderNodeTexNoise")
    ruido.inputs["Scale"].default_value = escala
    ruido.inputs["Detail"].default_value = detalhe
    nt.links.new(coord.outputs["Object"], ruido.inputs["Vector"])
    return ruido


def rampa(nt, entrada, paradas):
    rampa = nt.nodes.new("ShaderNodeValToRGB")
    els = rampa.color_ramp.elements
    els[0].position, els[0].color = paradas[0]
    els[1].position, els[1].color = paradas[-1]
    for pos, cor in paradas[1:-1]:
        e = els.new(pos)
        e.color = cor
    nt.links.new(entrada, rampa.inputs["Fac"])
    return rampa


def mistura(nt, fac, a, b):
    mix = nt.nodes.new("ShaderNodeMix")
    mix.data_type = "RGBA"
    for entrada, valor in (("Factor", fac), ("A", a), ("B", b)):
        alvo = mix.inputs[entrada] if entrada == "Factor" else mix.inputs[6 if entrada == "A" else 7]
        if isinstance(valor, bpy.types.NodeSocket):
            nt.links.new(valor, alvo)
        else:
            alvo.default_value = valor
    return mix.outputs[2]


def usar(obj, mat):
    obj.data.materials.clear()
    obj.data.materials.append(mat)
    return obj



def assar(obj, nome, tamanho, pasta, metalico=0.0, rugosidade=0.5, emissao=1.0):
    """Assa cor (DIFFUSE) e emissão (EMIT) de todos os materiais de `obj` na UV dele, em duas
    imagens `tamanho`² salvas em `pasta`, e troca tudo por um material só chamado `nome`."""
    ed._cycles_cpu(16)
    os.makedirs(pasta, exist_ok=True)
    imagens = {}
    for tipo in ("cor", "emissao"):
        img = bpy.data.images.new(f"{nome}_{tipo}", tamanho, tamanho, alpha=False)
        for mat in obj.data.materials:
            no = mat.node_tree.nodes.new("ShaderNodeTexImage")
            no.image = img
            mat.node_tree.nodes.active = no
        ed._select([obj], obj)
        if tipo == "cor":
            bpy.ops.object.bake(type="DIFFUSE", pass_filter={"COLOR"}, margin=8)
        else:
            bpy.ops.object.bake(type="EMIT", margin=8)
        img.filepath_raw = os.path.join(pasta, f"textura_{tipo}.png")
        img.file_format = "PNG"
        img.save()
        imagens[tipo] = img

    final = bpy.data.materials.new(nome)
    final.use_nodes = True
    nt = final.node_tree
    bsdf = nt.nodes["Principled BSDF"]
    for tipo, entrada in (("cor", "Base Color"), ("emissao", "Emission Color")):
        no = nt.nodes.new("ShaderNodeTexImage")
        no.image = imagens[tipo]
        nt.links.new(no.outputs["Color"], bsdf.inputs[entrada])
    bsdf.inputs["Emission Strength"].default_value = emissao
    bsdf.inputs["Metallic"].default_value = metalico
    bsdf.inputs["Roughness"].default_value = rugosidade
    obj.data.materials.clear()
    obj.data.materials.append(final)
    for p in obj.data.polygons:
        p.material_index = 0
