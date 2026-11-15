class_name EnemyCommon
extends CharacterBody3D
## Inimigo comum provisório (cápsula escura). Fica parado até o alvo entrar na
## detecção, então anda em linha reta até ele; no alcance, avisa (`telegraph`),
## bate (`attack`) e recarrega (`cooldown`) antes de voltar a perseguir. Com a
## postura quebrada fica atordoado (`stunned`, dano em dobro); sem vida, morre
## (`dead`).

const GRAVITY := 20.0
## Folga nas durações dos estados: soma de passos de 1/60 s não fecha exata.
const TIME_EPS := 0.0001
const TELEGRAPH_COLOR := Color("#ff2020")
const TELEGRAPH_ENERGY := 2.0
## Multiplicador do dano recebido em `stunned`.
const CRIT_MULTIPLIER := 2.0

## Emitido uma vez, quando o inimigo morre.
signal enemy_died

@export var target: Node3D
## Inimigo cósmico: seus golpes também tiram sanidade (a partir da T23).
@export var is_cosmic := true
@export var move_speed := 2.4
@export var detection_range := 6.7
@export var attack_range := 1.5

@onready var stats: StatsComponent = $Stats
@onready var posture: PostureComponent = $Posture
@onready var state_machine: StateMachine = $StateMachine
@onready var claw: Hitbox3D = $Claw
@onready var hurtbox: Hurtbox3D = $Hurtbox
@onready var body: MeshInstance3D = $Body


func _ready() -> void:
	claw.source = self
	hurtbox.hurt.connect(_on_hurt)
	posture.posture_broken.connect(_on_posture_broken)
	stats.died.connect(_on_died)
	state_machine.init(self)


func _physics_process(delta: float) -> void:
	step(delta)


## O trabalho de um `_physics_process`; os testes chamam direto.
func step(delta: float) -> void:
	state_machine.process_physics(delta)
	if not is_on_floor():
		velocity.y -= GRAVITY * delta
	move_and_slide()


## Golpe do herói: dano (× 2 se atordoado) e postura. Morto, ignora.
func _on_hurt(hitbox: Hitbox3D) -> void:
	if not stats.is_alive():
		return
	var dano := hitbox.damage * (CRIT_MULTIPLIER if is_state(&"stunned") else 1.0)
	stats.take_damage(dano)
	if not stats.is_alive():
		return
	posture.damage_posture(hitbox.posture_damage)


func _on_posture_broken() -> void:
	if stats.is_alive():
		state_machine.change_state(&"stunned")


func _on_died() -> void:
	state_machine.change_state(&"dead")
	enemy_died.emit()


func is_state(key: StringName) -> bool:
	var atual := state_machine.current_state
	return atual != null and state_machine.states.get(key) == atual


## Desliga corpo, hurtbox e garra: o morto não colide, não apanha, não bate.
func disable_collisions() -> void:
	claw.deactivate()
	collision_layer = 0
	collision_mask = 0
	hurtbox.set_deferred(&"monitorable", false)
	for no: Node in [self, hurtbox, claw]:
		for filho in no.get_children():
			if filho is CollisionShape3D:
				filho.set_deferred(&"disabled", true)


## O `StatsComponent` do alvo (propriedade `stats` ou primeiro filho), ou `null`.
func target_stats() -> StatsComponent:
	if not is_instance_valid(target):
		return null
	var s = target.get(&"stats")
	if s is StatsComponent:
		return s
	for filho in target.get_children():
		if filho is StatsComponent:
			return filho
	return null


## Distância até o alvo no plano XZ; `INF` sem alvo.
func distance_to_target() -> float:
	if not is_instance_valid(target):
		return INF
	var d := target.global_position - global_position
	return Vector2(d.x, d.z).length()


## Direção (XZ, comprimento 1) até o alvo; zero sem alvo ou em cima dele.
func direction_to_target() -> Vector3:
	if not is_instance_valid(target):
		return Vector3.ZERO
	var d := target.global_position - global_position
	d.y = 0.0
	return d.normalized() if d.length() > 0.001 else Vector3.ZERO


func can_see_target() -> bool:
	return distance_to_target() <= detection_range


## Liga ou desliga o vermelho emissivo do aviso no material do corpo.
func set_telegraph_glow(on: bool) -> void:
	var mat := body.mesh.material as StandardMaterial3D
	if mat == null:
		return
	mat.emission_enabled = on
	if on:
		mat.emission = TELEGRAPH_COLOR
		mat.emission_energy_multiplier = TELEGRAPH_ENERGY


func set_horizontal_velocity(v: Vector3) -> void:
	velocity.x = v.x
	velocity.z = v.z


## Gira o corpo para `dir` no plano XZ; direção nula é ignorada.
func face(dir: Vector3) -> void:
	var plano := Vector3(dir.x, 0.0, dir.z)
	if plano.length() < 0.001:
		return
	look_at(global_position + plano, Vector3.UP)
