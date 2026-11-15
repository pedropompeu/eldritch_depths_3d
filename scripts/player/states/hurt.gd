extends State
## Atingido: 0,3 s ignorando a entrada, empurrado 0,5 m para longe de quem
## bateu. Um golpe novo no meio recomeça o estado.

const DURATION := 0.3
const KNOCKBACK := 0.5

var _left := 0.0
var _push := Vector3.ZERO


func enter() -> void:
	_left = DURATION
	_push = actor.last_hit_dir * (KNOCKBACK / DURATION)
	actor.sword.deactivate()


func exit() -> void:
	actor.velocity.x = 0.0
	actor.velocity.z = 0.0


func process_physics(delta: float) -> void:
	actor.velocity.x = _push.x
	actor.velocity.z = _push.z
	_left -= delta
	if _left <= 0.0:
		state_machine.change_state(&"move" if actor.move_dir != Vector3.ZERO else &"idle")
