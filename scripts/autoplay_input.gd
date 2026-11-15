extends RefCounted
## Entrada automática para medir desempenho sem ninguém no controle: anda em
## círculo, ataca e esquiva em pulsos regulares. Só depende do relógio.

const MOVE_PERIOD := 4.0
const ATTACK_PERIOD := 0.8
const ROLL_PERIOD := 3.0
## A esquiva fica defasada em meio período para não cair junto com o ataque.
const ROLL_OFFSET := 1.5
## Quanto tempo cada pulso fica apertado (pega pelo menos um passo a 60 Hz).
const PULSE := 0.05


## `Callable` de entrada no formato de `Player3D.input_source`, com o tempo
## contado a partir de `start_ms` (em `Time.get_ticks_msec()`).
static func make(start_ms: int) -> Callable:
	return func() -> Dictionary:
		var t := (Time.get_ticks_msec() - start_ms) / 1000.0
		var angulo := TAU * t / MOVE_PERIOD
		return {
			move = Vector2(cos(angulo), sin(angulo)),
			attack = fmod(t, ATTACK_PERIOD) < PULSE,
			roll = fmod(t + ROLL_OFFSET, ROLL_PERIOD) < PULSE,
		}
