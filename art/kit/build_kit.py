"""Kit modular (B14): peças de pedra da sala, modeladas por script, com uma textura só.

Rodar da raiz: tools/blender.sh art/kit/build_kit.py
Saídas:
  assets/models/kit/{piso,parede,parede_porta,canto,coluna}.glb
  art/kit/texturas/kit_pedra.png (fonte da textura compartilhada, 1024²)
  .godot/capturas_tmp/kit/pecas.png e montagem.png (prévias para o portão)

Grade de 2 m (docs/arte/guia-de-estilo.md): cada peça tem a origem no canto de grade, base em
z = 0 no Blender (y = 0 no glTF) e cresce em +X e +Z do glTF (−Y no Blender). Medidas: piso
2 × 2 × 0,15 m; parede 2 × 3 × 0,4 m; parede com vão de 2 × 2,4 m; canto 0,4 × 0,4 × 3 m;
coluna 1 × 1 × 3 m. Orçamento: ≤ 1.500 triângulos e 1 material por peça, textura 1024²
compartilhada (1 tile = 2 m, então a pedra casa de uma peça para a outra).

As juntas ficam na geometria (blocos em running bond com folga sobre uma placa de fundo) e a
irregularidade vem de uma semente fixa. O enquadramento "atual" (T32 a) dispensa detalhe que
some a 10 m de câmera: o valor (pedra 0,18–0,26) e a junta é que desenham a parede.
"""
import math
import os
import sys

import bpy
import numpy as np
from mathutils import Vector

RAIZ = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, os.path.join(RAIZ, "tools", "blender"))
import ed_blender as ed  # noqa: E402

SAIDA = os.path.join(RAIZ, "assets", "models", "kit")
TEX_FONTE = os.path.join(RAIZ, "art", "kit", "texturas", "kit_pedra.png")
TMP = os.path.join(RAIZ, ".godot", "capturas_tmp", "kit")

# Paleta (docs/arte/guia-de-estilo.md): a pedra fica sempre um degrau abaixo do herói.
PEDRA = "#3a3a40"
PEDRA_SOMBRA = "#1c1c22"
PEDRA_GASTA = "#5c5852"

SEMENTE = 20261120
TEX = 1024
GAP = 0.02          # folga entre blocos (a junta escura da placa de fundo aparece)
CHANFRO = 0.007
TILE = 2.0          # 1 tile da textura cobre 2 m em todas as peças


# ---------------------------------------------------------------- textura

def _srgb(hexcor):
    """Hex → RGB em sRGB 0–1 (é o que um PNG de 8 bits guarda; o guia mede valor em sRGB)."""
    h = hexcor.lstrip("#")
    return np.array([int(h[i:i + 2], 16) / 255.0 for i in (0, 2, 4)], dtype=np.float32)


def _campo_oscilacoes(n, rng):
    """Nuvem suave e contínua nas bordas (frequências inteiras = textura sem costura)."""
    eixo = np.arange(n, dtype=np.float32)
    x, y = np.meshgrid(eixo, eixo, indexing="ij")
    campo = np.zeros((n, n), dtype=np.float32)
    peso = 0.0
    for oitava in range(4):
        freq = 2 ** oitava * 5
        amplitude = 0.62 ** oitava
        for _ in range(5):
            ang = rng.uniform(0, 2 * math.pi)
            fase = rng.uniform(0, 2 * math.pi)
            campo += amplitude * np.sin(2 * math.pi * freq *
                                        (x * math.cos(ang) + y * math.sin(ang)) / n + fase)
        peso += amplitude * 5
    campo /= peso
    return (campo - campo.min()) / (campo.max() - campo.min())


def _grao(n, rng):
    """Grão fino, periódico para não marcar a emenda do tile."""
    base = rng.random((64, 64)).astype(np.float32)
    base = (base + np.roll(base, 1, 0) + np.roll(base, 1, 1) +
            np.roll(np.roll(base, 1, 0), 1, 1)) / 4
    fator = n // 64
    return np.kron(base, np.ones((fator, fator), dtype=np.float32))


def textura_pedra():
    """Manchas largas entre pedra-sombra e pedra, quinas gastas em poucas manchas e grão leve.

    O valor fica na faixa do guia (face 0,18–0,26; quina gasta 0,30–0,36) e nenhum albedo
    passa de 0,65. Sem luz direcional embutida e sem vermelho de aviso: a luz vem da cena.
    """
    rng = np.random.default_rng(SEMENTE)
    nuvem = _campo_oscilacoes(TEX, rng)
    grao = _grao(TEX, rng)
    alto = _campo_oscilacoes(TEX, rng)

    sombra, pedra, gasta = _srgb(PEDRA_SOMBRA), _srgb(PEDRA), _srgb(PEDRA_GASTA)

    # A maior parte da face perto de `pedra`; a sombra só nas reentrâncias da nuvem.
    t = np.clip(0.45 + 0.85 * nuvem + 0.12 * (grao - 0.5), 0.0, 1.0)[..., None]
    cor = sombra * (1.0 - t) + pedra * t
    # Quina gasta: manchas raras, mais claras, que é onde a luz rasante bate.
    mancha = (np.clip((alto - 0.74) / 0.22, 0.0, 1.0) * 0.55)[..., None]
    cor = cor * (1.0 - mancha) + gasta * mancha
    # Pincelada larga: um tico mais quente ou mais frio, sem sair da paleta.
    cor = np.clip(cor * (0.96 + 0.08 * (grao - 0.5))[..., None], 0.0, 0.65)

    rgba = np.ones((TEX, TEX, 4), dtype=np.float32)
    rgba[..., :3] = cor

    os.makedirs(os.path.dirname(TEX_FONTE), exist_ok=True)
    img = bpy.data.images.new("kit_pedra", TEX, TEX, alpha=False)
    img.colorspace_settings.name = "sRGB"
    img.pixels.foreach_set(rgba.ravel())
    img.filepath_raw = TEX_FONTE
    img.file_format = "PNG"
    img.save()
    img.pack()
    return img


def material_pedra(img):
    m = bpy.data.materials.new("kit_pedra")
    m.use_nodes = True
    nt = m.node_tree
    bsdf = nt.nodes["Principled BSDF"]
    tex = nt.nodes.new("ShaderNodeTexImage")
    tex.image = img
    tex.interpolation = "Linear"
    tex.extension = "REPEAT"
    nt.links.new(tex.outputs["Color"], bsdf.inputs["Base Color"])
    bsdf.inputs["Roughness"].default_value = 0.82
    bsdf.inputs["Metallic"].default_value = 0.0
    bsdf.inputs["Specular IOR Level"].default_value = 0.35
    return m


# ---------------------------------------------------------------- geometria

def caixa(nome, tamanho, canto, material, chanfro=CHANFRO, segmentos=1):
    """Bloco retangular com chanfro; `canto` é o vértice de menor x, y e z."""
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(
        canto[0] + tamanho[0] / 2, canto[1] + tamanho[1] / 2, canto[2] + tamanho[2] / 2))
    obj = bpy.context.view_layer.objects.active
    obj.scale = tamanho
    ed.apply_transforms(obj)
    obj.name = nome
    largura = min(chanfro, min(tamanho) * 0.25)
    if largura > 0:
        mod = obj.modifiers.new("chanfro", "BEVEL")
        mod.width = largura
        mod.segments = segmentos
        mod.limit_method = "ANGLE"
        mod.angle_limit = math.radians(40)
        bpy.ops.object.modifier_apply(modifier=mod.name)
    obj.data.materials.clear()
    obj.data.materials.append(material)
    return obj


def _faixas(comprimento, bloco=1.0, desloc=0.0):
    """Cortes de uma fileira: blocos inteiros, com meio bloco nas pontas quando alternada."""
    xs = [i * bloco - desloc * bloco * 0.5 for i in range(int(comprimento / bloco) + 2)]
    for a, b in zip(xs[:-1], xs[1:]):
        a, b = max(a, 0.0), min(b, comprimento)
        if b - a > GAP:
            yield a, b


def _fiadas(prefixo, largura, altura, fiadas, frente, espessura, material, rng, base=0.0):
    """Blocos em running bond na face de uma parede. O fundo do bloco encosta na placa; a
    frente ressaltada entre 0 e 6 mm é a irregularidade que a luz rasante desenha."""
    partes = []
    altura_bloco = altura / fiadas
    for r in range(fiadas):
        for a, b in _faixas(largura, desloc=0.5 if r % 2 else 0.0):
            ressalto = rng.uniform(0.0, 0.004)
            partes.append(caixa(
                f"{prefixo}_{r}_{a:.2f}",
                (b - a - GAP, espessura + ressalto, altura_bloco - GAP),
                (a + GAP / 2, frente - ressalto, base + r * altura_bloco + GAP / 2), material))
    return partes


def _lajes(prefixo, largura, profundidade, fiadas, base, material, rng):
    """Lajes do piso em running bond; cada uma levanta 0 a 4 mm e nunca passa dos 15 cm."""
    partes = []
    prof_laje = profundidade / fiadas
    for r in range(fiadas):
        for a, b in _faixas(largura, desloc=0.5 if r % 2 else 0.0):
            partes.append(caixa(
                f"{prefixo}_{r}_{a:.2f}",
                (b - a - GAP, prof_laje - GAP, 0.058 + rng.uniform(0.0, 0.004)),
                (a + GAP / 2, -profundidade + r * prof_laje + GAP / 2, base), material,
                chanfro=0.016))
    return partes


def peca_piso(material, rng):
    fundo = caixa("piso_fundo", (2.0, 2.0, 0.092), (0.0, -2.0, 0.0), material)
    return [fundo] + _lajes("piso_laje", 2.0, 2.0, 2, 0.092, material, rng)


def peca_parede(material, rng):
    # Placa de fundo fecha o vão entre os blocos e garante a espessura exata de 0,4 m.
    fundo = caixa("parede_fundo", (2.0, 0.34, 3.0), (0.0, -0.34, 0.0), material)
    return [fundo] + _fiadas("parede_bloco", 2.0, 3.0, 3, -0.40, 0.064, material, rng)


def peca_parede_porta(material, rng):
    # Vão de 2 m × 2,4 m: só a soleira embaixo (é ela que põe a base em y = 0 e fecha os
    # 2 × 3 × 0,4 m da tabela) e a verga acima, com a chave no centro.
    partes = [caixa("porta_soleira", (2.0, 0.40, 0.06), (0.0, -0.40, 0.0), material)]
    partes += _fiadas("porta_verga", 2.0, 0.60, 2, -0.40, 0.064, material, rng, base=2.40)
    partes.append(caixa("porta_chave", (0.34, 0.076, 0.46), (0.83, -0.406, 2.42), material,
                        chanfro=0.010))
    return partes


def peca_canto(material, rng):
    return [
        caixa("canto_base", (0.40, 0.40, 0.26), (0.0, -0.40, 0.0), material),
        caixa("canto_fuste", (0.30, 0.30, 2.48), (0.05, -0.35, 0.26), material),
        caixa("canto_capiteu", (0.40, 0.40, 0.26), (0.0, -0.40, 2.74), material),
    ]


def peca_coluna(material, rng):
    return [
        caixa("coluna_base", (1.00, 1.00, 0.24), (0.0, -1.00, 0.0), material),
        caixa("coluna_fuste", (0.78, 0.78, 2.52), (0.11, -0.89, 0.24), material),
        caixa("coluna_capiteu", (1.00, 1.00, 0.24), (0.0, -1.00, 2.76), material),
    ]


PECAS = {
    "piso": peca_piso,
    "parede": peca_parede,
    "parede_porta": peca_parede_porta,
    "canto": peca_canto,
    "coluna": peca_coluna,
}

MEDIDAS = {
    "piso": (2.0, 2.0, 0.15),
    "parede": (2.0, 0.4, 3.0),
    "parede_porta": (2.0, 0.4, 3.0),
    "canto": (0.4, 0.4, 3.0),
    "coluna": (1.0, 1.0, 3.0),
}


# ---------------------------------------------------------------- UV e montagem

def uv_caixa(obj, escala=TILE):
    """Projeção pela face dominante: 1 tile da textura cobre 2 m em qualquer peça, então a
    pedra casa de uma peça para a outra sem emenda visível."""
    malha = obj.data
    if not malha.uv_layers:
        malha.uv_layers.new(name="UVMap")
    uv = malha.uv_layers.active.data
    for poli in malha.polygons:
        n = poli.normal
        for li in poli.loop_indices:
            v = malha.vertices[malha.loops[li].vertex_index].co
            if abs(n.z) >= max(abs(n.x), abs(n.y)):
                u, w = v.x, v.y
            elif abs(n.x) >= abs(n.y):
                u, w = v.y, v.z
            else:
                u, w = v.x, v.z
            uv[li].uv = (u / escala, w / escala)


def montar(nome, material, rng):
    partes = PECAS[nome](material, rng)
    obj = ed.join_meshes(partes, nome)
    ed.apply_transforms(obj)
    ed._select([obj], obj)
    bpy.ops.object.shade_smooth_by_angle(angle=math.radians(35))
    uv_caixa(obj)
    return obj


# ---------------------------------------------------------------- prévias

def _luz(cena, cor, energia, pos, raio):
    dados = bpy.data.lights.new("luz", "POINT")
    dados.color = ed._linear(cor)
    dados.energy = energia
    dados.shadow_soft_size = raio
    obj = bpy.data.objects.new("luz", dados)
    cena.collection.objects.link(obj)
    obj.location = pos
    return obj


def render(caminho, objs, largura=1600, altura=760, elevacao=20, azimute=-14,
           alvo=None, folga=1.12, lente=85):
    """Prévia em perspectiva com a luz do guia: fundo breu, quente à frente (duas luzes, para
    as duas faces visíveis da peça), frio atrás para a silhueta e um recheio frio fraco."""
    cena = bpy.context.scene
    ed._cycles_cpu(48)
    cena.render.resolution_x = largura
    cena.render.resolution_y = altura
    cena.render.resolution_percentage = 100
    cena.render.image_settings.file_format = "PNG"
    mundo_antigo = cena.world
    mundo = bpy.data.worlds.new("previa_kit")
    mundo.use_nodes = True
    mundo.node_tree.nodes["Background"].inputs["Color"].default_value = (
        *ed._linear(ed.FUNDO), 1.0)
    cena.world = mundo

    lo, hi = ed._caixa(objs)
    centro = alvo if alvo is not None else (lo + hi) / 2
    ext = max(max(hi - lo), 1.0)
    criados = [
        _luz(cena, ed.LUZ_PRINCIPAL, 830.0 * ext * ext,
             centro + Vector((0.35, -1.15, 1.05)) * ext, ext * 0.10),
        _luz(cena, "#7c8fb5", 470.0 * ext * ext,
             centro + Vector((-1.05, -0.95, 0.55)) * ext, ext * 0.25),
        _luz(cena, ed.CONTRALUZ, 400.0 * ext * ext,
             centro + Vector((-0.55, 1.15, 1.20)) * ext, ext * 0.25),
    ]

    dados = bpy.data.cameras.new("previa_kit")
    cam = bpy.data.objects.new("previa_kit", dados)
    cena.collection.objects.link(cam)
    cena.camera = cam
    dados.lens = lente
    dados.clip_end = ext * 30
    elev = math.radians(elevacao)
    azim = math.radians(azimute)
    direcao = Vector((math.sin(azim) * math.cos(elev), -math.cos(azim) * math.cos(elev),
                      math.sin(elev))).normalized()
    # Enquadra os oito cantos da caixa: `dados.angle` é o campo horizontal (sensor AUTO num
    # render deitado), e a profundidade de cada canto entra na conta porque o mais perto
    # projeta maior. Lente longa achata a fila de peças.
    tan_h = math.tan(dados.angle / 2)
    tan_v = tan_h * altura / largura
    frente = -direcao
    direita = frente.cross(Vector((0.0, 0.0, 1.0))).normalized()
    cima = direita.cross(frente)
    distancia = 0.0
    for i in (0.0, 1.0):
        for j in (0.0, 1.0):
            for k in (0.0, 1.0):
                rel = Vector((lo.x + i * (hi.x - lo.x), lo.y + j * (hi.y - lo.y),
                              lo.z + k * (hi.z - lo.z))) - centro
                distancia = max(distancia, rel.dot(frente) + max(
                    abs(rel.dot(direita)) / tan_h, abs(rel.dot(cima)) / tan_v))
    cam.location = centro + direcao * distancia * folga
    ed._olhar(cam, centro)

    os.makedirs(os.path.dirname(caminho), exist_ok=True)
    cena.render.filepath = caminho
    bpy.ops.render.render(write_still=True)

    for o in (cam, *criados):
        dados_o = o.data
        bpy.data.objects.remove(o)
        if isinstance(dados_o, bpy.types.Camera):
            bpy.data.cameras.remove(dados_o)
        else:
            bpy.data.lights.remove(dados_o)
    cena.world = mundo_antigo
    bpy.data.worlds.remove(mundo)
    bpy.context.view_layer.update()
    print("PREVIA", caminho)


def _duplicar(obj, local, rotacao=0.0):
    copia = obj.copy()
    copia.data = obj.data.copy()
    bpy.context.scene.collection.objects.link(copia)
    copia.hide_render = False
    copia.location = local
    copia.rotation_euler = (0.0, 0.0, rotacao)
    return copia


def _descartar(objs):
    """Tira as cópias da prévia (as peças originais ficam escondidas, não são tocadas)."""
    for o in objs:
        malha = o.data
        bpy.data.objects.remove(o)
        bpy.data.meshes.remove(malha)
    bpy.context.view_layer.update()


def previa_pecas(pecas):
    """As cinco peças em fila, de frente, para Pedro ler todas de uma vez."""
    objs = []
    for i, nome in enumerate(("piso", "parede", "parede_porta", "canto", "coluna")):
        objs.append(_duplicar(pecas[nome], (i * 2.8, 0.0, 0.0)))
    render(os.path.join(TMP, "pecas.png"), objs, elevacao=18, azimute=-10, folga=1.06)
    _descartar(objs)


def previa_montagem(pecas):
    """Canto de sala de 4 × 4 m: piso, parede, parede com a porta, canto e a coluna dentro."""
    objs = []
    for i in range(2):
        for j in range(2):
            objs.append(_duplicar(pecas["piso"], (i * 2.0, -j * 2.0, 0.0)))
    # Parede norte (ao longo de X), com a porta no segundo módulo.
    objs.append(_duplicar(pecas["parede"], (0.0, 0.0, 0.0)))
    objs.append(_duplicar(pecas["parede_porta"], (2.0, 0.0, 0.0)))
    # Parede leste (girada −90°: cresce em −Y, com os blocos virados para dentro da sala).
    objs.append(_duplicar(pecas["parede"], (4.0, 0.0, 0.0), math.radians(-90)))
    objs.append(_duplicar(pecas["parede"], (4.0, -2.0, 0.0), math.radians(-90)))
    objs.append(_duplicar(pecas["canto"], (3.6, 0.0, 0.0)))
    objs.append(_duplicar(pecas["coluna"], (0.3, -2.7, 0.0)))
    render(os.path.join(TMP, "montagem.png"), objs, largura=1500, altura=900,
           elevacao=28, azimute=-42, folga=1.10, lente=110)
    _descartar(objs)


def main():
    ed.reset_scene()
    rng = np.random.default_rng(SEMENTE)
    material = material_pedra(textura_pedra())

    pecas = {}
    for nome in PECAS:
        pecas[nome] = montar(nome, material, rng)
        ed.export_glb([pecas[nome]], os.path.join(SAIDA, nome + ".glb"))
        rel = ed.report([pecas[nome]])
        esperado = MEDIDAS[nome]
        if any(abs(a - b) > 0.02 for a, b in zip(rel["dims"], esperado)):
            raise RuntimeError("%s: medidas %s fora da tabela %s" %
                               (nome, rel["dims"], list(esperado)))
        print("RELATORIO", nome, rel)
        pecas[nome].hide_render = True

    previa_pecas(pecas)
    previa_montagem(pecas)


main()
