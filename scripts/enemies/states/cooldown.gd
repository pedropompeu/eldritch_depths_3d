extends State
## Recarga: 0,6 s parado depois do golpe; então volta a perseguir.

const DURATION := 0.6

var _t := 0.0


func enter() -> void:
	_t = 0.0


func process_physics(delta: float) -> void:
	actor.set_horizontal_velocity(Vector3.ZERO)
	_t += delta
	if _t >= DURATION - actor.TIME_EPS:
		state_machine.change_state(&"chase")
