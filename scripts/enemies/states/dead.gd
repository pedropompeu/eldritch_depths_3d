extends State
## Morto: desliga as colisões, dá XP ao alvo e se apaga 1 s depois.

const FADE_TIME := 1.0

var _t := 0.0


func enter() -> void:
	_t = 0.0
	actor.set_horizontal_velocity(Vector3.ZERO)
	actor.disable_collisions()
	var alvo: StatsComponent = actor.target_stats()
	if alvo:
		alvo.gain_xp(actor.stats.xp_reward)


func process_physics(delta: float) -> void:
	actor.set_horizontal_velocity(Vector3.ZERO)
	_t += delta
	if _t >= FADE_TIME - actor.TIME_EPS and not actor.is_queued_for_deletion():
		actor.queue_free()
