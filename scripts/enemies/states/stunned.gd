extends State
## Atordoado (postura quebrada): 1,5 s parado, recebendo dano em dobro. Esse
## tempo é o do inimigo no 2D e manda sobre os 3,0 s da postura: ao sair, pede
## a recuperação dela.

const DURATION := 1.5

var _t := 0.0


func enter() -> void:
	_t = 0.0
	actor.set_horizontal_velocity(Vector3.ZERO)


func exit() -> void:
	actor.posture.recover()


func process_physics(delta: float) -> void:
	actor.set_horizontal_velocity(Vector3.ZERO)
	_t += delta
	if _t >= DURATION - actor.TIME_EPS:
		state_machine.change_state(&"chase")
