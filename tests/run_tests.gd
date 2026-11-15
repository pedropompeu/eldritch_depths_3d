extends SceneTree
## Runner caseiro: roda todo método `test_*` de cada `res://tests/test_*.gd`, em ordem alfabética.
## Uso: godot --headless --path . -s res://tests/run_tests.gd

const TEST_DIR := "res://tests"


func _initialize() -> void:
	_run()


func _run() -> void:
	await process_frame
	var total := 0
	var falhas := 0
	var arquivos := Array(DirAccess.get_files_at(TEST_DIR)).filter(
		func(f: String) -> bool: return f.begins_with("test_") and f.ends_with(".gd") and f != "test_case.gd"
	)
	arquivos.sort()
	for arquivo in arquivos:
		var script: Script = load(TEST_DIR.path_join(arquivo))
		if script == null:
			print("FAIL %s::<carga>: script não carregou" % arquivo)
			total += 1
			falhas += 1
			continue
		var obj = script.new()
		for metodo in _metodos_de_teste(script):
			total += 1
			obj.failures.clear()
			if obj.get_method_argument_count(metodo) == 1:
				await obj.call(metodo, self)
			else:
				await obj.call(metodo)
			if not obj.failures.is_empty():
				falhas += 1
				for msg in obj.failures:
					print("FAIL %s::%s: %s" % [arquivo, metodo, msg])
	if falhas == 0:
		print("OK: %d testes" % total)
		quit(0)
	else:
		print("FALHOU: %d de %d" % [falhas, total])
		quit(1)


func _metodos_de_teste(script: Script) -> Array[String]:
	var nomes: Array[String] = []
	for m in script.get_script_method_list():
		var nome: String = m["name"]
		if nome.begins_with("test_") and not nome in nomes:
			nomes.append(nome)
	nomes.sort()
	return nomes
