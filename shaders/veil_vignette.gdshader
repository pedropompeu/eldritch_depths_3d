shader_type canvas_item;
// Vinheta da sanidade: borda escura arroxeada que se fecha conforme
// `intensity` sobe. Em 0 é totalmente transparente; em 1 o centro limpo ainda
// mede 0,35 da meia-diagonal da tela.

uniform float intensity : hint_range(0.0, 1.0) = 0.0;
uniform vec4 tint : source_color = vec4(0.102, 0.059, 0.141, 1.0);

// Raio limpo (fração da meia-diagonal) com a intensidade máxima.
const float MIN_INNER = 0.35;
// Largura da transição do limpo até a cor cheia.
const float FEATHER = 0.45;

void fragment() {
	float aspect = SCREEN_PIXEL_SIZE.y / SCREEN_PIXEL_SIZE.x;
	vec2 d = (UV - 0.5) * vec2(aspect, 1.0);
	// 0 no centro, 1 no canto.
	float r = length(d) / length(vec2(aspect, 1.0) * 0.5);
	float inner = mix(1.0, MIN_INNER, intensity);
	float a = smoothstep(inner, inner + FEATHER, r);
	COLOR = vec4(tint.rgb, a * mix(0.35, 1.0, intensity) * step(0.0001, intensity));
}
