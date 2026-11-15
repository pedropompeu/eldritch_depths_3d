extends State
## Inimigo parado: espera o alvo entrar na detecção.


func process_physics(_delta: float) -> void:
	actor.set_horizontal_velocity(Vector3.ZERO)
	if actor.can_see_target():
		state_machine.change_state(&"chase")
