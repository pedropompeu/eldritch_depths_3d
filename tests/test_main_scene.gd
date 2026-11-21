extends TestCase
## T25: cena principal — sala cinza, herói com luz, câmera, inimigo e o dreno
## ambiente de sanidade.

const CENA := "res://scenes/main.tscn"
const PASSO := 1.0 / 60.0


func _montar(tree: SceneTree) -> Node:
	var main: Node = load(CENA).instantiate()
	tree.root.add_child(main)
	await tree.physics_frame
	return main


func _achar(raiz: Node, tipo: String) -> Node:
	for no in raiz.find_children("*", "", true, false):
		var s: Script = no.get_script()
		if no.is_class(tipo) or (s and s.get_global_name() == tipo):
			return no
	return null


func test_main_carrega(tree: SceneTree) -> void:
	var main: Node = await _montar(tree)
	var heroi: Player3D = _achar(main, "Player3D")
	var inimigo: EnemyCommon = _achar(main, "EnemyCommon")
	var rig: CameraRig3D = _achar(main, "CameraRig3D")
	assert_true(heroi != null, "tem Player3D")
	assert_true(inimigo != null, "tem EnemyCommon")
	assert_true(rig != null, "tem CameraRig3D")
	assert_true(_achar(main, "WorldEnvironment") != null, "tem WorldEnvironment")
	assert_true(_achar(main, "DirectionalLight3D") == null, "sem luz direcional")
	if heroi:
		var luz := heroi.get_node_or_null("HeroLight") as OmniLight3D
		assert_true(luz != null, "HeroLight é filha do herói")
		assert_true(heroi.camera_rig == rig, "o herói usa o rig da cena")
		assert_true(heroi.hero_died.get_connections().size() > 0, "morte do herói ligada ao recarregamento")
	if rig:
		assert_true(rig.target == heroi, "a câmera segue o herói")
	if inimigo and heroi:
		assert_true(inimigo.target == heroi, "o inimigo mira o herói")
		var d := inimigo.global_position - heroi.global_position
		assert_near(Vector2(d.x, d.z).length(), 6.0, 0.01, "inimigo a 6 m")
	assert_true(main.find_child("DoorSlot", true, false) is Marker3D, "DoorSlot na sala")
	main.queue_free()


func test_sala_do_kit(tree: SceneTree) -> void:
	## B15: a sala montada com as peças do kit cobre o mesmo lugar da sala cinza.
	var main: Node = await _montar(tree)
	assert_true(main.has_node("KitRoom"), "main.tscn usa a KitRoom")
	assert_false(main.has_node("GreyboxRoom"), "a sala cinza saiu da cena")
	var espaco: PhysicsDirectSpaceState3D = main.get_world_3d().direct_space_state
	var acertos := 0
	for i in 5:
		for j in 5:
			var x := -6.0 + i * 3.0
			var z := -6.0 + j * 3.0
			var q := PhysicsRayQueryParameters3D.create(Vector3(x, 2.0, z),
				Vector3(x, -1.0, z), 1)
			var r: Dictionary = espaco.intersect_ray(q)
			if not r.is_empty() and absf(r.position.y) < 0.02:
				acertos += 1
	assert_eq(acertos, 25, "piso contínuo em 25 pontos da grade")
	# A coluna fica em (4, 0), no caminho do raio para +X; os raios de lado saem
	# deslocados em Z para medir a parede, não a coluna.
	var lados := [[Vector3(0.0, 1.5, -2.5), Vector3.RIGHT],
		[Vector3(0.0, 1.5, 2.5), Vector3.LEFT],
		[Vector3(0.0, 1.5, 0.0), Vector3.FORWARD],
		[Vector3(0.0, 1.5, 0.0), Vector3.BACK]]
	for lado in lados:
		var origem: Vector3 = lado[0]
		var dir: Vector3 = lado[1]
		var q := PhysicsRayQueryParameters3D.create(origem, origem + dir * 9.0, 1)
		var r: Dictionary = espaco.intersect_ray(q)
		assert_false(r.is_empty(), "parede em %s" % str(dir))
		if not r.is_empty():
			assert_near(origem.distance_to(r.position), 8.0, 0.3,
				"parede em %s a 8 m" % str(dir))
	var vaga: Marker3D = main.find_child("DoorSlot", true, false)
	assert_true(vaga != null, "KitRoom tem DoorSlot")
	if vaga:
		assert_vec_near(vaga.global_position, Vector3(0.0, 1.5, -8.0), 0.01,
			"DoorSlot no mesmo lugar da sala cinza")
	main.queue_free()


func test_drena_sanidade(tree: SceneTree) -> void:
	var main: Node = await _montar(tree)
	var heroi: Player3D = _achar(main, "Player3D")
	heroi.stats.set_process(false)
	var antes := heroi.stats.current_sanity
	for i in 600:
		heroi.stats._process(PASSO)
	assert_near(antes - heroi.stats.current_sanity, 8.0, 0.01, "0,8/s por 10 s")
	main.queue_free()
