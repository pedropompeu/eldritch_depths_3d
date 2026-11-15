"""B03: testes do módulo ed_blender. Rodar com tools/test_blender.sh (Blender sem janela)."""
import json
import os
import struct
import subprocess
import sys
import traceback

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.abspath(os.path.join(AQUI, "..", "..", ".."))
sys.path.insert(0, os.path.join(RAIZ, "tools", "blender"))

import bpy  # noqa: E402
import ed_blender as ed  # noqa: E402

TMP = os.path.join(RAIZ, ".godot", "capturas_tmp", "blender_tests")
os.makedirs(TMP, exist_ok=True)


def _cubo(tamanho=2.0, local=(0.0, 0.0, 0.0)):
    bpy.ops.mesh.primitive_cube_add(size=tamanho, location=local)
    return bpy.context.active_object


def _icosfera(sub=6):
    # No Blender, subdivisions=1 já é o icosaedro (20 faces): 2 → 80, 3 → 320, 6 → 20.480.
    bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=sub, radius=1.0)
    return bpy.context.active_object


def _png_tamanho(caminho):
    with open(caminho, "rb") as f:
        cab = f.read(24)
    assert cab[:8] == b"\x89PNG\r\n\x1a\n", "não é PNG: %s" % caminho
    return struct.unpack(">II", cab[16:24])


def _perto(a, b, eps, msg=""):
    assert abs(a - b) <= eps, "%s esperado %s ± %s, veio %s" % (msg, b, eps, a)


def test_escala_altura():
    ed.reset_scene()
    obj = _cubo(2.0)
    ed.scale_to_height(obj, 1.8)
    _perto(ed.report([obj])["dims"][2], 1.8, 0.001, "altura")


def test_origem_nos_pes():
    ed.reset_scene()
    obj = _cubo(1.0, (3.0, -2.0, 5.0))
    ed.set_origin_to_feet(obj)
    r = ed.report([obj])
    _perto(r["min_z"], 0.0, 0.001, "base")
    _perto(obj.location.x, 0.0, 0.001, "origem x")
    _perto(obj.location.y, 0.0, 0.001, "origem y")
    xs = [(obj.matrix_world @ v.co).x for v in obj.data.vertices]
    _perto((min(xs) + max(xs)) / 2, 0.0, 0.001, "centro x")


def test_decimate():
    ed.reset_scene()
    obj = _icosfera(6)
    assert ed.report([obj])["tris"] == 20480
    final = ed.decimate_to(obj, 5000)
    assert 4000 <= final <= 5000, "triângulos depois: %d" % final
    assert ed.report([obj])["tris"] == final


def test_exporta_e_reimporta():
    ed.reset_scene()
    obj = _icosfera(3)
    tris = ed.report([obj])["tris"]
    caminho = os.path.join(TMP, "ico.glb")
    ed.export_glb([obj], caminho)
    ed.reset_scene()
    novos = ed.import_any(caminho)
    assert len(novos) >= 1
    assert ed.report(novos)["tris"] == tris


def test_turnaround():
    ed.reset_scene()
    obj = _cubo(1.0, (0.0, 0.0, 0.5))
    saida = os.path.join(TMP, "turn")
    arquivos = ed.render_turnaround([obj], saida, size=128)
    nomes = sorted(os.path.basename(a) for a in arquivos)
    assert nomes == ["costas.png", "frente.png", "lado.png", "tres_quartos.png"], nomes
    for a in arquivos:
        assert _png_tamanho(a) == (128, 128), a
    # Câmeras e luzes da pré-visualização não ficam na cena.
    assert [o.name for o in bpy.context.scene.objects] == [obj.name]


def test_relatorio():
    ed.reset_scene()
    obj = _icosfera(3)
    caminho = os.path.join(TMP, "rel.glb")
    ed.export_glb([obj], caminho)
    proc = subprocess.run([os.path.join(RAIZ, "tools", "blender.sh"), "tools/blender/report.py", caminho],
                          cwd=RAIZ, capture_output=True, text=True, timeout=120)
    linhas = [l for l in proc.stdout.splitlines() if l.startswith("RELATORIO ")]
    assert proc.returncode == 0, proc.stdout[-500:] + proc.stderr[-500:]
    assert len(linhas) == 1, proc.stdout[-500:]
    dados = json.loads(linhas[0][len("RELATORIO "):])
    assert set(dados) == {"tris", "dims", "min_z", "materials", "has_uv", "bones", "actions"}, sorted(dados)
    assert dados["tris"] == 320


def test_remesh_quadriflow():
    ed.reset_scene()
    obj = _icosfera(3)
    novo = ed.remesh_quadriflow(obj, 600)
    assert novo is not obj and obj.name in bpy.data.objects
    faces = len(novo.data.polygons)
    assert 300 <= faces <= 1200, "faces: %d" % faces
    quads = sum(1 for p in novo.data.polygons if len(p.vertices) == 4)
    assert quads / faces > 0.9, "quads: %d de %d" % (quads, faces)


def test_bake_color():
    ed.reset_scene()
    bpy.ops.mesh.primitive_plane_add(size=2.0)
    src = bpy.context.active_object
    mat = bpy.data.materials.new("vermelho")
    mat.use_nodes = True
    mat.node_tree.nodes["Principled BSDF"].inputs["Base Color"].default_value = (0.8, 0.0, 0.0, 1.0)
    src.data.materials.append(mat)
    bpy.ops.mesh.primitive_plane_add(size=2.0)
    dst = bpy.context.active_object
    ed.smart_uv(dst)
    assert ed.report([dst])["has_uv"]
    saida = ed.bake_color(src, dst, 64, os.path.join(TMP, "bake.png"))
    assert _png_tamanho(saida) == (64, 64)
    img = bpy.data.images.load(saida)
    px = list(img.pixels)
    meio = (32 * 64 + 32) * 4
    r, g, b = px[meio:meio + 3]
    assert r > 0.5 and g < 0.1 and b < 0.1, "cor assada no meio: %s" % ((r, g, b),)


def test_join_meshes():
    ed.reset_scene()
    a = _cubo(1.0)
    b = _cubo(1.0, (3.0, 0.0, 0.0))
    junto = ed.join_meshes([a, b], "junto")
    assert junto.name == "junto"
    assert [o.name for o in bpy.context.scene.objects] == ["junto"]
    assert ed.report([junto])["tris"] == 24


def _rodar():
    testes = [(n, f) for n, f in globals().items() if n.startswith("test_") and callable(f)]
    falhas = 0
    for nome, f in testes:
        try:
            f()
        except Exception as e:  # noqa: BLE001
            falhas += 1
            print("FAIL %s: %s" % (nome, e or type(e).__name__))
            traceback.print_exc(limit=3)
    print("OK: %d testes" % len(testes) if falhas == 0 else "FALHOU: %d de %d" % (falhas, len(testes)))
    sys.stdout.flush()
    return 1 if falhas else 0


sys.exit(_rodar())
