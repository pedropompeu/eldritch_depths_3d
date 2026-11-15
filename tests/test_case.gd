class_name TestCase
extends RefCounted
## Base dos testes. Uma falha entra em `failures` e não aborta o teste.

var failures: Array[String] = []


func assert_eq(a, b, msg := "") -> void:
	if not (typeof(a) == typeof(b) and a == b) and not _numeros_iguais(a, b):
		_falha("esperado %s, veio %s" % [str(b), str(a)], msg)


func assert_near(a: float, b: float, eps := 0.001, msg := "") -> void:
	if is_nan(a) or is_nan(b) or absf(a - b) > eps:
		_falha("esperado %s ± %s, veio %s" % [str(b), str(eps), str(a)], msg)


func assert_true(c: bool, msg := "") -> void:
	if not c:
		_falha("esperado verdadeiro", msg)


func assert_false(c: bool, msg := "") -> void:
	if c:
		_falha("esperado falso", msg)


func assert_vec_near(a: Vector3, b: Vector3, eps := 0.001, msg := "") -> void:
	var ok := not (is_nan(a.x) or is_nan(a.y) or is_nan(a.z)) and a.distance_to(b) <= eps
	if not ok:
		_falha("esperado %s ± %s, veio %s" % [str(b), str(eps), str(a)], msg)


## int e float com o mesmo valor contam como iguais (ex.: 2 e 2.0).
func _numeros_iguais(a, b) -> bool:
	var num := [TYPE_INT, TYPE_FLOAT]
	return typeof(a) in num and typeof(b) in num and float(a) == float(b)


func _falha(detalhe: String, msg: String) -> void:
	failures.append(detalhe if msg.is_empty() else "%s (%s)" % [msg, detalhe])
