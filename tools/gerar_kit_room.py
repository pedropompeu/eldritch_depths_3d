"""Gera `scenes/world/kit_room.tscn` (B15): a sala do 1A montada com as peças do kit.

Rodar da raiz: python3 tools/gerar_kit_room.py
A cena é gerada porque são ~100 instâncias com a mesma regra de grade; mexer no layout aqui e
rodar de novo é mais seguro do que editar 1.500 linhas de .tscn à mão.

Layout (o mesmo do `greybox_room.tscn`):
- piso de 16 × 16 m em lajes de 2 m, com o topo em y = 0 (a peça tem 0,15 m e assenta em
  y = −0,15);
- paredes de 3 m centradas nas linhas x = ±8 e z = ±8 (a face interna fica a 7,8 m do
  centro, dentro da tolerância de ±0,3 do teste), com os blocos virados para dentro;
- porta de 2 m centrada em x = 0 na parede norte, com o `DoorSlot` e o véu em (0, 1,5, −8);
- coluna de 1 × 1 m em (4, 0) e saleta de 4 × 4 m atrás da porta (z de −12 a −8);
- o `WorldEnvironment` é o mesmo da sala cinza.

As peças têm a origem no canto de grade e crescem em +X e +Z; por isso as paredes leste e sul
usam rotação de 90° e 180° em Y para os blocos olharem para dentro da sala.
"""
import math
import os

RAIZ = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SAIDA = os.path.join(RAIZ, "scenes", "world", "kit_room.tscn")

# Grade do kit (docs/arte/guia-de-estilo.md) e medidas da sala do 1A.
GRADE = 2.0
METADE = 8.0
ESPESSURA = 0.4
ALTURA_PISO = 0.15

AMBIENTE = """[sub_resource type="Environment" id="Env_sala"]
background_mode = 1
background_color = Color(0.0196078, 0.0235294, 0.0392157, 1)
ambient_light_source = 2
ambient_light_color = Color(0.12549, 0.141176, 0.188235, 1)
ambient_light_energy = 0.05
tonemap_mode = 3
glow_enabled = true
glow_intensity = 0.4
fog_enabled = true
fog_light_color = Color(0.0431373, 0.0509804, 0.0705882, 1)
fog_density = 0.03
"""

EXT = [
    ("res://scenes/world/kit/piso.tscn", "1_piso"),
    ("res://scenes/world/kit/parede.tscn", "2_parede"),
    ("res://scenes/world/kit/parede_porta.tscn", "3_porta"),
    ("res://scenes/world/kit/coluna.tscn", "4_coluna"),
]


def num(v):
    """Número no formato que o Godot lê (sem zeros à direita)."""
    return "%g" % round(float(v), 6)


def giro_y(graus):
    """Linhas da matriz de rotação em torno de Y (é assim que o .tscn escreve a base)."""
    c, s = math.cos(math.radians(graus)), math.sin(math.radians(graus))
    return (round(c, 6), 0.0, round(s, 6), 0.0, 1.0, 0.0, round(-s, 6), 0.0, round(c, 6))


def transform(base, origem):
    valores = list(base) + list(origem)
    return "Transform3D(%s)" % ", ".join(num(v) for v in valores)


IDENTIDADE = (1.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 1.0)


def no(nome, pai, cena, base, origem, extras=""):
    linhas = ['[node name="%s" parent="%s" instance=ExtResource("%s")]' % (nome, pai, cena),
              "transform = " + transform(base, origem)]
    if extras:
        linhas.append(extras)
    return "\n".join(linhas) + "\n"


def partes():
    """Blocos de nós por grupo, na ordem em que entram no arquivo."""
    partes = []

    piso = ""
    for i in range(int(2 * METADE / GRADE)):
        for j in range(int(2 * METADE / GRADE)):
            x = -METADE + i * GRADE
            z = -METADE + j * GRADE
            piso += "\n" + no("Floor_%d_%d" % (i, j), "Geometry/Floor", "1_piso",
                              IDENTIDADE, (x, -ALTURA_PISO, z))
    partes.append(("Floor", piso))

    norte = ""
    for k, x in enumerate([-9.0, -7.0, -5.0, -3.0, 1.0, 3.0, 5.0, 7.0]):
        norte += "\n" + no("WallNorth_%d" % k, "Geometry/Walls", "2_parede", IDENTIDADE,
                           (x, 0.0, -METADE - ESPESSURA / 2))
    norte += "\n" + no("DoorWall", "Geometry/Walls", "3_porta", IDENTIDADE,
                       (-1.0, 0.0, -METADE - ESPESSURA / 2))
    sul = ""
    base_sul = giro_y(180)
    for k in range(9):
        x0 = -9.0 + k * GRADE
        sul += "\n" + no("WallSouth_%d" % k, "Geometry/Walls", "2_parede", base_sul,
                         (x0 + GRADE, 0.0, METADE + ESPESSURA / 2))
    oeste = ""
    base_oeste = giro_y(90)
    for k in range(8):
        z0 = -METADE - ESPESSURA / 2 + k * GRADE
        oeste += "\n" + no("WallWest_%d" % k, "Geometry/Walls", "2_parede", base_oeste,
                           (-METADE - ESPESSURA / 2, 0.0, z0 + GRADE))
    leste = ""
    base_leste = giro_y(-90)
    for k in range(8):
        z0 = -METADE - ESPESSURA / 2 + k * GRADE
        leste += "\n" + no("WallEast_%d" % k, "Geometry/Walls", "2_parede", base_leste,
                           (METADE + ESPESSURA / 2, 0.0, z0))
    partes.append(("Walls", norte + sul + oeste + leste))

    partes.append((None, "\n" + no("Column", "Geometry", "4_coluna", IDENTIDADE,
                                    (3.5, 0.0, -0.5))))

    saleta = ""
    for i in range(2):
        for j in range(2):
            saleta += "\n" + no("AnteFloor_%d_%d" % (i, j), "Geometry/AnteRoom", "1_piso",
                                IDENTIDADE, (-2.0 + i * GRADE, -ALTURA_PISO,
                                             -12.0 + j * GRADE))
    for k in range(2):
        saleta += "\n" + no("AnteWallNorth_%d" % k, "Geometry/AnteRoom", "2_parede", IDENTIDADE,
                            (-2.0 + k * GRADE, 0.0, -12.0 - ESPESSURA / 2))
        saleta += "\n" + no("AnteWallWest_%d" % k, "Geometry/AnteRoom", "2_parede", base_oeste,
                            (-2.0 - ESPESSURA / 2, 0.0, -12.0 + k * GRADE + GRADE))
        saleta += "\n" + no("AnteWallEast_%d" % k, "Geometry/AnteRoom", "2_parede", base_leste,
                            (2.0 + ESPESSURA / 2, 0.0, -12.0 + k * GRADE))
    partes.append(("AnteRoom", saleta))
    return partes


def montar():
    grupos = partes()
    cabecalho = ["[gd_scene load_steps=%d format=3]\n" % (len(EXT) + 2), ""]
    for caminho, ident in EXT:
        cabecalho.append('[ext_resource type="PackedScene" path="%s" id="%s"]'
                         % (caminho, ident))
    cabecalho.append("")
    texto = "\n".join(cabecalho) + AMBIENTE + "\n"
    texto += '[node name="KitRoom" type="Node3D"]\n'
    texto += '\n[node name="WorldEnvironment" type="WorldEnvironment" parent="."]\n'
    texto += 'environment = SubResource("Env_sala")\n'
    texto += '\n[node name="Geometry" type="Node3D" parent="."]\n'
    for nome, corpo in grupos:
        if nome is not None:
            texto += '\n[node name="%s" type="Node3D" parent="Geometry"]\n' % nome
        texto += corpo
    texto += '\n[node name="DoorSlot" type="Marker3D" parent="."]\n'
    texto += "transform = " + transform(IDENTIDADE, (0.0, 1.5, -METADE)) + "\n"
    return texto


def main():
    texto = montar()
    os.makedirs(os.path.dirname(SAIDA), exist_ok=True)
    with open(SAIDA, "w", encoding="utf-8") as f:
        f.write(texto)
    print("GERADO", SAIDA, len(texto.splitlines()), "linhas")


if __name__ == "__main__":
    main()
