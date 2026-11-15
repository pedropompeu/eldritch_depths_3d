extends State
## Golpe: a garra fica ativa por 0,25 s. Inimigo cósmico também tira 15 de
## sanidade.

const DURATION := 0.25
const COSMIC_SANITY_DAMAGE := 15.0

var _t := 0.0


func enter() -> void:
	_t = 0.0
	actor.claw.sanity_damage = COSMIC_SANITY_DAMAGE if actor.is_cosmic else 0.0
	actor.claw.activate()


func exit() -> void:
	actor.claw.deactivate()


func process_physics(delta: float) -> void:
	actor.set_horizontal_velocity(Vector3.ZERO)
	_t += delta
	if _t >= DURATION - actor.TIME_EPS:
		state_machine.change_state(&"cooldown")
