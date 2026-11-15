extends TestCase
## T28: rótulos de botão por dispositivo (texto, sem ícones neste bloco).


func test_frasco_de_sangue() -> void:
	assert_eq(InputPrompt.label_for(&"use_blood_flask", false), "1")
	assert_eq(InputPrompt.label_for(&"use_blood_flask", true), "↓")


func test_laudano() -> void:
	assert_eq(InputPrompt.label_for(&"use_laudanum", false), "2")
	assert_eq(InputPrompt.label_for(&"use_laudanum", true), "↑")


func test_interagir() -> void:
	assert_eq(InputPrompt.label_for(&"interact", false), "E")
	assert_eq(InputPrompt.label_for(&"interact", true), "B")


func test_outra_acao() -> void:
	assert_eq(InputPrompt.label_for(&"attack", false), "")
	assert_eq(InputPrompt.label_for(&"attack", true), "")
	assert_eq(InputPrompt.label_for(&"nao_existe", true), "")
