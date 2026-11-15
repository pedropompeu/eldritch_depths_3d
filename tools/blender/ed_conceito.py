"""Blockout de personagem para folha de conceito (B05, B11): peças, materiais e render.

Os scripts `build_conceito.py` de cada personagem montam o corpo com estas peças e chamam
`render`, que grava frente, lado, costas (ortográficas, mesma escala) e 3/4 com fundo
transparente; `tools/folha_conceito.py` junta as três primeiras sobre cinza.
Escala: 1 unidade = 1 m, Z para cima, pés em z = 0, olhando para −Y.
"""
import math
import os

import bpy
import bmesh
from mathutils import Matrix, Vector

import ed_blender as ed
import ed_modelagem as em


# ---------------------------------------------------------------- geometria

def orientar(obj, origem, direcao):
    """Põe o +Z local de `obj` ao longo de `direcao`, com o +Y local o mais perto do +Y do mundo."""
    rot = Vector(direcao).normalized().to_track_quat("Z", "Y").to_matrix().to_4x4()
    obj.matrix_world = Matrix.Translation(Vector(origem)) @ rot
    return obj


def segmento(nome, a, b, perfil, seg=14):
    """Sólido de revolução de `a` a `b`. `perfil` = [(raio, t)], t de 0 (em a) a 1 (em b)."""
    a, b = Vector(a), Vector(b)
    comp = (b - a).length
    obj = em.torno(nome, [(r, t * comp) for r, t in perfil], seg)
    return orientar(obj, a, b - a)


def casca(nome, perfil, abertura, seg=40, escala_y=1.0):
    """Superfície de revolução em torno de Z aberta na frente (−Y). `perfil` = [(raio, z)];
    `abertura(z)` = meio ângulo da abertura em rad. Fica sem espessura (usar `engrossar`)."""
    bm = bmesh.new()
    aneis = []
    for r, z in perfil:
        a0 = max(abertura(z), 1e-3)
        anel = []
        for k in range(seg):
            th = a0 + (2 * math.pi - 2 * a0) * k / (seg - 1)
            anel.append(bm.verts.new((r * math.sin(th), -r * math.cos(th) * escala_y, z)))
        aneis.append(anel)
    for a, b in zip(aneis, aneis[1:]):
        for k in range(seg - 1):
            bm.faces.new((a[k], a[k + 1], b[k + 1], b[k]))
    return _objeto(nome, bm)


def grade(nome, nx, nz, ponto):
    """Folha (nx × nz vértices); `ponto(u, v)` com u, v em [0, 1] devolve (x, y, z)."""
    bm = bmesh.new()
    vs = [[bm.verts.new(ponto(i / (nx - 1), j / (nz - 1))) for i in range(nx)] for j in range(nz)]
    uv = bm.loops.layers.uv.new("UVMap")
    for j in range(nz - 1):
        for i in range(nx - 1):
            f = bm.faces.new((vs[j][i], vs[j][i + 1], vs[j + 1][i + 1], vs[j + 1][i]))
            for loop, (a, b) in zip(f.loops, ((i, j), (i + 1, j), (i + 1, j + 1), (i, j + 1))):
                loop[uv].uv = (a / (nx - 1), 1 - b / (nz - 1))
    return _objeto(nome, bm)


def _objeto(nome, bm):
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    malha = bpy.data.meshes.new(nome)
    bm.to_mesh(malha)
    bm.free()
    obj = bpy.data.objects.new(nome, malha)
    bpy.context.scene.collection.objects.link(obj)
    return obj


def engrossar(obj, espessura, mat_dentro=None):
    """Solidify; com `mat_dentro`, a face de dentro leva esse material (o breu do capuz)."""
    mod = obj.modifiers.new("espessura", "SOLIDIFY")
    mod.thickness = espessura
    mod.offset = -1.0
    if mat_dentro is not None:
        obj.data.materials.append(mat_dentro)
        mod.material_offset = 1
    return obj


def esfera(nome, raio, local, escala=(1, 1, 1), sub=3):
    bpy.ops.mesh.primitive_uv_sphere_add(radius=raio, location=local, segments=8 * sub,
                                         ring_count=4 * sub)
    obj = bpy.context.view_layer.objects.active
    obj.name = nome
    obj.scale = escala
    return obj


def gema(nome, raio, local):
    bpy.ops.mesh.primitive_ico_sphere_add(radius=raio, subdivisions=1, location=local)
    obj = bpy.context.view_layer.objects.active
    obj.name = nome
    return obj


def caixa(nome, centro, meio, chanfro=0.0, rotacao=None):
    bpy.ops.mesh.primitive_cube_add(size=2.0, location=centro)
    obj = bpy.context.view_layer.objects.active
    obj.name = nome
    obj.scale = meio
    if rotacao is not None:
        obj.rotation_euler = rotacao
    if chanfro:
        mod = obj.modifiers.new("chanfro", "BEVEL")
        mod.width = chanfro
        mod.segments = 2
    return obj


def suave(obj):
    for p in obj.data.polygons:
        p.use_smooth = True
    return obj


# ---------------------------------------------------------------- materiais

def material(nome, cor, rugosidade=0.7, metalico=0.0, variacao=0.0, emissao=0.0):
    m, nt, bsdf = em.mat(nome)
    bsdf.inputs["Roughness"].default_value = rugosidade
    bsdf.inputs["Metallic"].default_value = metalico
    if variacao:
        r = em.ruido(nt, 22.0, 4.0)
        escuro = tuple(c * (1 - variacao) for c in em.rgba(cor)[:3]) + (1.0,)
        nt.links.new(em.mistura(nt, r.outputs["Fac"], escuro, em.rgba(cor)), bsdf.inputs["Base Color"])
    else:
        bsdf.inputs["Base Color"].default_value = em.rgba(cor)
    if emissao:
        bsdf.inputs["Emission Color"].default_value = em.rgba(cor)
        bsdf.inputs["Emission Strength"].default_value = emissao
    return m


def imagem_runas(largura=128, altura=1024, linhas=11, semente=7):
    """Coluna de glifos angulosos (haste vertical e traços de runa) no alfa de uma imagem.
    Sorteio fixo, então a coluna sai igual a cada build."""
    import random
    import numpy as np

    sorteio = random.Random(semente)
    alfa = np.zeros((altura, largura), dtype=np.float32)
    passo = altura / linhas
    w, h = largura * 0.5, passo * 0.62          # tamanho do glifo
    ys, xs = np.mgrid[0:altura, 0:largura]

    def traco(a, b, grossura=5.0):
        (x0, y0), (x1, y1) = a, b
        dx, dy = x1 - x0, y1 - y0
        t = np.clip(((xs - x0) * dx + (ys - y0) * dy) / (dx * dx + dy * dy + 1e-9), 0, 1)
        d = np.hypot(xs - (x0 + t * dx), ys - (y0 + t * dy))
        np.maximum(alfa, np.clip(grossura - d, 0, 1), out=alfa)

    for n in range(linhas):
        cx, cy = largura / 2, (n + 0.5) * passo
        topo, base = (cx, cy - h / 2), (cx, cy + h / 2)
        e, d = cx - w / 2, cx + w / 2
        traco(topo, base)                                     # haste
        opcoes = [
            ((cx, cy - h / 2), (d, cy - h / 6)),              # galho de cima para a direita
            ((cx, cy - h / 6), (d, cy + h / 6)),              # galho do meio
            ((cx, cy - h / 2), (e, cy - h / 6)),              # galho de cima para a esquerda
            ((e, cy), (d, cy - h / 4)),                       # corte diagonal
            ((cx, cy - h / 6), (d, cy - h / 3)),              # bandeira
            ((d, cy - h / 6), (cx, cy + h / 6)),              # volta do galho
            ((e, cy + h / 6), (cx, cy - h / 6)),              # cunha à esquerda
        ]
        for a, b in sorteio.sample(opcoes, sorteio.choice((1, 2, 2, 3))):
            traco(a, b)

    img = bpy.data.images.new("runas", largura, altura, alpha=True)
    px = np.ones((altura, largura, 4), dtype=np.float32)
    px[..., 3] = alfa[::-1]                                   # imagem do Blender começa embaixo
    img.pixels.foreach_set(px.ravel())
    img.pack()
    return img


def mat_runas(nome, base, cor_runa, rugosidade=0.55, metalico=0.3, brilho=0.0):
    """Pano ou placa pela UV da grade (u na largura, v na altura): barra escura nas bordas, uma
    coluna central de runas gravadas (`imagem_runas`), faixas finas na horizontal e o resto liso."""
    m, nt, bsdf = em.mat(nome)
    bsdf.inputs["Roughness"].default_value = rugosidade
    bsdf.inputs["Metallic"].default_value = metalico
    N = nt.nodes
    coord = N.new("ShaderNodeTexCoord")
    sep = N.new("ShaderNodeSeparateXYZ")
    nt.links.new(coord.outputs["UV"], sep.inputs["Vector"])

    def op(tipo, a, b=None, c=None):
        no = N.new("ShaderNodeMath")
        no.operation = tipo
        for i, v in enumerate((a, b, c)):
            if v is None:
                continue
            if isinstance(v, bpy.types.NodeSocket):
                nt.links.new(v, no.inputs[i])
            else:
                no.inputs[i].default_value = v
        return no.outputs[0]

    du = op("ABSOLUTE", op("SUBTRACT", sep.outputs["X"], 0.5))           # 0 no centro, 0,5 na borda
    borda = op("GREATER_THAN", du, 0.43)
    faixa = op("LESS_THAN", op("PINGPONG", op("MULTIPLY", sep.outputs["Y"], 7.0), 0.5), 0.03)
    # Coluna central (u de 0,3 a 0,7) com a textura de runas, sem repetir.
    mapa = N.new("ShaderNodeVectorMath")
    mapa.operation = "MULTIPLY_ADD"
    mapa.inputs[1].default_value = (2.5, 1.0, 1.0)
    mapa.inputs[2].default_value = (-0.75, 0.0, 0.0)
    nt.links.new(coord.outputs["UV"], mapa.inputs[0])
    tex = N.new("ShaderNodeTexImage")
    tex.image = imagem_runas()
    tex.extension = "CLIP"
    tex.interpolation = "Cubic"
    nt.links.new(mapa.outputs[0], tex.inputs["Vector"])
    runa = tex.outputs["Alpha"]
    fac = op("MAXIMUM", op("MAXIMUM", borda, faixa), runa)
    cor = em.mistura(nt, fac, em.rgba(base), em.rgba(cor_runa))
    nt.links.new(cor, bsdf.inputs["Base Color"])
    if brilho:
        nt.links.new(cor, bsdf.inputs["Emission Color"])
        forca = N.new("ShaderNodeMath")
        forca.operation = "MULTIPLY"
        forca.inputs[1].default_value = brilho
        nt.links.new(fac, forca.inputs[0])
        nt.links.new(forca.outputs[0], bsdf.inputs["Emission Strength"])
    return m


# ---------------------------------------------------------------- render

def render(pasta, alvo_z=0.92, tamanho=1024, escala_orto=2.0):
    """Frente, lado (de perfil, olhando para a direita da imagem), costas e 3/4, com fundo
    transparente, luz uniforme e contorno (Freestyle)."""
    cena = bpy.context.scene
    ed._cycles_cpu(64)
    cena.render.resolution_x = cena.render.resolution_y = tamanho
    cena.render.film_transparent = True
    cena.render.image_settings.file_format = "PNG"
    cena.render.image_settings.color_mode = "RGBA"
    cena.view_settings.view_transform = "Standard"
    cena.render.use_freestyle = True
    cena.render.line_thickness_mode = "ABSOLUTE"
    cena.render.line_thickness = 1.3
    fs = cena.view_layers[0].freestyle_settings
    ls = fs.linesets[0] if fs.linesets else fs.linesets.new("contorno")
    if ls.linestyle is None:
        ls.linestyle = bpy.data.linestyles.new("contorno")
    ls.linestyle.color = (0.04, 0.035, 0.05)

    mundo = bpy.data.worlds.new("conceito")
    mundo.use_nodes = True
    fundo = mundo.node_tree.nodes["Background"]
    fundo.inputs["Color"].default_value = (0.55, 0.55, 0.57, 1)
    fundo.inputs["Strength"].default_value = 1.0
    cena.world = mundo
    sol = bpy.data.objects.new("sol", bpy.data.lights.new("sol", "SUN"))
    sol.data.energy = 2.2
    sol.data.angle = math.radians(25)
    cena.collection.objects.link(sol)

    cam = bpy.data.objects.new("cam", bpy.data.cameras.new("cam"))
    cena.collection.objects.link(cam)
    cena.camera = cam
    alvo = Vector((0, 0, alvo_z))
    os.makedirs(pasta, exist_ok=True)
    vistas = [
        ("frente", Vector((0, -1, 0)), True),
        ("lado", Vector((-1, 0, 0)), True),   # câmera à direita do personagem: ele olha para a direita
        ("costas", Vector((0, 1, 0)), True),
        ("tres_quartos", Vector((-0.55, -0.83, 0.18)), False),
    ]
    for nome, direcao, orto in vistas:
        d = direcao.normalized()
        # Sol sempre vindo de cima, um pouco à esquerda e de frente para a câmera.
        luz = (d + Vector((0, 0, 1.2)) + d.cross(Vector((0, 0, 1))) * 0.5).normalized()
        sol.rotation_euler = (-luz).to_track_quat("-Z", "Y").to_euler()
        if orto:
            cam.data.type = "ORTHO"
            cam.data.ortho_scale = escala_orto
            cam.location = alvo + d * 6
        else:
            cam.data.type = "PERSP"
            cam.data.lens = 50
            cam.location = alvo + d * 4.6
        cam.rotation_euler = (alvo - cam.location).to_track_quat("-Z", "Y").to_euler()
        cena.render.filepath = os.path.join(pasta, nome + ".png")
        bpy.ops.render.render(write_still=True)
