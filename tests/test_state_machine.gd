extends TestCase
## T08: máquina de estados com ator genérico (Node), usada por herói e inimigo.


class EstadoContador extends State:
	var enters := 0
	var exits := 0

	func enter() -> void:
		enters += 1

	func exit() -> void:
		exits += 1


func _maquina() -> StateMachine:
	var sm := StateMachine.new()
	for nome in ["A", "B"]:
		var s := EstadoContador.new()
		s.name = nome
		sm.add_child(s)
	return sm


func test_init_com_node3d() -> void:
	var sm := _maquina()
	var ator := Node3D.new()
	sm.init(ator)
	var a: EstadoContador = sm.get_node("A")
	var b: EstadoContador = sm.get_node("B")
	assert_true(sm.current_state == a, "deveria entrar no primeiro estado filho")
	assert_eq(a.enters, 1)
	assert_true(a.actor == ator, "o estado deveria receber o ator")
	assert_true(a.state_machine == sm)
	sm.change_state(&"b")
	assert_eq(a.exits, 1)
	assert_eq(b.enters, 1)
	assert_true(sm.current_state == b)
	sm.free()
	ator.free()


func test_chave_inexistente_nao_troca() -> void:
	var sm := _maquina()
	var ator := Node3D.new()
	sm.init(ator)
	var a: EstadoContador = sm.get_node("A")
	sm.change_state(&"zzz")
	assert_true(sm.current_state == a, "chave inexistente não deveria trocar o estado")
	assert_eq(a.exits, 0)
	sm.free()
	ator.free()
