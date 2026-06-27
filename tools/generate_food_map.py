from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "assets" / "images" / "wuhan-food-map.png"

W, H = 1600, 1000
PAD_X, PAD_Y = 120, 112
LON_MIN, LON_MAX = 114.205, 114.515
LAT_MIN, LAT_MAX = 30.475, 30.625

COLORS = {
    "bg": (248, 242, 232),
    "paper": (255, 250, 243),
    "ink": (31, 47, 53),
    "muted": (94, 109, 105),
    "line": (226, 211, 190),
    "river": (58, 132, 157),
    "river_light": (135, 190, 203),
    "red": (169, 72, 56),
    "green": (75, 104, 79),
    "gold": (204, 148, 66),
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


F_TITLE = font(48, True)
F_SUB = font(28)
F_LABEL = font(34, True)
F_SMALL = font(24)
F_TINY = font(20)


def xy(lon, lat):
    x = PAD_X + (lon - LON_MIN) / (LON_MAX - LON_MIN) * (W - PAD_X * 2)
    y = PAD_Y + (LAT_MAX - lat) / (LAT_MAX - LAT_MIN) * (H - PAD_Y * 2)
    return int(round(x)), int(round(y))


def draw_polyline(draw, points, width, fill, joint="curve"):
    coords = [xy(lon, lat) for lon, lat in points]
    draw.line(coords, width=width, fill=fill, joint=joint)
    radius = width // 2
    for x, y in coords:
        draw.ellipse((x - radius, y - radius, x + radius, y + radius), fill=fill)


def rounded_label(draw, lon, lat, title, subtitle, align="left", color=COLORS["paper"]):
    x, y = xy(lon, lat)
    title_box = draw.textbbox((0, 0), title, font=F_LABEL)
    sub_box = draw.textbbox((0, 0), subtitle, font=F_SMALL)
    bw = max(title_box[2], sub_box[2]) + 54
    bh = 106
    if align == "right":
        x -= bw
    elif align == "center":
        x -= bw // 2
    box = (x, y, x + bw, y + bh)
    shadow = (box[0] + 8, box[1] + 10, box[2] + 8, box[3] + 10)
    draw.rounded_rectangle(shadow, radius=22, fill=(0, 0, 0, 28))
    draw.rounded_rectangle(box, radius=22, fill=color, outline=COLORS["line"], width=2)
    draw.text((x + 26, y + 16), title, font=F_LABEL, fill=COLORS["ink"])
    draw.text((x + 26, y + 61), subtitle, font=F_SMALL, fill=COLORS["muted"])
    return box


def landmark(draw, lon, lat, text):
    x, y = xy(lon, lat)
    draw.ellipse((x - 7, y - 7, x + 7, y + 7), fill=COLORS["gold"], outline=COLORS["paper"], width=3)
    draw.text((x + 12, y - 15), text, font=F_TINY, fill=COLORS["ink"])


def pin(draw, lon, lat, number, title, subtitle, label_xy):
    x, y = xy(lon, lat)
    draw.ellipse((x - 15, y - 15, x + 15, y + 15), fill=COLORS["red"], outline=COLORS["paper"], width=5)
    draw.text((x - 7, y - 14), str(number), font=F_TINY, fill=COLORS["paper"])
    width = 360
    height = 86
    bx, by = label_xy
    anchor_x = bx + (0 if bx > x else width)
    draw.line((x, y, anchor_x, by + height // 2), fill=COLORS["red"], width=3)
    draw.rounded_rectangle((bx, by, bx + width, by + height), radius=18, fill=COLORS["paper"], outline=COLORS["line"], width=2)
    draw.text((bx + 18, by + 12), title, font=F_SMALL, fill=COLORS["ink"])
    draw.text((bx + 18, by + 47), subtitle, font=F_TINY, fill=COLORS["muted"])


img = Image.new("RGBA", (W, H), COLORS["bg"] + (255,))
draw = ImageDraw.Draw(img, "RGBA")

# City zones are deliberately soft blocks: enough orientation, not a fake street map.
draw.rounded_rectangle((112, 156, 690, 482), radius=42, fill=COLORS["hankou"] + (175,))
draw.rounded_rectangle((128, 560, 545, 840), radius=42, fill=COLORS["hanyang"] + (150,))
draw.rounded_rectangle((775, 430, 1396, 842), radius=42, fill=COLORS["wuchang"] + (166,))
draw.text((150, 178), "汉口", font=F_TITLE, fill=COLORS["ink"])
draw.text((152, 236), "商埠 / 码头 / 过早 / 夜宵", font=F_SMALL, fill=COLORS["muted"])
draw.text((166, 596), "汉阳", font=F_TITLE, fill=COLORS["ink"])
draw.text((168, 654), "晴川 / 知音 / 工业武汉", font=F_SMALL, fill=COLORS["muted"])
draw.text((812, 462), "武昌", font=F_TITLE, fill=COLORS["ink"])
draw.text((814, 520), "首义 / 省博 / 东湖 / 过早", font=F_SMALL, fill=COLORS["muted"])

draw_polyline(
    draw,
    [(114.20, 30.548), (114.24, 30.553), (114.285, 30.563), (114.34, 30.575), (114.43, 30.596), (114.515, 30.612)],
    58,
    COLORS["river_light"] + (232,),
)
draw_polyline(
    draw,
    [(114.20, 30.548), (114.24, 30.553), (114.285, 30.563), (114.34, 30.575), (114.43, 30.596), (114.515, 30.612)],
    34,
    COLORS["river"] + (238,),
)
draw_polyline(
    draw,
    [(114.185, 30.625), (114.215, 30.613), (114.245, 30.596), (114.285, 30.568)],
    44,
    COLORS["river_light"] + (220,),
)
draw_polyline(
    draw,
    [(114.185, 30.625), (114.215, 30.613), (114.245, 30.596), (114.285, 30.568)],
    25,
    COLORS["river"] + (235,),
)

draw.text(xy(114.40, 30.604), "长江", font=F_SMALL, fill=(255, 250, 243, 245))
draw.text(xy(114.22, 30.606), "汉江", font=F_SMALL, fill=(255, 250, 243, 245))
cx, cy = xy(114.285, 30.568)
draw.ellipse((cx - 10, cy - 10, cx + 10, cy + 10), fill=COLORS["gold"])
draw.text((cx + 18, cy - 30), "两江交汇", font=F_TINY, fill=COLORS["ink"])

draw.text((106, 48), "武汉小吃街区位置图", font=F_TITLE, fill=COLORS["ink"])
draw.text((108, 108), "北向上 · 位置示意，不替代导航；用来判断今天往汉口、武昌还是光谷走。", font=F_SUB, fill=COLORS["muted"])

pin(draw, 114.309, 30.604, 1, "山海关路 / 沈阳路", "汉口过早，住汉口最顺", (625, 180))
pin(draw, 114.283, 30.581, 2, "水塔街 / 江汉路", "汉口核心，接江汉关", (118, 330))
pin(draw, 114.266, 30.589, 3, "万松园 / 雪松路", "6/27 晚上湖北菜夜宵", (118, 456))
pin(draw, 114.312, 30.545, 4, "粮道街 / 大成路", "武昌过早，接首义/省博", (655, 666))
pin(draw, 114.400, 30.507, 5, "光谷核心商圈", "入住前晚餐，别押酒店周边", (1025, 682))

landmark(draw, 114.292, 30.574, "江汉关 / 轮渡")
landmark(draw, 114.365, 30.560, "省博 / 东湖")
landmark(draw, 114.485, 30.486, "光谷希尔顿方向")

# North arrow and legend.
draw.polygon([(1412, 82), (1392, 132), (1432, 132)], fill=COLORS["ink"])
draw.line((1412, 128, 1412, 188), fill=COLORS["ink"], width=5)
draw.text((1393, 196), "北", font=F_SMALL, fill=COLORS["ink"])

legend = (108, 882, 1492, 944)
draw.rounded_rectangle(legend, radius=22, fill=(255, 250, 243, 230), outline=COLORS["line"], width=2)
draw.text((136, 905), "读图：汉口吃热闹，武昌吃清晨，光谷只作收尾。点位是街区级位置，现场按排队、距离和天气选店。", font=F_SMALL, fill=COLORS["ink"])

OUT.parent.mkdir(parents=True, exist_ok=True)
img.convert("RGB").save(OUT, quality=92, optimize=True)
print(OUT)
