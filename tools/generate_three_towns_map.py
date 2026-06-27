from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "assets" / "images" / "wuhan-three-towns-map.png"
BG = ROOT / "assets" / "images" / "wuhan-three-towns-ink-bg.png"

W, H = 1600, 1120
PAD_X, PAD_Y = 120, 120
LON_MIN, LON_MAX = 114.18, 114.43
LAT_MIN, LAT_MAX = 30.47, 30.64

COLORS = {
    "bg": (248, 242, 232),
    "paper": (255, 250, 243),
    "ink": (31, 47, 53),
    "muted": (92, 108, 104),
    "line": (226, 211, 190),
    "river": (54, 128, 154),
    "river_light": (138, 192, 204),
    "gold": (204, 148, 66),
    "red": (169, 72, 56),
    "hankou": (245, 229, 210),
    "wuchang": (232, 238, 217),
    "hanyang": (235, 226, 210),
}


def font(size, bold=False):
    candidates = [
        r"C:\Windows\Fonts\msyhbd.ttc" if bold else r"C:\Windows\Fonts\msyh.ttc",
        r"C:\Windows\Fonts\simhei.ttf",
        r"C:\Windows\Fonts\simsun.ttc",
    ]
    for path in candidates:
        if Path(path).exists():
            return ImageFont.truetype(path, size)
    return ImageFont.load_default()


F_TITLE = font(52, True)
F_SUB = font(28)
F_LABEL = font(48, True)
F_SMALL = font(26)
F_TINY = font(22)


def xy(lon, lat):
    x = PAD_X + (lon - LON_MIN) / (LON_MAX - LON_MIN) * (W - PAD_X * 2)
    y = PAD_Y + (LAT_MAX - lat) / (LAT_MAX - LAT_MIN) * (H - PAD_Y * 2)
    return int(round(x)), int(round(y))


def draw_polyline(draw, points, width, fill):
    coords = [xy(lon, lat) for lon, lat in points]
    draw.line(coords, width=width, fill=fill, joint="curve")
    radius = width // 2
    for x, y in coords:
        draw.ellipse((x - radius, y - radius, x + radius, y + radius), fill=fill)


def zone(draw, box, title, subtitle, fill):
    draw.rounded_rectangle(box, radius=42, fill=fill + (172,), outline=(255, 250, 243, 125), width=2)


def small_landmark(draw, lon, lat, text, label_xy):
    x, y = xy(lon, lat)
    bx, by = label_xy
    draw.ellipse((x - 9, y - 9, x + 9, y + 9), fill=COLORS["red"], outline=COLORS["paper"], width=4)
    draw.line((x, y, bx, by + 15), fill=COLORS["red"], width=2)
    draw.rounded_rectangle((bx - 12, by - 8, bx + 190, by + 42), radius=14, fill=(255, 250, 243, 210), outline=COLORS["line"], width=1)
    draw.text((bx, by), text, font=F_TINY, fill=COLORS["ink"])


if BG.exists():
    img = Image.open(BG).convert("RGBA").resize((W, H))
    veil = Image.new("RGBA", (W, H), COLORS["bg"] + (102,))
    img = Image.alpha_composite(img, veil)
else:
    img = Image.new("RGBA", (W, H), COLORS["bg"] + (255,))
draw = ImageDraw.Draw(img, "RGBA")

draw.rounded_rectangle((78, 38, 1248, 164), radius=30, fill=(255, 250, 243, 188))
draw.text((106, 58), "武汉三镇格局位置图", font=F_TITLE, fill=COLORS["ink"])
draw.text((108, 124), "参考高德地图截图校正走向：长江自西南向东北，汉江自西北汇入。", font=F_SUB, fill=COLORS["muted"])

# Soft town areas, aligned to the real relation of the two rivers.
zone(draw, (138, 188, 735, 480), "汉口", "商埠 / 码头 / 租界 / 夜宵", COLORS["hankou"])
zone(draw, (116, 575, 665, 905), "汉阳", "知音 / 晴川 / 工业 / 汉阳造", COLORS["hanyang"])
zone(draw, (880, 315, 1458, 920), "武昌", "省城 / 首义 / 楚文化 / 东湖", COLORS["wuchang"])

# Rivers. Long river shape is simplified but projected from local control points.
draw_polyline(
    draw,
    [(114.255, 30.468), (114.265, 30.500), (114.277, 30.535), (114.289, 30.568), (114.315, 30.592), (114.355, 30.615), (114.425, 30.638)],
    86,
    COLORS["river_light"] + (232,),
)
draw_polyline(
    draw,
    [(114.255, 30.468), (114.265, 30.500), (114.277, 30.535), (114.289, 30.568), (114.315, 30.592), (114.355, 30.615), (114.425, 30.638)],
    52,
    COLORS["river"] + (238,),
)
draw_polyline(
    draw,
    [(114.185, 30.623), (114.215, 30.612), (114.245, 30.596), (114.289, 30.568)],
    54,
    COLORS["river_light"] + (226,),
)
draw_polyline(
    draw,
    [(114.185, 30.623), (114.215, 30.612), (114.245, 30.596), (114.289, 30.568)],
    32,
    COLORS["river"] + (238,),
)

draw.text(xy(114.330, 30.604), "长江", font=F_SMALL, fill=(255, 250, 243, 238))
draw.text(xy(114.217, 30.610), "汉江", font=F_SMALL, fill=(255, 250, 243, 238))

# Redraw town labels above the river strokes for readability.
draw.text((176, 244), "汉口", font=F_LABEL, fill=COLORS["ink"])
draw.text((178, 308), "商埠 / 码头 / 租界 / 夜宵", font=F_SMALL, fill=COLORS["muted"])
draw.text((154, 660), "汉阳", font=F_LABEL, fill=COLORS["ink"])
draw.text((156, 724), "知音 / 晴川 / 工业 / 汉阳造", font=F_SMALL, fill=COLORS["muted"])
draw.text((940, 485), "武昌", font=F_LABEL, fill=COLORS["ink"])
draw.text((942, 549), "省城 / 首义 / 楚文化 / 东湖", font=F_SMALL, fill=COLORS["muted"])

cx, cy = xy(114.289, 30.568)
draw.ellipse((cx - 13, cy - 13, cx + 13, cy + 13), fill=COLORS["gold"], outline=COLORS["paper"], width=4)
draw.text((cx + 18, cy - 34), "两江交汇", font=F_TINY, fill=COLORS["ink"])

small_landmark(draw, 114.292, 30.574, "江汉关 / 轮渡", (610, 382))
small_landmark(draw, 114.310, 30.544, "首义 / 黄鹤楼", (910, 710))
small_landmark(draw, 114.265, 30.553, "晴川阁", (210, 828))

# North arrow.
draw.polygon([(1412, 86), (1392, 136), (1432, 136)], fill=COLORS["ink"])
draw.line((1412, 132, 1412, 194), fill=COLORS["ink"], width=5)
draw.text((1393, 202), "北", font=F_SMALL, fill=COLORS["ink"])

legend = (108, 980, 1492, 1044)
draw.rounded_rectangle(legend, radius=22, fill=(255, 250, 243, 230), outline=COLORS["line"], width=2)
draw.text((136, 1004), "读图：汉口在汉江以北，汉阳在汉江以南且长江西侧，武昌在长江东侧。", font=F_SMALL, fill=COLORS["ink"])

OUT.parent.mkdir(parents=True, exist_ok=True)
img.convert("RGB").save(OUT, quality=92, optimize=True)
print(OUT)
