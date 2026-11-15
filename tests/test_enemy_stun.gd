extends TestCase
## T24: postura quebrada atordoa por 1,5 s, golpe no atordoado é crítico (× 2)
## e a morte desliga o inimigo, dá XP ao alvo e o apaga em 1 s.

const CENA := "res://scenes/enemies/enemy_common.tscn"
const PASSO := 1.0 / 60.0


## Devolve [raiz, inimigo, alvo, stats do alvo, golpe do herói]. O alvo fica
## a 10 m (fora da detecção), para o inimigo não sair do lugar; o golpe do
## herói (time 0, dano 20) fica sobre o inimigo, desligado.
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

	var alvo := Node3D.new()
	alvo.position = Vector3(0, 0, -10)
	var stats := StatsComponent.new()
	alvo.add_child(stats)
	raiz.add_child(alvo)

	var golpe := Hitbox3D.new()
	golpe.team = 0
	golpe.damage = 20.0
	var forma_golpe := CollisionShape3D.new()
	var esfera := SphereShape3D.new()
	esfera.radius = 1.0
	forma_golpe.shape = esfera
	golpe.add_child(forma_golpe)
	golpe.position = Vector3(0, 0.8, 0)
	raiz.add_child(golpe)

	var inimigo: EnemyCommon = load(CENA).instantiate()
	inimigo.target = alvo
	raiz.add_child(inimigo)
	tree.root.add_child(raiz)
	inimigo.set_physics_process(false)
	# A postura não deve se recuperar sozinha entre as checagens.
	inimigo.posture.set_process(false)
	await tree.physics_frame
	await tree.physics_frame
	return [raiz, inimigo, alvo, stats, golpe]


func _passos(inimigo: EnemyCommon, segundos: float) -> void:
	for i in roundi(segundos / PASSO):
		inimigo.step(PASSO)


func _estado(inimigo: EnemyCommon) -> StringName:
	return inimigo.state_machine.current_state.name


func _bater(golpe: Hitbox3D) -> void:
	golpe.activate()
	golpe.deactivate()


func test_postura_quebrada_atordoa(tree: SceneTree) -> void:
	var m: Array = await _montar(tree)
	var inimigo: EnemyCommon = m[1]
	inimigo.posture.damage_posture(100)
	assert_eq(_estado(inimigo), &"Stunned")
	_passos(inimigo, 1.4)
	assert_eq(_estado(inimigo), &"Stunned", "ainda atordoado antes de 1,5 s")
	_passos(inimigo, 0.2)
	assert_true(_estado(inimigo) != &"Stunned", "sai do atordoamento depois de 1,5 s")
	assert_false(inimigo.posture.is_broken, "a postura recupera ao sair")
	assert_near(inimigo.posture.current, 0.0, 0.001)
	m[0].queue_free()


func test_golpe_comum_enche_postura(tree: SceneTree) -> void:
	var m: Array = await _montar(tree)
	var inimigo: EnemyCommon = m[1]
	_bater(m[4])
	assert_near(inimigo.stats.current_health, 40.0, 0.001)
	assert_near(inimigo.posture.current, 20.0, 0.001)
	m[0].queue_free()


func test_critico_atordoado(tree: SceneTree) -> void:
	var m: Array = await _montar(tree)
	var inimigo: EnemyCommon = m[1]
	inimigo.posture.damage_posture(100)
	_bater(m[4])
	assert_near(inimigo.stats.current_health, 20.0, 0.001, "20 × 2 no atordoado")
	m[0].queue_free()


func test_morte_da_xp(tree: SceneTree) -> void:
	var m: Array = await _montar(tree)
	var inimigo: EnemyCommon = m[1]
	var mortes := {n = 0}
	inimigo.enemy_died.connect(func(): mortes.n += 1)
	m[4].damage = 60.0
	_bater(m[4])
	assert_eq(_estado(inimigo), &"Dead")
	assert_near(m[3].current_xp, 35.0, 0.001)
	assert_eq(mortes.n, 1)
	await tree.physics_frame
	assert_eq(inimigo.collision_layer, 0, "corpo sem colisão")
	assert_false(inimigo.hurtbox.monitorable, "hurtbox desligada")
	# Golpe depois da morte não conta.
	_bater(m[4])
	assert_eq(mortes.n, 1)
	assert_near(m[3].current_xp, 35.0, 0.001)
	_passos(inimigo, 0.9)
	assert_false(inimigo.is_queued_for_deletion(), "ainda some aos poucos")
	_passos(inimigo, 0.15)
	assert_true(inimigo.is_queued_for_deletion(), "apagado em 1 s")
	m[0].queue_free()
