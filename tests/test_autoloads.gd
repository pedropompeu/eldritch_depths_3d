extends TestCase
## T05: busca de autoload por nome, que substitui `Engine.has_singleton` (achado A01).


func test_get_autoload(tree: SceneTree) -> void:
	var autoloads := tree.root.get_node_or_null("Autoloads")
	assert_true(autoloads != null, "o autoload Autoloads deveria estar em /root")
	if autoloads == null:
		return
	assert_true(autoloads.get_autoload(&"Autoloads") != null, "deveria achar o próprio Autoloads")
	assert_true(autoloads.get_autoload(&"Inexistente") == null, "autoload inexistente deveria dar null")
