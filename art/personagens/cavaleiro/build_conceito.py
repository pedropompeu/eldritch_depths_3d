"""Conceito do Cavaleiro (B05) por blockout 3D: modelado por script e renderizado em três vistas.

Rodar da raiz: tools/blender.sh art/personagens/cavaleiro/build_conceito.py
Saídas: .godot/capturas_tmp/cavaleiro_conceito/{frente,lado,costas,tres_quartos}.png (fundo
transparente). A folha sai de `tools/folha_conceito.py`.

Sem gerador de imagem: Pedro pediu "faça você mesmo" e a cota grátis do Space acabou. As três
vistas saem do mesmo modelo, então batem entre si por construção. Fiel ao hero.png do 2D:
capuz marrom fundo, máscara de caveira em osso na sombra, gema violeta na testa e no peito,
ombreiras e manoplas de aço escuro, casaco longo de couro aberto na frente com cravos violeta
na barra, tabardo cinza-prata rúnico, cinto com fivela e bolsas, capa escura esfarrapada,
grevas e botas de placa. Pose A (braços a 45°), mãos vazias, sem a espada (B08).

Escala: 1 unidade = 1 m, Z para cima, pés em z = 0, olhando para −Y. Altura 1,80 m.
"""
import math
import os
import sys

from mathutils import Vector

RAIZ = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
sys.path.insert(0, os.path.join(RAIZ, "tools", "blender"))
import ed_blender as ed  # noqa: E402
import ed_modelagem as em  # noqa: E402
import ed_conceito as ec  # noqa: E402
from ed_conceito import (caixa, casca, engrossar, esfera, gema, grade,  # noqa: E402
                         orientar, segmento, suave)

TMP = os.path.join(RAIZ, ".godot", "capturas_tmp", "cavaleiro_conceito")

# Paleta do conceito: os tons do hero.png, um pouco mais claros que no jogo para ler no cinza.
COURO_CASACO = "#5e3d29"
COURO_CAPUZ = "#4b3222"
COURO_CINTO = "#3a2618"
ACO = "#474a57"
TABARDO = "#a3a5ad"
TABARDO_RUNA = "#5f616b"
OSSO = "#c4b79a"
CAPA = "#221c26"
CALCA = "#2b2321"
BREU = em.BREU
RUNA = em.RUNA

# Esqueleto da pose A.
OMBRO = 0.20, 1.42      # x, z do ombro
BRACO = 0.29, 0.26, 0.17  # braço, antebraço, mão
QUADRIL = 0.10, 0.93
JOELHO = 0.135, 0.50
TORNOZELO = 0.17, 0.09


# ---------------------------------------------------------------- materiais

def materiais():
    material = ec.material
    return {
        "casaco": material("casaco", COURO_CASACO, 0.75, variacao=0.25),
        "capuz": material("capuz", COURO_CAPUZ, 0.8, variacao=0.25),
        "cinto": material("cinto", COURO_CINTO, 0.7, variacao=0.2),
        "aco": material("aco", ACO, 0.4, metalico=0.75, variacao=0.15),
        "tabardo": ec.mat_runas("tabardo", TABARDO, TABARDO_RUNA),
        "osso": material("osso", OSSO, 0.6, variacao=0.12),
        "capa": material("capa", CAPA, 0.85, variacao=0.3),
        "calca": material("calca", CALCA, 0.85),
        "breu": material("breu", BREU, 1.0),
        "runa": material("runa", RUNA, 0.3, emissao=3.0),
    }


# ---------------------------------------------------------------- corpo

def r_tronco(z):
    """Raio do tronco (antes do achatamento em Y) por altura; liga o tabardo e a capa ao corpo."""
    pts = [(0.90, 0.13), (0.95, 0.16), (1.02, 0.15), (1.10, 0.16), (1.25, 0.19), (1.38, 0.20),
           (1.46, 0.17), (1.52, 0.07)]
    if z <= pts[0][0]:
        return pts[0][1]
    for (z0, r0), (z1, r1) in zip(pts, pts[1:]):
        if z <= z1:
            return r0 + (r1 - r0) * (z - z0) / (z1 - z0)
    return pts[-1][1]


PERFIL_CASACO = [(0.17, 1.46), (0.215, 1.39), (0.22, 1.25), (0.19, 1.06), (0.205, 0.96),
                 (0.25, 0.72), (0.29, 0.48), (0.31, 0.32)]
ESCALA_Y_TRONCO = 0.62
ESCALA_Y_CASACO = 0.72


def r_casaco(z):
    pts = sorted((z_, r) for r, z_ in PERFIL_CASACO)
    if z <= pts[0][0]:
        return pts[0][1]
    for (z0, r0), (z1, r1) in zip(pts, pts[1:]):
        if z <= z1:
            return r0 + (r1 - r0) * (z - z0) / (z1 - z0)
    return pts[-1][1]


def corpo(M):
    p = []
    tronco = em.torno("tronco", [(0.0, 0.88)] + [(r_tronco(z), z) for z in
                      (0.90, 0.95, 1.02, 1.10, 1.25, 1.38, 1.46, 1.52)] + [(0.0, 1.53)], 20)
    tronco.scale = (1, ESCALA_Y_TRONCO, 1)
    p.append(em.usar(suave(tronco), M["aco"]))
    p.append(em.usar(suave(em.torno("pescoco", [(0.0, 1.47), (0.055, 1.47), (0.05, 1.57),
                                               (0.0, 1.57)], 12)), M["breu"]))
    # Cabeça em breu: só a máscara aparece na sombra do capuz.
    p.append(em.usar(suave(esfera("cabeca", 0.105, (0, 0, 1.62))), M["breu"]))

    for lado in (-1, 1):
        q = Vector((lado * QUADRIL[0], 0, QUADRIL[1]))
        j = Vector((lado * JOELHO[0], -0.01, JOELHO[1]))
        t = Vector((lado * TORNOZELO[0], 0, TORNOZELO[1]))
        p.append(em.usar(suave(segmento(f"coxa{lado}", q, j, [(0.0, 0), (0.085, 0.02), (0.08, 0.5),
                                                               (0.066, 1.0), (0.0, 1.0)])), M["calca"]))
        p.append(em.usar(suave(segmento(f"greva{lado}", j, t, [(0.0, -0.02), (0.064, 0.0),
                                                               (0.066, 0.3), (0.05, 0.85),
                                                               (0.056, 1.0), (0.0, 1.0)])), M["aco"]))
        p.append(em.usar(suave(esfera(f"joelheira{lado}", 0.062, j + Vector((0, -0.025, 0)),
                                      (1, 0.8, 1))), M["aco"]))
        p.append(em.usar(caixa(f"bota{lado}", (t.x, -0.04, 0.05), (0.052, 0.125, 0.05), 0.022),
                         M["aco"]))
    return p


def bracos(M):
    p = []
    for lado in (-1, 1):
        d = Vector((lado * math.sin(math.radians(45)), 0, -math.cos(math.radians(45))))
        s = Vector((lado * OMBRO[0], 0, OMBRO[1]))
        cot = s + d * BRACO[0]
        pulso = cot + d * BRACO[1]
        ponta = pulso + d * BRACO[2]
        p.append(em.usar(suave(segmento(f"braco{lado}", s, cot, [(0.0, 0), (0.06, 0.02), (0.056, 0.6),
                                                                 (0.05, 1.0), (0.0, 1.0)])), M["casaco"]))
        p.append(em.usar(suave(esfera(f"cotoveleira{lado}", 0.052, cot)), M["aco"]))
        p.append(em.usar(suave(segmento(f"manopla{lado}", cot, pulso, [
            (0.0, 0.05), (0.046, 0.05), (0.05, 0.55), (0.06, 0.9), (0.062, 1.0), (0.0, 1.0)])), M["aco"]))
        # Mão em luva de placa, palma virada para a coxa: largura em Y, espessura no plano do braço.
        mao = caixa(f"mao{lado}", (0, 0, 0), (0.022, 0.042, BRACO[2] / 2 * 0.9), 0.012)
        orientar(mao, pulso + d * (BRACO[2] / 2), d)
        mao.scale = (0.022, 0.042, BRACO[2] / 2 * 0.9)
        p.append(em.usar(mao, M["aco"]))
        dedao = caixa(f"dedao{lado}", (0, 0, 0), (0.014, 0.014, 0.035), 0.008)
        orientar(dedao, pulso + d * 0.05 + Vector((0, -0.045, 0)), d)
        dedao.scale = (0.014, 0.014, 0.035)
        p.append(em.usar(dedao, M["aco"]))

        # Ombreira: três placas sobrepostas descendo pelo braço.
        eixo = Vector((lado * 0.5, 0, 0.87))
        for i, (esc, desce) in enumerate(((1.0, 0.0), (0.86, 0.075), (0.74, 0.14))):
            placa = em.torno(f"ombreira{lado}_{i}", [
                (0.0, 0.06 * esc), (0.05 * esc, 0.055 * esc), (0.088 * esc, 0.034 * esc),
                (0.108 * esc, 0.0), (0.114 * esc, -0.035 * esc)], 18)
            orientar(placa, s + Vector((0, 0, 0.035)) + d * desce, eixo)
            p.append(em.usar(engrossar(suave(placa), 0.012), M["aco"]))
    return p


def cabeca(M):
    p = []
    # Capuz fundo, aberto na frente do rosto e descendo em gola até o peito.
    def abertura(z):
        if z > 1.745:
            return 0.0
        if z > 1.70:
            return math.radians(36) * (1.745 - z) / 0.045
        return math.radians(36) if z > 1.50 else math.radians(24)

    perfil = [(0.0, 1.82), (0.06, 1.815), (0.115, 1.795), (0.15, 1.765), (0.165, 1.73),
              (0.172, 1.68), (0.17, 1.62), (0.165, 1.56), (0.17, 1.51), (0.20, 1.47),
              (0.235, 1.43), (0.25, 1.385)]
    capuz = casca("capuz", perfil, abertura, seg=36)
    capuz.location = (0, -0.012, 0)
    capuz.scale = (1, 0.95, 1)
    em.usar(capuz, M["capuz"])
    p.append(engrossar(suave(capuz), 0.016, M["breu"]))

    # Máscara de caveira em osso.
    p.append(em.usar(suave(esfera("cranio", 1.0, (0, -0.07, 1.625), (0.078, 0.052, 0.078))), M["osso"]))
    p.append(em.usar(suave(esfera("maxilar", 1.0, (0, -0.078, 1.56), (0.052, 0.04, 0.04))), M["osso"]))
    for lado in (-1, 1):
        p.append(em.usar(suave(esfera(f"orbita{lado}", 0.026, (lado * 0.032, -0.105, 1.618),
                                      (1, 0.55, 0.85))), M["breu"]))
    nariz = em.torno("nariz", [(0.0, -0.016), (0.012, -0.016), (0.0, 0.012)], 3)
    nariz.location = (0, -0.115, 1.588)
    p.append(em.usar(nariz, M["breu"]))
    for k in range(-2, 3):
        p.append(em.usar(caixa(f"dente{k}", (k * 0.0105, -0.111, 1.553), (0.0035, 0.004, 0.008)),
                         M["breu"]))
    p.append(em.usar(gema("gema_testa", 0.012, (0, -0.118, 1.672)), M["runa"]))
    return p


def roupa(M):
    p = []

    # Casaco longo aberto na frente: a abertura cresce do peito para a barra.
    def abertura(z):
        if z > 1.30:
            return math.radians(14)
        if z > 1.0:
            return math.radians(14 + 16 * (1.30 - z) / 0.30)
        return math.radians(30 + 16 * (1.0 - z) / 0.68)

    casaco = casca("casaco", PERFIL_CASACO, abertura, seg=44, escala_y=ESCALA_Y_CASACO)
    em.usar(casaco, M["casaco"])
    p.append(engrossar(suave(casaco), 0.014))
    # Cravos violeta na barra.
    z = PERFIL_CASACO[-1][1] + 0.025
    a0 = abertura(z)
    for k in range(17):
        th = a0 + (2 * math.pi - 2 * a0) * k / 16
        r = PERFIL_CASACO[-1][0] + 0.004
        p.append(em.usar(gema(f"cravo{k}", 0.009, (r * math.sin(th),
                                                   -r * math.cos(th) * ESCALA_Y_CASACO, z)), M["runa"]))

    # Tabardo na frente, do peito aos joelhos, curvado sobre o corpo.
    def ponto_tabardo(u, v):
        z = 1.30 - v * 0.86
        meia = 0.105 + 0.025 * v
        x = (u - 0.5) * 2 * meia
        if z >= 0.95:
            y = -ESCALA_Y_TRONCO * r_tronco(z) - 0.012
        else:
            y = -ESCALA_Y_TRONCO * r_tronco(0.95) - 0.012 - 0.015 * (0.95 - z) / 0.51
        return (x, y + 1.6 * x * x, z)

    tab = grade("tabardo", 9, 18, ponto_tabardo)
    em.usar(tab, M["tabardo"])
    p.append(engrossar(suave(tab), 0.008))
    p.append(em.usar(gema("gema_peito", 0.019, (0, -ESCALA_Y_TRONCO * r_tronco(1.33) - 0.02, 1.33)),
                     M["runa"]))
    p.append(em.usar(suave(em.anel("engaste_peito", 0.022, 0.005, 16, 6,
                                   (0, -ESCALA_Y_TRONCO * r_tronco(1.33) - 0.016, 1.33),
                                   (math.radians(90), 0, 0))), M["aco"]))

    # Cinto por cima do tabardo, fivela e bolsas na frente.
    cinto = em.torno("cinto", [(0.0, 0.98), (0.172, 0.98), (0.175, 1.035), (0.0, 1.035)], 24)
    cinto.scale = (1, 0.68, 1)
    p.append(em.usar(suave(cinto), M["cinto"]))
    p.append(em.usar(caixa("fivela", (0, -0.122, 1.007), (0.026, 0.006, 0.024), 0.004), M["aco"]))
    for lado in (-1, 1):
        p.append(em.usar(caixa(f"bolsa{lado}", (lado * 0.078, -0.118, 0.965), (0.028, 0.02, 0.034),
                               0.01, (0, 0, lado * math.radians(-18))), M["cinto"]))

    # Capa esfarrapada pendendo dos ombros, por fora do casaco.
    def ponto_capa(u, v):
        x = (u - 0.5) * 2 * (0.25 + 0.1 * v)
        fundo = 0.28 + 0.11 * abs(math.sin(x * 29)) ** 3 + 0.05 * abs(math.sin(x * 13 + 1.0))
        z = 1.45 - v * (1.45 - fundo)
        y = ESCALA_Y_CASACO * r_casaco(z) + 0.048 - 0.7 * x * x + 0.022 * math.sin(x * 24) * (0.4 + v)
        return (x, y, z)

    capa = grade("capa", 26, 20, ponto_capa)
    em.usar(capa, M["capa"])
    p.append(engrossar(suave(capa), 0.01))
    return p


def main():
    ed.reset_scene()
    M = materiais()
    partes = corpo(M) + bracos(M) + cabeca(M) + roupa(M)
    ec.render(TMP)
    print("RELATORIO", ed.report(partes))


main()
