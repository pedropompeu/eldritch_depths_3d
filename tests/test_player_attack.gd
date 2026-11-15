extends TestCase
## T18: ataque em dois golpes — vigor, um acerto por golpe, combo na
## recuperação e travada de frame. Cada teste monta piso, rig, herói e uma
## hurtbox de inimigo (time 1) a 1 m à frente do herói.

const CENA := "res://scenes/player/player_3d.tscn"
const CENA_RIG := "res://scenes/camera/camera_rig_3d.tscn"
const InputModeScript := preload("res://scripts/core/input_mode.gd")
const PASSO := 1.0 / 60.0

var _modo_antes: int


## Devolve [raiz, herói, entrada, contagem]. No modo PAD sem analógico e sem
## movimento, a mira fica em `Vector3.FORWARD` (-Z), onde está a hurtbox.
func _montar(tree: SceneTree) -> Array:
	var modo: Node = Autoloads.get_autoload(&"InputMode")
	_modo_antes = modo.mode
	modo.mode = InputModeScript.Mode.PAD

	var raiz := Node3D.new()
	var piso := StaticBody3D.new()
	var forma := CollisionShape3D.new()
	var caixa := BoxShape3D.new()
	caixa.size = Vector3(40, 1, 40)
	forma.shape = caixa
	forma.position = Vector3(0, -0.5, 0)
	piso.add_child(forma)
	raiz.add_child(piso)

	var alvo := Hurtbox3D.new()
	alvo.team = 1
	var forma_alvo := CollisionShape3D.new()
	var esfera := SphereShape3D.new()
	esfera.radius = 0.5
	forma_alvo.shape = esfera
	alvo.add_child(forma_alvo)
	alvo.position = Vector3(0, 0.9, -1.0)
	raiz.add_child(alvo)
	var contagem := {hurt = 0}
	alvo.hurt.connect(func(_h): contagem.hurt += 1)

	var rig: CameraRig3D = load(CENA_RIG).instantiate()
	var heroi: Player3D = load(CENA).instantiate()
	heroi.camera_rig = rig
	var entrada := {move = Vector2.ZERO, attack = false}
	heroi.input_source = func(): return entrada
	rig.target = heroi
	raiz.add_child(heroi)
	raiz.add_child(rig)
	tree.root.add_child(raiz)
	heroi.set_physics_process(false)
	await tree.physics_frame
	await tree.physics_frame
	return [raiz, heroi, entrada, contagem]


func _desmontar(m: Array) -> void:
	Autoloads.get_autoload(&"InputMode").mode = _modo_antes
	m[0].queue_free()


func _apertar_ataque(heroi: Player3D, entrada: Dictionary) -> void:
	entrada.attack = true
	heroi.step(PASSO)
	entrada.attack = false


func _passos(heroi: Player3D, segundos: float) -> void:
	for i in roundi(segundos / PASSO):
		heroi.step(PASSO)


func test_ataque_gasta_vigor_e_acerta_uma_vez(tree: SceneTree) -> void:
	var m: Array = await _montar(tree)
	var heroi: Player3D = m[1]
	_apertar_ataque(heroi, m[2])
	assert_eq(heroi.state_machine.current_state.name, &"Attack")
	assert_near(heroi.stats.current_stamina, 82.0, 0.001)
	_passos(heroi, 0.4)
	assert_eq(m[3].hurt, 1, "um golpe acerta uma vez")
	assert_false(heroi.sword.active, "a espada desliga ao sair da fase ativa")
	_passos(heroi, 0.1)
	assert_eq(heroi.state_machine.current_state.name, &"Idle")
	_desmontar(m)


func test_combo_segundo_golpe(tree: SceneTree) -> void:
	var m: Array = await _montar(tree)
	var heroi: Player3D = m[1]
	_apertar_ataque(heroi, m[2])
	# Até a recuperação do golpe 1 (começa em 0,26 s).
	_passos(heroi, 0.3)
	assert_eq(m[3].hurt, 1)
	_apertar_ataque(heroi, m[2])
	assert_near(heroi.stats.current_stamina, 60.0, 0.001, "18 + 22 de vigor")
	_passos(heroi, 0.45)
	assert_eq(m[3].hurt, 2, "o segundo golpe acerta de novo")
	_desmontar(m)


func test_ataque_com_travada(tree: SceneTree) -> void:
	var m: Array = await _montar(tree)
	var heroi: Player3D = m[1]
	_apertar_ataque(heroi, m[2])
	heroi.step(0.3)
	assert_eq(m[3].hurt, 1, "a travada não pula a fase ativa")
	assert_false(heroi.sword.active)
	_desmontar(m)


func test_sem_vigor_nao_ataca(tree: SceneTree) -> void:
	var m: Array = await _montar(tree)
	var heroi: Player3D = m[1]
	heroi.stats.current_stamina = 10.0
	_apertar_ataque(heroi, m[2])
	assert_eq(heroi.state_machine.current_state.name, &"Idle")
	assert_near(heroi.stats.current_stamina, 10.0, 0.001)
	_passos(heroi, 0.4)
	assert_eq(m[3].hurt, 0)
	_desmontar(m)
