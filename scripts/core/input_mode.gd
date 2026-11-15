extends Node
## Modo de entrada atual: teclado e mouse (KBM) ou controle (PAD). Troca sozinho
## pelo último dispositivo usado; a mira e os rótulos de botão seguem o modo.

signal mode_changed(mode: Mode)

enum Mode { KBM, PAD }

## Abaixo disso, o analógico é drift e não conta como uso do controle.
const STICK_DEADZONE := 0.2
## Movimento de mouse menor que isso (px) é tremida e não troca o modo.
const MOUSE_MIN_MOTION := 2.0

var mode: Mode = Mode.KBM


func _ready() -> void:
	Input.joy_connection_changed.connect(_on_joy_connection_changed)


func _input(event: InputEvent) -> void:
	handle_event(event)


func handle_event(event: InputEvent) -> void:
	if event is InputEventJoypadButton:
		if event.pressed:
			_set_mode(Mode.PAD)
	elif event is InputEventJoypadMotion:
		if absf(event.axis_value) > STICK_DEADZONE:
			_set_mode(Mode.PAD)
	elif event is InputEventMouseMotion:
		if event.relative.length() > MOUSE_MIN_MOTION:
			_set_mode(Mode.KBM)
	elif event is InputEventMouseButton:
		_set_mode(Mode.KBM)
	elif event is InputEventKey:
		if event.pressed:
			_set_mode(Mode.KBM)


func _on_joy_connection_changed(_device: int, connected: bool) -> void:
	if not connected and Input.get_connected_joypads().is_empty():
		_set_mode(Mode.KBM)


func _set_mode(novo: Mode) -> void:
	if novo == mode:
		return
	mode = novo
	mode_changed.emit(mode)
