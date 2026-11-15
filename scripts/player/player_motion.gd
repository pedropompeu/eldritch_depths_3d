class_name PlayerMotion
extends RefCounted
## Matemática de movimento do herói, sem nós: direção relativa à câmera e
## aceleração. Valores em metros (1 m = 27 px do 2D).

const WALK_SPEED := 5.0
const ACCEL := 40.0
const DECEL := 60.0


## Converte a direção na tela (x para a direita, y para baixo) numa direção no
## plano XZ, girada pelo yaw da câmera em torno de `Vector3.UP`. O comprimento
## nunca passa de 1, então a diagonal não anda mais rápido.
static func input_to_world(input: Vector2, cam_yaw: float) -> Vector3:
	var dir := Vector3(input.x, 0.0, input.y).limit_length(1.0)
	return dir.rotated(Vector3.UP, cam_yaw)


## Aproxima `current` de `wish * max_speed`, avançando `accel * delta` por passo.
## Quem chama passa `DECEL` quando `wish` é zero.
static func compute_velocity(current: Vector3, wish: Vector3, max_speed: float, accel: float, delta: float) -> Vector3:
	return current.move_toward(wish * max_speed, accel * delta)
