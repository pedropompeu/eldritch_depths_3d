extends TestCase
## B04+: props prontos em assets/models/props/ cabem no orçamento e na escala do guia de estilo.


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
	var caixa := AABB()
	var primeira := true
	for mi in malhas:
		var xf := mi.transform
		var pai := mi.get_parent()
		while pai is Node3D:
			xf = (pai as Node3D).transform * xf
			pai = pai.get_parent()
		for s in mi.mesh.get_surface_count():
			var arr := mi.mesh.surface_get_arrays(s)
			var idx: PackedInt32Array = arr[Mesh.ARRAY_INDEX]
			var verts: PackedVector3Array = arr[Mesh.ARRAY_VERTEX]
			tris += (idx.size() if idx.size() > 0 else verts.size()) / 3
			for v in verts:
				var p := xf * v
				if primeira:
					caixa = AABB(p, Vector3.ZERO)
					primeira = false
				else:
					caixa = caixa.expand(p)
	return {"tris": tris, "caixa": caixa, "malhas": malhas.size()}


func test_braseiro() -> void:
	var raiz := _carregar_glb("res://assets/models/props/braseiro.glb")
	assert_true(raiz != null, "assets/models/props/braseiro.glb não abre")
	if raiz == null:
		return
	var m := _medir(raiz)
	raiz.free()
	var caixa: AABB = m.caixa
	assert_true(m.tris > 0 and m.tris <= 3000, "triângulos: %d (limite 3.000)" % m.tris)
	assert_true(caixa.size.y >= 0.8 and caixa.size.y <= 1.2, "altura: %.3f m (0,8 a 1,2)" % caixa.size.y)
	assert_near(caixa.position.y, 0.0, 0.03, "base fora do chão")


func test_cena_braseiro() -> void:
	var cena := load("res://scenes/props/brazier.tscn") as PackedScene
	assert_true(cena != null, "scenes/props/brazier.tscn não carrega")
	if cena == null:
		return
	var b := cena.instantiate()
	assert_true(b is StaticBody3D, "a raiz do braseiro deve ser StaticBody3D")
	assert_eq((b as CollisionObject3D).collision_layer, 1, "braseiro fora da camada 1")
	var forma := b.get_node_or_null("CollisionShape3D") as CollisionShape3D
	assert_true(forma != null and forma.shape is CylinderShape3D, "falta colisão em cilindro")
	var luz := b.get_node_or_null("FlameLight") as OmniLight3D
	assert_true(luz != null, "falta a OmniLight3D FlameLight")
	if luz != null:
		assert_false(luz.shadow_enabled, "FlameLight com sombra (desligada por desempenho)")
		assert_true(luz.light_color.is_equal_approx(Color("#ff8a3d")), "FlameLight fora da cor brasa")
	var malhas: Array[MeshInstance3D] = []
	_malhas(b, malhas)
	assert_true(malhas.size() > 0, "braseiro sem o modelo")
	b.free()
