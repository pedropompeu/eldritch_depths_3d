class_name CameraRig3D
extends Node3D
## Câmera fixa inclinada, estilo Diablo. O rig segue o alvo e gira `yaw_deg`
## em Y; a câmera fica recuada `distance` ao longo do eixo inclinado
## `pitch_deg` e olha para a origem do rig.

enum Preset { ATUAL, PROXIMA }

const HERO_HEIGHT := 1.8
## Fração da altura da tela ocupada pelo herói em cada enquadramento.
const FRACTION := { Preset.ATUAL: 1.0 / 13.0, Preset.PROXIMA: 1.0 / 8.0 }

@export var target: Node3D
@export var pitch_deg := 55.0
@export var yaw_deg := 45.0
@export var fov_deg := 40.0
@export var follow_sharpness := 8.0
@export var preset: Preset = Preset.ATUAL

## Distância da câmera até a origem do rig, em metros. Vai até a distância do
## preset pelo mesmo lerp do seguimento.
var distance: float = 0.0
var _target_distance: float = 0.0

@onready var _camera: Camera3D = $Camera3D


## Distância em que um objeto de altura `h` ocupa a fração `f` da altura da tela.
static func distance_for_fraction(h: float, f: float, fov: float) -> float:
	return h / (f * 2.0 * tan(deg_to_rad(fov) / 2.0))


func _ready() -> void:
	set_preset(preset)
	distance = _target_distance
	rotation.y = get_yaw()
	_camera.fov = fov_deg
	_posicionar_camera()
	if target:
		global_position = target.global_position


func _process(delta: float) -> void:
	step(delta)


func _unhandled_input(event: InputEvent) -> void:
	if event.is_action_pressed(&"debug_camera_preset"):
		toggle_preset()


## Define só a distância-alvo; a troca acontece suave nos próximos passos.
func set_preset(p: Preset) -> void:
	preset = p
	_target_distance = distance_for_fraction(HERO_HEIGHT, FRACTION[p], fov_deg)


func toggle_preset() -> void:
	set_preset(Preset.PROXIMA if preset == Preset.ATUAL else Preset.ATUAL)


func get_yaw() -> float:
	return deg_to_rad(yaw_deg)


## Um passo de seguimento. O lerp exponencial dá o mesmo resultado em qualquer fps.
func step(delta: float) -> void:
	var peso := 1.0 - exp(-follow_sharpness * delta)
	if target:
		position = position.lerp(target.global_position, peso)
	distance = lerpf(distance, _target_distance, peso)
	_posicionar_camera()


func _posicionar_camera() -> void:
	var pitch := deg_to_rad(pitch_deg)
	var recuo := Vector3(0.0, sin(pitch), cos(pitch)) * distance
	_camera.transform = Transform3D(Basis.looking_at(-recuo, Vector3.UP), recuo)
