extends State
## Parry: 0,22 s de janela com `Hurtbox.parrying` ligado e 0,18 s de
## recuperação. O herói para e encara a mira. Quem decide o que acontece com o
## golpe que chega é `Player3D._on_hurt`.
##
## Como na esquiva, a janela vale para o intervalo do frame inteiro e é
## marcada no começo do passo, antes de o frame processar golpes.

const COST := 15.0
const WINDOW := 0.22
const RECOVERY := 0.18

var _timeline := ActionTimeline.new([
	{name = &"window", duration = WINDOW},
	{name = &"recovery", duration = RECOVERY},
])


## Chamado pelos estados de chão. Gasta o vigor e entra no parry; sem vigor,
## devolve falso e nada muda.
func try_begin() -> bool:
	if not actor.stats.consume_stamina(COST):
		return false
	state_machine.change_state(&"parry")
	return true


func enter() -> void:
	_timeline.reset()
	# Golpe que chegue ainda no frame do aperto já pega a janela aberta.
	actor.hurtbox.parrying = true
	actor.face(actor.aim_dir)


func exit() -> void:
	actor.hurtbox.parrying = false


func process_physics(delta: float) -> void:
	actor.walk(delta, 0.0)
	actor.face(actor.aim_dir)
	var de := _timeline.elapsed()
	actor.hurtbox.parrying = _timeline.is_in(&"window", de, de + delta)
	_timeline.advance(delta)
	if _timeline.finished():
		state_machine.change_state(&"move" if actor.move_dir != Vector3.ZERO else &"idle")
