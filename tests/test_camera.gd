extends TestCase
## T12: câmera fixa inclinada — distância pelo tamanho do herói na tela e
## seguimento que não depende do fps.

const CENA := "res://scenes/camera/camera_rig_3d.tscn"


func test_distancia_proxima() -> void:
	assert_near(CameraRig3D.distance_for_fraction(1.8, 1.0 / 8.0, 40.0), 19.78, 0.05)


func test_distancia_atual() -> void:
	assert_near(CameraRig3D.distance_for_fraction(1.8, 1.0 / 13.0, 40.0), 32.15, 0.05)


func test_seguimento_independe_do_fps(tree: SceneTree) -> void:
	var alvo := Node3D.new()
	tree.root.add_child(alvo)
	var a: CameraRig3D = load(CENA).instantiate()
	var b: CameraRig3D = load(CENA).instantiate()
	for rig in [a, b]:
		rig.target = alvo
		tree.root.add_child(rig)
	# O rig nasce em cima do alvo; o alvo anda depois, para o seguimento valer.
	alvo.global_position = Vector3(10, 0, 0)
	a.step(0.0)
	assert_near(a.position.x, 0.0, 0.001, "passo zero não deveria mover o rig")
	for i in 60:
		a.step(1.0 / 60)
	for i in 30:
		b.step(1.0 / 30)
	assert_vec_near(a.position, b.position, 0.01)
	assert_true(a.position.x > 9.0, "o rig deveria ter chegado perto do alvo: %s" % a.position)
	for n in [a, b, alvo]:
		n.queue_free()


func test_alvo_projeta_no_centro(tree: SceneTree) -> void:
	var vp := SubViewport.new()
	vp.size = Vector2i(1920, 1080)
	tree.root.add_child(vp)
	var alvo := Node3D.new()
	vp.add_child(alvo)
	alvo.global_position = Vector3(3, 0, -2)
	var rig: CameraRig3D = load(CENA).instantiate()
	rig.target = alvo
	# Fora do passo de física, a câmera interpolada responde com a pose
	# desenhada, que só anda com frames de verdade. Aqui só a geometria importa.
	rig.physics_interpolation_mode = Node.PHYSICS_INTERPOLATION_MODE_OFF
	vp.add_child(rig)
	for i in 120:
		rig.step(1.0 / 60)
	var cam: Camera3D = rig.get_node("Camera3D")
	assert_near(cam.fov, 40.0)
	var p := cam.unproject_position(alvo.global_position)
	var centro := Vector2(960, 540)
	assert_true(absf(p.x - centro.x) < 0.02 * 1920 and absf(p.y - centro.y) < 0.02 * 1080,
		"alvo em %s, longe do centro %s" % [p, centro])
	assert_near(cam.global_position.distance_to(alvo.global_position), rig.distance, 0.05)
	vp.queue_free()


func test_interpolacao_de_fisica(tree: SceneTree) -> void:
	# Revisão final: o herói anda no passo de física; sem interpolação, ele
	# treme contra o cenário em monitores acima de 60 Hz.
	assert_true(ProjectSettings.get_setting("physics/common/physics_interpolation", false), "interpolação de física ligada no projeto")
	var rig: CameraRig3D = load(CENA).instantiate()
	tree.root.add_child(rig)
	await tree.process_frame
	assert_true(rig.is_physics_processing(), "a câmera anda no passo de física, junto com o herói")
	assert_false(rig.is_processing(), "e não no frame de desenho")
	rig.queue_free()
