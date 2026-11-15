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


def casca(nome, perfil, abertura, seg=40, escala_y=1.0, dobra=None):
    """Superfície de revolução em torno de Z aberta na frente (−Y). `perfil` = [(raio, z)];
    `abertura(z)` = meio ângulo da abertura em rad; `dobra(th, z)` soma ao raio (pregas do
    pano). Fica sem espessura (usar `engrossar`)."""
    bm = bmesh.new()
    aneis = []
    for r, z in perfil:
        a0 = max(abertura(z), 1e-3)
        anel = []
        for k in range(seg):
            th = a0 + (2 * math.pi - 2 * a0) * k / (seg - 1)
            rr = r + (dobra(th, z) if dobra else 0.0)
            anel.append(bm.verts.new((rr * math.sin(th), -rr * math.cos(th) * escala_y, z)))
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


def liso(obj, nivel=1):
    """Subdivisão (Catmull-Clark) para o pano e as placas curvas não mostrarem as facetas."""
    mod = obj.modifiers.new("liso", "SUBSURF")
    mod.levels = mod.render_levels = nivel
    return suave(obj)


def aplicar(obj):
    """Aplica os modificadores do objeto na malha (sem operador, pelo depsgraph)."""
    dg = bpy.context.evaluated_depsgraph_get()
    malha = bpy.data.meshes.new_from_object(obj.evaluated_get(dg))
    obj.modifiers.clear()
    obj.data = malha
    return obj


def booleana(obj, outros, operacao="DIFFERENCE"):
    """Une ou recorta `outros` em `obj` (solver exato) e apaga os outros da cena."""
    for o in outros:
        aplicar(o)
        mod = obj.modifiers.new("bool", "BOOLEAN")
        mod.operation = operacao
        mod.solver = "EXACT"
        mod.object = o
        aplicar(obj)
        bpy.data.objects.remove(o)
    return obj


def amassar(obj, forca=0.006, escala=0.06, nivel=2):
    """Rugas finas de pano: subdivide e desloca pela normal com um ruído de nuvens."""
    mod = obj.modifiers.new("liso", "SUBSURF")
    mod.levels = mod.render_levels = nivel
    tex = bpy.data.textures.new(obj.name + "_rugas", "CLOUDS")
    tex.noise_scale = escala
    tex.noise_depth = 3
    desl = obj.modifiers.new("rugas", "DISPLACE")
    desl.texture = tex
    desl.texture_coords = "LOCAL"
    desl.strength = forca
    desl.mid_level = 0.5
    return suave(obj)


def mao(nome, pulso, d, n, palma=0.085, largura=0.08, espessura=0.028, dedo=0.08, raio=0.0105,
        curva=0.35, ponta=0.85):
    """Mão com palma, quatro dedos de duas falanges e polegar. `d` = direção do braço (para os
    dedos), `n` = lado da palma (os dedos dobram para ele). Devolve a lista de peças."""
    d, n = Vector(d).normalized(), Vector(n).normalized()
    w = d.cross(n).normalized()
    frente = -1.0 if w.y > 0 else 1.0           # polegar para a frente (−Y)
    pulso = Vector(pulso)
    pecas = []
    pal = caixa(f"{nome}_palma", (0, 0, 0), (1, 1, 1), 0.35)
    orientar(pal, pulso + d * (palma / 2), d)
    pal.scale = (espessura / 2, largura / 2, palma / 2)
    pecas.append(pal)

    def falange(rotulo, a, b, r0, r1):
        pecas.append(suave(segmento(rotulo, a, b, [(0.0, -0.1), (r0 * 0.9, 0.0), (r0, 0.25),
                                                    (r1, 0.85), (r1 * 0.6, 1.05), (0.0, 1.12)], 10)))

    for i, fator in enumerate((0.9, 1.0, 0.95, 0.78)):
        off = (i - 1.5) / 1.5 * largura * 0.36
        k = pulso + d * palma + w * off
        l = dedo * fator
        d1 = (d * math.cos(curva) + n * math.sin(curva)).normalized()
        d2 = (d * math.cos(2.2 * curva) + n * math.sin(2.2 * curva)).normalized()
        m = k + d1 * l * 0.55
        falange(f"{nome}_dedo{i}a", k - d * 0.008, m, raio, raio * 0.95)
        falange(f"{nome}_dedo{i}b", m, m + d2 * l * 0.45, raio * 0.92, raio * ponta)
    base = pulso + d * palma * 0.3 + w * frente * largura * 0.42 + n * espessura * 0.25
    t1 = (d * 0.55 + n * 0.45 + w * frente * 0.35).normalized()
    t2 = (d * 0.8 + n * 0.55).normalized()
    meio = base + t1 * dedo * 0.5
    falange(f"{nome}_polegar_a", base, meio, raio * 1.15, raio * 1.05)
    falange(f"{nome}_polegar_b", meio, meio + t2 * dedo * 0.38, raio * 1.0, raio * ponta)
    return pecas


# ---------------------------------------------------------------- materiais

def acabamento(nt, cor, ao=0.6, borda=None, forca_borda=1.0):
    """Leva `cor` (socket ou RGBA) ao jeito do guia de estilo: pinceladas largas (variação de
    valor em manchas grandes), sombra de oclusão pintada nas reentrâncias e borda que pega luz
    nas quinas (`borda` = cor da quina, ex. aço-gume). Devolve o socket da cor final."""
    N = nt.nodes
    coord = N.new("ShaderNodeTexCoord")
    pincel = N.new("ShaderNodeTexNoise")
    pincel.inputs["Scale"].default_value = 7.0
    pincel.inputs["Detail"].default_value = 1.5
    pincel.inputs["Distortion"].default_value = 0.8
    nt.links.new(coord.outputs["Object"], pincel.inputs["Vector"])
    faixa = N.new("ShaderNodeMapRange")
    faixa.inputs["From Min"].default_value = 0.3
    faixa.inputs["From Max"].default_value = 0.7
    faixa.inputs["To Min"].default_value = 0.88
    faixa.inputs["To Max"].default_value = 1.1
    nt.links.new(pincel.outputs["Fac"], faixa.inputs["Value"])
    mult = N.new("ShaderNodeMix")
    mult.data_type = "RGBA"
    mult.blend_type = "MULTIPLY"
    mult.inputs["Factor"].default_value = 1.0
    if isinstance(cor, bpy.types.NodeSocket):
        nt.links.new(cor, mult.inputs[6])
    else:
        mult.inputs[6].default_value = cor
    cinza = N.new("ShaderNodeCombineColor")
    for k in range(3):
        nt.links.new(faixa.outputs["Result"], cinza.inputs[k])
    nt.links.new(cinza.outputs["Color"], mult.inputs[7])
    saida = mult.outputs[2]

    if ao:
        oclusao = N.new("ShaderNodeAmbientOcclusion")
        oclusao.inputs["Distance"].default_value = 0.12
        oclusao.samples = 8
        inv = N.new("ShaderNodeMath")
        inv.operation = "MULTIPLY_ADD"
        inv.inputs[1].default_value = -ao
        inv.inputs[2].default_value = ao
        nt.links.new(oclusao.outputs["AO"], inv.inputs[0])          # ao·(1 − AO)
        sombra = N.new("ShaderNodeMix")
        sombra.data_type = "RGBA"
        sombra.blend_type = "MULTIPLY"
        nt.links.new(inv.outputs[0], sombra.inputs["Factor"])
        nt.links.new(saida, sombra.inputs[6])
        sombra.inputs[7].default_value = (0.16, 0.12, 0.2, 1.0)     # sombra fria, puxada ao véu
        saida = sombra.outputs[2]

    if borda is not None:
        chanfro = N.new("ShaderNodeBevel")
        chanfro.samples = 8
        chanfro.inputs["Radius"].default_value = 0.008
        geo = N.new("ShaderNodeNewGeometry")
        dot = N.new("ShaderNodeVectorMath")
        dot.operation = "DOT_PRODUCT"
        nt.links.new(chanfro.outputs["Normal"], dot.inputs[0])
        nt.links.new(geo.outputs["Normal"], dot.inputs[1])
        quina = N.new("ShaderNodeMapRange")
        quina.inputs["From Min"].default_value = 0.995
        quina.inputs["From Max"].default_value = 0.93
        quina.inputs["To Max"].default_value = forca_borda
        nt.links.new(dot.outputs["Value"], quina.inputs["Value"])
        # Superfícies lisas não têm quina: o contorno da forma (onde ela vira para longe do
        # olho) também pega a cor da borda, como o brilho pintado numa placa curva.
        perfil = N.new("ShaderNodeLayerWeight")
        perfil.inputs["Blend"].default_value = 0.35
        contorno = N.new("ShaderNodeMapRange")
        contorno.inputs["From Min"].default_value = 0.55
        contorno.inputs["From Max"].default_value = 0.95
        contorno.inputs["To Max"].default_value = 0.7 * forca_borda
        nt.links.new(perfil.outputs["Facing"], contorno.inputs["Value"])
        juntos = N.new("ShaderNodeMath")
        juntos.operation = "MAXIMUM"
        nt.links.new(quina.outputs["Result"], juntos.inputs[0])
        nt.links.new(contorno.outputs["Result"], juntos.inputs[1])
        saida = em.mistura(nt, juntos.outputs[0], saida, em.rgba(borda))
    return saida


def _no(nt, tipo, entradas=None, **props):
    no = nt.nodes.new(tipo)
    for k, v in props.items():
        setattr(no, k, v)
    for k, v in (entradas or {}).items():
        if isinstance(v, bpy.types.NodeSocket):
            nt.links.new(v, no.inputs[k])
        else:
            no.inputs[k].default_value = v
    return no


def _soma(nt, a, b, peso_b=1.0):
    return _no(nt, "ShaderNodeMath", {0: b, 1: peso_b, 2: a}, operation="MULTIPLY_ADD").outputs[0]


def relevo(nt, bsdf, tipo, forca=1.0, rugosidade=0.6):
    """Relevo físico por tipo de superfície (Bump na normal) e rugosidade que varia: couro
    granulado e vincado, aço martelado e riscado, pano com trama e amassado, osso poroso e
    rachado. Coordenadas de objeto, então o desenho não depende de UV."""
    obj = _no(nt, "ShaderNodeTexCoord").outputs["Object"]

    def ruido(escala, detalhe=4.0, vetor=None, esticar=None):
        v = vetor or obj
        if esticar:
            v = _no(nt, "ShaderNodeVectorMath", {0: v, 1: esticar}, operation="MULTIPLY").outputs[0]
        return _no(nt, "ShaderNodeTexNoise", {"Vector": v, "Scale": escala, "Detail": detalhe,
                                               "Roughness": 0.6}).outputs["Fac"]

    def voronoi(escala, saida="Distance", feature="F1"):
        return _no(nt, "ShaderNodeTexVoronoi", {"Vector": obj, "Scale": escala},
                   feature=feature).outputs[saida]

    if tipo == "pele":
        altura = _soma(nt, voronoi(45.0), ruido(110.0, 6.0), 0.6)
        risco = ruido(8.0, 4.0)
        dist = 0.002
    elif tipo == "couro":
        altura = _soma(nt, voronoi(260.0), ruido(9.0, 8.0, esticar=(1.0, 1.0, 5.0)), 1.4)
        risco = ruido(14.0, 6.0)
        dist = 0.0025
    elif tipo == "aco":
        martelo = voronoi(32.0, "Distance", "SMOOTH_F1")
        risco = ruido(3.0, 12.0, esticar=(1.0, 1.0, 45.0))
        altura = _soma(nt, martelo, risco, 0.35)
        dist = 0.0012
    elif tipo == "pano":
        trama = _no(nt, "ShaderNodeTexWave", {"Vector": obj, "Scale": 420.0, "Distortion": 1.5},
                    wave_type="BANDS", bands_direction="DIAGONAL").outputs["Fac"]
        altura = _soma(nt, trama, ruido(6.0, 6.0), 3.0)
        risco = ruido(11.0, 5.0)
        dist = 0.003
    else:  # osso
        racha = voronoi(16.0, "Distance", "DISTANCE_TO_EDGE")
        racha = _no(nt, "ShaderNodeMapRange", {"Value": racha, "From Min": 0.0, "From Max": 0.04}).outputs[0]
        altura = _soma(nt, ruido(60.0, 8.0), racha, 2.0)
        risco = ruido(20.0, 6.0)
        dist = 0.002
    bump = _no(nt, "ShaderNodeBump", {"Height": altura, "Strength": 0.55 * forca, "Distance": dist})
    nt.links.new(bump.outputs["Normal"], bsdf.inputs["Normal"])
    rug = _no(nt, "ShaderNodeMapRange", {"Value": risco, "From Min": 0.3, "From Max": 0.7,
                                          "To Min": rugosidade * 0.75, "To Max": min(1.0, rugosidade * 1.25)})
    nt.links.new(rug.outputs[0], bsdf.inputs["Roughness"])
    return altura


def material(nome, cor, rugosidade=0.7, metalico=0.0, variacao=0.0, emissao=0.0, ao=0.6,
             borda=None, superficie=None, forca_relevo=1.0):
    """`superficie` ("couro", "aco", "pano", "osso") liga o relevo físico de `relevo`."""
    m, nt, bsdf = em.mat(nome)
    bsdf.inputs["Roughness"].default_value = rugosidade
    bsdf.inputs["Metallic"].default_value = metalico
    if variacao:
        r = em.ruido(nt, 22.0, 4.0)
        escuro = tuple(c * (1 - variacao) for c in em.rgba(cor)[:3]) + (1.0,)
        base = em.mistura(nt, r.outputs["Fac"], escuro, em.rgba(cor))
    else:
        base = em.rgba(cor)
    if emissao:
        bsdf.inputs["Base Color"].default_value = em.rgba(cor)
        bsdf.inputs["Emission Color"].default_value = em.rgba(cor)
        bsdf.inputs["Emission Strength"].default_value = emissao
    else:
        nt.links.new(acabamento(nt, base, ao, borda), bsdf.inputs["Base Color"])
        if superficie:
            relevo(nt, bsdf, superficie, forca_relevo, rugosidade)
        if superficie == "pele":
            # Pele úmida: luz entra um pouco (subsuperfície) e uma película brilhante por cima.
            bsdf.inputs["Subsurface Weight"].default_value = 0.35
            bsdf.inputs["Subsurface Radius"].default_value = (0.8, 0.25, 0.6)
            bsdf.inputs["Subsurface Scale"].default_value = 0.01
            bsdf.inputs["Coat Weight"].default_value = 0.25
            bsdf.inputs["Coat Roughness"].default_value = 0.35
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


def mat_runas(nome, base, cor_runa, rugosidade=0.55, metalico=0.3, brilho=0.0, cor_barra=None,
              faixas=True, sujeira=0.0, superficie=None):
    """Pano ou placa pela UV da grade (u na largura, v na altura): barra nas bordas, uma coluna
    central de runas gravadas (`imagem_runas`), faixas finas na horizontal e o resto liso. Com
    `cor_barra`, barra e faixas usam essa cor e só as runas levam `cor_runa` e brilho (guia: runa
    em no máximo 5% da área)."""
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
    if not faixas:
        faixa = op("MULTIPLY", faixa, 0.0)
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
    ornato = op("MAXIMUM", borda, faixa)
    if cor_barra:
        fac = runa
        cor = em.mistura(nt, fac, em.mistura(nt, ornato, em.rgba(base), em.rgba(cor_barra)),
                         em.rgba(cor_runa))
    else:
        fac = op("MAXIMUM", ornato, runa)
        cor = em.mistura(nt, fac, em.rgba(base), em.rgba(cor_runa))
    if sujeira:
        # Barra encardida: escurece de baixo (v = 1) para cima, com borda irregular.
        irregular = em.ruido(nt, 9.0, 3.0).outputs["Fac"]
        # UV da grade: y = 1 em cima, 0 na barra.
        sobe = op("SUBTRACT", op("ADD", op("MULTIPLY", irregular, 0.25), 1.0), sep.outputs["Y"])
        grau = op("MULTIPLY", op("POWER", op("MINIMUM", op("MAXIMUM", op("MULTIPLY", op("SUBTRACT", sobe, 0.55), 2.2), 0.0), 1.0), 1.3), sujeira)
        cor = em.mistura(nt, op("MINIMUM", grau, 1.0), cor, (0.10, 0.075, 0.06, 1.0))
    nt.links.new(acabamento(nt, cor, 0.5), bsdf.inputs["Base Color"])
    if superficie:
        relevo(nt, bsdf, superficie, 1.0, rugosidade)
    if brilho:
        nt.links.new(cor, bsdf.inputs["Emission Color"])
        forca = N.new("ShaderNodeMath")
        forca.operation = "MULTIPLY"
        forca.inputs[1].default_value = brilho
        nt.links.new(fac, forca.inputs[0])
        nt.links.new(forca.outputs[0], bsdf.inputs["Emission Strength"])
    return m


# ---------------------------------------------------------------- render

LUZ_HEROI = "#ffb36b"


def render(pasta, alvo_z=0.92, tamanho=1024, escala_orto=2.0, amostras=96):
    """Folha: frente, lado (de perfil, olhando para a direita da imagem), costas e 3/4, com
    fundo transparente e luz neutra, sem contorno (o guia de estilo não usa). Depois a prova
    de luz do jogo: fundo em breu e só uma luz quente por cima, como a HeroLight, mais um fio
    violeta por trás (`jogo_frente`, `jogo_tres_quartos`)."""
    cena = bpy.context.scene
    ed._cycles_cpu(amostras)
    cena.cycles.use_denoising = True
    cena.render.resolution_x = cena.render.resolution_y = tamanho
    cena.render.image_settings.file_format = "PNG"
    cena.render.image_settings.color_mode = "RGBA"
    cena.view_settings.view_transform = "AgX"
    try:
        cena.view_settings.look = "AgX - Medium High Contrast"
    except TypeError:
        pass
    cena.render.use_freestyle = False

    mundo = bpy.data.worlds.new("conceito")
    mundo.use_nodes = True
    wt = mundo.node_tree
    fundo = wt.nodes["Background"]
    # Céu em degradê (chão escuro, horizonte médio, alto claro): o metal tem o que refletir.
    direcao = wt.nodes.new("ShaderNodeTexCoord")
    sep = wt.nodes.new("ShaderNodeSeparateXYZ")
    wt.links.new(direcao.outputs["Generated"], sep.inputs["Vector"])
    altura = wt.nodes.new("ShaderNodeMapRange")
    altura.inputs["From Min"].default_value = -1.0
    wt.links.new(sep.outputs["Z"], altura.inputs["Value"])
    ceu = em.rampa(wt, altura.outputs["Result"], [(0.0, (0.06, 0.06, 0.07, 1)), (0.48, (0.32, 0.32, 0.34, 1)),
                                          (0.56, (0.55, 0.55, 0.58, 1)), (1.0, (0.95, 0.95, 0.97, 1))])
    ligacao_ceu = wt.links.new(ceu.outputs["Color"], fundo.inputs["Color"])
    cena.world = mundo
    sol = bpy.data.objects.new("sol", bpy.data.lights.new("sol", "SUN"))
    sol.data.angle = math.radians(25)
    cena.collection.objects.link(sol)
    heroi = bpy.data.objects.new("luz_heroi", bpy.data.lights.new("luz_heroi", "POINT"))
    heroi.data.color = em.rgba(LUZ_HEROI)[:3]
    heroi.data.shadow_soft_size = 0.25
    cena.collection.objects.link(heroi)
    contra = bpy.data.objects.new("contraluz", bpy.data.lights.new("contraluz", "AREA"))
    contra.data.color = em.rgba(em.RUNA)[:3]
    contra.data.size = 1.5
    cena.collection.objects.link(contra)

    cam = bpy.data.objects.new("cam", bpy.data.cameras.new("cam"))
    cena.collection.objects.link(cam)
    cena.camera = cam
    alvo = Vector((0, 0, alvo_z))
    os.makedirs(pasta, exist_ok=True)

    def mirar(direcao, orto):
        d = direcao.normalized()
        if orto:
            cam.data.type = "ORTHO"
            cam.data.ortho_scale = escala_orto
            cam.location = alvo + d * 6
        else:
            cam.data.type = "PERSP"
            cam.data.lens = 50
            cam.location = alvo + d * 3.3
        cam.rotation_euler = (alvo - cam.location).to_track_quat("-Z", "Y").to_euler()
        return d

    def foto(nome):
        cena.render.filepath = os.path.join(pasta, nome + ".png")
        bpy.ops.render.render(write_still=True)

    # Folha: luz neutra.
    cena.render.film_transparent = True
    fundo.inputs["Strength"].default_value = 0.9
    sol.data.energy = 2.6
    heroi.data.energy = contra.data.energy = 0.0
    vistas = [
        ("frente", Vector((0, -1, 0)), True),
        ("lado", Vector((-1, 0, 0)), True),   # câmera à direita do personagem: ele olha para a direita
        ("costas", Vector((0, 1, 0)), True),
        ("tres_quartos", Vector((-0.55, -0.83, 0.18)), False),
    ]
    for nome, direcao, orto in vistas:
        d = mirar(direcao, orto)
        # Sol sempre vindo de cima, um pouco à esquerda e de frente para a câmera.
        luz = (d + Vector((0, 0, 1.2)) + d.cross(Vector((0, 0, 1))) * 0.5).normalized()
        sol.rotation_euler = (-luz).to_track_quat("-Z", "Y").to_euler()
        foto(nome)

    # Prova de luz do jogo: breu, luz quente do herói por cima e na frente, fio violeta atrás.
    cena.render.film_transparent = False
    wt.links.remove(ligacao_ceu)
    fundo.inputs["Color"].default_value = em.rgba(em.BREU)
    fundo.inputs["Strength"].default_value = 1.0
    sol.data.energy = 0.0
    heroi.data.energy = 260.0
    heroi.location = (0.35, -1.1, 2.4)
    contra.data.energy = 60.0
    contra.location = (0.0, 1.4, 2.0)
    contra.rotation_euler = (Vector((0, 0, alvo_z)) - contra.location).to_track_quat("-Z", "Y").to_euler()
    for nome, direcao, orto in (("jogo_frente", Vector((0, -1, 0)), True),
                                ("jogo_tres_quartos", Vector((-0.55, -0.83, 0.18)), False)):
        mirar(direcao, orto)
        foto(nome)
