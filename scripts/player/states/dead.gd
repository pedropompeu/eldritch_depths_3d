extends State
## Morto: parado para sempre. Não sai deste estado por nenhuma entrada; quem
## reinicia a cena é o jogo.


func enter() -> void:
	actor.sword.deactivate()
	actor.velocity.x = 0.0
	actor.velocity.z = 0.0


func process_physics(_delta: float) -> void:
	actor.velocity.x = 0.0
	actor.velocity.z = 0.0
