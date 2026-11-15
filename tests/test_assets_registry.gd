extends TestCase
## B02: todo arquivo de arte do jogo e todo bruto de serviço tem linha em context/assets.md.


func test_registro_acusa_falta() -> void:
	var arquivos := PackedStringArray(["assets/models/props/a.glb", "art/brutos/2026-11-15-flux-b.png"])
	var registro := "## Assets\n\n| arquivo | tipo |\n|---|---|\n| `assets/models/props/a.glb` | modelo |\n\nCitado só no texto: art/brutos/2026-11-15-flux-b.png\n"
	var faltam := AssetsRegistry.missing_entries(arquivos, registro)
	assert_eq(faltam, PackedStringArray(["art/brutos/2026-11-15-flux-b.png"]))


func test_assets_registrados() -> void:
	var texto := FileAccess.get_file_as_string("res://context/assets.md")
	assert_false(texto.is_empty(), "context/assets.md não existe ou está vazio")
	var faltam := AssetsRegistry.missing_entries(AssetsRegistry.list_registrable_files(), texto)
	assert_eq(faltam.size(), 0, "sem linha em context/assets.md: %s" % ", ".join(faltam))
