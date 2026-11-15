class_name StateMachine
extends Node
## Gerenciador genérico de estados finitos (FSM) para personagens e inimigos.
## Portado do 2D. A chave de cada estado é o nome do nó em minúsculas.

## Estado inicial opcional; sem ele, `init` entra no primeiro estado filho.
@export var initial_state: State

var current_state: State
var states: Dictionary = {}


func init(actor: Node) -> void:
	var primeiro: State = null
	for child in get_children():
		if child is State:
			states[StringName(String(child.name).to_lower())] = child
			child.state_machine = self
			child.actor = actor
			if primeiro == null:
				primeiro = child
	var inicial: State = initial_state if initial_state else primeiro
	if inicial:
		change_state(StringName(String(inicial.name).to_lower()))


func change_state(key: StringName) -> void:
	var chave := StringName(String(key).to_lower())
	if not states.has(chave):
		# Aviso, não erro: chave errada não deve derrubar o jogo.
		push_warning("StateMachine: estado '%s' não encontrado." % chave)
		return
	if current_state:
		current_state.exit()
	current_state = states[chave]
	current_state.enter()


func process_input(event: InputEvent) -> void:
	if current_state:
		current_state.process_input(event)


func process_frame(delta: float) -> void:
	if current_state:
		current_state.process_frame(delta)


func process_physics(delta: float) -> void:
	if current_state:
		current_state.process_physics(delta)
