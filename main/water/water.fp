#define mulscale 2.5
#define height 0.3
#define tide 0.3
#define foamthickness 0.1
#define timescale 0.45
#define FOAM_COL vec4(0.8125, 0.9609, 0.9648, 0.5)

#define OCTAVE 3

varying mediump vec2 var_texcoord0;

uniform lowp vec4 time;

float rand(vec2 coords) {
	return fract(sin(dot(coords, vec2(23.53, 44.0))) * 60.45);
}

float perlin(vec2 coords) {
	vec2 i = floor(coords);
	vec2 f = fract(coords);
	vec2 u = smoothstep(0.0, 1.0, f);

	float a = rand(i);
	float b = rand(i + vec2(1.0, 0.0));
	float c = rand(i + vec2(0.0, 1.0));
	float d = rand(i + vec2(1.0, 1.0));

	return mix(mix(a, b, u.x), mix(c, d, u.x), u.y);
}

float fbm(vec2 coords) {
	float value = 0.0;
	float scale = 0.5;

	for (int i = 0; i < OCTAVE; i++) {
		value += perlin(coords) * scale;
		coords *= 2.0;
		scale *= 0.5;
	}
	return value;
}

void main() {
	vec2 UV = var_texcoord0;
	float newtime = time.x * timescale + 0.25;

	float fbmval = fbm(vec2(
		UV.x * mulscale + 0.2 * sin(0.3 * newtime) + 0.15 * newtime,
		-0.05 * newtime + UV.y * mulscale + 0.1 * cos(0.68 * newtime)
	));

	float myheight = height + tide * sin(newtime + 5.0 * UV.x - 8.0 * UV.y);
	float withinFoam = step(myheight, fbmval) * step(fbmval, myheight + foamthickness);

	vec4 color = withinFoam * FOAM_COL;

	gl_FragColor = color;
}
