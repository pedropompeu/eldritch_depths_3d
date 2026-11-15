extends TestCase
## T29: HUD mínimo — canto superior esquerdo, pequeno em qualquer tela, barras
## que seguem os valores e contadores de frasco com o rótulo do dispositivo.

const CENA := "res://scenes/ui/hud_minimal.tscn"
const InputModeScript := preload("res://scripts/core/input_mode.gd")


## Devolve [viewport, hud, stats].
func _montar(tree: SceneTree, tamanho := Vector2i(1920, 1080)) -> Array:
	var vp := SubViewport.new()
	vp.size = tamanho
	var stats := StatsComponent.new()
	vp.add_child(stats)
	stats.set_process(false)
	var hud: HudMinimal = load(CENA).instantiate()
	vp.add_child(hud)
	tree.root.add_child(vp)
	hud.bind(stats)
	await tree.process_frame
	return [vp, hud, stats]


func test_area_menor_que_6_por_cento(tree: SceneTree) -> void:
	for tamanho in [Vector2i(1920, 1080), Vector2i(2560, 1080), Vector2i(1280, 800)]:
		var m: Array = await _montar(tree, tamanho)
		var r: Rect2 = m[1].hud_rect()
		var tela := Rect2(Vector2.ZERO, Vector2(tamanho))
		assert_true(r.get_area() > 0.0, "%s: HUD tem área" % tamanho)
		assert_true(r.get_area() < 0.06 * tela.get_area(), "%s: área %.0f px² passa de 6%%" % [tamanho, r.get_area()])
		assert_true(tela.encloses(r), "%s: HUD dentro da tela (%s)" % [tamanho, r])
		assert_true(r.end.x < tela.size.x * 0.5 and r.end.y < tela.size.y * 0.5, "%s: só no canto superior esquerdo (%s)" % [tamanho, r])
		m[0].queue_free()


func test_barra_segue_vida(tree: SceneTree) -> void:
	var m: Array = await _montar(tree)
	m[2].take_damage(50)
	var fundo: Control = m[1].get_node("Health")
	var cheio: Control = m[1].get_node("Health/Fill")
	assert_near(cheio.size.x, fundo.size.x * 0.5, 1.0)
	assert_near(fundo.size.x, 240.0, 1.0, "2,4 px por ponto de vida em 1080p")
	assert_near(fundo.size.y, 6.0, 0.01, "6 px de altura em 1080p")
	m[0].queue_free()


func test_prompt_troca_com_modo(tree: SceneTree) -> void:
	var m: Array = await _montar(tree)
	var rotulo: Label = m[1].get_node("BloodLabel")
	Autoloads.get_autoload(&"InputMode").mode_changed.emit(InputModeScript.Mode.PAD)
	assert_true(rotulo.text.begins_with("↓"), "rótulo no controle: %s" % rotulo.text)
	Autoloads.get_autoload(&"InputMode").mode_changed.emit(InputModeScript.Mode.KBM)
	assert_true(rotulo.text.begins_with("1"), "rótulo no teclado: %s" % rotulo.text)
	m[0].queue_free()


func test_contador_frasco(tree: SceneTree) -> void:
	var m: Array = await _montar(tree)
	var rotulo: Label = m[1].get_node("BloodLabel")
	assert_true(rotulo.text.ends_with("×3"), "começa com 3: %s" % rotulo.text)
	m[2].take_damage(50)
	m[2].use_blood_flask()
	assert_true(rotulo.text.ends_with("×2"), "contador: %s" % rotulo.text)
	m[0].queue_free()
