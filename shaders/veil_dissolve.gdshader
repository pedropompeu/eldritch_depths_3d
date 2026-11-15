shader_type spatial;
render_mode cull_disabled;
// Parede do Véu: some em manchas de ruído conforme `dissolve` vai de 0 a 1,
// com borda violeta acesa no recorte. Brilho fraco próprio, para ser vista no
// escuro.

uniform float dissolve : hint_range(0.0, 1.0) = 0.0;
uniform vec4 albedo : source_color = vec4(0.16, 0.1, 0.22, 1.0);
uniform vec4 edge_color : source_color = vec4(0.62, 0.35, 1.0, 1.0);
uniform float edge_width = 0.08;
uniform float glow = 0.25;

varying vec3 local_pos;

float hash(vec3 p) {
	p = fract(p * 0.3183099 + 0.1);
	p *= 17.0;
	return fract(p.x * p.y * p.z * (p.x + p.y + p.z));
}

float value_noise(vec3 x) {
	vec3 i = floor(x);
	vec3 f = fract(x);
	f = f * f * (3.0 - 2.0 * f);
	return mix(
		mix(mix(hash(i + vec3(0, 0, 0)), hash(i + vec3(1, 0, 0)), f.x),
			mix(hash(i + vec3(0, 1, 0)), hash(i + vec3(1, 1, 0)), f.x), f.y),
		mix(mix(hash(i + vec3(0, 0, 1)), hash(i + vec3(1, 0, 1)), f.x),
			mix(hash(i + vec3(0, 1, 1)), hash(i + vec3(1, 1, 1)), f.x), f.y),
		f.z);
}

void vertex() {
	local_pos = VERTEX;
}

void fragment() {
	float n = value_noise(local_pos * 2.5) * 0.7 + value_noise(local_pos * 7.0) * 0.3;
	// Em 1 tudo some, inclusive o ruído máximo.
	if (n < dissolve * 1.001) {
		discard;
	}
	float edge = 1.0 - smoothstep(0.0, edge_width, n - dissolve);
	ALBEDO = albedo.rgb;
	ROUGHNESS = 0.6;
	EMISSION = albedo.rgb * glow + edge_color.rgb * edge * step(0.001, dissolve) * 3.0;
}
