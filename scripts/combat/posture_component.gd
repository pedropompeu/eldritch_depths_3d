class_name PostureComponent
extends Node
## Postura: enche com golpes e parries; no máximo, quebra e deixa o dono
## atordoado por `stagger_duration`, a janela do golpe crítico. Fora da quebra,
## volta a 0 a `recovery_rate` por segundo.
##
## Portado do 2D com a escala invertida (lá a barra começava cheia e caía) e
## sem a espera de 2,2 s antes de recuperar — ver rulings da T16 no ledger.

signal posture_changed(current: float, max_val: float)
signal posture_broken
signal posture_recovered

@export var max_posture := 100.0
@export var stagger_duration := 3.0
## Postura recuperada por segundo.
@export var recovery_rate := 14.0

var current := 0.0
var is_broken := false
var _stagger_left := 0.0


func _process(delta: float) -> void:
	step(delta)


func damage_posture(amount: float) -> void:
	if is_broken or amount <= 0.0:
		return
	current = minf(current + amount, max_posture)
	posture_changed.emit(current, max_posture)
	if current >= max_posture:
		is_broken = true
		_stagger_left = stagger_duration
		posture_broken.emit()


## Encerra a quebra antes do `stagger_duration` (o dono decide quanto dura o
## atordoamento; o inimigo comum usa 1,5 s). Sem quebra, não faz nada.
func recover() -> void:
	if not is_broken:
		return
	is_broken = false
	_stagger_left = 0.0
	current = 0.0
	posture_changed.emit(current, max_posture)
	posture_recovered.emit()


func step(delta: float) -> void:
	if is_broken:
		_stagger_left -= delta
		if _stagger_left <= 0.0:
			is_broken = false
			current = 0.0
			posture_changed.emit(current, max_posture)
			posture_recovered.emit()
		return
	if current > 0.0:
		current = maxf(0.0, current - recovery_rate * delta)
		posture_changed.emit(current, max_posture)
