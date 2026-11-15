extends State
## Herói andando: acelera rumo à entrada e gira o corpo para onde anda. Sem
## entrada, freia aqui e só volta a `idle` quando a velocidade zera.


func process_physics(delta: float) -> void:
	if actor.input.roll and actor.try_roll():
		return
	if actor.input.parry and actor.try_parry():
		return
	if actor.input.attack and actor.try_attack():
		return
	actor.walk(delta)
	if actor.move_dir != Vector3.ZERO:
		actor.face(actor.move_dir)
	elif actor.horizontal_speed() < actor.STOP_EPS:
		state_machine.change_state(&"idle")
