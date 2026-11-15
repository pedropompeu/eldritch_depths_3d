extends Node
## Busca de autoload por nome. Substitui a checagem de singleton da Engine,
## que sempre retorna falso para autoloads (achado A01 em context/achados.md).
##
## Uso: `var save := Autoloads.get_autoload(&"SaveManager")`; checar `null`
## e `has_method` antes de chamar.


## Devolve o autoload `/root/<name>`, ou `null` (sem erro) se ele não existe.
func get_autoload(name: StringName) -> Node:
	return get_tree().root.get_node_or_null(NodePath(name))
