"""Conceito do Cultista (B11) por blockout 3D: modelado por script e renderizado em três vistas.

Rodar da raiz: tools/blender.sh art/inimigos/cultista/build_conceito.py
Saídas: .godot/capturas_tmp/cultista_conceito/{frente,lado,costas,tres_quartos}.png (fundo
transparente). A folha sai de `tools/folha_conceito.py`.

Fiel ao cultist.png do 2D: capuz carmim pontudo caindo para trás, rosto em breu com dois
olhos violeta acesos; capinha nos ombros e manto vinho aberto na frente, barra recortada em
pontas, bordas laranja-ferrugem; sobremanto violeta e azul com runas; três contas violeta
grandes no peito; cinto com medalhão violeta; tentáculos roxo-escuros com ventosas rosadas
saindo de baixo da barra, enrolando no chão e subindo nas pontas. Pose A, mãos vazias: a
adaga curva (B12) e a chama (efeito) ficam de fora.

Escala: 1 unidade = 1 m, Z para cima, pés em z = 0, olhando para −Y. Ponta do capuz ≈ 1,90 m.
"""
import math
import os
import sys

import bmesh
import bpy
from mathutils import Vector

RAIZ = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
sys.path.insert(0, os.path.join(RAIZ, "tools", "blender"))
import ed_blender as ed  # noqa: E402
import ed_conceito as ec  # noqa: E402
import ed_modelagem as em  # noqa: E402
from ed_conceito import (caixa, casca, engrossar, esfera, gema, grade,  # noqa: E402
                         segmento, suave)

TMP = os.path.join(RAIZ, ".godot", "capturas_tmp", "cultista_conceito")

CARMIM = "#8c1c2a"
VINHO = "#5e1726"
FERRUGEM = "#b45a2c"
SOBREMANTO = "#3b2a63"
SOBREMANTO_RUNA = "#7f6cff"
VESTE = "#2c2236"
COURO = "#3d2618"
MAO = "#3a3046"
TENTACULO = "#2f1d42"
VENTOSA = "#c47aa8"
OLHO = "#d26bff"
BREU = em.BREU
RUNA = em.RUNA

OMBRO = 0.19, 1.40
BRACO = 0.28, 0.25, 0.16
QUADRIL = 0.10, 0.92
JOELHO = 0.13, 0.50
TORNOZELO = 0.16, 0.09
ESCALA_Y = 0.66


# ---------------------------------------------------------------- materiais

def mat_borda(nome, base, borda, fundo=0.13, lado=0.035):
    """Pano pela UV da grade: borda laranja na barra (v perto de 0) e nas beiradas da frente
    (u perto de 0 ou 1), com o limite da barra tremido por ruído (pano gasto)."""
    m, nt, bsdf = em.mat(nome)
    bsdf.inputs["Roughness"].default_value = 0.85
    N = nt.nodes
    coord = N.new("ShaderNodeTexCoord")
    sep = N.new("ShaderNodeSeparateXYZ")
    nt.links.new(coord.outputs["UV"], sep.inputs["Vector"])
    r = em.ruido(nt, 30.0, 3.0)

    def op(tipo, a, b):
        no = N.new("ShaderNodeMath")
        no.operation = tipo
        for i, v in enumerate((a, b)):
            if isinstance(v, bpy.types.NodeSocket):
                nt.links.new(v, no.inputs[i])
            else:
                no.inputs[i].default_value = v
        return no.outputs[0]

    limite = op("ADD", op("MULTIPLY", r.outputs["Fac"], fundo * 0.6), fundo * 0.7)
    na_barra = op("LESS_THAN", sep.outputs["Y"], limite)
    du = op("ABSOLUTE", op("SUBTRACT", sep.outputs["X"], 0.5), 0.0)
    na_beira = op("GREATER_THAN", du, 0.5 - lado)
    fac = op("MAXIMUM", na_barra, na_beira)
    escuro = tuple(c * 0.75 for c in em.rgba(base)[:3]) + (1.0,)
    pano = em.mistura(nt, r.outputs["Fac"], escuro, em.rgba(base))
    nt.links.new(em.mistura(nt, fac, pano, em.rgba(borda)), bsdf.inputs["Base Color"])
    return m


def materiais():
    material = ec.material
    return {
        "capuz": material("capuz", CARMIM, 0.85, variacao=0.25),
        "capinha": mat_borda("capinha", CARMIM, FERRUGEM, fundo=0.16),
        "manto": mat_borda("manto", VINHO, FERRUGEM, fundo=0.12),
        "manga": material("manga", CARMIM, 0.85, variacao=0.25),
        "punho": material("punho", FERRUGEM, 0.8),
        "sobremanto": ec.mat_runas("sobremanto", SOBREMANTO, SOBREMANTO_RUNA, 0.8, 0.0, brilho=0.7),
        "veste": material("veste", VESTE, 0.85, variacao=0.2),
        "couro": material("couro", COURO, 0.7, variacao=0.2),
        "mao": material("mao", MAO, 0.7),
        "tentaculo": material("tentaculo", TENTACULO, 0.45, variacao=0.3),
        "ventosa": material("ventosa", VENTOSA, 0.5),
        "breu": material("breu", BREU, 1.0),
        "olho": material("olho", OLHO, 0.3, emissao=8.0),
        "runa": material("runa", RUNA, 0.3, emissao=3.0),
        "metal": material("metal", "#4a4652", 0.4, metalico=0.7),
    }


# ---------------------------------------------------------------- peças

def interpola(pts, z):
    pts = sorted(pts)
    if z <= pts[0][0]:
        return pts[0][1]
    for (z0, r0), (z1, r1) in zip(pts, pts[1:]):
        if z <= z1:
            return r0 + (r1 - r0) * (z - z0) / (z1 - z0)
    return pts[-1][1]


def manto(nome, raio, z_topo, fundo, abertura, nx=48, nz=22, escala_y=ESCALA_Y):
    """Pano em volta do corpo, aberto na frente, com a barra em `fundo(θ)`.
    `raio(z)`, `abertura(z)` em rad. UV: u em volta (0 e 1 nas beiradas da frente), v de 0
    (barra) a 1 (topo)."""
    def ponto(u, v):
        z_alvo = z_topo - v * z_topo                       # chute para a abertura
        a0 = abertura(z_alvo)
        th = a0 + (2 * math.pi - 2 * a0) * u
        zb = fundo(th)
        z = z_topo - v * (z_topo - zb)
        a0 = abertura(z)
        th = a0 + (2 * math.pi - 2 * a0) * u
        r = raio(z)
        return (r * math.sin(th), -r * math.cos(th) * escala_y, z)
    return grade(nome, nx, nz, ponto)


def tubo(nome, pontos, raios, lateral, amostras=56, seg=10):
    """Tubo por uma Catmull-Rom plana (no plano perpendicular a `lateral`), com raio
    interpolado de `raios`, ponta fechada. Devolve o objeto e as amostras (centro, raio,
    normal do lado de dentro da curva)."""
    P = [Vector(p) for p in pontos]
    L = Vector(lateral).normalized()

    def cr(t):
        n = len(P) - 1
        i = min(int(t * n), n - 1)
        s = t * n - i
        p0, p1, p2, p3 = P[max(i - 1, 0)], P[i], P[i + 1], P[min(i + 2, n)]
        return 0.5 * ((2 * p1) + (-p0 + p2) * s + (2 * p0 - 5 * p1 + 4 * p2 - p3) * s * s
                      + (-p0 + 3 * p1 - 3 * p2 + p3) * s ** 3)

    def raio(t):
        x = t * (len(raios) - 1)
        i = min(int(x), len(raios) - 2)
        return raios[i] + (raios[i + 1] - raios[i]) * (x - i)

    cs = [cr(k / (amostras - 1)) for k in range(amostras)]
    bm = bmesh.new()
    aneis, dados = [], []
    for k, c in enumerate(cs):
        tg = (cs[min(k + 1, amostras - 1)] - cs[max(k - 1, 0)]).normalized()
        B = tg.cross(L).normalized()
        if B.z < 0 and k == 0:
            L = -L
            B = -B
        r = raio(k / (amostras - 1))
        aneis.append([bm.verts.new(c + r * (math.cos(2 * math.pi * j / seg) * L
                                            + math.sin(2 * math.pi * j / seg) * B))
                      for j in range(seg)])
        dados.append((c, r, B))
    for a, b in zip(aneis, aneis[1:]):
        for j in range(seg):
            bm.faces.new((a[j], a[(j + 1) % seg], b[(j + 1) % seg], b[j]))
    ponta = bm.verts.new(cs[-1] + (cs[-1] - cs[-2]).normalized() * raios[-1])
    for j in range(seg):
        bm.faces.new((aneis[-1][j], aneis[-1][(j + 1) % seg], ponta))
    bm.faces.new(list(reversed(aneis[0])))
    return ec._objeto(nome, bm), dados, L


def tentaculo(M, nome, phi, caminho, r0):
    """`caminho` = [(ρ, z)] no plano vertical que sai do centro no ângulo `phi` (0 = frente)."""
    rad = Vector((math.sin(phi), -math.cos(phi), 0))
    lat = Vector((math.cos(phi), math.sin(phi), 0))
    pts = [rad * rho + Vector((0, 0, z)) for rho, z in caminho]
    raios = [r0, r0 * 0.95, r0 * 0.8, r0 * 0.62, r0 * 0.45, r0 * 0.3, r0 * 0.18]
    obj, dados, L = tubo(nome, pts, raios, lat)
    p = [em.usar(suave(obj), M["tentaculo"])]
    for k in range(6, len(dados) - 3, 3):
        c, r, B = dados[k]
        for lado in (-1, 1):
            pos = c + B * r * 0.9 + L * lado * r * 0.42
            p.append(em.usar(suave(esfera(f"{nome}_ventosa{k}{lado}", r * 0.3, pos, sub=2)),
                             M["ventosa"]))
    return p


# ---------------------------------------------------------------- montagem

R_TRONCO = [(0.88, 0.13), (0.95, 0.155), (1.02, 0.15), (1.10, 0.155), (1.25, 0.18),
            (1.36, 0.19), (1.44, 0.16), (1.50, 0.06)]


def corpo(M):
    p = []
    tronco = em.torno("tronco", [(0.0, 0.86)] + [(r, z) for z, r in R_TRONCO] + [(0.0, 1.51)], 20)
    tronco.scale = (1, ESCALA_Y, 1)
    p.append(em.usar(suave(tronco), M["veste"]))
    p.append(em.usar(suave(em.torno("pescoco", [(0.0, 1.46), (0.05, 1.46), (0.048, 1.56),
                                               (0.0, 1.56)], 12)), M["breu"]))
    p.append(em.usar(suave(esfera("cabeca", 0.1, (0, 0, 1.61))), M["breu"]))
    for lado in (-1, 1):
        p.append(em.usar(suave(esfera(f"olho{lado}", 0.016, (lado * 0.034, -0.094, 1.625),
                                      (1.3, 0.5, 0.75))), M["olho"]))
        q = Vector((lado * QUADRIL[0], 0, QUADRIL[1]))
        j = Vector((lado * JOELHO[0], -0.01, JOELHO[1]))
        t = Vector((lado * TORNOZELO[0], 0, TORNOZELO[1]))
        p.append(em.usar(suave(segmento(f"coxa{lado}", q, j, [(0.0, 0), (0.08, 0.02), (0.075, 0.5),
                                                               (0.06, 1.0), (0.0, 1.0)])), M["veste"]))
        p.append(em.usar(suave(segmento(f"canela{lado}", j, t, [(0.0, 0), (0.06, 0.0), (0.055, 0.4),
                                                                (0.05, 1.0), (0.0, 1.0)])), M["couro"]))
        p.append(em.usar(caixa(f"bota{lado}", (t.x, -0.035, 0.045), (0.05, 0.115, 0.045), 0.02),
                         M["couro"]))

        # Braço em pose A com manga larga de boca laranja; mão escura.
        d = Vector((lado * math.sin(math.radians(45)), 0, -math.cos(math.radians(45))))
        s = Vector((lado * OMBRO[0], 0, OMBRO[1]))
        cot = s + d * BRACO[0]
        pulso = cot + d * BRACO[1]
        p.append(em.usar(suave(segmento(f"braco{lado}", s, cot, [(0.0, 0), (0.055, 0.02), (0.05, 1.0),
                                                                 (0.0, 1.0)])), M["veste"]))
        p.append(em.usar(suave(segmento(f"antebraco{lado}", cot, pulso, [(0.0, 0), (0.045, 0.0),
                                                                         (0.04, 1.0), (0.0, 1.0)])),
                         M["mao"]))
        manga = segmento(f"manga{lado}", s + d * 0.04, pulso - d * 0.03, [
            (0.07, 0.0), (0.075, 0.4), (0.1, 0.8), (0.12, 1.0)])
        p.append(em.usar(engrossar(suave(manga), 0.008), M["manga"]))
        p.append(em.usar(suave(segmento(f"punho{lado}", pulso - d * 0.05, pulso - d * 0.03, [
            (0.118, 0.0), (0.124, 0.5), (0.122, 1.0)])), M["punho"]))
        mao = caixa(f"mao{lado}", (0, 0, 0), (0.02, 0.04, 0.075), 0.012)
        ec.orientar(mao, pulso + d * 0.08, d)
        mao.scale = (0.02, 0.04, 0.075)
        p.append(em.usar(mao, M["mao"]))
    return p


def roupa(M):
    p = []

    # Capuz carmim pontudo, aberto no rosto; a ponta cai para trás.
    def abertura_capuz(z):
        if z > 1.74:
            return 0.0
        if z > 1.70:
            return math.radians(38) * (1.74 - z) / 0.04
        return math.radians(38) if z > 1.50 else math.radians(26)

    perfil = [(0.0, 1.92), (0.035, 1.87), (0.075, 1.81), (0.12, 1.75), (0.155, 1.69),
              (0.165, 1.62), (0.16, 1.55), (0.165, 1.50), (0.2, 1.46), (0.23, 1.42)]
    capuz = casca("capuz", perfil, abertura_capuz, seg=36)
    for v in capuz.data.vertices:
        if v.co.z > 1.70:
            v.co.y += (v.co.z - 1.70) ** 1.6 * 3.2
    capuz.location = (0, -0.012, 0)
    em.usar(capuz, M["capuz"])
    p.append(engrossar(suave(capuz), 0.016, M["breu"]))

    # Capinha nos ombros, de pontas, aberta na frente.
    capinha = manto("capinha", lambda z: interpola([(1.24, 0.30), (1.36, 0.25), (1.46, 0.18)], z),
                    1.46, lambda th: 1.22 + 0.06 * abs(math.sin(th * 4.5)),
                    lambda z: math.radians(16), nx=40, nz=8)
    em.usar(capinha, M["capinha"])
    p.append(engrossar(suave(capinha), 0.012))

    # Manto vinho em sino, aberto na frente, barra em pontas de comprimentos diferentes.
    def r_manto(z):
        return interpola([(0.05, 0.42), (0.3, 0.37), (0.6, 0.29), (0.95, 0.215), (1.05, 0.19),
                          (1.25, 0.2), (1.40, 0.19)], z)

    def abertura_manto(z):
        return math.radians(10 + 34 * max(0.0, min(1.0, (1.2 - z) / 1.0)))

    def barra(th):
        return 0.10 + 0.17 * abs(math.sin(th * 3.5 + 0.4)) ** 2 + 0.06 * abs(math.sin(th * 9.0))

    m = manto("manto", r_manto, 1.40, barra, abertura_manto, nx=56, nz=26)
    em.usar(m, M["manto"])
    p.append(engrossar(suave(m), 0.014))

    # Sobremanto rúnico na frente, visível pela abertura do manto.
    def ponto_sobre(u, v):
        z = 1.0 - v * 0.82
        meia = 0.11 + 0.1 * v
        x = (u - 0.5) * 2 * meia
        y = -ESCALA_Y * interpola([(0.2, 0.33), (0.6, 0.27), (0.95, 0.2), (1.0, 0.19)], z) * 0.92
        return (x, y + 1.2 * x * x, z)

    sobre = grade("sobremanto", 9, 18, ponto_sobre)
    em.usar(sobre, M["sobremanto"])
    p.append(engrossar(suave(sobre), 0.008))
    p.append(em.usar(suave(em.torno("saia", [(0.0, 0.2), (0.27, 0.2), (0.2, 0.6), (0.16, 0.95),
                                             (0.0, 0.95)], 20)), M["veste"]))
    p[-1].scale = (1, ESCALA_Y * 1.05, 1)

    # Contas violeta no peito: três grandes em V e duas menores.
    for i, (x, z, r) in enumerate(((-0.075, 1.33, 0.022), (0.0, 1.27, 0.028), (0.075, 1.33, 0.022),
                                   (-0.12, 1.385, 0.014), (0.12, 1.385, 0.014))):
        y = -ESCALA_Y * interpola(R_TRONCO, z) * (1 - (x / 0.2) ** 2 * 0.5) - r * 0.5
        p.append(em.usar(suave(esfera(f"conta{i}", r, (x, y, z), sub=2)), M["runa"]))

    # Cinto com medalhão violeta.
    cinto = em.torno("cinto", [(0.0, 0.99), (0.165, 0.99), (0.168, 1.04), (0.0, 1.04)], 24)
    cinto.scale = (1, ESCALA_Y * 1.05, 1)
    p.append(em.usar(suave(cinto), M["couro"]))
    bpy.ops.mesh.primitive_cylinder_add(vertices=20, radius=0.034, depth=0.012,
                                        location=(0, -0.118, 1.015),
                                        rotation=(math.radians(90), 0, 0))
    medalhao = bpy.context.view_layer.objects.active
    p.append(em.usar(suave(medalhao), M["metal"]))
    p.append(em.usar(gema("medalhao_gema", 0.02, (0, -0.126, 1.015)), M["runa"]))

    # Tentáculos: saem de baixo da barra, deitam no chão e enrolam a ponta; os dos lados sobem.
    baixo = [(0.2, 0.2), (0.3, 0.05), (0.44, 0.035), (0.56, 0.05), (0.63, 0.13), (0.6, 0.21),
             (0.53, 0.21), (0.52, 0.15)]
    alto = [(0.22, 0.25), (0.34, 0.06), (0.48, 0.05), (0.58, 0.18), (0.6, 0.42), (0.55, 0.6),
            (0.47, 0.62), (0.45, 0.53)]
    for i, (phi, cam, r0) in enumerate(((-35, baixo, 0.05), (35, baixo, 0.05), (-95, alto, 0.058),
                                        (95, alto, 0.058), (-150, baixo, 0.048),
                                        (150, baixo, 0.048))):
        p += tentaculo(M, f"tentaculo{i}", math.radians(phi), cam, r0)
    return p


def main():
    ed.reset_scene()
    M = materiais()
    partes = corpo(M) + roupa(M)
    ec.render(TMP, alvo_z=0.97)
    print("RELATORIO", ed.report(partes))


main()
