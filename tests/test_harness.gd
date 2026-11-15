extends TestCase
## Testes do próprio runner: garantem que os asserts registram e toleram o que devem.


func test_assert_near_tolera_epsilon():
	assert_near(1.0, 1.0005)
	assert_eq(failures.size(), 0, "assert_near deveria tolerar diferença menor que o epsilon")


func test_assert_eq_registra_falha():
	var t := TestCase.new()
	t.assert_eq(1, 2)
	assert_eq(t.failures.size(), 1)
