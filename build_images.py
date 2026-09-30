#!/usr/bin/env python3
"""Copy + optimise curated images from oldsite scrape into pub/images/."""
import os
from PIL import Image, ImageOps

SRC = os.path.join("pub", "oldsite", "media")
DST = os.path.join("pub", "images")
GAL = os.path.join(DST, "gallery")
os.makedirs(GAL, exist_ok=True)

# (src_filename, dest_name, max_px)
IMAGES = [
    ("f74c9d_4ad93de0d23a491d95194a0abe6feadc~mv2.jpeg", "hero-front.jpg", 1920),
    ("f74c9d_75eb144b135e4d7dbe65cd772494aa85~mv2.jpeg", "floating-glass.jpg", 1200),
    ("f74c9d_4bacbd6daa8745d4bda27a25baf087d3~mv2.jpg", "fireplace.jpg", 1200),
    ("f74c9d_1f5ae3076d974fed9e7a8538dec3cc61~mv2.jpg", "offer-room.jpg", 1200),
    ("f74c9d_a9e7e225d96a4cae9b319d6abc1c0132~mv2.jpg", "offer-meal.jpg", 1200),
    ("f74c9d_dec5f30e311644f9bc2eb72d423f5147~mv2.jpg", "logo-1938.jpg", 1200),
    ("f74c9d_224d60cc13554554886e02d441caea67~mv2.jpg", "whisky-bar.jpg", 1920),
    # taps
    ("f74c9d_0d9d27a3b7e24c1db10038f1c09db4a4~mv2.png", "tap-travla.png", 600),
    ("f74c9d_40e090a6ffab40e9b4a469320168b246~mv2.jpg", "tap-carlton-draught.jpg", 800),
    ("f74c9d_4eb7630cf2314f48a359b871eaee2104~mv2.jpeg", "tap-reschs.jpg", 800),
    ("f74c9d_e8b5a00d642d4ce5a6a5086565b255d4~mv2.jpg", "tap-great-northern.jpg", 800),
    ("f74c9d_30cb98d5b31f4b80ad701a286fe5d544~mv2.jpg", "tap-asahi.jpg", 800),
    ("f74c9d_b100c4d77c3c4e53bf42c070964520ab~mv2.jpeg", "tap-carlton-dry.jpg", 800),
    ("f74c9d_fddc865471c04d1899dcfcb10e65be04~mv2.png", "tap-vb.png", 600),
    ("f74c9d_08a07e519e6f458982cd1ab60f9659aa~mv2.jpg", "tap-hard-rated.jpg", 800),
    # rooms
    ("f74c9d_46f8cb9cbec543c39e07769649c88180~mv2.jpg", "room-single.jpg", 1200),
    ("f74c9d_804b9a28fbe9457482686f1db71678d4~mv2.jpg", "room-twin.jpg", 1200),
    ("f74c9d_4daa3024f97146b08222b87de6a8d52e~mv2.jpg", "room-queen.jpg", 1200),
    # merch
    ("f74c9d_1622b8db0a484b039b82b81cba284fc9~mv2.png", "merch-hoodie-back.jpg", 1200),
    ("f74c9d_aff479a4b4e3457f9424a4b988aba626~mv2.png", "merch-hoodie-front.jpg", 1200),
    ("f74c9d_64f462cc10c44e31a1a2001893a05b53~mv2.jpg", "merch-stuck-shirt.jpg", 1200),
    ("f74c9d_2acce150cacb4180a361d09428a6f61f~mv2.jpg", "merch-stuck-legend.jpg", 1200),
    ("f74c9d_dfadbb9ba7084a9d8f9e4f49ddb4082b~mv2.png", "merch-longsleeve.jpg", 1200),
    ("f74c9d_734c234f0364442180c70f5912d4605f~mv2.jpg", "merch-hat-pink.jpg", 1000),
    ("f74c9d_eb6188d990d44d258e127602e436ca68~mv2.jpg", "merch-hat-navy.jpg", 1000),
    ("f74c9d_53e2b64d9c544edf9f221a185606c7cd~mv2.jpg", "merch-hat-tan.jpg", 1000),
    ("f74c9d_6995cb2d72a24349b0fa9bc94d7616dd~mv2.png", "merch-beanie.jpg", 1200),
    ("f74c9d_27f1513d6d70412593f4e316a7527b99~mv2.jpg", "merch-stubby.jpg", 1000),
    ("f74c9d_0b14614d3bd64b5eb4e7cc378598f871~mv2.png", "badge-cfh.jpg", 1000),
    ("f74c9d_64b3fe9e7fd243f4888f7a9406ffdb28~mv2.jpg", "merch-hero.jpg", 1920),
]

GALLERY = [
    # 1938 whisky bar / 1st birthday
    ("f74c9d_181ccf51f28141e684f16d1108403513~mv2.png", "gallery/bar-01.jpg"),
    ("f74c9d_837a346eee7e4d4ca33c7cba9a7c40c0~mv2.jpg", "gallery/bar-02.jpg"),
    ("f74c9d_a630bd4b6bac44e380673b4c0fe7f76b~mv2.jpg", "gallery/bar-03.jpg"),
    ("f74c9d_e734119757fc41ae967b47128989e17c~mv2.jpg", "gallery/bar-04.jpg"),
    ("f74c9d_3289b0b7b9a04b099028bc5174f26291~mv2.jpg", "gallery/bar-05.jpg"),
    # Mick Pearce - Tatts Finke Desert Race 2025
    ("f74c9d_01ee4016ed10443283f7d65672165db1~mv2.jpg", "gallery/finke-01.jpg"),
    ("f74c9d_264c254f81574382aa9d59024efd6bb6~mv2.jpg", "gallery/finke-02.jpg"),
    ("f74c9d_a69e80cb50064ac284e67e4bfaf9365e~mv2.jpg", "gallery/finke-03.jpg"),
    # The Narrow Road To The Deep North - behind the scenes
    ("f74c9d_5412fb5f62c445a5a2cdc957062ab088~mv2.jpg", "gallery/film-01.jpg"),
    ("f74c9d_51c2e6f471ac46ff86817954216399c3~mv2.jpg", "gallery/film-02.jpg"),
    ("f74c9d_2e2f535a7a8240e8a4db8ca6b8b14811~mv2.jpg", "gallery/film-03.jpg"),
    ("f74c9d_b652e45adc28466fa8fbcbcd7e38e51e~mv2.jpg", "gallery/film-04.jpg"),
    ("f74c9d_5c148ae280684f28bf30be44dd4087b3~mv2.jpg", "gallery/film-05.jpg"),
    ("f74c9d_a92f756b0a944590ad2c6aace2dbee85~mv2.jpg", "gallery/film-06.jpg"),
    ("f74c9d_6fd1574ffd6c46628f976d8f242eb65d~mv2.jpg", "gallery/film-07.jpg"),
    ("f74c9d_1a31ab0087a94724b19e8139677e7069~mv2.jpg", "gallery/film-08.jpg"),
    ("f74c9d_861783c215c24f6499bfb4d067de9ae2~mv2.jpg", "gallery/film-09.jpg"),
    ("f74c9d_c0e9b1126bad4e568376a6fa54efc331~mv2.jpg", "gallery/film-10.jpg"),
    # ANZAC Day / Australia Day 2025
    ("f74c9d_215536c519d646d18f552a4cd4aee414~mv2.jpg", "gallery/anzac-01.jpg"),
    ("f74c9d_04d9a450528c406eb23de43dbef27fcb~mv2.jpg", "gallery/ausday-01.jpg"),
]


def process(src, dst, max_px, keep_png=False):
    path = os.path.join(SRC, src)
    img = ImageOps.exif_transpose(Image.open(path))
    img = img.convert("RGBA") if keep_png else img.convert("RGB")
    w, h = img.size
    if max(w, h) > max_px:
        s = max_px / max(w, h)
        img = img.resize((round(w * s), round(h * s)), Image.LANCZOS)
    out = os.path.join(DST, dst)
    os.makedirs(os.path.dirname(out), exist_ok=True)
    if keep_png:
        img.save(out, "PNG", optimize=True)
    else:
        img.save(out, "JPEG", quality=82, optimize=True, progressive=True)
    return out, os.path.getsize(out)


total = 0
for src, dst, mx in IMAGES + [(s, d, 1600) for s, d in GALLERY]:
    keep_png = dst.endswith(".png")
    out, size = process(src, dst, mx, keep_png)
    total += size
    print(f"{dst}  {size//1024}KB")

# favicon from the gold 1938 logo
img = Image.open(os.path.join(SRC, "f74c9d_dec5f30e311644f9bc2eb72d423f5147~mv2.jpg")).convert("RGB")
img.thumbnail((64, 64), Image.LANCZOS)
img.save(os.path.join(DST, "favicon.png"), "PNG")
print(f"\ntotal {total/1024/1024:.1f}MB")
