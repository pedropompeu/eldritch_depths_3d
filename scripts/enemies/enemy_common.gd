class_name EnemyCommon
extends CharacterBody3D
## Inimigo comum provisório (cápsula escura). Fica parado até o alvo entrar na
## detecção, então anda em linha reta até ele e para no alcance de ataque. A
## T23 troca a parada no alcance pelo `telegraph`.

const GRAVITY := 20.0

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
	state_machine.init(self)


func _physics_process(delta: float) -> void:
	step(delta)


## O trabalho de um `_physics_process`; os testes chamam direto.
func step(delta: float) -> void:
	state_machine.process_physics(delta)
	if not is_on_floor():
		velocity.y -= GRAVITY * delta
	move_and_slide()


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


func set_horizontal_velocity(v: Vector3) -> void:
	velocity.x = v.x
	velocity.z = v.z


## Gira o corpo para `dir` no plano XZ; direção nula é ignorada.
func face(dir: Vector3) -> void:
	var plano := Vector3(dir.x, 0.0, dir.z)
	if plano.length() < 0.001:
		return
	look_at(global_position + plano, Vector3.UP)
