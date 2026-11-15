extends Node3D
## Cena principal do Bloco 1A: sala cinza, herói, câmera e um inimigo. Liga o
## dreno ambiente de sanidade e recarrega a cena 2 s depois da morte do herói.

const AMBIENT_SANITY_DRAIN := 0.8
const RELOAD_DELAY := 2.0

@onready var hero: Player3D = $Player3D


func _ready() -> void:
	hero.stats.ambient_sanity_drain = AMBIENT_SANITY_DRAIN
	hero.hero_died.connect(_on_hero_died)


func _on_hero_died() -> void:
	await get_tree().create_timer(RELOAD_DELAY).timeout
	get_tree().reload_current_scene()
