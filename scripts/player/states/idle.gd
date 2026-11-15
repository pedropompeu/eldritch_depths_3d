extends State
## Herói parado: freia o que sobrou e passa a `move` assim que há entrada.


func process_physics(delta: float) -> void:
	if actor.input.roll and actor.try_roll():
		return
	if actor.input.attack and actor.try_attack():
		return
	actor.walk(delta)
	if actor.move_dir != Vector3.ZERO:
		state_machine.change_state(&"move")
