class_name HudMinimal
extends Control
## HUD mínimo, à moda soulslike: três barras finas (vida, vigor, sanidade) e os
## contadores de frasco, no canto superior esquerdo. Tudo é medido em pixels de
## 1080p e escalado pela altura da tela; nada vai ao centro nem embaixo.

const REF_HEIGHT := 1080.0
const MARGIN := 24.0
const BAR_HEIGHT := 6.0
const BAR_GAP := 4.0
## Largura por ponto do máximo, com teto.
const PX_PER_POINT := 2.4
const MAX_BAR_WIDTH := 360.0
const MARK_WIDTH := 1.0
## Espaço entre a última barra e os contadores, e entre os dois contadores.
const COUNTER_GAP := 8.0
const COUNTER_SPACING := 20.0
const FONT_SIZE := 16.0
const FONT_OUTLINE := 4.0
const InputModeScript := preload("res://scripts/core/input_mode.gd")

var _stats: StatsComponent
var _is_pad := false

@onready var _health: ColorRect = $Health
@onready var _stamina: ColorRect = $Stamina
@onready var _sanity: ColorRect = $Sanity
@onready var _blood_label: Label = $BloodLabel
@onready var _laudanum_label: Label = $LaudanumLabel


func _ready() -> void:
	get_viewport().size_changed.connect(_layout)


## Liga o HUD a um `StatsComponent` e ao modo de entrada. Lê os valores atuais
## na hora; depois segue os sinais.
func bind(stats: StatsComponent) -> void:
	_stats = stats
	stats.health_changed.connect(_on_value_changed.unbind(2))
	stats.stamina_changed.connect(_on_value_changed.unbind(2))
	stats.sanity_changed.connect(_on_value_changed.unbind(2))
	stats.flasks_changed.connect(_on_value_changed.unbind(4))
	var modo := Autoloads.get_autoload(&"InputMode")
	if modo:
		_is_pad = modo.mode == InputModeScript.Mode.PAD
		modo.mode_changed.connect(_on_mode_changed)
	_layout()


## União dos retângulos visíveis do HUD, em pixels da tela.
func hud_rect() -> Rect2:
	var r := Rect2()
	var primeiro := true
	for filho in [_health, _stamina, _sanity, _blood_label, _laudanum_label]:
		if not filho.visible:
			continue
		var g: Rect2 = filho.get_global_rect()
		r = g if primeiro else r.merge(g)
		primeiro = false
	return r


func _on_value_changed() -> void:
	_layout()


func _on_mode_changed(mode: int) -> void:
	_is_pad = mode == InputModeScript.Mode.PAD
	_layout()


## Recalcula posições, tamanhos e textos para a tela e os valores atuais.
func _layout() -> void:
	if _stats == null or not is_inside_tree():
		return
	var s := get_viewport_rect().size.y / REF_HEIGHT
	var margem := MARGIN * s
	var y := margem
	for par in [
		[_health, _stats.current_health, _stats.max_health],
		[_stamina, _stats.current_stamina, _stats.max_stamina],
		[_sanity, _stats.current_sanity, _stats.max_sanity],
	]:
		_place_bar(par[0], Vector2(margem, y), par[2], par[1], s)
		y += (BAR_HEIGHT + BAR_GAP) * s
	_place_marks(s)

	var fonte := roundi(FONT_SIZE * s)
	var x := margem
	y += (COUNTER_GAP - BAR_GAP) * s
	for par in [
		[_blood_label, &"use_blood_flask", _stats.current_blood_flasks],
		[_laudanum_label, &"use_laudanum", _stats.current_laudanum_flasks],
	]:
		var rotulo: Label = par[0]
		rotulo.text = "%s ×%d" % [InputPrompt.label_for(par[1], _is_pad), par[2]]
		rotulo.add_theme_font_size_override(&"font_size", fonte)
		rotulo.add_theme_constant_override(&"outline_size", roundi(FONT_OUTLINE * s))
		rotulo.position = Vector2(x, y)
		rotulo.size = rotulo.get_combined_minimum_size()
		x += rotulo.size.x + COUNTER_SPACING * s


func _place_bar(fundo: ColorRect, pos: Vector2, maximo: float, atual: float, s: float) -> void:
	var largura := minf(PX_PER_POINT * maximo, MAX_BAR_WIDTH) * s
	fundo.position = pos
	fundo.size = Vector2(largura, BAR_HEIGHT * s)
	var cheio: ColorRect = fundo.get_node("Fill")
	var fracao := clampf(atual / maximo, 0.0, 1.0) if maximo > 0.0 else 0.0
	cheio.position = Vector2.ZERO
	cheio.size = Vector2(largura * fracao, BAR_HEIGHT * s)


## Marcas de 1 px na barra de sanidade nos limites do Véu (60 e 30).
func _place_marks(s: float) -> void:
	var largura := _sanity.size.x
	var marca := maxf(1.0, roundf(MARK_WIDTH * s))
	for par in [[&"Mark60", Veil.THRESHOLD_FINO], [&"Mark30", Veil.THRESHOLD_RASGADO]]:
		var no: ColorRect = _sanity.get_node(NodePath(par[0]))
		no.position = Vector2(roundf(largura * par[1] / _stats.max_sanity), 0.0)
		no.size = Vector2(marca, _sanity.size.y)
