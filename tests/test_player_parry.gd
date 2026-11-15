extends TestCase
## T20: parry — na janela, o herói não toma dano e a postura de quem bateu
## enche 50; fora dela, o golpe dói; golpe cósmico tira sanidade.

const CENA := "res://scenes/player/player_3d.tscn"
const CENA_RIG := "res://scenes/camera/camera_rig_3d.tscn"
const PASSO := 1.0 / 60.0


## Devolve [raiz, herói, entrada, golpe, postura do atacante].
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

	# Atacante de teste: um nó com postura e uma hitbox inimiga sobre o herói.
	var atacante := Node3D.new()
	var postura := PostureComponent.new()
	atacante.add_child(postura)
	var golpe := Hitbox3D.new()
	golpe.team = 1
	golpe.source = atacante
	var forma_golpe := CollisionShape3D.new()
	var esfera := SphereShape3D.new()
	esfera.radius = 1.0
	forma_golpe.shape = esfera
	golpe.add_child(forma_golpe)
	golpe.position = Vector3(0, 0.9, 0)
	atacante.add_child(golpe)
	raiz.add_child(atacante)

	var rig: CameraRig3D = load(CENA_RIG).instantiate()
	var heroi: Player3D = load(CENA).instantiate()
	heroi.camera_rig = rig
	var entrada := {move = Vector2.ZERO, parry = false}
	heroi.input_source = func(): return entrada
	rig.target = heroi
	raiz.add_child(heroi)
	raiz.add_child(rig)
	tree.root.add_child(raiz)
	heroi.set_physics_process(false)
	# A postura do atacante não deve se recuperar sozinha entre as checagens.
	postura.set_process(false)
	await tree.physics_frame
	await tree.physics_frame
	return [raiz, heroi, entrada, golpe, postura]


func _apertar_parry(heroi: Player3D, entrada: Dictionary) -> void:
	entrada.parry = true
	heroi.step(PASSO)
	entrada.parry = false


func _passos(heroi: Player3D, segundos: float) -> void:
	for i in roundi(segundos / PASSO):
		heroi.step(PASSO)


func test_parry_quebra_postura(tree: SceneTree) -> void:
	var m: Array = await _montar(tree)
	var heroi: Player3D = m[1]
	_apertar_parry(heroi, m[2])
	assert_eq(heroi.state_machine.current_state.name, &"Parry")
	assert_near(heroi.stats.current_stamina, 85.0, 0.001)
	_passos(heroi, 0.1)
	m[3].activate()
	assert_near(heroi.stats.current_health, 100.0, 0.001, "parry na janela não toma dano")
	assert_near(m[4].current, 50.0, 0.001, "postura do atacante")
	m[0].queue_free()


func test_parry_atrasado_toma_dano(tree: SceneTree) -> void:
	var m: Array = await _montar(tree)
	var heroi: Player3D = m[1]
	_apertar_parry(heroi, m[2])
	_passos(heroi, 0.3)
	assert_false(heroi.hurtbox.parrying, "a janela de 0,22 s já fechou")
	m[3].activate()
	assert_near(heroi.stats.current_health, 80.0, 0.001)
	assert_near(m[4].current, 0.0, 0.001)
	m[0].queue_free()


func test_golpe_cosmico_tira_sanidade(tree: SceneTree) -> void:
	var m: Array = await _montar(tree)
	var heroi: Player3D = m[1]
	m[3].sanity_damage = 15.0
	m[3].activate()
	assert_near(heroi.stats.current_sanity, 85.0, 0.001)
	assert_near(heroi.stats.current_health, 80.0, 0.001)
	m[0].queue_free()


func test_travada_que_termina_o_parry(tree: SceneTree) -> void:
	# Revisão final: um passo de 0,35 s que cobre a janela e também termina o
	# parry não pode fechar a janela antes dos golpes do frame.
	var m: Array = await _montar(tree)
	var heroi: Player3D = m[1]
	_apertar_parry(heroi, m[2])
	heroi.step(0.1)
	heroi.step(0.35)
	assert_true(heroi.state_machine.current_state.name != &"Parry", "a travada terminou o parry")
	m[3].activate()
	assert_near(heroi.stats.current_health, 100.0, 0.001, "o golpe do mesmo frame ainda é aparado")
	assert_near(m[4].current, 50.0, 0.001, "postura do atacante")
	m[3].deactivate()
	heroi.step(PASSO)
	assert_false(heroi.hurtbox.parrying, "no passo seguinte a janela fecha")
	m[0].queue_free()
