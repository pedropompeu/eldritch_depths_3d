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


func test_drena_sanidade(tree: SceneTree) -> void:
	var main: Node = await _montar(tree)
	var heroi: Player3D = _achar(main, "Player3D")
	heroi.stats.set_process(false)
	var antes := heroi.stats.current_sanity
	for i in 600:
		heroi.stats._process(PASSO)
	assert_near(antes - heroi.stats.current_sanity, 8.0, 0.01, "0,8/s por 10 s")
	main.queue_free()
