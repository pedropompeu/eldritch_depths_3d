extends TestCase
## T15: hitbox e hurtbox 3D. A hitbox acerta na própria chamada de `activate`
## quem já está sobreposto, e cada hurtbox no máximo uma vez por ativação.


func _caixa(area: Area3D, team: int) -> Area3D:
	area.team = team
	var forma := CollisionShape3D.new()
	var esfera := SphereShape3D.new()
	esfera.radius = 0.5
	forma.shape = esfera
	area.add_child(forma)
	return area


## Monta hitbox e hurtbox no mesmo lugar e devolve [raiz, hitbox, hurtbox, contagem].
func _montar(tree: SceneTree, team_hit: int, team_hurt: int) -> Array:
	var raiz := Node3D.new()
	var hit: Hitbox3D = _caixa(Hitbox3D.new(), team_hit)
	var hurt: Hurtbox3D = _caixa(Hurtbox3D.new(), team_hurt)
	raiz.add_child(hit)
	raiz.add_child(hurt)
	tree.root.add_child(raiz)
	var contagem := {hurt = 0}
	hurt.hurt.connect(func(_h): contagem.hurt += 1)
	await tree.physics_frame
	await tree.physics_frame
	return [raiz, hit, hurt, contagem]


func test_acerta_ao_ativar_sobreposto(tree: SceneTree) -> void:
	var m: Array = await _montar(tree, 0, 1)
	var landed := []
	m[1].hit_landed.connect(func(h): landed.append(h))
	m[1].activate()
	assert_eq(m[3].hurt, 1, "deveria acertar na mesma chamada, sem esperar frame")
	assert_eq(landed.size(), 1)
	m[0].queue_free()


func test_uma_vez_por_ativacao(tree: SceneTree) -> void:
	var m: Array = await _montar(tree, 0, 1)
	m[1].activate()
	for i in 5:
		await tree.physics_frame
	assert_eq(m[3].hurt, 1)
	m[0].queue_free()


func test_reativar_acerta_de_novo(tree: SceneTree) -> void:
	var m: Array = await _montar(tree, 0, 1)
	m[1].activate()
	m[1].deactivate()
	m[1].activate()
	assert_eq(m[3].hurt, 2)
	m[0].queue_free()


func test_mesmo_time_nao_acerta(tree: SceneTree) -> void:
	var m: Array = await _montar(tree, 0, 0)
	m[1].activate()
	await tree.physics_frame
	await tree.physics_frame
	assert_eq(m[3].hurt, 0)
	m[0].queue_free()


func test_invulneravel(tree: SceneTree) -> void:
	var m: Array = await _montar(tree, 0, 1)
	m[2].invulnerable = true
	m[1].activate()
	await tree.physics_frame
	await tree.physics_frame
	assert_eq(m[3].hurt, 0)
	m[0].queue_free()


func test_inimigo_acerta_heroi(tree: SceneTree) -> void:
	var m: Array = await _montar(tree, 1, 0)
	m[1].activate()
	assert_eq(m[3].hurt, 1)
	m[0].queue_free()


func test_entra_durante_ativacao(tree: SceneTree) -> void:
	var m: Array = await _montar(tree, 0, 1)
	m[2].position = Vector3(5, 0, 0)
	await tree.physics_frame
	await tree.physics_frame
	m[1].activate()
	assert_eq(m[3].hurt, 0, "longe não acerta")
	m[2].position = Vector3.ZERO
	for i in 3:
		await tree.physics_frame
	assert_eq(m[3].hurt, 1, "deveria acertar ao entrar com a hitbox ativa")
	m[0].queue_free()


func test_inativa_nao_acerta_quem_entra(tree: SceneTree) -> void:
	var m: Array = await _montar(tree, 0, 1)
	m[2].position = Vector3(5, 0, 0)
	await tree.physics_frame
	await tree.physics_frame
	m[2].position = Vector3.ZERO
	for i in 3:
		await tree.physics_frame
	assert_eq(m[3].hurt, 0)
	m[0].queue_free()
