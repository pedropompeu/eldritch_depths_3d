extends State
## Esquiva: 0,34 s a 10,4 m/s na direção do movimento (parado, na da mira).
## Invencível de 0,04 a 0,26 s. Nada a interrompe; no fim volta ao chão.
##
## A invencibilidade usa o intervalo do frame inteiro (`is_in`) e é marcada no
## começo do passo, antes de o frame processar golpes: uma travada que pula
## por cima da janela ainda conta como dentro dela.

const COST := 20.0
const SPEED := 10.4
const STARTUP := 0.04
const INVULN := 0.22
const TAIL := 0.08

var _timeline := ActionTimeline.new([
	{name = &"startup", duration = STARTUP},
	{name = &"invuln", duration = INVULN},
	{name = &"tail", duration = TAIL},
])
var _dir := Vector3.FORWARD


## Chamado pelos estados de chão. Gasta o vigor e entra na esquiva; sem vigor,
## devolve falso e nada muda.
func try_begin() -> bool:
	if not actor.stats.consume_stamina(COST):
		return false
	state_machine.change_state(&"roll")
	return true


func enter() -> void:
	_timeline.reset()
	var base: Vector3 = actor.move_dir if actor.move_dir != Vector3.ZERO else actor.aim_dir
	_dir = Vector3(base.x, 0.0, base.z).normalized()
	if _dir == Vector3.ZERO:
		_dir = Vector3.FORWARD
	actor.face(_dir)
	_aplicar_velocidade()


func exit() -> void:
	actor.hurtbox.invulnerable = false


func process_physics(delta: float) -> void:
	var de := _timeline.elapsed()
	actor.hurtbox.invulnerable = _timeline.is_in(&"invuln", de, de + delta)
	_timeline.advance(delta)
	_aplicar_velocidade()
	if _timeline.finished():
		state_machine.change_state(&"move" if actor.move_dir != Vector3.ZERO else &"idle")


func _aplicar_velocidade() -> void:
	actor.velocity.x = _dir.x * SPEED
	actor.velocity.z = _dir.z * SPEED
