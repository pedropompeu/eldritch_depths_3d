extends TestCase
## T23: ciclo do inimigo no alcance — aviso (0,4 s), golpe (0,25 s) e recarga
## (0,6 s). O alvo é um `Node3D` com hurtbox do herói e `StatsComponent`,
## ligado como no `Player3D._on_hurt`.

const CENA := "res://scenes/enemies/enemy_common.tscn"
const PASSO := 1.0 / 60.0


## Devolve [raiz, inimigo, alvo, stats do alvo]. Alvo 1 m à frente (-Z).
func _montar(tree: SceneTree, cosmico := true) -> Array:
	var raiz := Node3D.new()
	var piso := StaticBody3D.new()
	var forma := CollisionShape3D.new()
	var caixa := BoxShape3D.new()
	caixa.size = Vector3(40, 1, 40)
	forma.shape = caixa
	forma.position = Vector3(0, -0.5, 0)
	piso.add_child(forma)
	raiz.add_child(piso)

	var alvo := Node3D.new()
	alvo.position = Vector3(0, 0, -1)
	var stats := StatsComponent.new()
	alvo.add_child(stats)
	var hurtbox := Hurtbox3D.new()
	hurtbox.team = 0
	var forma_alvo := CollisionShape3D.new()
	var capsula := CapsuleShape3D.new()
	capsula.radius = 0.4
	capsula.height = 1.8
	forma_alvo.shape = capsula
	forma_alvo.position = Vector3(0, 0.9, 0)
	hurtbox.add_child(forma_alvo)
	alvo.add_child(hurtbox)
	hurtbox.hurt.connect(func(h: Hitbox3D):
		stats.take_damage(h.damage)
		stats.drain_sanity(h.sanity_damage))
	raiz.add_child(alvo)

	var inimigo: EnemyCommon = load(CENA).instantiate()
	inimigo.target = alvo
	inimigo.is_cosmic = cosmico
	raiz.add_child(inimigo)
	tree.root.add_child(raiz)
	inimigo.set_physics_process(false)
	await tree.physics_frame
	await tree.physics_frame
	return [raiz, inimigo, alvo, stats]


func _passos(inimigo: EnemyCommon, segundos: float) -> void:
	for i in roundi(segundos / PASSO):
		inimigo.step(PASSO)


## Dois passos: `idle` vê o alvo e vai a `chase`; `chase`, no alcance, vai a
## `telegraph`.
func _ate_avisar(inimigo: EnemyCommon) -> void:
	inimigo.step(PASSO)
	inimigo.step(PASSO)


func _estado(inimigo: EnemyCommon) -> StringName:
	return inimigo.state_machine.current_state.name


func test_telegrafa_antes_de_bater(tree: SceneTree) -> void:
	var m: Array = await _montar(tree)
	var inimigo: EnemyCommon = m[1]
	_ate_avisar(inimigo)
	assert_eq(_estado(inimigo), &"Telegraph")
	_passos(inimigo, 0.39)
	assert_near(m[3].current_health, 100.0, 0.001, "nenhum dano durante o aviso")
	_passos(inimigo, 0.31)
	assert_near(m[3].current_health, 85.0, 0.001, "um golpe de 15 até 0,7 s")
	m[0].queue_free()


func test_aviso_brilha_vermelho(tree: SceneTree) -> void:
	var m: Array = await _montar(tree)
	var inimigo: EnemyCommon = m[1]
	var mat: StandardMaterial3D = inimigo.body.mesh.material
	assert_false(mat.emission_enabled)
	_ate_avisar(inimigo)
	assert_true(mat.emission_enabled, "vermelho emissivo no aviso")
	assert_eq(mat.emission, Color("#ff2020"))
	assert_near(mat.emission_energy_multiplier, 2.0, 0.001)
	_passos(inimigo, 0.45)
	assert_eq(_estado(inimigo), &"Attack")
	assert_false(mat.emission_enabled, "volta ao normal ao sair do aviso")
	m[0].queue_free()


func test_nao_gira_depois_do_aviso(tree: SceneTree) -> void:
	var m: Array = await _montar(tree)
	var inimigo: EnemyCommon = m[1]
	_ate_avisar(inimigo)
	var frente := -inimigo.global_transform.basis.z
	# O alvo esquiva para o lado; o inimigo não acompanha.
	m[2].position = Vector3(1.0, 0, -0.5)
	_passos(inimigo, 0.3)
	assert_true((-inimigo.global_transform.basis.z).is_equal_approx(frente), "mesma direção do início do aviso")
	m[0].queue_free()


func test_golpe_cosmico_tira_sanidade(tree: SceneTree) -> void:
	var m: Array = await _montar(tree)
	var inimigo: EnemyCommon = m[1]
	_passos(inimigo, 0.7)
	assert_near(m[3].current_health, 85.0, 0.001)
	assert_near(m[3].current_sanity, 85.0, 0.001)
	m[0].queue_free()


func test_nao_cosmico_nao_tira(tree: SceneTree) -> void:
	var m: Array = await _montar(tree, false)
	var inimigo: EnemyCommon = m[1]
	_passos(inimigo, 0.7)
	assert_near(m[3].current_health, 85.0, 0.001)
	assert_near(m[3].current_sanity, 100.0, 0.001)
	m[0].queue_free()


func test_recarga(tree: SceneTree) -> void:
	var m: Array = await _montar(tree)
	var inimigo: EnemyCommon = m[1]
	# Aviso (0,4 s) + golpe (0,25 s): começa a recarga.
	_passos(inimigo, 0.7)
	assert_eq(_estado(inimigo), &"Cooldown")
	assert_false(inimigo.claw.active, "a garra desliga ao fim do golpe")
	assert_near(m[3].current_health, 85.0, 0.001)
	_passos(inimigo, 0.5)
	assert_near(m[3].current_health, 85.0, 0.001, "nenhum dano novo na recarga")
	# Fim da recarga: volta a `chase` e, no alcance, avisa de novo.
	_passos(inimigo, 0.2)
	assert_eq(_estado(inimigo), &"Telegraph")
	m[0].queue_free()
