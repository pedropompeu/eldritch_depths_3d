class_name State
extends Node
## Classe base para todos os estados de personagens e entidades.
## Portada do 2D; o ator agora é qualquer `Node` (no 3D, `CharacterBody3D`).

var state_machine = null
var actor: Node = null


func enter() -> void:
	pass


func exit() -> void:
	pass


func process_input(_event: InputEvent) -> void:
	pass


func process_frame(_delta: float) -> void:
	pass


func process_physics(_delta: float) -> void:
	pass
