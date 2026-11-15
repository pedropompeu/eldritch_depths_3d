extends TestCase
## T27: vinheta da sanidade — curva da intensidade, nó na cena principal ligado
## à sanidade do herói, tecla de depuração (F9) e argumento `--sanity=`.

const CENA_MAIN := "res://scenes/main.tscn"
const MainScript := preload("res://scripts/main.gd")


## Devolve [main, herói, vinheta]. O dreno ambiente fica parado e a sanidade
## volta a 100 (o primeiro frame já drenou um pouco).
func _montar(tree: SceneTree) -> Array:
	var main: Node = load(CENA_MAIN).instantiate()
	tree.root.add_child(main)
	await tree.physics_frame
	var heroi: Player3D = main.get_node("Player3D")
	heroi.stats.set_process(false)
	heroi.stats.current_sanity = heroi.stats.max_sanity
	return [main, heroi, main.find_child("Vignette", true, false)]


func test_intensidade() -> void:
	assert_near(MainScript.vignette_intensity(100.0), 0.0, 0.0001)
	assert_near(MainScript.vignette_intensity(60.0), 0.0, 0.0001)
	assert_near(MainScript.vignette_intensity(30.0), 0.5, 0.0001)
	assert_near(MainScript.vignette_intensity(0.0), 1.0, 0.0001)


func test_vinheta_existe(tree: SceneTree) -> void:
	var m: Array = await _montar(tree)
	var vinheta := m[2] as ColorRect
	assert_true(vinheta != null, "Vignette é um ColorRect")
	if vinheta:
		assert_eq(vinheta.mouse_filter, Control.MOUSE_FILTER_IGNORE)
		assert_true(vinheta.get_parent() is CanvasLayer, "fica num CanvasLayer")
		assert_near(vinheta.anchor_right, 1.0, 0.0001, "tela cheia")
		assert_near(vinheta.anchor_bottom, 1.0, 0.0001, "tela cheia")
		var material := vinheta.material as ShaderMaterial
		assert_true(material != null and material.shader != null, "shader carregado")
		if material and material.shader:
			assert_true(material.shader.code.contains("uniform float intensity"), "uniform intensity")
			assert_near(material.get_shader_parameter(&"intensity"), 0.0, 0.0001, "sanidade cheia: sem vinheta")
	m[0].queue_free()


func test_sanidade_atualiza_vinheta(tree: SceneTree) -> void:
	var m: Array = await _montar(tree)
	m[1].stats.drain_sanity(70)
	var material := (m[2] as ColorRect).material as ShaderMaterial
	assert_near(material.get_shader_parameter(&"intensity"), 0.5, 0.0001)
	m[0].queue_free()


func test_f9_derruba_sanidade(tree: SceneTree) -> void:
	var m: Array = await _montar(tree)
	var tecla := InputEventAction.new()
	tecla.action = &"debug_sanity_drop"
	tecla.pressed = true
	m[0]._unhandled_input(tecla)
	assert_near(m[1].stats.current_sanity, 80.0, 0.001, "F9 tira 20 de sanidade na build de depuração")
	m[0].queue_free()


func test_argumento_sanidade() -> void:
	assert_near(MainScript.sanity_from_args(PackedStringArray(["--sanity=20"])), 20.0, 0.0001)
	assert_near(MainScript.sanity_from_args(PackedStringArray(["--outra", "--sanity=55.5"])), 55.5, 0.0001)
	assert_eq(MainScript.sanity_from_args(PackedStringArray()), -1.0, "sem argumento: -1")
	assert_eq(MainScript.sanity_from_args(PackedStringArray(["--sanity=abc"])), -1.0, "valor inválido: -1")
