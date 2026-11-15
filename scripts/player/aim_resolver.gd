class_name AimResolver
extends RefCounted
## Resolve a direção de mira do herói no plano XZ, com quedas seguras: o
## resultado sempre tem comprimento 1 e nunca é zero nem NaN.

const PARALLEL_EPS := 0.0001
const MIN_MOUSE_DIST := 0.1
const STICK_MIN := 0.2
const ZERO_EPS := 0.0001


## Ponto em que o raio cruza o plano horizontal `y = plane_y`, ou `null` se o
## raio é quase paralelo ao plano ou o ponto fica atrás da origem.
static func ground_point(origin: Vector3, dir: Vector3, plane_y: float) -> Variant:
	if absf(dir.y) < PARALLEL_EPS:
		return null
	var t := (plane_y - origin.y) / dir.y
	if t < 0.0:
		return null
	return origin + dir * t


## Direção de mira (y = 0, comprimento 1). Ordem: mouse (KBM) a mais de 0,1 m
## do herói; analógico direito (PAD) acima de 0,2; movimento; última mira;
## `Vector3.FORWARD`.
static func resolve(is_pad: bool, actor_pos: Vector3, mouse_ground: Variant, right_stick_world: Vector3, move_dir: Vector3, last_aim: Vector3) -> Vector3:
	if not is_pad and mouse_ground is Vector3:
		var para_mouse := _plano(mouse_ground - actor_pos)
		if para_mouse.length() > MIN_MOUSE_DIST:
			return para_mouse.normalized()
	if is_pad:
		var stick := _plano(right_stick_world)
		if stick.length() > STICK_MIN:
			return stick.normalized()
	for candidata in [move_dir, last_aim]:
		var c := _plano(candidata)
		if c.length() > ZERO_EPS:
			return c.normalized()
	return Vector3.FORWARD


static func _plano(v: Vector3) -> Vector3:
	if not v.is_finite():
		return Vector3.ZERO
	return Vector3(v.x, 0.0, v.z)
