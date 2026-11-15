extends State
## Aviso do golpe: 0,4 s parado, corpo vermelho emissivo. Encara o alvo só ao
## entrar e não gira depois, para a esquiva para o lado funcionar.

const DURATION := 0.4

var _t := 0.0


func enter() -> void:
	_t = 0.0
	actor.face(actor.direction_to_target())
	actor.set_telegraph_glow(true)


func exit() -> void:
	actor.set_telegraph_glow(false)


func process_physics(delta: float) -> void:
	actor.set_horizontal_velocity(Vector3.ZERO)
	_t += delta
	if _t >= DURATION - actor.TIME_EPS:
		state_machine.change_state(&"attack")
