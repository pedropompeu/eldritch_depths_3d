class_name Veil
extends RefCounted
## O Véu: a sanidade vista como percepção da realidade. Quanto mais fino o Véu,
## mais o herói enxerga. Limites provisórios (60 e 30); o efeito de cada faixa
## segue em aberto com Pedro (spec §9).

enum Band { CLARO, FINO, RASGADO }

const THRESHOLD_FINO := 60.0
const THRESHOLD_RASGADO := 30.0


## Faixa do Véu para a sanidade dada: CLARO ≥ 60, FINO ≥ 30, RASGADO abaixo.
static func band_for(sanity: float) -> Band:
	if sanity >= THRESHOLD_FINO:
		return Band.CLARO
	if sanity >= THRESHOLD_RASGADO:
		return Band.FINO
	return Band.RASGADO
