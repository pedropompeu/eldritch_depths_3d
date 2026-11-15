extends State
## Perseguição em linha reta (sem navegação neste bloco). No alcance de ataque,
## para e continua aqui; a T23 passa a ir para `telegraph`.


func process_physics(_delta: float) -> void:
	if not actor.can_see_target():
		state_machine.change_state(&"idle")
		return
	var dir: Vector3 = actor.direction_to_target()
	actor.face(dir)
	if actor.distance_to_target() <= actor.attack_range:
		actor.set_horizontal_velocity(Vector3.ZERO)
		return
	actor.set_horizontal_velocity(dir * actor.move_speed)
