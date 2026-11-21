class_name VeilWall
extends StaticBody3D
## Parede que só existe enquanto o Véu está claro. Quando a faixa chega a
## `opens_at`, a colisão some na hora e a malha se dissolve em 0,6 s. Volta a
## fechar quando a faixa cai abaixo de `opens_at`, mas nunca sobre alguém:
## com um corpo em `Inside`, o fechamento fica pendente até esvaziar.

const DISSOLVE_TIME := 0.6
## Camada do mundo (1), a mesma das paredes da sala.
const WORLD_LAYER := 1
## Malha da parede do kit: o Véu usa a mesma pedra da sala, no lugar da caixa.
const MALHA_PEDRA: PackedScene = preload("res://assets/models/kit/parede.glb")

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
	_usar_malha_do_kit()
	_material = mesh.material_override as ShaderMaterial
	if _material == null:
		_material = mesh.mesh.surface_get_material(0) as ShaderMaterial
	dissolve = dissolve


## Troca a caixa pela malha de `parede.glb` (B15). O material do shader entra
## por `material_override`, então a malha compartilhada com a sala não muda.
## A peça do kit tem a origem no canto de grade; a colisão fica centrada no nó,
## então o `Mesh` recebe o deslocamento contrário ao centro da malha.
func _usar_malha_do_kit() -> void:
	var copia := MALHA_PEDRA.instantiate()
	for no in copia.find_children("*", "MeshInstance3D", true, false):
		var peca := no as MeshInstance3D
		if peca.mesh:
			mesh.mesh = peca.mesh
			mesh.position = -peca.mesh.get_aabb().get_center()
			break
	copia.free()


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
