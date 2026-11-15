class_name Hurtbox3D
extends Area3D
## Área que recebe golpes. Quem trata dano e parry é o dono, ao ouvir `hurt`.
## Camadas: herói 6, inimigos 7 (tabela em context/arquitetura.md#colisao).

signal hurt(hitbox: Hitbox3D)

## 0 = herói, 1 = inimigo. Define a camada no `_ready`.
@export var team: int = 0

var invulnerable := false
var parrying := false


func _ready() -> void:
	collision_layer = 1 << (5 if team == 0 else 6)
	collision_mask = 0
	monitoring = false
	monitorable = true


func receive(hitbox: Hitbox3D) -> void:
	if invulnerable:
		return
	hurt.emit(hitbox)
