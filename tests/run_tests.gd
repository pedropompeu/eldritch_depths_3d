extends SceneTree
## Runner caseiro: roda todo método `test_*` de cada `res://tests/test_*.gd`, em ordem alfabética.
## Uso: godot --headless --path . -s res://tests/run_tests.gd

const TEST_DIR := "res://tests"


## Captura erros da engine (erro de script, push_error, erro de shader) durante cada teste.
## Sem isso, um teste que quebra no meio é abortado em silêncio e conta como aprovado.
## Avisos (push_warning) não contam.
class ErrorCatcher extends Logger:
	var _mutex := Mutex.new()
	var _erros: Array[String] = []

	func _log_error(function: String, file: String, line: int, code: String, rationale: String,
			_editor_notify: bool, error_type: int, _script_backtraces: Array[ScriptBacktrace]) -> void:
		if error_type == ERROR_TYPE_WARNING:
			return
		var texto := rationale if not rationale.is_empty() else code
		_mutex.lock()
		_erros.append("erro da engine em %s:%d (%s): %s" % [file, line, function, texto])
		_mutex.unlock()

	func _log_message(_message: String, _error: bool) -> void:
		pass

	func take() -> Array[String]:
		_mutex.lock()
		var r := _erros.duplicate()
		_erros.clear()
		_mutex.unlock()
		return r

## Um teste que passa disto (travado num await ou abortado por erro) reprova a suíte inteira.
const TEST_TIMEOUT_MS := 30000

var _catcher := ErrorCatcher.new()
var _teste_atual := ""
var _inicio_teste_ms := 0
var _terminou := false


## Vigia: se o teste atual estourar o tempo, reprova e sai em vez de travar.
func _process(_delta: float) -> bool:
	if _terminou or _teste_atual.is_empty():
		return false
	if Time.get_ticks_msec() - _inicio_teste_ms > TEST_TIMEOUT_MS:
		for msg in _catcher.take():
			print("FAIL %s: %s" % [_teste_atual, msg])
		print("FAIL %s: passou de %d s (travou num await ou abortou por erro)" % [_teste_atual, TEST_TIMEOUT_MS / 1000])
		print("FALHOU: suíte interrompida")
		_terminou = true
		quit(1)
	return false


func _initialize() -> void:
	_run()


func _run() -> void:
	OS.add_logger(_catcher)
	await process_frame
	var total := 0
	var falhas := 0
	var arquivos := Array(DirAccess.get_files_at(TEST_DIR)).filter(
		func(f: String) -> bool: return f.begins_with("test_") and f.ends_with(".gd") and f != "test_case.gd"
	)
	arquivos.sort()
	for arquivo in arquivos:
		var script: Script = load(TEST_DIR.path_join(arquivo))
		if script == null or not script.can_instantiate():
			print("FAIL %s::<carga>: script não carregou (erro de sintaxe?)" % arquivo)
			total += 1
			falhas += 1
			continue
		var obj = script.new()
		for metodo in _metodos_de_teste(script):
			total += 1
			obj.failures.clear()
			_catcher.take()
			_teste_atual = "%s::%s" % [arquivo, metodo]
			_inicio_teste_ms = Time.get_ticks_msec()
			if obj.get_method_argument_count(metodo) == 1:
				await obj.call(metodo, self)
			else:
				await obj.call(metodo)
			obj.failures.append_array(_catcher.take())
			if not obj.failures.is_empty():
				falhas += 1
				for msg in obj.failures:
					print("FAIL %s::%s: %s" % [arquivo, metodo, msg])
	_teste_atual = ""
	_terminou = true
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
