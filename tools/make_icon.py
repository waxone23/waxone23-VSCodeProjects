"""Generate the app icon (PNG, ICO, ICNS). Needs Pillow: python tools/make_icon.py"""

from pathlib import Path

from PIL import Image, ImageChops, ImageDraw, ImageFilter

SIZE = 1024
SS = 2  # supersampling for smooth edges
OUT = Path(__file__).resolve().parent.parent / "assets"
BAR_COLORS = ["#ff5d73", "#ffb347", "#5dd39e", "#5db0ff"]  # same as the level meters
BAR_HEIGHTS = [0.52, 0.86, 0.40, 0.68]


def vertical_gradient(size: int, top: tuple, bottom: tuple) -> Image.Image:
    img = Image.new("RGB", (size, size))
    px = img.load()
    for y in range(size):
        t = y / (size - 1)
        color = tuple(int(top[i] + (bottom[i] - top[i]) * t) for i in range(3))
        for x in range(size):
            px[x, y] = color
    return img


def build() -> Image.Image:
    s = SIZE * SS
    margin = int(s * 0.055)
    radius = int(s * 0.225)

    # background: dark gradient squircle-ish rounded square
    bg = vertical_gradient(s, (40, 40, 52), (16, 16, 21)).convert("RGBA")
    mask = Image.new("L", (s, s), 0)
    ImageDraw.Draw(mask).rounded_rectangle((margin, margin, s - margin, s - margin), radius, fill=255)
    canvas = Image.new("RGBA", (s, s), (0, 0, 0, 0))
    canvas.paste(bg, (0, 0), mask)

    # soft inner rim
    rim = Image.new("RGBA", (s, s), (0, 0, 0, 0))
    ImageDraw.Draw(rim).rounded_rectangle(
        (margin, margin, s - margin, s - margin), radius, outline=(255, 255, 255, 34), width=int(s * 0.004)
    )
    canvas = Image.alpha_composite(canvas, rim)

    # equalizer bars
    inner = s - 2 * margin
    bar_w = int(inner * 0.125)
    gap = int(inner * 0.06)
    total = 4 * bar_w + 3 * gap
    x0 = margin + (inner - total) // 2
    baseline = margin + int(inner * 0.73)
    max_h = int(inner * 0.56)

    glow = Image.new("RGBA", (s, s), (0, 0, 0, 0))
    bars = Image.new("RGBA", (s, s), (0, 0, 0, 0))
    gd, bd = ImageDraw.Draw(glow), ImageDraw.Draw(bars)
    for i, (color, h) in enumerate(zip(BAR_COLORS, BAR_HEIGHTS)):
        x = x0 + i * (bar_w + gap)
        top = baseline - int(max_h * h)
        box = (x, top, x + bar_w, baseline)
        gd.rounded_rectangle(box, bar_w // 2, fill=color)
        bd.rounded_rectangle(box, bar_w // 2, fill=color)

    glow = glow.filter(ImageFilter.GaussianBlur(s * 0.022))
    glow.putalpha(glow.getchannel("A").point(lambda a: int(a * 0.55)))

    # thin baseline under the bars
    line_y = baseline + int(inner * 0.045)
    ImageDraw.Draw(bars).rounded_rectangle(
        (x0, line_y, x0 + total, line_y + int(inner * 0.008)), int(inner * 0.004), fill=(255, 255, 255, 46)
    )

    # clip everything to the rounded square
    layers = Image.alpha_composite(glow, bars)
    layers.putalpha(ImageChops.multiply(layers.getchannel("A"), mask))
    canvas = Image.alpha_composite(canvas, layers)
    return canvas.resize((SIZE, SIZE), Image.LANCZOS)


if __name__ == "__main__":
    OUT.mkdir(exist_ok=True)
    icon = build()
    icon.save(OUT / "icon.png")
    icon.save(OUT / "icon.ico", sizes=[(16, 16), (24, 24), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)])
    icon.save(OUT / "icon.icns")
    print("wrote", sorted(p.name for p in OUT.iterdir()))
