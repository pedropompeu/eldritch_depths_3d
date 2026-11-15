extends TestCase
## T10: troca automática entre teclado e mouse (KBM) e controle (PAD).
## Cada teste usa a própria instância, não o autoload global.

const IM := preload("res://scripts/core/input_mode.gd")


func _novo() -> Array:
	var im = IM.new()
	var emissoes: Array = []
	im.mode_changed.connect(func(m): emissoes.append(m))
	return [im, emissoes]


func _eixo(valor: float) -> InputEventJoypadMotion:
	var e := InputEventJoypadMotion.new()
	e.axis = JOY_AXIS_LEFT_X
	e.axis_value = valor
	return e


func _botao_pad() -> InputEventJoypadButton:
	var e := InputEventJoypadButton.new()
	e.button_index = JOY_BUTTON_A
	e.pressed = true
	return e


func _mouse(rel: Vector2) -> InputEventMouseMotion:
	var e := InputEventMouseMotion.new()
	e.relative = rel
	return e


func test_comeca_em_kbm() -> void:
	var im = IM.new()
	assert_eq(im.mode, IM.Mode.KBM)
	im.free()


func test_stick_acima_deadzone_vira_pad() -> void:
	var r := _novo()
	r[0].handle_event(_eixo(0.5))
	assert_eq(r[0].mode, IM.Mode.PAD)
	assert_eq(r[1].size(), 1)
	r[0].free()


func test_drift_nao_troca() -> void:
	var r := _novo()
	r[0].handle_event(_eixo(0.15))
	assert_eq(r[0].mode, IM.Mode.KBM)
	assert_eq(r[1].size(), 0)
	r[0].free()


func test_mouse_volta_kbm() -> void:
	var r := _novo()
	r[0].handle_event(_eixo(0.5))
	r[0].handle_event(_mouse(Vector2(4, 0)))
	assert_eq(r[0].mode, IM.Mode.KBM)
	assert_eq(r[1], [IM.Mode.PAD, IM.Mode.KBM])
	r[0].free()


func test_mouse_tremido_nao_troca() -> void:
	var r := _novo()
	r[0].handle_event(_eixo(0.5))
	r[0].handle_event(_mouse(Vector2(1, 0)))
	assert_eq(r[0].mode, IM.Mode.PAD)
	r[0].free()


func test_botao_do_pad_vira_pad() -> void:
	var r := _novo()
	r[0].handle_event(_botao_pad())
	assert_eq(r[0].mode, IM.Mode.PAD)
	r[0].free()


func test_sem_reemissao() -> void:
	var r := _novo()
	r[0].handle_event(_botao_pad())
	r[0].handle_event(_eixo(0.9))
	assert_eq(r[1].size(), 1)
	r[0].free()


func test_desconexao_volta_kbm() -> void:
	var r := _novo()
	# A consulta de controles é injetada: o teste vale com ou sem controle plugado.
	r[0].connected_joypads = func() -> Array: return []
	r[0].handle_event(_botao_pad())
	r[0]._on_joy_connection_changed(0, false)
	assert_eq(r[0].mode, IM.Mode.KBM)
	r[0].free()


func test_desconexao_com_outro_controle_fica_pad() -> void:
	var r := _novo()
	r[0].connected_joypads = func() -> Array: return [1]
	r[0].handle_event(_botao_pad())
	r[0]._on_joy_connection_changed(0, false)
	assert_eq(r[0].mode, IM.Mode.PAD, "ainda há um controle conectado")
	r[0].free()


func test_tecla_e_clique_voltam_kbm() -> void:
	var r := _novo()
	r[0].handle_event(_botao_pad())
	var k := InputEventKey.new()
	k.physical_keycode = KEY_W
	k.pressed = true
	r[0].handle_event(k)
	assert_eq(r[0].mode, IM.Mode.KBM)
	r[0].handle_event(_botao_pad())
	var c := InputEventMouseButton.new()
	c.button_index = MOUSE_BUTTON_LEFT
	c.pressed = true
	r[0].handle_event(c)
	assert_eq(r[0].mode, IM.Mode.KBM)
	r[0].free()
