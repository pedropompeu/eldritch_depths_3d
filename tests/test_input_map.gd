extends TestCase
## Mapa de controles: toda ação existe e as de jogo funcionam no teclado/mouse e no controle.

const TODAS := [
	&"move_up", &"move_down", &"move_left", &"move_right",
	&"aim_up", &"aim_down", &"aim_left", &"aim_right",
	&"attack", &"roll", &"parry", &"spell_cosmic",
	&"use_blood_flask", &"use_laudanum", &"interact",
	&"debug_sanity_drop", &"debug_camera_preset",
]

const DE_JOGO := [
	&"move_up", &"move_down", &"move_left", &"move_right",
	&"attack", &"roll", &"parry", &"spell_cosmic",
	&"use_blood_flask", &"use_laudanum", &"interact",
]


func test_todas_as_acoes_existem():
	for nome in TODAS:
		assert_true(InputMap.has_action(nome), nome)


func test_acoes_de_jogo_tem_teclado_e_pad():
	for nome in DE_JOGO:
		if not InputMap.has_action(nome):
			assert_true(false, "%s não existe" % nome)
			continue
		var tem_kbm := false
		var tem_pad := false
		for ev in InputMap.action_get_events(nome):
			if ev is InputEventKey or ev is InputEventMouseButton:
				tem_kbm = true
			elif ev is InputEventJoypadButton or ev is InputEventJoypadMotion:
				tem_pad = true
		assert_true(tem_kbm, "%s sem teclado/mouse" % nome)
		assert_true(tem_pad, "%s sem controle" % nome)


func test_deadzone():
	if not InputMap.has_action(&"move_up"):
		assert_true(false, "move_up não existe")
		return
	assert_near(InputMap.action_get_deadzone(&"move_up"), 0.2)
