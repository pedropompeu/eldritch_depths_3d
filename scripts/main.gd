extends Node3D
## Cena principal do Bloco 1A: sala cinza, herói, câmera, um inimigo e a parede
## do Véu. Liga o dreno ambiente de sanidade, repassa a faixa do Véu do herói às
## paredes do Véu e recarrega a cena 2 s depois da morte do herói.

const AMBIENT_SANITY_DRAIN := 0.8
const RELOAD_DELAY := 2.0

@onready var hero: Player3D = $Player3D


func _ready() -> void:
	hero.stats.ambient_sanity_drain = AMBIENT_SANITY_DRAIN
	hero.hero_died.connect(_on_hero_died)
	hero.stats.veil_band_changed.connect(_on_veil_band_changed)


## Repassa a faixa do Véu do herói a todas as paredes do Véu.
func _on_veil_band_changed(band: Veil.Band) -> void:
	for parede in get_tree().get_nodes_in_group(&"veil_walls"):
		parede.set_band(band)


func _on_hero_died() -> void:
	await get_tree().create_timer(RELOAD_DELAY).timeout
	get_tree().reload_current_scene()
