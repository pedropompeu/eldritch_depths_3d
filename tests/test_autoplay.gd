extends TestCase
## T30: modo automático — a entrada gerada varia no tempo e, na cena
## principal, assume o herói e faz o inimigo reaparecer depois de morrer.

const AutoplayInput := preload("res://scripts/autoplay_input.gd")
const MainScript := preload("res://scripts/main.gd")
const CENA_MAIN := "res://scenes/main.tscn"


## Entrada do `Callable` como se ele tivesse começado `segundos` atrás.
func _amostra(segundos: float) -> Dictionary:
	var agora := Time.get_ticks_msec()
	return AutoplayInput.make(agora - roundi(segundos * 1000.0)).call()


func test_autoplay_varia() -> void:
	var direcoes: Array[Vector2] = []
	var atacou := false
	for t in [0.0, 1.0, 2.0, 3.0]:
		var e := _amostra(t)
		direcoes.append(e.move)
		atacou = atacou or e.attack
	for i in direcoes.size():
		for j in range(i + 1, direcoes.size()):
			assert_true(direcoes[i].distance_to(direcoes[j]) > 0.1, "direções %d e %d iguais: %s" % [i, j, direcoes])
	assert_true(atacou, "attack pulsa em pelo menos uma amostra")


func test_esquiva_pulsa() -> void:
	var esquivou := false
	for i in 60:
		esquivou = esquivou or _amostra(i * 0.05).roll
	assert_true(esquivou, "roll pulsa nos 3 primeiros segundos")


func test_argumento_autoplay() -> void:
	assert_true(MainScript.has_autoplay_arg(PackedStringArray(["--autoplay"])))
	assert_false(MainScript.has_autoplay_arg(PackedStringArray(["--sanity=20"])))


func test_main_autoplay_reaparece_inimigo(tree: SceneTree) -> void:
	var main: Node = load(CENA_MAIN).instantiate()
	tree.root.add_child(main)
	await tree.physics_frame
	var heroi: Player3D = main.get_node("Player3D")
	var padrao := heroi.input_source
	main.enable_autoplay()
	assert_true(heroi.input_source != padrao, "o autoplay assume a entrada do herói")
	var inimigo: EnemyCommon = main.get_node("EnemyCommon")
	var lugar := inimigo.global_transform
	var id_antigo := inimigo.get_instance_id()
	inimigo.stats.take_damage(1000)
	await tree.create_timer(MainScript.ENEMY_RESPAWN_DELAY + 0.3).timeout
	var novos: Array = main.get_children().filter(func(n): return n is EnemyCommon and n.get_instance_id() != id_antigo and not n.is_queued_for_deletion())
	assert_eq(novos.size(), 1, "um inimigo novo depois de %s s" % MainScript.ENEMY_RESPAWN_DELAY)
	if novos.size() == 1:
		assert_true(novos[0].target == heroi, "o novo inimigo persegue o herói")
		assert_true(novos[0].global_transform.origin.distance_to(lugar.origin) < 0.01, "reaparece no lugar de origem")
	main.queue_free()
