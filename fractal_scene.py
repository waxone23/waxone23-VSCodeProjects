import moderngl
import numpy as np
import subprocess
import shlex

# Innstillinger
WIDTH, HEIGHT = 1920, 1080  # Full HD Landscape
FPS = 30
SECONDS = 4  # En 4-sekunders loop
TOTAL_FRAMES = FPS * SECONDS

# Shader-koden (Psychedelic Fractal)
VERTEX_SHADER = """
#version 330
in vec2 in_vert;
void main() {
    gl_Position = vec4(in_vert, 0.0, 1.0);
}
"""

FRAGMENT_SHADER = """
#version 330
out vec4 f_color;
uniform float time;
uniform vec2 resolution;

void main() {
    vec2 uv = (gl_FragCoord.xy * 2.0 - resolution.xy) / min(resolution.y, resolution.x);
    
    // Kamera-bevegelse i fraktal-rommet
    vec3 ro = vec3(0.0, 0.0, -2.0 + sin(time * 0.5) * 0.5);
    vec3 rd = normalize(vec3(uv, 1.2));
    
    float t = 0.0;
    for(int i = 0; i < 50; i++) {
        vec3 p = ro + rd * t;
        // Den "smeltende" logikken
        p = abs(mod(p - 1.0, 2.0) - 1.0);
        float d = length(p.xy) - 0.3 + sin(p.z + time) * 0.1;
        if(d < 0.001) break;
        t += d * 0.5;
    }
    
    // Farge-skift (70s cinematic palette inspirasjon)
    vec3 col = 0.5 + 0.5 * cos(time + t + vec3(0, 2, 4));
    f_color = vec4(col * exp(-0.2 * t), 1.0);
}
"""


def render_to_mp4():
    # Opprett ModernGL context (headless)
    ctx = moderngl.create_standalone_context()
    prog = ctx.program(vertex_shader=VERTEX_SHADER, fragment_shader=FRAGMENT_SHADER)

    # Framebuffer
    fbo = ctx.framebuffer(color_attachments=[ctx.texture((WIDTH, HEIGHT), 4)])
    fbo.use()

    # Fullskjerm quad
    vertices = np.array([-1.0, -1.0, 1.0, -1.0, -1.0, 1.0, 1.0, 1.0], dtype="f4")
    vbo = ctx.buffer(vertices)
    vao = ctx.vertex_array(prog, [(vbo, "2f", "in_vert")])

    # FFMPEG Command
    output_file = "wax_fractal_loop.mp4"
    cmd = (
        f"ffmpeg -y -f rawvideo -pix_fmt rgba -s {WIDTH}x{HEIGHT} -r {FPS} "
        f"-i - -c:v libx264 -pix_fmt yuv420p -preset fast {output_file}"
    )
    process = subprocess.Popen(shlex.split(cmd), stdin=subprocess.PIPE)

    print(f"🎬 Starter rendering av {output_file}...")

    for i in range(TOTAL_FRAMES):
        prog["time"].value = i / FPS
        prog["resolution"].value = (WIDTH, HEIGHT)

        vao.render(moderngl.TRIANGLE_STRIP)

        # Les rådata og send direkte til FFMPEG pipe
        data = fbo.read(components=4)
        # Vi må flippe bildet vertikalt for ModernGL -> FFMPEG
        img_array = np.frombuffer(data, dtype=np.uint8).reshape(HEIGHT, WIDTH, 4)
        process.stdin.write(np.flipud(img_array).tobytes())

        if i % 10 == 0:
            print(f"Frame {i}/{TOTAL_FRAMES} ferdig...")

    process.stdin.close()
    process.wait()
    print(f"✅ Ferdig! Video lagret som {output_file}")


if __name__ == "__main__":
    render_to_mp4()
