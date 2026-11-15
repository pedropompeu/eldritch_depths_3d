class_name Hitbox3D
extends Area3D
## Área de golpe. `activate` já atinge, na mesma chamada, toda hurtbox que
## estiver sobreposta (não espera o próximo frame de física); enquanto ativa,
## atinge também quem entrar. Cada hurtbox leva no máximo um golpe por ativação.
## Camadas: herói 4 (detecta 7), inimigos 5 (detecta 6).

signal hit_landed(hurtbox: Hurtbox3D)

## 0 = herói, 1 = inimigo. Define camada e máscara no `_ready`.
@export var team: int = 0
@export var damage: float = 20.0
@export var posture_damage: float = 20.0
@export var sanity_damage: float = 0.0

var active := false
## Quem bate (herói ou inimigo).
var source: Node

var _atingidas: Array[Hurtbox3D] = []


func _ready() -> void:
	collision_layer = 1 << (3 if team == 0 else 4)
	collision_mask = 1 << (6 if team == 0 else 5)
	monitoring = true
	monitorable = false
	area_entered.connect(_on_area_entered)


func activate() -> void:
	active = true
	_atingidas.clear()
	for hurtbox in _sobrepostas_agora():
		_atingir(hurtbox)


func deactivate() -> void:
	active = false


func _on_area_entered(area: Area3D) -> void:
	if active and area is Hurtbox3D:
		_atingir(area)


func _atingir(hurtbox: Hurtbox3D) -> void:
	if hurtbox in _atingidas:
		return
	# Conta como atingida mesmo se invulnerável: a esquiva escapa do golpe
	# inteiro, não só do começo dele.
	_atingidas.append(hurtbox)
	if hurtbox.invulnerable:
		return
	hurtbox.receive(self)
	hit_landed.emit(hurtbox)


## Consulta direta ao espaço físico com cada forma da hitbox.
func _sobrepostas_agora() -> Array[Hurtbox3D]:
	var achadas: Array[Hurtbox3D] = []
	if not is_inside_tree():
		return achadas
	var espaco := get_world_3d().direct_space_state
	for child in get_children():
		if not (child is CollisionShape3D) or child.disabled or child.shape == null:
			continue
		var q := PhysicsShapeQueryParameters3D.new()
		q.shape = child.shape
		q.transform = child.global_transform
		q.collision_mask = collision_mask
		q.collide_with_areas = true
		q.collide_with_bodies = false
		q.exclude = [get_rid()]
		for r in espaco.intersect_shape(q, 32):
			var c = r.get("collider")
			if c is Hurtbox3D and not (c in achadas):
				achadas.append(c)
	return achadas
