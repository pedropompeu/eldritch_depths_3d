extends TestCase
## T11: mira com quedas seguras (mouse fora do chão, drift, herói parado).

const O := Vector3.ZERO


func test_raio_acerta_chao() -> void:
	var p = AimResolver.ground_point(Vector3(0, 10, 0), Vector3(0, -1, 1).normalized(), 0.0)
	assert_true(p is Vector3, "deveria acertar o chão")
	if p is Vector3:
		assert_vec_near(p, Vector3(0, 0, 10))


func test_raio_acima_do_horizonte_e_null() -> void:
	assert_true(AimResolver.ground_point(Vector3(0, 10, 0), Vector3(0, 0.2, 1), 0.0) == null)


func test_raio_paralelo_e_null() -> void:
	assert_true(AimResolver.ground_point(Vector3(0, 10, 0), Vector3(0, 0, 1), 0.0) == null)


func test_kbm_mira_no_mouse() -> void:
	assert_vec_near(AimResolver.resolve(false, O, Vector3(3, 0, 0), Vector3.ZERO, Vector3.ZERO, Vector3.ZERO), Vector3(1, 0, 0))


func test_kbm_sem_chao_cai_no_movimento() -> void:
	assert_vec_near(AimResolver.resolve(false, O, null, Vector3.ZERO, Vector3(1, 0, 0), Vector3.ZERO), Vector3(1, 0, 0))


func test_parado_sem_chao_mantem_ultima() -> void:
	assert_vec_near(AimResolver.resolve(false, O, null, Vector3.ZERO, Vector3.ZERO, Vector3(0, 0, 1)), Vector3(0, 0, 1))


func test_pad_stick_ganha_do_movimento() -> void:
	assert_vec_near(AimResolver.resolve(true, O, null, Vector3(0, 0, -1), Vector3(1, 0, 0), Vector3.ZERO), Vector3(0, 0, -1))


func test_pad_drift_usa_movimento() -> void:
	assert_vec_near(AimResolver.resolve(true, O, null, Vector3(0.1, 0, 0), Vector3(0, 0, 1), Vector3.ZERO), Vector3(0, 0, 1))


func test_nunca_zero() -> void:
	for pad in [false, true]:
		var a := AimResolver.resolve(pad, O, null, Vector3.ZERO, Vector3.ZERO, Vector3.ZERO)
		assert_near(a.length(), 1.0)
		assert_false(is_nan(a.x) or is_nan(a.y) or is_nan(a.z), "mira com NaN")


func test_mouse_em_cima_do_heroi_cai_no_movimento() -> void:
	var a := AimResolver.resolve(false, Vector3(2, 0, 2), Vector3(2.05, 0, 2), Vector3.ZERO, Vector3(0, 0, -1), Vector3.ZERO)
	assert_vec_near(a, Vector3(0, 0, -1))


func test_resultado_fica_no_plano() -> void:
	# Herói acima do plano do mouse (degrau): a mira ignora a diferença de altura.
	var a := AimResolver.resolve(false, Vector3(0, 1, 0), Vector3(3, 0, 0), Vector3.ZERO, Vector3.ZERO, Vector3.ZERO)
	assert_vec_near(a, Vector3(1, 0, 0))


func test_mouse_nan_cai_no_movimento() -> void:
	var nan_v := Vector3(NAN, 0, NAN)
	var a := AimResolver.resolve(false, O, nan_v, Vector3.ZERO, Vector3(1, 0, 0), Vector3.ZERO)
	assert_vec_near(a, Vector3(1, 0, 0))
