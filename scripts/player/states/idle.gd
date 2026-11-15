extends State
## Herói parado: freia o que sobrou e passa a `move` assim que há entrada.


func process_physics(delta: float) -> void:
	actor.walk(delta)
	if actor.move_dir != Vector3.ZERO:
		state_machine.change_state(&"move")
