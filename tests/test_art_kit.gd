extends TestCase
## B14: peças do kit modular — arquivos, orçamento, medidas da tabela e origem no canto de grade.
## A grade é de 2 m (guia de estilo) e cada peça tem origem no canto: base em y = 0, crescendo em +X e +Z.

const DIMENSOES := {
	"piso": Vector3(2.0, 0.15, 2.0),
	"parede": Vector3(2.0, 3.0, 0.4),
	"parede_porta": Vector3(2.0, 3.0, 0.4),
	"canto": Vector3(0.4, 3.0, 0.4),
	"coluna": Vector3(1.0, 3.0, 1.0),
}
const MAX_TRIS := 1500
const TOLERANCIA := 0.02


static func _carregar_glb(caminho: String) -> Node3D:
	var doc := GLTFDocument.new()
	var estado := GLTFState.new()
	if doc.append_from_file(ProjectSettings.globalize_path(caminho), estado) != OK:
		return null
	return doc.generate_scene(estado) as Node3D


static func _malhas(no: Node, saida: Array[MeshInstance3D]) -> void:
	if no is MeshInstance3D:
		saida.append(no)
	for filho in no.get_children():
		_malhas(filho, saida)


static func _medir(raiz: Node3D) -> Dictionary:
	var malhas: Array[MeshInstance3D] = []
	_malhas(raiz, malhas)
	var tris := 0
	var superficies := 0
	var vertices := PackedVector3Array()
	var caixa := AABB()
	var primeira := true
	for mi in malhas:
		var xf := mi.transform
		var pai := mi.get_parent()
		while pai is Node3D:
			xf = (pai as Node3D).transform * xf
			pai = pai.get_parent()
		superficies += mi.mesh.get_surface_count()
		for s in mi.mesh.get_surface_count():
			var arr := mi.mesh.surface_get_arrays(s)
			var idx: PackedInt32Array = arr[Mesh.ARRAY_INDEX]
			var verts: PackedVector3Array = arr[Mesh.ARRAY_VERTEX]
			tris += (idx.size() if idx.size() > 0 else verts.size()) / 3
			for v in verts:
				var p := xf * v
				vertices.append(p)
				if primeira:
					caixa = AABB(p, Vector3.ZERO)
					primeira = false
				else:
					caixa = caixa.expand(p)
	return {"tris": tris, "caixa": caixa, "superficies": superficies, "vertices": vertices}


func test_pecas_do_kit() -> void:
	for nome in DIMENSOES:
		var caminho := "res://assets/models/kit/%s.glb" % nome
		var raiz := _carregar_glb(caminho)
		assert_true(raiz != null, "%s não abre" % caminho)
		if raiz == null:
			continue
		var m := _medir(raiz)
		raiz.free()
		var caixa: AABB = m.caixa
		assert_true(m.tris > 0 and m.tris <= MAX_TRIS,
				"%s: triângulos %d (limite %d)" % [nome, m.tris, MAX_TRIS])
		assert_eq(m.superficies, 1, "%s: %d materiais (o guia pede 1)" % [nome, m.superficies])
		assert_vec_near(caixa.size, DIMENSOES[nome], TOLERANCIA,
				"%s: medidas %s (tabela %s)" % [nome, str(caixa.size), str(DIMENSOES[nome])])
		assert_near(caixa.position.y, 0.0, TOLERANCIA, "%s: base fora do chão" % nome)
		assert_near(caixa.position.x, 0.0, TOLERANCIA, "%s: origem fora do canto de grade em X" % nome)
		assert_near(caixa.position.z, 0.0, TOLERANCIA, "%s: origem fora do canto de grade em Z" % nome)


func test_vao_da_porta() -> void:
	var raiz := _carregar_glb("res://assets/models/kit/parede_porta.glb")
	assert_true(raiz != null, "assets/models/kit/parede_porta.glb não abre")
	if raiz == null:
		return
	var m := _medir(raiz)
	raiz.free()
	var vertices: PackedVector3Array = m.vertices
	var dentro := 0
	for p in vertices:
		# Vão de 2 m de largura × 2,4 m de altura: nenhum vértice da peça pode cair ali
		# (a soleira fica abaixo de 0,1 m e a verga acima de 2,4 m).
		if absf(p.x - 1.0) < 0.9 and p.y > 0.1 and p.y < 2.3:
			dentro += 1
	assert_eq(dentro, 0, "%d vértices dentro do vão da porta" % dentro)
