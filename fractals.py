import pygame
import moderngl
import numpy as np
import time

# Shader source (GLSL) - This is where the magic happens
VERTEX_SHADER = """
#version 330
in vec2 in_vert;
out vec2 uv;
void main() {
    gl_Position = vec4(in_vert, 0.0, 1.0);
    uv = in_vert;
}
"""

FRAGMENT_SHADER = """
#version 330
out vec4 f_color;
in vec2 uv;
uniform float time;
uniform vec2 resolution;

// Fractal formula (Mandelbox-inspired)
float map(vec3 p) {
    p.xz *= mat2(cos(time*0.1), sin(time*0.1), -sin(time*0.1), cos(time*0.1));
    p.xy *= mat2(cos(time*0.15), sin(time*0.15), -sin(time*0.15), cos(time*0.15));
    
    vec3 q = p;
    float scale = 2.5;
    for (int i = 0; i < 8; i++) {
        p = abs(p) - vec3(0.5, 1.2, 0.5);
        float r2 = dot(p, p);
        if (r2 < 0.5) p *= 2.0;
        else if (r2 < 1.0) p /= r2;
        p = p * scale + q;
    }
    return length(p) * pow(scale, -8.0);
}

void main() {
    vec2 p = uv * resolution.y / resolution.x;
    vec3 ro = vec3(0.0, 0.0, -3.0 + sin(time * 0.2)); // Camera position
    vec3 rd = normalize(vec3(p, 1.5)); // Ray direction
    
    float t = 0.0;
    for (int i = 0; i < 64; i++) {
        float d = map(ro + rd * t);
        if (d < 0.001 || t > 10.0) break;
        t += d;
    }
    
    vec3 col = vec3(0.0);
    if (t < 10.0) {
        float edge = 1.0 - (float(t) / 10.0);
        // Psychedelic color shifting
        col = 0.5 + 0.5 * cos(time + t + vec3(0, 2, 4));
        col *= edge;
    }
    
    f_color = vec4(col, 1.0);
}
"""


def main():
    pygame.init()
    screen_size = (1080, 1920)  # Vertical for mobile/SoMe
    pygame.display.set_mode(screen_size, pygame.OPENGL | pygame.DOUBLEBUF)
    ctx = moderngl.create_context()

    prog = ctx.program(vertex_shader=VERTEX_SHADER, fragment_shader=FRAGMENT_SHADER)

    vertices = np.array([-1.0, -1.0, 1.0, -1.0, -1.0, 1.0, 1.0, 1.0], dtype="f4")
    vbo = ctx.buffer(vertices)
    vao = ctx.vertex_array(prog, [(vbo, "2f", "in_vert")])

    clock = pygame.time.Clock()
    start_time = time.time()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        current_time = time.time() - start_time

        ctx.clear(0, 0, 0)
        prog["time"].value = current_time
        prog["resolution"].value = screen_size

        vao.render(moderngl.TRIANGLE_STRIP)
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()
