extends TestCase
## T17: herói provisório — parado, andar relativo à câmera e mira pelo
## movimento no controle. Cada teste monta o herói, um rig de câmera e um piso.

const CENA := "res://scenes/player/player_3d.tscn"
const CENA_RIG := "res://scenes/camera/camera_rig_3d.tscn"
const InputModeScript := preload("res://scripts/core/input_mode.gd")
const PASSO := 1.0 / 60.0


## Monta piso, rig e herói; devolve [raiz, herói, entrada]. `entrada` é o
## dicionário que o `input_source` injetado devolve — o teste muda os campos.
func _montar(tree: SceneTree, yaw_deg := 45.0) -> Array:
	var raiz := Node3D.new()
	var piso := StaticBody3D.new()
	var forma := CollisionShape3D.new()
	var caixa := BoxShape3D.new()
	caixa.size = Vector3(40, 1, 40)
	forma.shape = caixa
	forma.position = Vector3(0, -0.5, 0)
	piso.add_child(forma)
	raiz.add_child(piso)

	var rig: CameraRig3D = load(CENA_RIG).instantiate()
	rig.yaw_deg = yaw_deg
	var heroi: Player3D = load(CENA).instantiate()
	heroi.camera_rig = rig
	var entrada := {move = Vector2.ZERO}
	heroi.input_source = func(): return entrada
	rig.target = heroi
	raiz.add_child(heroi)
	raiz.add_child(rig)
	tree.root.add_child(raiz)
	# Os testes dão os passos na mão.
	heroi.set_physics_process(false)
	await tree.physics_frame
	await tree.physics_frame
	return [raiz, heroi, entrada]


func _horizontal(v: Vector3) -> Vector3:
	return Vector3(v.x, 0.0, v.z)


func test_parado_e_idle(tree: SceneTree) -> void:
	var m: Array = await _montar(tree)
	var heroi: Player3D = m[1]
	for i in 10:
		heroi.step(PASSO)
	assert_eq(heroi.state_machine.current_state.name, &"Idle")
	assert_vec_near(heroi.velocity, Vector3.ZERO, 0.01)
	m[0].queue_free()


func test_anda_e_move(tree: SceneTree) -> void:
	var m: Array = await _montar(tree)
	var heroi: Player3D = m[1]
	m[2].move = Vector2(1, 0)
	for i in 30:
		heroi.step(PASSO)
	assert_eq(heroi.state_machine.current_state.name, &"Move")
	assert_near(_horizontal(heroi.velocity).length(), 5.0, 0.01)
	m[0].queue_free()


func test_movimento_relativo_a_camera(tree: SceneTree) -> void:
	var m: Array = await _montar(tree, 45.0)
	var heroi: Player3D = m[1]
	m[2].move = Vector2(0, -1)
	for i in 30:
		heroi.step(PASSO)
	assert_vec_near(heroi.velocity, Vector3(-3.54, 0, -3.54), 0.01)
	m[0].queue_free()


func test_mira_segue_movimento_no_pad(tree: SceneTree) -> void:
	var modo: Node = Autoloads.get_autoload(&"InputMode")
	var antes: int = modo.mode
	modo.mode = InputModeScript.Mode.PAD
	var m: Array = await _montar(tree, 45.0)
	var heroi: Player3D = m[1]
	m[2].move = Vector2(1, 0)
	m[2].aim = Vector2.ZERO
	heroi.step(PASSO)
	var esperado := PlayerMotion.input_to_world(Vector2(1, 0), deg_to_rad(45.0)).normalized()
	assert_vec_near(heroi.aim_dir, esperado, 0.001)
	modo.mode = antes
	m[0].queue_free()
