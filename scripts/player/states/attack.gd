extends State
## Ataque em dois golpes. Cada golpe é uma linha do tempo preparo → ativo →
## recuperação; a espada só fica ligada na fase ativa. Apertar ataque na
## recuperação encadeia o outro golpe (1 → 2 → 1). Durante o golpe o herói
## anda a 20% e encara a mira.

const WINDUP := 0.08
const ACTIVE := 0.18
const RECOVERY := 0.14
## Vigor do golpe 1 e do golpe 2.
const COSTS: Array[float] = [18.0, 22.0]
const MOVE_SCALE := 0.2

## 0 = golpe 1, 1 = golpe 2.
var hit_index := 0

var _timeline := ActionTimeline.new([
	{name = &"windup", duration = WINDUP},
	{name = &"active", duration = ACTIVE},
	{name = &"recovery", duration = RECOVERY},
])
## Se a espada já ligou neste golpe; evita religar (e acertar de novo) na
## mesma fase ativa.
var _ligou := false


## Chamado pelos estados de chão. Gasta o vigor do golpe 1 e entra no ataque;
## sem vigor, devolve falso e nada muda.
func try_begin() -> bool:
	if not actor.stats.consume_stamina(COSTS[0]):
		return false
	hit_index = 0
	state_machine.change_state(&"attack")
	return true


func enter() -> void:
	_comecar_golpe()


func exit() -> void:
	actor.sword.deactivate()


func process_physics(delta: float) -> void:
	actor.walk(delta, MOVE_SCALE)
	actor.face(actor.aim_dir)
	if _timeline.current() == &"recovery" and actor.input.attack:
		var proximo := (hit_index + 1) % COSTS.size()
		if actor.stats.consume_stamina(COSTS[proximo]):
			hit_index = proximo
			_comecar_golpe()
			return
	var tocadas := _timeline.advance(delta)
	if &"active" in tocadas and not _ligou:
		_ligou = true
		actor.sword.activate()
	if _timeline.current() != &"active":
		actor.sword.deactivate()
	if _timeline.finished():
		state_machine.change_state(&"move" if actor.move_dir != Vector3.ZERO else &"idle")


func _comecar_golpe() -> void:
	_timeline.reset()
	_ligou = false
	actor.sword.deactivate()
	actor.sword.damage = actor.base_damage
	actor.face(actor.aim_dir)
