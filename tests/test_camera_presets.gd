extends TestCase
## T13: enquadramentos "atual" (herói em 1/13 da tela) e "próxima" (1/8), com F7.

const CENA := "res://scenes/camera/camera_rig_3d.tscn"


func _rig(tree: SceneTree) -> CameraRig3D:
	var rig: CameraRig3D = load(CENA).instantiate()
	tree.root.add_child(rig)
	return rig


func test_preset_inicial(tree: SceneTree) -> void:
	var rig := _rig(tree)
	assert_eq(rig.preset, CameraRig3D.Preset.ATUAL)
	for i in 300:
		rig.step(1.0 / 60)
	assert_near(rig.distance, 32.15, 0.05)
	rig.queue_free()


func test_troca_suave(tree: SceneTree) -> void:
	var rig := _rig(tree)
	rig.set_preset(CameraRig3D.Preset.PROXIMA)
	rig.step(1.0 / 60)
	assert_true(rig.distance > 19.78 and rig.distance < 32.15, "deveria estar no meio da troca: %s" % rig.distance)
	for i in 300:
		rig.step(1.0 / 60)
	assert_near(rig.distance, 19.78, 0.05)
	rig.queue_free()


func test_toggle(tree: SceneTree) -> void:
	var rig := _rig(tree)
	rig.toggle_preset()
	assert_eq(rig.preset, CameraRig3D.Preset.PROXIMA)
	rig.toggle_preset()
	assert_eq(rig.preset, CameraRig3D.Preset.ATUAL)
	rig.queue_free()


func test_f7_alterna(tree: SceneTree) -> void:
	var rig := _rig(tree)
	var ev := InputEventAction.new()
	ev.action = &"debug_camera_preset"
	ev.pressed = true
	rig._unhandled_input(ev)
	assert_eq(rig.preset, CameraRig3D.Preset.PROXIMA)
	rig.queue_free()
