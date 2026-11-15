class_name StatsComponent
extends Node
## Vida, vigor, sanidade, XP e frascos. Portado do projeto 2D (mesmos sinais,
## exports e padrões), com o dreno ambiente e o sinal de faixa do Véu.

## Sinal disparado quando a vida atual é alterada.
signal health_changed(new_val: float, max_val: float)

## Sinal disparado quando a vida atinge zero.
signal died

## Sinal disparado quando a estamina atual é alterada.
signal stamina_changed(new_val: float, max_val: float)

## Sinal disparado quando a sanidade atual é alterada.
signal sanity_changed(new_val: float, max_val: float)

## Sinal disparado quando XP ou Nível são alterados.
signal xp_changed(current_xp: float, xp_to_next: float, level: int)
signal leveled_up(new_level: int, stats: StatsComponent)

## Sinal disparado quando a contagem de frascos rápidos é alterada.
signal flasks_changed(blood_current: int, blood_max: int, laudanum_current: int, laudanum_max: int)

## Sinal opcional para notificar mudanças no estado de exaustão.
signal exhaustion_changed(is_exhausted: bool)

## Sinal disparado só quando a sanidade cruza para outra faixa do Véu.
signal veil_band_changed(band: Veil.Band)

@export_group("Health")
## Vida máxima da entidade.
@export var max_health: float = 100.0

@export_group("Stamina")
## Estamina máxima da entidade.
@export var max_stamina: float = 100.0

## Taxa de regeneração da estamina por segundo.
@export var stamina_regen_rate: float = 25.0

## Duração em segundos do estado de exaustão ao esgotar a estamina.
@export var exhaustion_duration: float = 1.0

## Tempo de atraso após consumir estamina antes de reiniciar a regeneração.
@export var stamina_regen_delay: float = 0.5

@export_group("Sanity")
## Sanidade máxima da entidade.
@export var max_sanity: float = 100.0

## Dreno contínuo de sanidade, em unidades por segundo (0 = sem dreno).
@export var ambient_sanity_drain: float = 0.0

@export_group("Consumables")
## Quantidade máxima de frascos de sangue e láudano
@export var max_blood_flasks: int = 3
@export var max_laudanum_flasks: int = 2

## Valores correntes
var current_health: float = 100.0
var current_stamina: float = 100.0
var current_sanity: float = 100.0
var current_blood_flasks: int = 3
var current_laudanum_flasks: int = 2

## Estado de exaustão (quando estamina atinge zero)
var is_exhausted: bool = false
var _is_dead: bool = false
var _regen_delay_timer: float = 0.0
var _exhaustion_timer: float = 0.0


func _ready() -> void:
	current_health = max_health
	current_stamina = max_stamina
	current_sanity = max_sanity
	current_blood_flasks = max_blood_flasks
	current_laudanum_flasks = max_laudanum_flasks


func _process(delta: float) -> void:
	if _is_dead:
		return
	
	if ambient_sanity_drain > 0.0:
		drain_sanity(ambient_sanity_drain * delta)
	
	# Gerencia timer de exaustão caso esteja exausto
	if is_exhausted:
		_exhaustion_timer -= delta
		if _exhaustion_timer <= 0.0:
			is_exhausted = false
			exhaustion_changed.emit(false)
	
	# Gerencia o delay após o último gasto de estamina
	if _regen_delay_timer > 0.0:
		_regen_delay_timer -= delta
	
	if not is_exhausted and _regen_delay_timer <= 0.0 and current_stamina < max_stamina:
		var regen = stamina_regen_rate
		var perks := Autoloads.get_autoload(&"PerksManager")
		if perks and perks.has_method("get_stamina_regen_multiplier"):
			regen *= perks.get_stamina_regen_multiplier()
		# TODO porte: penalidade de StatusEffectComponent (ver 2D)
		recover_stamina(regen * delta)


## Aplica dano à vida. Dispara died caso zere.
func take_damage(amount: float) -> void:
	if _is_dead or amount <= 0.0:
		return
	
	current_health = clampf(current_health - amount, 0.0, max_health)
	health_changed.emit(current_health, max_health)
	
	if current_health <= 0.0:
		_is_dead = true
		died.emit()


## Restaura vida até o valor máximo.
func heal(amount: float) -> void:
	if _is_dead or amount <= 0.0:
		return
	
	current_health = clampf(current_health + amount, 0.0, max_health)
	health_changed.emit(current_health, max_health)


## Consome estamina se houver quantidade suficiente. Retorna true se bem-sucedido.
func consume_stamina(cost: float) -> bool:
	if cost <= 0.0:
		return true
	
	if current_stamina < cost or is_exhausted:
		return false
	
	current_stamina = clampf(current_stamina - cost, 0.0, max_stamina)
	_regen_delay_timer = stamina_regen_delay
	stamina_changed.emit(current_stamina, max_stamina)
	
	if current_stamina <= 0.0:
		is_exhausted = true
		_exhaustion_timer = exhaustion_duration
		exhaustion_changed.emit(true)
	
	return true


## Recupera estamina até o valor máximo.
func recover_stamina(amount: float) -> void:
	if amount <= 0.0 or current_stamina >= max_stamina:
		return
	
	current_stamina = clampf(current_stamina + amount, 0.0, max_stamina)
	stamina_changed.emit(current_stamina, max_stamina)


## Reduz a sanidade da entidade (Horror Cósmico).
func drain_sanity(amount: float) -> void:
	if amount <= 0.0:
		return
	
	var antes := get_veil_band()
	current_sanity = clampf(current_sanity - amount, 0.0, max_sanity)
	sanity_changed.emit(current_sanity, max_sanity)
	_emitir_troca_de_faixa(antes)


## Restaura a sanidade da entidade.
func restore_sanity(amount: float) -> void:
	if amount <= 0.0:
		return
	
	var antes := get_veil_band()
	current_sanity = clampf(current_sanity + amount, 0.0, max_sanity)
	sanity_changed.emit(current_sanity, max_sanity)
	_emitir_troca_de_faixa(antes)


## Faixa do Véu para a sanidade atual.
func get_veil_band() -> Veil.Band:
	return Veil.band_for(current_sanity)


func _emitir_troca_de_faixa(antes: Veil.Band) -> void:
	var depois := get_veil_band()
	if depois != antes:
		veil_band_changed.emit(depois)


## Retorna true se a entidade estiver viva.
func is_alive() -> bool:
	return not _is_dead and current_health > 0.0


@export_group("Progression")
## Nível da entidade.
@export var level: int = 1
## XP concedido ao ser derrotado (para inimigos).
@export var xp_reward: float = 35.0
## XP atual acumulado (para o jogador).
var current_xp: float = 0.0
## XP necessário para o próximo nível.
var xp_to_next: float = 80.0


## Concede pontos de experiência e gerencia evolução de nível.
func gain_xp(amount: float) -> void:
	if amount <= 0.0 or _is_dead:
		return
	
	current_xp += amount
	while current_xp >= xp_to_next:
		current_xp -= xp_to_next
		level += 1
		xp_to_next = round(xp_to_next * 1.45)
		
		# Bônus permanente de atributos ao subir de nível
		max_health += 15.0
		current_health = max_health
		max_stamina += 10.0
		current_stamina = max_stamina
		restore_sanity(40.0)
		
		health_changed.emit(current_health, max_health)
		stamina_changed.emit(current_stamina, max_stamina)
		leveled_up.emit(level, self)
	
	xp_changed.emit(current_xp, xp_to_next, level)


## Consome um Frasco de Sangue para regenerar 40% de vida instantaneamente.
func use_blood_flask() -> bool:
	if current_blood_flasks <= 0 or current_health >= max_health or _is_dead:
		return false
	current_blood_flasks -= 1
	heal(max_health * 0.40)
	flasks_changed.emit(current_blood_flasks, max_blood_flasks, current_laudanum_flasks, max_laudanum_flasks)
	return true


## Consome um Elixir de Láudano para estabilizar a mente e restaurar 50% de sanidade.
func use_laudanum_flask() -> bool:
	if current_laudanum_flasks <= 0 or current_sanity >= max_sanity or _is_dead:
		return false
	current_laudanum_flasks -= 1
	restore_sanity(max_sanity * 0.50)
	flasks_changed.emit(current_blood_flasks, max_blood_flasks, current_laudanum_flasks, max_laudanum_flasks)
	return true



## Recarrega todos os frascos rápidos para suas capacidades máximas (usado no Altar).
func refill_flasks() -> void:
	current_blood_flasks = max_blood_flasks
	current_laudanum_flasks = max_laudanum_flasks
	flasks_changed.emit(current_blood_flasks, max_blood_flasks, current_laudanum_flasks, max_laudanum_flasks)
