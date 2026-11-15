class_name InputPrompt
extends RefCounted
## Rótulo do botão de uma ação para o dispositivo em uso. Texto puro neste
## bloco; os valores espelham o mapa de entrada do `project.godot`.

## ação → [teclado e mouse, controle]
const LABELS := {
	&"use_blood_flask": ["1", "↓"],
	&"use_laudanum": ["2", "↑"],
	&"interact": ["E", "B"],
}


## Rótulo de `action` no controle (`is_pad`) ou no teclado; "" se a ação não
## tem rótulo.
static func label_for(action: StringName, is_pad: bool) -> String:
	var par: Array = LABELS.get(action, ["", ""])
	return par[1] if is_pad else par[0]
