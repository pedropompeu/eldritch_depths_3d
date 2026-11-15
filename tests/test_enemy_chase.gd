extends TestCase
## T22: inimigo comum parado fora da detecção, perseguindo dentro dela e
## parando no alcance de ataque.

const CENA := "res://scenes/enemies/enemy_common.tscn"
const PASSO := 1.0 / 60.0


## Devolve [raiz, inimigo, alvo]. O inimigo nasce na origem; o alvo, `dist`
## metros à frente (-Z).
func _montar(tree: SceneTree, dist: float) -> Array:
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
	alvo.position = Vector3(0, 0, -dist)
	raiz.add_child(alvo)
	var inimigo: EnemyCommon = load(CENA).instantiate()
	inimigo.target = alvo
	raiz.add_child(inimigo)
	tree.root.add_child(raiz)
	inimigo.set_physics_process(false)
	await tree.physics_frame
	await tree.physics_frame
	return [raiz, inimigo, alvo]


func _passos(inimigo: EnemyCommon, n: int) -> void:
	for i in n:
		inimigo.step(PASSO)


func _horizontal(v: Vector3) -> float:
	return Vector2(v.x, v.z).length()


func test_parado_fora_da_deteccao(tree: SceneTree) -> void:
	var m: Array = await _montar(tree, 8.0)
	var inimigo: EnemyCommon = m[1]
	_passos(inimigo, 60)
	assert_eq(inimigo.state_machine.current_state.name, &"Idle")
	assert_near(_horizontal(inimigo.velocity), 0.0, 0.001)
	m[0].queue_free()


func test_persegue_dentro_da_deteccao(tree: SceneTree) -> void:
	var m: Array = await _montar(tree, 5.0)
	var inimigo: EnemyCommon = m[1]
	var antes := inimigo.global_position
	_passos(inimigo, 10)
	assert_eq(inimigo.state_machine.current_state.name, &"Chase")
	assert_near(_horizontal(inimigo.velocity), 2.4, 0.01)
	assert_true(inimigo.global_position.z < antes.z - 0.2, "anda rumo ao alvo (-Z)")
	m[0].queue_free()


func test_para_no_alcance(tree: SceneTree) -> void:
	var m: Array = await _montar(tree, 1.2)
	var inimigo: EnemyCommon = m[1]
	_passos(inimigo, 10)
	# Desde a T23, parar no alcance já começa o aviso do golpe.
	assert_eq(inimigo.state_machine.current_state.name, &"Telegraph")
	assert_near(_horizontal(inimigo.velocity), 0.0, 0.001)
	m[0].queue_free()


func test_sem_alvo_fica_parado(tree: SceneTree) -> void:
	var m: Array = await _montar(tree, 3.0)
	var inimigo: EnemyCommon = m[1]
	inimigo.target = null
	_passos(inimigo, 10)
	assert_eq(inimigo.state_machine.current_state.name, &"Idle")
	m[0].queue_free()


func test_material_proprio_por_inimigo(tree: SceneTree) -> void:
	var raiz := Node3D.new()
	var a: EnemyCommon = load(CENA).instantiate()
	var b: EnemyCommon = load(CENA).instantiate()
	raiz.add_child(a)
	raiz.add_child(b)
	tree.root.add_child(raiz)
	var mat_a: Material = a.body.mesh.material
	var mat_b: Material = b.body.mesh.material
	assert_true(mat_a != null and mat_b != null, "o corpo tem material")
	assert_true(mat_a != mat_b, "trocar a cor de um não pinta o outro")
	raiz.queue_free()
