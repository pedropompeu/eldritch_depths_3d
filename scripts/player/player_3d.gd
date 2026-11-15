class_name Player3D
extends CharacterBody3D
## Herói provisório (cápsula). Lê a entrada uma vez por passo, converte o
## movimento pela câmera, resolve a mira e entrega o resto à máquina de
## estados. A partir da T18 os estados de ação usam `input`, `aim_dir` e `face`.

const GRAVITY := 20.0
## Abaixo disso (m/s) o herói conta como parado.
const STOP_EPS := 0.01
const InputModeScript := preload("res://scripts/core/input_mode.gd")
## Distância do centro da seta de mira até os pés do herói.
const ARROW_OFFSET := 0.9
const ARROW_HEIGHT := 0.05

## Emitido uma vez, quando o herói morre.
signal hero_died

@export var camera_rig: CameraRig3D
@export var base_damage := 20.0
## Postura que um parry bem-sucedido enche em quem bateu. (i) ajustável no
## teste de Pedro (T32).
@export var parry_posture_damage := 50.0
## Reservado para o bloqueio, que não existe neste bloco: declarado e sem uso.
@export var shield_mitigation := 0.5

var aim_dir: Vector3 = Vector3.FORWARD
var move_dir: Vector3 = Vector3.ZERO
## Devolve o dicionário de entrada do passo. O padrão lê `Input` e `InputMode`;
## os testes injetam outro.
var input_source: Callable
## Entrada do passo atual (ver `read_input`).
var input: Dictionary = {}
## Direção (no plano XZ, comprimento 1) de quem bateu até o herói, no último
## golpe recebido. O estado `hurt` empurra para cá.
var last_hit_dir: Vector3 = Vector3.BACK
## Ligado quando a esquiva ou o parry terminam: a invencibilidade e a janela de
## parry só se desligam no começo do próximo passo (ver `release_guard_next_step`).
var _release_guard := false

@onready var stats: StatsComponent = $Stats
@onready var posture: PostureComponent = $Posture
@onready var state_machine: StateMachine = $StateMachine
@onready var sword: Hitbox3D = $Sword
@onready var hurtbox: Hurtbox3D = $Hurtbox
@onready var aim_arrow: MeshInstance3D = $AimArrow


func _init() -> void:
	input_source = _read_devices


func _ready() -> void:
	sword.source = self
	sword.damage = base_damage
	hurtbox.hurt.connect(_on_hurt)
	stats.died.connect(_on_died)
	input = _empty_input()
	state_machine.init(self)
	_update_arrow()


func _physics_process(delta: float) -> void:
	step(delta)


## Entrada do passo: `{move, aim, attack, roll, parry, flask, laudanum}`. Os
## botões vêm como `just_pressed`. Campo ausente na fonte cai no valor vazio.
func read_input() -> Dictionary:
	var d := _empty_input()
	if input_source.is_valid():
		d.merge(input_source.call(), true)
	return d


## O trabalho de um `_physics_process`; os testes chamam direto.
func step(delta: float) -> void:
	if _release_guard:
		_release_guard = false
		hurtbox.invulnerable = false
		hurtbox.parrying = false
	input = read_input()
	var yaw := camera_rig.get_yaw() if camera_rig else 0.0
	move_dir = PlayerMotion.input_to_world(input.move, yaw)
	_update_aim(yaw)
	_use_flasks()
	state_machine.process_physics(delta)
	if not is_on_floor():
		velocity.y -= GRAVITY * delta
	move_and_slide()
	_update_arrow()


## Chamado no `exit()` da esquiva e do parry. Os golpes do frame são
## processados depois do passo; se o passo que terminou a ação já tivesse
## desligado a proteção, uma travada que cobre a janela e o fim da ação deixaria
## passar o golpe daquele mesmo frame. A proteção fica até o próximo passo.
func release_guard_next_step() -> void:
	_release_guard = true


## Acelera (ou freia, sem entrada) a velocidade horizontal rumo a `move_dir`.
## `speed_scale` reduz a velocidade máxima (o ataque anda a 20%).
func walk(delta: float, speed_scale := 1.0) -> void:
	var accel := PlayerMotion.ACCEL if move_dir != Vector3.ZERO else PlayerMotion.DECEL
	var horiz := PlayerMotion.compute_velocity(Vector3(velocity.x, 0.0, velocity.z), move_dir, PlayerMotion.WALK_SPEED * speed_scale, accel, delta)
	velocity.x = horiz.x
	velocity.z = horiz.z


## Tenta começar o ataque (T18). Falso sem vigor ou sem o estado na cena.
func try_attack() -> bool:
	return _try_action(&"attack")


## Tenta começar a esquiva (T19). Falso sem vigor ou sem o estado na cena.
func try_roll() -> bool:
	return _try_action(&"roll")


## Tenta começar o parry (T20). Falso sem vigor ou sem o estado na cena.
func try_parry() -> bool:
	return _try_action(&"parry")


func _try_action(key: StringName) -> bool:
	var acao: State = state_machine.states.get(key)
	return acao != null and acao.try_begin()


## Golpe que chegou na hurtbox (a esquiva já filtrou os invulneráveis). No
## parry, o herói não sofre nada e a postura de quem bateu enche; senão, dano,
## sanidade e o estado `hurt` (T21).
func _on_hurt(hitbox: Hitbox3D) -> void:
	if hurtbox.parrying:
		var alvo := _posture_of(hitbox.source)
		if alvo:
			alvo.damage_posture(parry_posture_damage)
		return
	if not stats.is_alive():
		return
	last_hit_dir = _away_from(hitbox)
	stats.take_damage(hitbox.damage)
	stats.drain_sanity(hitbox.sanity_damage)
	# Se o golpe matou, `_on_died` já levou ao estado `dead`.
	if stats.is_alive() and state_machine.states.has(&"hurt"):
		state_machine.change_state(&"hurt")


func _on_died() -> void:
	state_machine.change_state(&"dead")
	hero_died.emit()


func is_dead() -> bool:
	return _state_is(&"dead")


## Frascos valem em qualquer estado, menos `hurt` e `dead`.
func _use_flasks() -> void:
	if _state_is(&"hurt") or _state_is(&"dead"):
		return
	if input.flask:
		stats.use_blood_flask()
	if input.laudanum:
		stats.use_laudanum_flask()


func _state_is(key: StringName) -> bool:
	var atual := state_machine.current_state
	return atual != null and state_machine.states.get(key) == atual


## Direção de quem bateu (o `source`, ou a própria hitbox) até o herói. Se os
## dois coincidem no plano, empurra para trás do herói.
func _away_from(hitbox: Hitbox3D) -> Vector3:
	var origem: Node3D = hitbox.source if hitbox.source is Node3D else hitbox
	var d := global_position - origem.global_position
	d.y = 0.0
	if d.length() < STOP_EPS:
		d = global_transform.basis.z
		d.y = 0.0
	return d.normalized() if d.length() > STOP_EPS else Vector3.BACK


## O `PostureComponent` filho de `node`, ou `null`.
static func _posture_of(node: Node) -> PostureComponent:
	if node == null:
		return null
	for filho in node.get_children():
		if filho is PostureComponent:
			return filho
	return null


func horizontal_speed() -> float:
	return Vector2(velocity.x, velocity.z).length()


## Gira o corpo para `dir` no plano XZ; direção nula é ignorada.
func face(dir: Vector3) -> void:
	var plano := Vector3(dir.x, 0.0, dir.z)
	if plano.length() < STOP_EPS:
		return
	look_at(global_position + plano, Vector3.UP)


func is_pad() -> bool:
	var modo := Autoloads.get_autoload(&"InputMode")
	return modo != null and modo.mode == InputModeScript.Mode.PAD


func _update_aim(yaw: float) -> void:
	var pad := is_pad()
	var mouse_ground: Variant = null
	if not pad:
		var cam := get_viewport().get_camera_3d()
		if cam:
			var mp := get_viewport().get_mouse_position()
			mouse_ground = AimResolver.ground_point(cam.project_ray_origin(mp), cam.project_ray_normal(mp), global_position.y)
	var stick := PlayerMotion.input_to_world(input.aim, yaw)
	aim_dir = AimResolver.resolve(pad, global_position, mouse_ground, stick, move_dir, aim_dir)


## A seta fica no chão, à frente do herói na direção da mira, independente de
## para onde o corpo olha. O cone nasce apontando para +Y; deitado, aponta -Z.
func _update_arrow() -> void:
	var deitar := Basis(Vector3.RIGHT, -PI / 2.0)
	aim_arrow.global_transform = Transform3D(
		Basis.looking_at(aim_dir, Vector3.UP) * deitar,
		global_position + aim_dir * ARROW_OFFSET + Vector3(0.0, ARROW_HEIGHT, 0.0))


func _empty_input() -> Dictionary:
	return {
		move = Vector2.ZERO, aim = Vector2.ZERO, attack = false, roll = false,
		parry = false, flask = false, laudanum = false,
	}


func _read_devices() -> Dictionary:
	return {
		move = Input.get_vector(&"move_left", &"move_right", &"move_up", &"move_down"),
		aim = Input.get_vector(&"aim_left", &"aim_right", &"aim_up", &"aim_down"),
		attack = Input.is_action_just_pressed(&"attack"),
		roll = Input.is_action_just_pressed(&"roll"),
		parry = Input.is_action_just_pressed(&"parry"),
		flask = Input.is_action_just_pressed(&"use_blood_flask"),
		laudanum = Input.is_action_just_pressed(&"use_laudanum"),
	}
