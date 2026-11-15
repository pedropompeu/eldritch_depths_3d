extends TestCase
## T19: esquiva — deslocamento, invencibilidade que sobrevive a uma travada de
## frame, fim da invencibilidade e custo de vigor.

const CENA := "res://scenes/player/player_3d.tscn"
const CENA_RIG := "res://scenes/camera/camera_rig_3d.tscn"
const PASSO := 1.0 / 60.0


## Devolve [raiz, herói, entrada].
func _montar(tree: SceneTree) -> Array:
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
	var heroi: Player3D = load(CENA).instantiate()
	heroi.camera_rig = rig
	var entrada := {move = Vector2.ZERO, roll = false}
	heroi.input_source = func(): return entrada
	rig.target = heroi
	raiz.add_child(heroi)
	raiz.add_child(rig)
	tree.root.add_child(raiz)
	heroi.set_physics_process(false)
	await tree.physics_frame
	await tree.physics_frame
	return [raiz, heroi, entrada]


func _apertar_esquiva(heroi: Player3D, entrada: Dictionary) -> void:
	entrada.roll = true
	heroi.step(PASSO)
	entrada.roll = false


func _passos(heroi: Player3D, segundos: float) -> void:
	for i in roundi(segundos / PASSO):
		heroi.step(PASSO)


func _horizontal(v: Vector3) -> Vector3:
	return Vector3(v.x, 0.0, v.z)


func test_esquiva_desloca(tree: SceneTree) -> void:
	var m: Array = await _montar(tree)
	var heroi: Player3D = m[1]
	m[2].move = Vector2(1, 0)
	var antes := heroi.global_position
	_apertar_esquiva(heroi, m[2])
	assert_eq(heroi.state_machine.current_state.name, &"Roll")
	assert_near(heroi.stats.current_stamina, 80.0, 0.001)
	_passos(heroi, 0.34)
	assert_near(_horizontal(heroi.global_position - antes).length(), 3.5, 0.3)
	m[0].queue_free()


func test_esquiva_invencivel_com_travada(tree: SceneTree) -> void:
	var m: Array = await _montar(tree)
	var heroi: Player3D = m[1]
	# Hitbox inimiga grande, parada sobre o caminho inteiro da esquiva.
	var golpe := Hitbox3D.new()
	golpe.team = 1
	var forma := CollisionShape3D.new()
	var esfera := SphereShape3D.new()
	esfera.radius = 5.0
	forma.shape = esfera
	golpe.add_child(forma)
	golpe.position = Vector3(0, 0.9, 0)
	m[0].add_child(golpe)
	var contagem := {hurt = 0}
	heroi.hurtbox.hurt.connect(func(_h): contagem.hurt += 1)
	await tree.physics_frame
	await tree.physics_frame
	# Controle: fora da esquiva, o mesmo golpe acerta.
	golpe.activate()
	assert_eq(contagem.hurt, 1, "controle: o golpe deveria acertar o herói parado")
	golpe.deactivate()
	# Desde a T21 o golpe de controle leva ao `hurt` (0,3 s sem entrada): espera
	# ele acabar antes de esquivar.
	_passos(heroi, 0.35)
	assert_eq(heroi.state_machine.current_state.name, &"Idle")
	# Desde a T20 o golpe de controle tira vida; vale a vida de antes da esquiva.
	var vida_antes := heroi.stats.current_health

	_apertar_esquiva(heroi, m[2])
	heroi.step(0.02)
	heroi.step(0.22)
	# O golpe do mesmo frame chega depois do passo do herói.
	golpe.activate()
	assert_eq(contagem.hurt, 1, "nenhum golpe novo durante a invencibilidade")
	assert_near(heroi.stats.current_health, vida_antes, 0.001)
	assert_eq(heroi.state_machine.current_state.name, &"Roll")
	m[0].queue_free()


func test_vulneravel_depois(tree: SceneTree) -> void:
	var m: Array = await _montar(tree)
	var heroi: Player3D = m[1]
	_apertar_esquiva(heroi, m[2])
	_passos(heroi, 0.15)
	assert_true(heroi.hurtbox.invulnerable, "no meio da esquiva o herói é invencível")
	_passos(heroi, 0.15)
	assert_false(heroi.hurtbox.invulnerable)
	m[0].queue_free()


func test_esquiva_sem_vigor_nao_sai(tree: SceneTree) -> void:
	var m: Array = await _montar(tree)
	var heroi: Player3D = m[1]
	heroi.stats.current_stamina = 10.0
	_apertar_esquiva(heroi, m[2])
	assert_eq(heroi.state_machine.current_state.name, &"Idle")
	assert_near(heroi.stats.current_stamina, 10.0, 0.001)
	assert_false(heroi.hurtbox.invulnerable)
	m[0].queue_free()


func test_travada_que_termina_a_esquiva(tree: SceneTree) -> void:
	# Revisão final: um passo de 0,3 s que cobre a janela e também termina a
	# esquiva não pode desligar a invencibilidade antes dos golpes do frame.
	var m: Array = await _montar(tree)
	var heroi: Player3D = m[1]
	var golpe := Hitbox3D.new()
	golpe.team = 1
	var forma := CollisionShape3D.new()
	var esfera := SphereShape3D.new()
	esfera.radius = 5.0
	forma.shape = esfera
	golpe.add_child(forma)
	golpe.position = Vector3(0, 0.9, 0)
	m[0].add_child(golpe)
	var contagem := {hurt = 0}
	heroi.hurtbox.hurt.connect(func(_h): contagem.hurt += 1)
	await tree.physics_frame
	await tree.physics_frame
	var vida := heroi.stats.current_health
	_apertar_esquiva(heroi, m[2])
	heroi.step(0.1)
	heroi.step(0.3)
	assert_true(heroi.state_machine.current_state.name != &"Roll", "a travada terminou a esquiva")
	golpe.activate()
	assert_eq(contagem.hurt, 0, "o golpe do mesmo frame ainda pega a invencibilidade")
	assert_near(heroi.stats.current_health, vida, 0.001)
	golpe.deactivate()
	heroi.step(PASSO)
	assert_false(heroi.hurtbox.invulnerable, "no passo seguinte o herói volta a ser vulnerável")
	m[0].queue_free()
