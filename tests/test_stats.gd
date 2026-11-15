extends TestCase
## T07: StatsComponent portado do 2D, com dreno ambiente e sinal de faixa do Véu.


func _stats() -> StatsComponent:
	var s := StatsComponent.new()
	s._ready()
	return s


func test_dreno_ambiente() -> void:
	var s := _stats()
	s.ambient_sanity_drain = 0.8
	for i in 10:
		s._process(1.0)
	assert_near(s.current_sanity, 92.0)
	s.free()


func test_sinal_de_faixa_so_na_troca() -> void:
	var s := _stats()
	var faixas: Array = []
	s.veil_band_changed.connect(func(b): faixas.append(b))
	s.drain_sanity(39)
	assert_eq(faixas.size(), 0, "61 ainda é CLARO")
	s.drain_sanity(2)
	assert_eq(faixas.size(), 1, "59 entra em FINO")
	if faixas.size() == 1:
		assert_eq(faixas[0], Veil.Band.FINO)
	s.drain_sanity(1)
	assert_eq(faixas.size(), 1, "58 continua em FINO")
	s.free()


func test_laudano_restaura_metade() -> void:
	var s := _stats()
	s.drain_sanity(80)
	assert_true(s.use_laudanum_flask())
	assert_near(s.current_sanity, 70.0)
	assert_eq(s.current_laudanum_flasks, 1)
	s.free()


func test_laudano_reabre_faixa() -> void:
	var s := _stats()
	s.drain_sanity(50)
	var faixas: Array = []
	s.veil_band_changed.connect(func(b): faixas.append(b))
	s.use_laudanum_flask()
	assert_eq(faixas, [Veil.Band.CLARO])
	assert_eq(s.get_veil_band(), Veil.Band.CLARO)
	s.free()


func test_vigor_exausto_nao_regenera() -> void:
	var s := _stats()
	s.consume_stamina(100)
	s._process(0.9)
	assert_near(s.current_stamina, 0.0, 0.001, "exausto não regenera")
	s._process(0.7)
	assert_true(s.current_stamina > 0.0, "depois da exaustão regenera")
	s.free()


func test_sem_perks_manager_nao_quebra() -> void:
	# Sem PerksManager, regenera a 25/s. Como no 2D, o frame que encerra o
	# atraso de 0,5 s já regenera com o delta inteiro: 50 + 25*0,6 + 25*1,0.
	var s := _stats()
	s.consume_stamina(50)
	s._process(0.6)
	s._process(1.0)
	assert_near(s.current_stamina, 90.0)
	s.free()


func test_nivel() -> void:
	var s := _stats()
	s.gain_xp(80)
	assert_eq(s.level, 2)
	assert_near(s.max_health, 115.0)
	assert_near(s.max_stamina, 110.0)
	assert_near(s.xp_to_next, 116.0)
	s.free()
