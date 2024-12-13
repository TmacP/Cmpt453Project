#define mulscale 5.0
#define height 0.6
#define tide 0.1
#define foamthickness 0.1
#define timescale 1.0
#define WATER_COL vec4(0.04, 0.38, 0.88, 0.0)
#define WATER2_COL vec4(0.04, 0.35, 0.78, 0.5)
#define FOAM_COL vec4(0.8125, 0.9609, 0.9648, 0.3)

#define OCTAVE 6

// texture coordinates that are set in the vertex shader
varying mediump vec2 var_texcoord0;

// time uniform that is altered by script
uniform lowp vec4 time;

float rand(vec2 coords) {
	return fract(sin(dot(coords, vec2(23.53, 44.0))) * 42350.45);
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
	float time = time.x * timescale + 0.25;
	float fbmval = fbm(vec2(UV.x * mulscale + 0.2 * sin(0.3 * time) + 0.15 * time, -0.05 * time + UV.y * mulscale + 0.1 * cos(0.68 * time)));
	float fbmvalshadow = fbm(vec2(UV.x * mulscale + 0.2 * sin(-0.6 * time + 25.0 * UV.y) + 0.15 * time + 3.0, -0.05 * time + UV.y * mulscale + 0.13 * cos(-0.68 * time)) - 7.0 + 0.1 * sin(0.43 * time));
	float myheight = height + tide * sin(time + 5.0 * UV.x - 8.0 * UV.y);
	float shadowheight = height + tide * 1.3 * cos(time + 2.0 * UV.x - 2.0 * UV.y);
	float withinFoam = step(myheight, fbmval) * step(fbmval, myheight + foamthickness);
	float shadow = (1.0 - withinFoam) * step(shadowheight, fbmvalshadow) * step(fbmvalshadow, shadowheight + foamthickness * 0.7);
	vec4 color = withinFoam * FOAM_COL + shadow * WATER2_COL + ((1.0 - withinFoam) * (1.0 - shadow)) * WATER_COL;
	gl_FragColor = color;
}
