class_name ActionTimeline
extends RefCounted
## Sequência de fases com duração (ex.: preparo, golpe ativo, recuperação).
## `advance` devolve todas as fases tocadas no intervalo, então uma travada de
## frame (delta de 0,3 s) não pula a janela ativa de um golpe nem a
## invencibilidade de uma esquiva.
##
## A fase i ocupa o intervalo [início, fim). Um intervalo [a, b] toca a fase
## quando início < b e fim > a.

var _phases: Array = []
var _starts: Array[float] = []
var _total := 0.0
var _elapsed := 0.0


## `phases`: lista de `{name: StringName, duration: float}`, em ordem.
func _init(phases: Array) -> void:
	_phases = phases
	for f in phases:
		_starts.append(_total)
		_total += float(f.duration)


## Avança o tempo e devolve, em ordem, as fases tocadas em [antes, depois].
func advance(delta: float) -> Array[StringName]:
	var de := _elapsed
	_elapsed = minf(_elapsed + maxf(delta, 0.0), _total)
	var tocadas: Array[StringName] = []
	if delta <= 0.0:
		if not current().is_empty():
			tocadas.append(current())
		return tocadas
	for i in _phases.size():
		if _starts[i] < de + delta and _fim(i) > de:
			tocadas.append(_phases[i].name)
	return tocadas


## Fase atual, ou `&""` quando a linha do tempo terminou.
func current() -> StringName:
	for i in _phases.size():
		if _elapsed >= _starts[i] and _elapsed < _fim(i):
			return _phases[i].name
	return &""


func finished() -> bool:
	return _elapsed >= _total


func elapsed() -> float:
	return _elapsed


func reset() -> void:
	_elapsed = 0.0


## Diz se a janela da fase `name` cruza o intervalo de tempo [from_t, to_t].
func is_in(name: StringName, from_t: float, to_t: float) -> bool:
	for i in _phases.size():
		if _phases[i].name == name and _starts[i] < to_t and _fim(i) > from_t:
			return true
	return false


func _fim(i: int) -> float:
	return _starts[i] + float(_phases[i].duration)
