extends TestCase
## T06: faixas do Véu pela sanidade (provisórias: 60 e 30).


func test_faixas_nos_limites() -> void:
	assert_eq(Veil.band_for(100.0), Veil.Band.CLARO)
	assert_eq(Veil.band_for(60.0), Veil.Band.CLARO)
	assert_eq(Veil.band_for(59.9), Veil.Band.FINO)
	assert_eq(Veil.band_for(30.0), Veil.Band.FINO)
	assert_eq(Veil.band_for(29.9), Veil.Band.RASGADO)
	assert_eq(Veil.band_for(0.0), Veil.Band.RASGADO)


func test_ordem_das_faixas() -> void:
	assert_true(Veil.Band.CLARO < Veil.Band.FINO and Veil.Band.FINO < Veil.Band.RASGADO)
