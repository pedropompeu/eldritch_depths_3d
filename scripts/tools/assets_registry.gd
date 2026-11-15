class_name AssetsRegistry
## Confere que cada arquivo de arte tem linha em context/assets.md (B02 da trilha de arte).
## A primeira célula de cada linha de tabela é o caminho do arquivo, relativo à raiz do projeto.

## Pastas varridas e as extensões que contam em cada uma (vazio = qualquer arquivo).
const PASTAS := {
	"assets/models": ["glb", "png", "jpg"],
	"art/brutos": [],
}


## Caminhos de `files` que não aparecem como primeira célula de nenhuma linha de tabela do registro.
static func missing_entries(files: PackedStringArray, registry_text: String) -> PackedStringArray:
	var registrados := {}
	for linha in registry_text.split("\n"):
		var l := linha.strip_edges()
		if not l.begins_with("|"):
			continue
		var celulas := l.split("|")
		if celulas.size() < 2:
			continue
		registrados[celulas[1].strip_edges().trim_prefix("`").trim_suffix("`")] = true
	var faltam := PackedStringArray()
	for f in files:
		if not registrados.has(f):
			faltam.append(f)
	return faltam


## Arquivos de arte do repositório que precisam de registro, relativos à raiz.
## Lê o disco direto (art/ tem .gdignore e a Godot não importa nada lá). Pastas ausentes contam como vazias.
static func list_registrable_files() -> PackedStringArray:
	var saida := PackedStringArray()
	var raiz := ProjectSettings.globalize_path("res://")
	for pasta in PASTAS:
		_varrer(raiz, pasta, PASTAS[pasta], saida)
	return saida


static func _varrer(raiz: String, rel: String, extensoes: Array, saida: PackedStringArray) -> void:
	var dir := DirAccess.open(raiz.path_join(rel))
	if dir == null:
		return
	for f in dir.get_files():
		if f.begins_with("."):
			continue
		if extensoes.is_empty() or f.get_extension().to_lower() in extensoes:
			saida.append(rel.path_join(f))
	for d in dir.get_directories():
		_varrer(raiz, rel.path_join(d), extensoes, saida)
