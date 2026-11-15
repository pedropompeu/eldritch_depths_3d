class_name VeilWall
extends StaticBody3D
## Parede que só existe enquanto o Véu está claro. Quando a faixa chega a
## `opens_at`, a colisão some na hora e a malha se dissolve em 0,6 s. Volta a
## fechar quando a faixa cai abaixo de `opens_at`, mas nunca sobre alguém:
## com um corpo em `Inside`, o fechamento fica pendente até esvaziar.

const DISSOLVE_TIME := 0.6
## Camada do mundo (1), a mesma das paredes da sala.
const WORLD_LAYER := 1

@export var opens_at: Veil.Band = Veil.Band.FINO

## 0 = parede inteira, 1 = dissolvida. Repassado ao material da malha.
var dissolve := 0.0:
	set(value):
		dissolve = clampf(value, 0.0, 1.0)
		if _material:
			_material.set_shader_parameter(&"dissolve", dissolve)

var _close_pending := false
var _tween: Tween
var _material: ShaderMaterial

@onready var mesh: MeshInstance3D = $Mesh
@onready var inside: Area3D = $Inside


func _ready() -> void:
	add_to_group(&"veil_walls")
	collision_layer = WORLD_LAYER
	_material = mesh.mesh.surface_get_material(0) as ShaderMaterial
	dissolve = dissolve


func _physics_process(_delta: float) -> void:
	if _close_pending and inside.get_overlapping_bodies().is_empty():
		_close()


## Recebe a faixa atual do Véu do herói.
func set_band(b: Veil.Band) -> void:
	if b >= opens_at:
		_close_pending = false
		_open()
	elif not is_solid():
		if inside.get_overlapping_bodies().is_empty():
			_close()
		else:
			_close_pending = true


func is_solid() -> bool:
	return collision_layer != 0


## A colisão sai zerando a camada (vale até no meio de um passo de física, ao
## contrário de desligar a forma).
func _open() -> void:
	if not is_solid():
		return
	collision_layer = 0
	_animate_dissolve(1.0)


func _close() -> void:
	_close_pending = false
	collision_layer = WORLD_LAYER
	_animate_dissolve(0.0)


func _animate_dissolve(to: float) -> void:
	if _tween:
		_tween.kill()
	_tween = create_tween()
	_tween.tween_property(self, ^"dissolve", to, DISSOLVE_TIME * absf(to - dissolve))
