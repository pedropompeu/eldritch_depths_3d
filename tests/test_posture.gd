extends TestCase
## T16: postura que enche com golpes e parries, quebra no máximo e se recupera.


func _postura() -> Array:
	var p := PostureComponent.new()
	var ev := {broken = 0, recovered = 0}
	p.posture_broken.connect(func(): ev.broken += 1)
	p.posture_recovered.connect(func(): ev.recovered += 1)
	return [p, ev]


func test_quebra_no_maximo() -> void:
	var r := _postura()
	r[0].damage_posture(100)
	assert_eq(r[1].broken, 1)
	assert_true(r[0].is_broken)
	r[0].damage_posture(30)
	assert_eq(r[1].broken, 1, "quebrada não quebra de novo")
	r[0].free()


func test_recupera_apos_3s() -> void:
	var r := _postura()
	r[0].damage_posture(100)
	r[0].step(2.9)
	assert_true(r[0].is_broken, "ainda quebrada aos 2,9 s")
	assert_eq(r[1].recovered, 0)
	r[0].step(0.2)
	assert_eq(r[1].recovered, 1)
	assert_false(r[0].is_broken)
	assert_near(r[0].current, 0.0)
	r[0].free()


func test_recuperacao_gradual() -> void:
	var r := _postura()
	r[0].damage_posture(50)
	r[0].step(1.0)
	assert_near(r[0].current, 36.0)
	r[0].step(10.0)
	assert_near(r[0].current, 0.0, 0.001, "não passa de zero")
	r[0].free()
