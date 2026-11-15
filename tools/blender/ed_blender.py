"""Kit do Blender sem janela para a trilha de arte do Eldritch Depths 3D (B03).

Todo `build.py` de peça usa estas funções: importar o bruto, limpar, caber no
orçamento, assar a cor, pôr a origem nos pés, renderizar as pré-visualizações e
exportar o .glb. Escala: 1 unidade = 1 m; Z para cima no Blender, Y no glTF.
"""
import math
import os

import bpy
from mathutils import Matrix, Vector

# Luz das pré-visualizações (docs/arte/guia-de-estilo.md).
FUNDO = "#05060a"
LUZ_PRINCIPAL = "#ffb36b"
CONTRALUZ = "#3a4a6a"


def _linear(hexcor):
    """Cor hex sRGB → tupla RGB linear (o que o Blender espera em luzes e mundo)."""
    def canal(c):
        c = c / 255.0
        return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4
    h = hexcor.lstrip("#")
    return tuple(canal(int(h[i:i + 2], 16)) for i in (0, 2, 4))


def _select(objs, active=None):
    for o in bpy.context.view_layer.objects:
        o.select_set(False)
    for o in objs:
        o.select_set(True)
    bpy.context.view_layer.objects.active = active or (objs[0] if objs else None)


def _com_filhos(objs):
    saida = []
    for o in objs:
        if o not in saida:
            saida.append(o)
        for f in o.children_recursive:
            if f not in saida:
                saida.append(f)
    return saida


def _malhas(objs):
    return [o for o in _com_filhos(objs) if o.type == "MESH"]


def _pontos_mundo(objs):
    dg = bpy.context.evaluated_depsgraph_get()
    pts = []
    for o in _malhas(objs):
        ev = o.evaluated_get(dg)
        m = ev.to_mesh()
        pts.extend(ev.matrix_world @ v.co for v in m.vertices)
        ev.to_mesh_clear()
    return pts


def _caixa(objs):
    pts = _pontos_mundo(objs)
    if not pts:
        return Vector((0, 0, 0)), Vector((0, 0, 0))
    lo = Vector((min(p.x for p in pts), min(p.y for p in pts), min(p.z for p in pts)))
    hi = Vector((max(p.x for p in pts), max(p.y for p in pts), max(p.z for p in pts)))
    return lo, hi


def _tris(obj):
    dg = bpy.context.evaluated_depsgraph_get()
    ev = obj.evaluated_get(dg)
    m = ev.to_mesh()
    m.calc_loop_triangles()
    n = len(m.loop_triangles)
    ev.to_mesh_clear()
    return n


def reset_scene():
    """Cena vazia, unidades métricas, escala 1."""
    bpy.ops.wm.read_factory_settings(use_empty=True)
    us = bpy.context.scene.unit_settings
    us.system = "METRIC"
    us.scale_length = 1.0


def import_any(path):
    """Importa .glb/.gltf/.fbx/.obj pela extensão e devolve os objetos novos."""
    antes = set(bpy.data.objects.keys())
    ext = os.path.splitext(path)[1].lower()
    if ext in (".glb", ".gltf"):
        bpy.ops.import_scene.gltf(filepath=path)
    elif ext == ".fbx":
        bpy.ops.import_scene.fbx(filepath=path)
    elif ext == ".obj":
        bpy.ops.wm.obj_import(filepath=path)
    else:
        raise ValueError("extensão não suportada: %s" % ext)
    return [bpy.data.objects[n] for n in bpy.data.objects.keys() if n not in antes]


def join_meshes(objs, name):
    malhas = [o for o in objs if o.type == "MESH"]
    _select(malhas, malhas[0])
    if len(malhas) > 1:
        bpy.ops.object.join()
    obj = bpy.context.view_layer.objects.active
    obj.name = name
    obj.data.name = name
    return obj


def apply_transforms(obj):
    _select([obj], obj)
    bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)


def scale_to_height(obj, height_m):
    """Escala uniforme até a altura em Z ser `height_m`."""
    lo, hi = _caixa([obj])
    altura = hi.z - lo.z
    if altura <= 0:
        raise ValueError("objeto sem altura: %s" % obj.name)
    obj.scale = obj.scale * (height_m / altura)
    apply_transforms(obj)


def set_origin_to_feet(obj):
    """Origem no centro XY da base; base em z = 0."""
    apply_transforms(obj)
    lo, hi = _caixa([obj])
    obj.data.transform(Matrix.Translation((-(lo.x + hi.x) / 2, -(lo.y + hi.y) / 2, -lo.z)))
    obj.location = (0.0, 0.0, 0.0)


def decimate_to(obj, max_tris):
    """Reduz com Decimate (collapse) até ≤ max_tris. Devolve os triângulos finais."""
    for _ in range(8):
        tris = _tris(obj)
        if tris <= max_tris:
            return tris
        mod = obj.modifiers.new("decimar", "DECIMATE")
        mod.decimate_type = "COLLAPSE"
        mod.ratio = max_tris / tris * 0.97
        _select([obj], obj)
        bpy.ops.object.modifier_apply(modifier=mod.name)
    tris = _tris(obj)
    if tris > max_tris:
        raise RuntimeError("decimate não chegou a %d (ficou %d)" % (max_tris, tris))
    return tris


def remesh_quadriflow(obj, target_faces):
    """Malha nova em quads (QuadriFlow) a partir de uma cópia; a original fica intacta.
    Se a malha não for fechada, passa antes por um remesh de voxel."""
    novo = obj.copy()
    novo.data = obj.data.copy()
    novo.name = obj.name + "_remesh"
    for c in obj.users_collection:
        c.objects.link(novo)
    _select([novo], novo)
    try:
        r = bpy.ops.object.quadriflow_remesh(target_faces=target_faces)
    except RuntimeError:
        r = {"CANCELLED"}
    if "FINISHED" not in r or len(novo.data.polygons) == len(obj.data.polygons):
        lo, hi = _caixa([novo])
        mod = novo.modifiers.new("voxel", "REMESH")
        mod.mode = "VOXEL"
        mod.voxel_size = max(hi - lo) / 150.0
        bpy.ops.object.modifier_apply(modifier=mod.name)
        r = bpy.ops.object.quadriflow_remesh(target_faces=target_faces)
        if "FINISHED" not in r:
            raise RuntimeError("quadriflow falhou em %s" % obj.name)
    return novo


def smart_uv(obj, margin=0.01):
    _select([obj], obj)
    bpy.ops.object.mode_set(mode="EDIT")
    bpy.ops.mesh.select_all(action="SELECT")
    bpy.ops.uv.smart_project(island_margin=margin)
    bpy.ops.object.mode_set(mode="OBJECT")


def _cycles_cpu(samples):
    cena = bpy.context.scene
    cena.render.engine = "CYCLES"
    cena.cycles.device = "CPU"
    cena.cycles.samples = samples


def bake_color(src, dst, size, out_png):
    """Assa a cor difusa de `src` na UV de `dst` (Cycles, CPU) e salva em `out_png`."""
    _cycles_cpu(4)
    img = bpy.data.images.new(os.path.basename(out_png), size, size, alpha=False)
    if not dst.data.materials:
        dst.data.materials.append(bpy.data.materials.new(dst.name + "_mat"))
    for mat in dst.data.materials:
        mat.use_nodes = True
        no = mat.node_tree.nodes.new("ShaderNodeTexImage")
        no.image = img
        mat.node_tree.nodes.active = no
    _select([src, dst], dst)
    bpy.ops.object.bake(type="DIFFUSE", pass_filter={"COLOR"}, use_selected_to_active=True,
                        cage_extrusion=0.05, margin=4)
    os.makedirs(os.path.dirname(os.path.abspath(out_png)), exist_ok=True)
    img.filepath_raw = out_png
    img.file_format = "PNG"
    img.save()
    return out_png


def _olhar(obj, alvo):
    obj.rotation_euler = (alvo - obj.location).to_track_quat("-Z", "Y").to_euler()


def render_turnaround(objs, out_dir, size=1024):
    """Quatro PNGs (frente, lado, costas, tres_quartos) com a luz do guia. A peça olha para −Y.
    Câmera e luzes são removidas no fim."""
    cena = bpy.context.scene
    _cycles_cpu(32)
    cena.render.resolution_x = size
    cena.render.resolution_y = size
    cena.render.resolution_percentage = 100
    cena.render.image_settings.file_format = "PNG"
    mundo_antigo = cena.world
    mundo = bpy.data.worlds.new("previa")
    mundo.use_nodes = True
    fundo = mundo.node_tree.nodes["Background"]
    fundo.inputs["Color"].default_value = (*_linear(FUNDO), 1.0)
    cena.world = mundo

    lo, hi = _caixa(objs)
    centro = (lo + hi) / 2
    ext = max(hi - lo) or 1.0
    raio = (hi - lo).length / 2 or 0.5

    criados = []

    def luz(nome, cor, energia, pos):
        dados = bpy.data.lights.new(nome, "POINT")
        dados.color = _linear(cor)
        dados.energy = energia
        dados.shadow_soft_size = ext * 0.2
        o = bpy.data.objects.new(nome, dados)
        cena.collection.objects.link(o)
        o.location = pos
        criados.append(o)

    luz("previa_principal", LUZ_PRINCIPAL, 120.0 * ext * ext, centro + Vector((0.6, -1.6, 1.4)) * ext)
    luz("previa_contraluz", CONTRALUZ, 200.0 * ext * ext, centro + Vector((-0.5, 1.6, 1.8)) * ext)

    cam_dados = bpy.data.cameras.new("previa_cam")
    cam = bpy.data.objects.new("previa_cam", cam_dados)
    cena.collection.objects.link(cam)
    criados.append(cam)
    cena.camera = cam
    cam_dados.clip_end = ext * 20

    os.makedirs(out_dir, exist_ok=True)
    elev = math.radians(55)
    vistas = [
        ("frente", Vector((0, -1, 0)), True),
        ("lado", Vector((1, 0, 0)), True),
        ("costas", Vector((0, 1, 0)), True),
        ("tres_quartos", Vector((math.sin(math.radians(35)) * math.cos(elev),
                                 -math.cos(math.radians(35)) * math.cos(elev), math.sin(elev))), False),
    ]
    saida = []
    for nome, direcao, orto in vistas:
        if orto:
            cam_dados.type = "ORTHO"
            cam_dados.ortho_scale = ext * 1.15
            dist = ext * 3
        else:
            cam_dados.type = "PERSP"
            cam_dados.lens = 50
            dist = raio / math.tan(cam_dados.angle / 2) * 1.15
        cam.location = centro + direcao.normalized() * dist
        _olhar(cam, centro)
        caminho = os.path.join(out_dir, nome + ".png")
        cena.render.filepath = caminho
        bpy.ops.render.render(write_still=True)
        saida.append(caminho)

    for o in criados:
        dados = o.data
        bpy.data.objects.remove(o)
        if isinstance(dados, bpy.types.Light):
            bpy.data.lights.remove(dados)
        else:
            bpy.data.cameras.remove(dados)
    cena.world = mundo_antigo
    bpy.data.worlds.remove(mundo)
    # Sem isto a camada de vista ainda lista os objetos removidos (None) e o próximo
    # _select (ex.: export_glb) quebra.
    bpy.context.view_layer.update()
    return saida


def export_glb(objs, path, animations=False):
    """glTF binário (Y para cima), modificadores aplicados; leva os filhos junto."""
    os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
    _select(_com_filhos(objs), objs[0])
    bpy.ops.export_scene.gltf(filepath=path, export_format="GLB", use_selection=True,
                              export_yup=True, export_apply=True, export_animations=animations)


def report(objs):
    """Resumo para conferir orçamento e escala: tris, dims [x, y, z] em m, min_z, materiais,
    UV, ossos e actions."""
    todos = _com_filhos(objs)
    malhas = [o for o in todos if o.type == "MESH"]
    armaduras = {o for o in todos if o.type == "ARMATURE"}
    armaduras.update(o.parent for o in malhas if o.parent and o.parent.type == "ARMATURE")
    lo, hi = _caixa(objs)
    materiais = {m.name for o in malhas for m in o.data.materials if m}
    return {
        "tris": sum(_tris(o) for o in malhas),
        "dims": [round(v, 4) for v in (hi - lo)],
        "min_z": round(lo.z, 4),
        "materials": len(materiais),
        "has_uv": bool(malhas) and all(len(o.data.uv_layers) > 0 for o in malhas),
        "bones": sum(len(a.data.bones) for a in armaduras),
        "actions": sorted(a.name for a in bpy.data.actions),
    }
