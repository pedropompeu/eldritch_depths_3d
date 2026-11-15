extends TestCase
## T21: dano (estado `hurt` com empurrão), morte e frascos.

const CENA := "res://scenes/player/player_3d.tscn"
const CENA_RIG := "res://scenes/camera/camera_rig_3d.tscn"
const PASSO := 1.0 / 60.0


## Devolve [raiz, herói, entrada, golpe]. O atacante fica 2 m à frente (-Z) e
## a hitbox dele, sobre o herói.
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

	var atacante := Node3D.new()
	atacante.position = Vector3(0, 0, -2)
	raiz.add_child(atacante)
	var golpe := Hitbox3D.new()
	golpe.team = 1
	golpe.source = atacante
	var forma_golpe := CollisionShape3D.new()
	var esfera := SphereShape3D.new()
	esfera.radius = 1.0
	forma_golpe.shape = esfera
	golpe.add_child(forma_golpe)
	golpe.position = Vector3(0, 0.9, 0)
	raiz.add_child(golpe)

	var rig: CameraRig3D = load(CENA_RIG).instantiate()
	var heroi: Player3D = load(CENA).instantiate()
	heroi.camera_rig = rig
	var entrada := {move = Vector2.ZERO}
	heroi.input_source = func(): return entrada
	rig.target = heroi
	raiz.add_child(heroi)
	raiz.add_child(rig)
	tree.root.add_child(raiz)
	heroi.set_physics_process(false)
	await tree.physics_frame
	await tree.physics_frame
	return [raiz, heroi, entrada, golpe]


func _passos(heroi: Player3D, segundos: float) -> void:
	for i in roundi(segundos / PASSO):
		heroi.step(PASSO)


func _apertar(heroi: Player3D, entrada: Dictionary, botao: StringName) -> void:
	entrada[botao] = true
	heroi.step(PASSO)
	entrada[botao] = false


func test_dano_entra_em_hurt(tree: SceneTree) -> void:
	var m: Array = await _montar(tree)
	var heroi: Player3D = m[1]
	var antes := heroi.global_position
	m[3].activate()
	assert_eq(heroi.state_machine.current_state.name, &"Hurt")
	assert_near(heroi.stats.current_health, 80.0, 0.001)
	# Entradas são ignoradas no `hurt`.
	m[2].move = Vector2(1, 0)
	_passos(heroi, 0.3)
	var empurrao := heroi.global_position - antes
	assert_near(Vector2(empurrao.x, empurrao.z).length(), 0.5, 0.05, "empurrão de 0,5 m")
	assert_true(empurrao.z > 0.4, "para longe do atacante (-Z): %s" % empurrao)
	m[2].move = Vector2.ZERO
	_passos(heroi, 0.05)
	assert_eq(heroi.state_machine.current_state.name, &"Idle")
	m[0].queue_free()


func test_morte(tree: SceneTree) -> void:
	var m: Array = await _montar(tree)
	var heroi: Player3D = m[1]
	var mortes := {n = 0}
	heroi.hero_died.connect(func(): mortes.n += 1)
	heroi.stats.take_damage(100)
	assert_eq(heroi.state_machine.current_state.name, &"Dead")
	assert_eq(mortes.n, 1)
	_apertar(heroi, m[2], &"attack")
	m[2].move = Vector2(1, 0)
	_passos(heroi, 0.2)
	assert_eq(heroi.state_machine.current_state.name, &"Dead")
	assert_near(Vector2(heroi.velocity.x, heroi.velocity.z).length(), 0.0, 0.001)
	# Golpe depois da morte não ressuscita o `hurt` nem emite outra morte.
	m[3].activate()
	assert_eq(heroi.state_machine.current_state.name, &"Dead")
	assert_eq(mortes.n, 1)
	m[0].queue_free()


func test_frasco_de_sangue(tree: SceneTree) -> void:
	var m: Array = await _montar(tree)
	var heroi: Player3D = m[1]
	heroi.stats.current_health = 50.0
	_apertar(heroi, m[2], &"flask")
	assert_near(heroi.stats.current_health, 90.0, 0.001)
	m[0].queue_free()


func test_laudano(tree: SceneTree) -> void:
	var m: Array = await _montar(tree)
	var heroi: Player3D = m[1]
	heroi.stats.current_sanity = 20.0
	_apertar(heroi, m[2], &"laudanum")
	assert_near(heroi.stats.current_sanity, 70.0, 0.001)
	m[0].queue_free()
