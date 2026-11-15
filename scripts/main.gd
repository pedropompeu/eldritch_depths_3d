extends Node3D
## Cena principal do Bloco 1A: sala cinza, herói, câmera, um inimigo e a parede
## do Véu. Liga o dreno ambiente de sanidade, repassa a faixa do Véu do herói às
## paredes do Véu, desenha a vinheta da sanidade, liga o HUD e recarrega a cena
## 2 s depois da morte do herói. Com `-- --autoplay`, o herói joga sozinho e o
## inimigo reaparece (para medir fps).

const AMBIENT_SANITY_DRAIN := 0.8
const RELOAD_DELAY := 2.0
## Sanidade em que a vinheta começa a aparecer (o limite do Véu fino).
const VIGNETTE_START := 60.0
## Quanto a tecla de depuração (F9) tira de sanidade.
const DEBUG_SANITY_DROP := 20.0
const SANITY_ARG := "--sanity="
const AUTOPLAY_ARG := "--autoplay"
## No modo automático, o inimigo reaparece este tempo depois de morrer.
const ENEMY_RESPAWN_DELAY := 2.0
const AutoplayInput := preload("res://scripts/autoplay_input.gd")
const EnemyScene := preload("res://scenes/enemies/enemy_common.tscn")

@onready var hero: Player3D = $Player3D
@onready var vignette: ColorRect = $VignetteLayer/Vignette
@onready var hud: HudMinimal = $HudLayer/HudMinimal
@onready var enemy: EnemyCommon = $EnemyCommon

var _enemy_spawn: Transform3D


func _ready() -> void:
	hero.stats.ambient_sanity_drain = AMBIENT_SANITY_DRAIN
	hero.hero_died.connect(_on_hero_died)
	hero.stats.veil_band_changed.connect(_on_veil_band_changed)
	hero.stats.sanity_changed.connect(_on_sanity_changed)
	_on_sanity_changed(hero.stats.current_sanity, hero.stats.max_sanity)
	hud.bind(hero.get_node("Stats"))
	_apply_sanity_arg()
	if has_autoplay_arg(OS.get_cmdline_user_args()):
		enable_autoplay()


## Intensidade da vinheta (0 a 1) para a sanidade dada: nada até 60, cheia em 0.
static func vignette_intensity(sanity: float) -> float:
	return clampf((VIGNETTE_START - sanity) / VIGNETTE_START, 0.0, 1.0)


## Valor de `--sanity=N` nos argumentos de usuário (depois de `--`), ou -1.
static func sanity_from_args(args: PackedStringArray) -> float:
	for arg in args:
		if arg.begins_with(SANITY_ARG):
			var valor := arg.trim_prefix(SANITY_ARG)
			if valor.is_valid_float():
				return valor.to_float()
	return -1.0


static func has_autoplay_arg(args: PackedStringArray) -> bool:
	return args.has(AUTOPLAY_ARG)


## Põe o herói no piloto automático e faz o inimigo reaparecer onde estava.
func enable_autoplay() -> void:
	hero.input_source = AutoplayInput.make(Time.get_ticks_msec())
	_enemy_spawn = enemy.global_transform
	enemy.enemy_died.connect(_on_enemy_died)


func _on_enemy_died() -> void:
	await get_tree().create_timer(ENEMY_RESPAWN_DELAY).timeout
	enemy = EnemyScene.instantiate()
	enemy.target = hero
	add_child(enemy)
	enemy.global_transform = _enemy_spawn
	# Teletransporte: sem isto a interpolação desenharia o inimigo deslizando
	# de onde nasceu até o ponto de surgimento.
	enemy.reset_physics_interpolation()
	enemy.enemy_died.connect(_on_enemy_died)


func _unhandled_input(event: InputEvent) -> void:
	if OS.is_debug_build() and event.is_action_pressed(&"debug_sanity_drop"):
		hero.stats.drain_sanity(DEBUG_SANITY_DROP)


## Só na build de depuração: `godot -- --sanity=20` começa com a sanidade em 20
## (pelo dreno normal, para a vinheta e as paredes reagirem).
func _apply_sanity_arg() -> void:
	if not OS.is_debug_build():
		return
	var alvo := sanity_from_args(OS.get_cmdline_user_args())
	if alvo >= 0.0 and alvo < hero.stats.current_sanity:
		hero.stats.drain_sanity(hero.stats.current_sanity - alvo)


func _on_sanity_changed(sanity: float, _max_sanity: float) -> void:
	var material := vignette.material as ShaderMaterial
	material.set_shader_parameter(&"intensity", vignette_intensity(sanity))


## Repassa a faixa do Véu do herói a todas as paredes do Véu.
func _on_veil_band_changed(band: Veil.Band) -> void:
	for parede in get_tree().get_nodes_in_group(&"veil_walls"):
		parede.set_band(band)


func _on_hero_died() -> void:
	await get_tree().create_timer(RELOAD_DELAY).timeout
	get_tree().reload_current_scene()
