extends TestCase
## T14: linha do tempo de ações que não pula fases numa travada de frame.

const FASES := [
	{name = &"windup", duration = 0.08},
	{name = &"active", duration = 0.18},
	{name = &"recovery", duration = 0.14},
]


func test_fases_em_ordem() -> void:
	var t := ActionTimeline.new(FASES)
	assert_eq(t.advance(0.05), [&"windup"])
	assert_eq(t.advance(0.05), [&"windup", &"active"])
	assert_eq(t.current(), &"active")


func test_delta_grande_nao_pula_active() -> void:
	var t := ActionTimeline.new(FASES)
	var tocadas := t.advance(0.3)
	assert_true(&"active" in tocadas, "active foi pulada: %s" % [tocadas])
	assert_eq(tocadas, [&"windup", &"active", &"recovery"])


func test_termina() -> void:
	var t := ActionTimeline.new(FASES)
	t.advance(0.5)
	assert_true(t.finished())
	assert_eq(t.current(), &"")
	assert_eq(t.advance(0.1), [], "depois de terminar não toca mais nada")


func test_reset() -> void:
	var t := ActionTimeline.new(FASES)
	t.advance(0.5)
	t.reset()
	assert_near(t.elapsed(), 0.0)
	assert_eq(t.current(), &"windup")
	assert_false(t.finished())


func test_is_in_cruza_intervalo() -> void:
	var t := ActionTimeline.new(FASES)
	# active vai de 0,08 a 0,26.
	assert_true(t.is_in(&"active", 0.0, 0.3), "intervalo que cobre a fase inteira")
	assert_true(t.is_in(&"active", 0.2, 0.25))
	assert_false(t.is_in(&"active", 0.0, 0.05))
	assert_false(t.is_in(&"active", 0.27, 0.4))
	assert_false(t.is_in(&"zzz", 0.0, 1.0))
