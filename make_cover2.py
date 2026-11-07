# -*- coding: utf-8 -*-
"""표지 v2 — 1200×1600. 제목 좌상, 브랜드 워드마크는 하단 중앙(썸네일과 같은 규칙).
두 가지 제목 서체를 뽑는다: cover.png(고딕 Black) / cover_serif.png(바탕체 Bold).
"""
import os
from PIL import Image, ImageDraw, ImageFont

ROOT = r"G:\내 드라이브\Hermes\사형제재검토\위키독스_책"
VF = r"C:\Windows\Fonts\NotoSansKR-VF.ttf"
SERIF = r"C:\Windows\Fonts\HANBatangB.ttf"
SANS = r"C:\Windows\Fonts\malgun.ttf"
W, H = 1200, 1600
BG = (11, 11, 11)
WHITE = (245, 245, 245)
GRAY = (150, 150, 150)
DIM = (95, 95, 95)
RED = (200, 46, 46)

TITLE = ["사형,", "집행되지 않는 형벌"]
SUB = "원문 아카이브 — 조문 · 판결 · 통계"
BRAND = "응징과 정의"
EN = "Retribution and Justice"
FOOT = "법령 · 헌법재판소 결정 · 대법원 판결 · 법무부 통계"


def vf(size, weight="Black"):
    f = ImageFont.truetype(VF, size)
    names = [n for n in f.get_variation_names() if weight.encode() in n]
    if names:
        f.set_variation_by_name(names[0])
    return f


def fit(text, font_fn, max_w, start, floor=20):
    s = start
    while s > floor:
        f = font_fn(s)
        if f.getlength(text) <= max_w:
            return f
        s -= 2
    return font_fn(floor)


def brand_mark(scale=1.5):
    """278×81의 scale배 워드마크(투명)."""
    w, h = int(278 * scale), int(81 * scale)
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rectangle([0, 0, w - 1, h - 1], outline=RED + (255,), width=max(2, int(3 * scale)))
    f = vf(int(46 * scale))
    bb = d.textbbox((0, 0), BRAND, font=f)
    bw, bh = bb[2] - bb[0], bb[3] - bb[1]
    d.text(((w - bw) / 2 - bb[0], (h - bh) / 2 - bb[1]), BRAND, font=f, fill=RED + (255,))
    return im


def build(title_font_fn, out_name):
    im = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(im)

    y = 512
    for line in TITLE:
        f = fit(line, title_font_fn, 960, 160 if line == TITLE[0] else 124)
        d.text((110, y), line, font=f, fill=WHITE)
        print(f"  '{line}' → {int(f.size)}pt 폭 {int(f.getlength(line))}px")
        y += int(f.size * 1.30)

    fs = fit(SUB, lambda s: vf(s, "Medium"), 960, 44)
    d.text((110, y + 30), SUB, font=fs, fill=GRAY)

    # 하단 중앙 워드마크
    mk = brand_mark(1.5)
    mx = (W - mk.width) // 2
    my = 1158
    im.paste(mk, (mx, my), mk)

    fe = vf(30, "Medium")
    tw = fe.getlength(EN)
    d.text(((W - tw) / 2, my + mk.height + 26), EN, font=fe, fill=DIM)

    d.line([(300, 1352), (900, 1352)], fill=(60, 60, 60), width=2)
    ff = vf(26, "Medium")
    for i, txt in enumerate([FOOT, "CC BY 4.0   ·   2026. 11."]):
        tx = (W - ff.getlength(txt)) / 2
        d.text((tx, 1386 + i * 44), txt, font=ff, fill=DIM)

    out = os.path.join(ROOT, "assets", out_name)
    im.save(out, quality=95)
    print("저장:", out, im.size)
    return out


if __name__ == "__main__":
    print("[고딕 Black]")
    build(lambda s: vf(s, "Black"), "cover.png")
    print("[바탕체 Bold]")
    build(lambda s: ImageFont.truetype(SERIF, s), "cover_serif.png")