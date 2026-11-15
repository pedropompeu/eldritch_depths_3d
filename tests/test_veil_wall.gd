extends TestCase
## T26: parede do Véu — sólida no Véu claro, abre no fino e no rasgado, não
## fecha com alguém dentro e, na cena principal, abre quando a sanidade cai.

const CENA := "res://scenes/world/veil_wall.tscn"
const CENA_MAIN := "res://scenes/main.tscn"


## Devolve [raiz, parede].
func _montar(tree: SceneTree) -> Array:
	var raiz := Node3D.new()
	var parede: VeilWall = load(CENA).instantiate()
	parede.position = Vector3(0, 1.5, 0)
	raiz.add_child(parede)
	tree.root.add_child(raiz)
	await tree.physics_frame
	return [raiz, parede]


func test_solida_no_claro(tree: SceneTree) -> void:
	var m: Array = await _montar(tree)
	var parede: VeilWall = m[1]
	assert_true(parede.is_solid())
	assert_true(parede.is_in_group(&"veil_walls"), "está no grupo veil_walls")
	m[0].queue_free()


func test_abre_no_fino(tree: SceneTree) -> void:
	var m: Array = await _montar(tree)
	var parede: VeilWall = m[1]
	parede.set_band(Veil.Band.FINO)
	assert_false(parede.is_solid())
	m[0].queue_free()


func test_abre_no_rasgado(tree: SceneTree) -> void:
	var m: Array = await _montar(tree)
	var parede: VeilWall = m[1]
	parede.set_band(Veil.Band.RASGADO)
	assert_false(parede.is_solid())
	m[0].queue_free()


func test_nao_fecha_com_corpo_dentro(tree: SceneTree) -> void:
	var m: Array = await _montar(tree)
	var parede: VeilWall = m[1]
	parede.set_band(Veil.Band.FINO)
	var corpo := CharacterBody3D.new()
	corpo.collision_layer = 2
	corpo.collision_mask = 0
	var forma := CollisionShape3D.new()
	var capsula := CapsuleShape3D.new()
	capsula.radius = 0.35
	forma.shape = capsula
	corpo.add_child(forma)
	corpo.position = Vector3(0, 1.5, 0)
	m[0].add_child(corpo)
	await tree.physics_frame
	await tree.physics_frame
	parede.set_band(Veil.Band.CLARO)
	assert_false(parede.is_solid(), "não fecha sobre quem está dentro")
	await tree.physics_frame
	assert_false(parede.is_solid(), "continua aberta enquanto o corpo está dentro")
	m[0].remove_child(corpo)
	corpo.free()
	await tree.physics_frame
	await tree.physics_frame
	assert_true(parede.is_solid(), "fecha quando o corpo sai")
	m[0].queue_free()


func test_main_queda_abre_parede(tree: SceneTree) -> void:
	var main: Node = load(CENA_MAIN).instantiate()
	tree.root.add_child(main)
	await tree.physics_frame
	var paredes := tree.get_nodes_in_group(&"veil_walls")
	assert_eq(paredes.size(), 1, "uma parede do Véu na cena principal")
	var heroi: Player3D = main.get_node("Player3D")
	if paredes.size() == 1:
		var parede: VeilWall = paredes[0]
		var vaga: Marker3D = main.find_child("DoorSlot", true, false)
		assert_true(parede.global_position.distance_to(vaga.global_position) < 0.01, "a parede fica no DoorSlot")
		assert_true(parede.is_solid())
		heroi.stats.drain_sanity(45)
		assert_false(parede.is_solid(), "abre no mesmo frame da queda")
	main.queue_free()
