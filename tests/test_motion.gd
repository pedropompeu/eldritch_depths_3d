extends TestCase
## T09: direção relativa à câmera e aceleração do herói.


func test_frente_com_yaw_zero() -> void:
	assert_vec_near(PlayerMotion.input_to_world(Vector2(0, -1), 0.0), Vector3(0, 0, -1))


func test_yaw_45() -> void:
	assert_vec_near(
		PlayerMotion.input_to_world(Vector2(0, -1), deg_to_rad(45)),
		Vector3(-0.7071, 0, -0.7071)
	)


func test_diagonal_normalizada() -> void:
	assert_near(PlayerMotion.input_to_world(Vector2(1, 1), 0.0).length(), 1.0)


func test_acelera_ate_velocidade() -> void:
	var v := Vector3.ZERO
	var max_x := 0.0
	for i in 30:
		v = PlayerMotion.compute_velocity(v, Vector3(1, 0, 0), 5.0, 40.0, 1.0 / 60)
		max_x = maxf(max_x, v.x)
	assert_near(v.x, 5.0)
	assert_true(max_x <= 5.0 + 0.0001, "a velocidade passou de 5,0: %s" % max_x)


func test_desacelera_ao_soltar() -> void:
	var v := Vector3(5, 0, 0)
	var frames := 0
	while v.length() > 0.0001 and frames < 100:
		v = PlayerMotion.compute_velocity(v, Vector3.ZERO, 5.0, PlayerMotion.DECEL, 1.0 / 60)
		frames += 1
	assert_true(frames <= 6, "levou %d frames para parar" % frames)
	assert_vec_near(v, Vector3.ZERO)
