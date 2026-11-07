# -*- coding: utf-8 -*-
"""표지 생성 — 1200×1600 (3:4). 검정 배경 + 제목 + 빨간 세로 도장.
실행: python make_cover.py
"""
import os
from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ROOT, "assets", "cover.png")
SERIF = r"C:\Windows\Fonts\HANBatangB.ttf"
SANS = r"C:\Windows\Fonts\malgun.ttf"
W, H = 1200, 1600
BG = (11, 11, 11)
WHITE = (245, 245, 245)
GRAY = (150, 150, 150)
DIM = (95, 95, 95)
RED = (198, 40, 40)

TITLE = ["확정된 형벌은", "집행되지 않는다"]
SUB = "사형제 재검토 원문 아카이브"
AUTHOR = "지은이 · 응징과 정의"
EN = "Retribution and Justice"
FOOT = "법령 · 헌법재판소 결정 · 대법원 판결 · 법무부 통계"
LIC = "CC BY 4.0"


def fit(text, path, max_w, start, floor=20):
    s = start
    while s > floor:
        f = ImageFont.truetype(path, s)
        if f.getlength(text) <= max_w:
            return f
        s -= 2
    return ImageFont.truetype(path, floor)


def seal(w=112, h=376):
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rectangle([0, 0, w - 1, h - 1], outline=RED + (255,), width=4)
    f = ImageFont.truetype(SERIF, 52)
    y = (h - 6 * 58) // 2
    for ch in "사형제재검토":
        tw = f.getlength(ch)
        d.text(((w - tw) / 2, y), ch, font=f, fill=RED + (255,))
        y += 58
    return im.rotate(-4, expand=True, resample=getattr(Image, "Resampling", Image).BICUBIC)


def main():
    os.makedirs(os.path.join(ROOT, "assets"), exist_ok=True)
    im = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(im)

    # 상단 얇은 선
    d.line([(110, 392), (330, 392)], fill=WHITE, width=4)

    y = 470
    for line in TITLE:
        f = fit(line, SERIF, 980, 132)
        tw = f.getlength(line)
        d.text(((W - tw) / 2 - 40, y), line, font=f, fill=WHITE)
        y += int(f.size * 1.42)

    # 부제
    fs = fit(SUB, SERIF, 900, 56)
    d.text(((W - fs.getlength(SUB)) / 2 - 40, y + 24), SUB, font=fs, fill=GRAY)

    # 도장 (우상단)
    im.paste(seal(), (1196 - 112, 452), seal())

    # 하단 블록
    fa = ImageFont.truetype(SANS, 40)
    d.text((110, 1240), AUTHOR, font=fa, fill=WHITE)
    fe = ImageFont.truetype(SANS, 30)
    d.text((110, 1296), EN, font=fe, fill=DIM)
    d.line([(110, 1360), (1090, 1360)], fill=(60, 60, 60), width=2)
    ff = ImageFont.truetype(SANS, 28)
    d.text((110, 1392), FOOT, font=ff, fill=DIM)
    d.text((110, 1440), LIC, font=ff, fill=DIM)
    d.text((110, 1488), "2026. 11.", font=ff, fill=DIM)

    im.save(OUT, quality=95)
    print("저장:", OUT, im.size)


if __name__ == "__main__":
    main()