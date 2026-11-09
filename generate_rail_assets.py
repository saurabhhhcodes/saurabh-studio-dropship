#!/usr/bin/env python3
"""
Generate rail-ready transparent front, side, and back view images for the 10 products.
Matches Heyyali's exact specs:
- Hook tip touches the top edge.
- Side view aspect ratio: ~0.30 (width ~600, height ~2000)
- Front / Back view aspect ratio: ~0.65 (width ~1300, height ~2000)
- Transparent background PNG/WebP
"""

import os
from PIL import Image, ImageDraw, ImageFont

BASE_DIR = "/Users/saurabhkumarbajpaiai/.gemini/antigravity/scratch/saurabh-studio-dropship"
IMAGES_DIR = os.path.join(BASE_DIR, "images")
os.makedirs(IMAGES_DIR, exist_ok=True)

# Colors
WALNUT_DARK = (45, 28, 18, 255)
SILVER_HOOK = (210, 215, 225, 255)
HOOK_SHADOW = (140, 145, 155, 255)

def draw_hanger_hook(draw, cx, cy, side_view=False):
    # Hook tip touches y=0
    # Silver curved hook
    if side_view:
        # Side view: hook seen in profile
        draw.arc([cx - 25, 5, cx + 25, 95], start=180, end=360, fill=SILVER_HOOK, width=10)
        draw.line([cx - 25, 50, cx - 25, 95], fill=SILVER_HOOK, width=10)
        draw.line([cx + 25, 50, cx, 145], fill=SILVER_HOOK, width=10)
        # Small screw mount into wooden hanger
        draw.rectangle([cx - 14, 140, cx + 14, 160], fill=(180, 185, 195, 255))
        # Walnut hanger top cross-section
        draw.rounded_rectangle([cx - 45, 155, cx + 45, 185], radius=8, fill=WALNUT_DARK)
    else:
        # Front/Back view: full symmetrical triangular hanger
        # Curved hook at top
        draw.arc([cx - 35, 5, cx + 35, 90], start=160, end=380, fill=SILVER_HOOK, width=10)
        draw.line([cx - 35, 48, cx - 35, 80], fill=SILVER_HOOK, width=10)
        draw.line([cx, 80, cx, 145], fill=SILVER_HOOK, width=10)
        draw.rectangle([cx - 16, 140, cx + 16, 162], fill=(180, 185, 195, 255))
        # Walnut triangular wooden hanger body
        hanger_pts = [
            (cx, 155),
            (cx - 360, 240),
            (cx - 360, 280),
            (cx + 360, 280),
            (cx + 360, 240)
        ]
        draw.polygon(hanger_pts, fill=WALNUT_DARK)
        # Wooden bevel highlight
        draw.line([(cx - 355, 245), (cx, 160), (cx + 355, 245)], fill=(75, 48, 32, 255), width=6)

PRODUCTS = [
    {"slug": "hoodie-black", "name": "Neo-Tokyo Dragon 400 GSM Hoodie", "price": "$199.00", "color": (22, 24, 28), "accent": (16, 185, 129), "type": "hoodie", "has_print": True},
    {"slug": "tee-apex", "name": "Prehistoric Apex 240 GSM Tee", "price": "$95.00", "color": (28, 30, 34), "accent": (6, 182, 212), "type": "tee", "has_print": True},
    {"slug": "hoodie-zen", "name": "Aesthetic Zen Mountain Hoodie", "price": "$189.00", "color": (42, 45, 52), "accent": (245, 158, 11), "type": "hoodie", "has_print": True},
    {"slug": "tee-bone", "name": "Tokyo Cyberpunk Boxy Tee", "price": "$89.00", "color": (235, 230, 220), "accent": (16, 185, 129), "type": "tee", "has_print": True},
    {"slug": "hoodie-oatmeal", "name": "Sand Oatmeal French Terry Hoodie", "price": "$185.00", "color": (212, 203, 190), "accent": (120, 100, 80), "type": "hoodie", "has_print": False},
    {"slug": "tee-navy", "name": "Midnight Indigo Oversized Tee", "price": "$92.00", "color": (28, 36, 52), "accent": (56, 189, 248), "type": "tee", "has_print": True},
    {"slug": "hoodie-sage", "name": "Kyoto Moss Heavyweight Hoodie", "price": "$192.00", "color": (85, 102, 90), "accent": (200, 220, 205), "type": "hoodie", "has_print": False},
    {"slug": "tee-charcoal", "name": "Vintage Washed Boxy Tee", "price": "$88.00", "color": (48, 52, 60), "accent": (244, 63, 94), "type": "tee", "has_print": True},
    {"slug": "hoodie-crimson", "name": "Neo-Tokyo Crimson Dusk Hoodie", "price": "$195.00", "color": (95, 24, 34), "accent": (251, 191, 36), "type": "hoodie", "has_print": True},
    {"slug": "tee-olive", "name": "Military Olive Heavy Boxy Tee", "price": "$94.00", "color": (68, 76, 62), "accent": (234, 179, 8), "type": "tee", "has_print": False}
]

def generate_product_images():
    print(f"Generating rail-ready images for {len(PRODUCTS)} products...")
    
    for p in PRODUCTS:
        slug = p["slug"]
        color = p["color"]
        accent = p["accent"]
        is_hoodie = p["type"] == "hoodie"
        
        # 1. SIDE VIEW (Width 600, Height 2000 -> aspect ratio 0.30)
        sw, sh = 600, 2000
        side_img = Image.new("RGBA", (sw, sh), (0, 0, 0, 0))
        sdraw = ImageDraw.Draw(side_img)
        
        # Hook at top (cx=300, cy=0)
        draw_hanger_hook(sdraw, 300, 0, side_view=True)
        
        # Side silhouette
        # Top shoulder / hood profile
        if is_hoodie:
            # Hood drape falling back
            hood_pts = [(260, 180), (140, 260), (160, 420), (280, 450), (320, 360)]
            sdraw.polygon(hood_pts, fill=tuple(max(0, c - 20) for c in color))
            # Shoulder to hem
            body_pts = [
                (280, 200), (410, 260), (390, 800), (370, 1400), (360, 1920),
                (240, 1920), (230, 1400), (220, 800), (230, 360), (260, 200)
            ]
            sdraw.polygon(body_pts, fill=color)
            # Hanging sleeve profile
            sleeve_pts = [(310, 270), (430, 340), (410, 1100), (370, 1450), (320, 1450), (330, 1100), (280, 360)]
            sdraw.polygon(sleeve_pts, fill=tuple(min(255, c + 15) for c in color))
            # Sleeve cuff
            sdraw.rounded_rectangle([320, 1430, 370, 1490], radius=8, fill=tuple(max(0, c - 15) for c in color))
            # Bottom rib hem
            sdraw.rounded_rectangle([235, 1880, 365, 1940], radius=10, fill=tuple(max(0, c - 15) for c in color))
        else:
            # Tee side profile
            body_pts = [
                (280, 190), (390, 240), (380, 800), (360, 1350), (350, 1880),
                (250, 1880), (240, 1350), (230, 800), (250, 240)
            ]
            sdraw.polygon(body_pts, fill=color)
            # Short sleeve side profile
            sleeve_pts = [(290, 240), (430, 320), (410, 680), (330, 680), (270, 350)]
            sdraw.polygon(sleeve_pts, fill=tuple(min(255, c + 15) for c in color))
            # Bottom hem
            sdraw.rounded_rectangle([245, 1850, 355, 1890], radius=8, fill=tuple(max(0, c - 15) for c in color))
            
        side_path = os.path.join(IMAGES_DIR, f"{slug}-side.webp")
        side_img.save(side_path, "WEBP", quality=90)
        
        # 2. FRONT VIEW (Width 1300, Height 2000 -> aspect ratio 0.65)
        fw, fh = 1300, 2000
        front_img = Image.new("RGBA", (fw, fh), (0, 0, 0, 0))
        fdraw = ImageDraw.Draw(front_img)
        fcx = fw // 2
        
        draw_hanger_hook(fdraw, fcx, 0, side_view=False)
        
        if is_hoodie:
            # Main Torso
            torso_pts = [
                (fcx - 340, 270), (fcx + 340, 270),
                (fcx + 360, 800), (fcx + 350, 1400), (fcx + 340, 1920),
                (fcx - 340, 1920), (fcx - 350, 1400), (fcx - 360, 800)
            ]
            fdraw.polygon(torso_pts, fill=color)
            # Left & Right Sleeves
            l_sleeve = [(fcx - 340, 270), (fcx - 560, 500), (fcx - 490, 1420), (fcx - 410, 1410), (fcx - 355, 800)]
            fdraw.polygon(l_sleeve, fill=tuple(max(0, c - 10) for c in color))
            r_sleeve = [(fcx + 340, 270), (fcx + 560, 500), (fcx + 490, 1420), (fcx + 410, 1410), (fcx + 355, 800)]
            fdraw.polygon(r_sleeve, fill=tuple(max(0, c - 10) for c in color))
            # Cuffs
            fdraw.rounded_rectangle([fcx - 490, 1410, fcx - 410, 1470], radius=8, fill=tuple(max(0, c - 20) for c in color))
            fdraw.rounded_rectangle([fcx + 410, 1410, fcx + 490, 1470], radius=8, fill=tuple(max(0, c - 20) for c in color))
            # Hood opening & neckline
            hood_open = [(fcx - 140, 260), (fcx + 140, 260), (fcx + 100, 420), (fcx, 460), (fcx - 100, 420)]
            fdraw.polygon(hood_open, fill=tuple(max(0, c - 30) for c in color))
            # Drawstrings
            fdraw.line([(fcx - 60, 430), (fcx - 70, 720)], fill=(210, 215, 220, 255), width=6)
            fdraw.line([(fcx + 60, 430), (fcx + 70, 720)], fill=(210, 215, 220, 255), width=6)
            # Silver aglets
            fdraw.rectangle([fcx - 75, 715, fcx - 65, 755], fill=(230, 235, 245, 255))
            fdraw.rectangle([fcx + 65, 715, fcx + 75, 755], fill=(230, 235, 245, 255))
            # Kangaroo Pocket
            pocket_pts = [
                (fcx - 240, 1280), (fcx + 240, 1280),
                (fcx + 290, 1680), (fcx - 290, 1680)
            ]
            fdraw.polygon(pocket_pts, fill=tuple(min(255, c + 12) for c in color))
            fdraw.line([(fcx - 240, 1280), (fcx + 240, 1280)], fill=(120, 125, 135, 100), width=3)
            # Bottom ribbed waistband
            fdraw.rounded_rectangle([fcx - 345, 1870, fcx + 345, 1940], radius=12, fill=tuple(max(0, c - 20) for c in color))
            # Center graphic if applicable
            if p["has_print"]:
                fdraw.rounded_rectangle([fcx - 180, 560, fcx + 180, 1140], radius=16, fill=(15, 15, 20, 180), outline=accent, width=4)
                # Geometric stylized cyber/apex badge
                fdraw.ellipse([fcx - 90, 720, fcx + 90, 900], outline=accent, width=6)
                fdraw.polygon([(fcx, 740), (fcx + 60, 860), (fcx - 60, 860)], fill=accent)
        else:
            # Tee Front View
            torso_pts = [
                (fcx - 320, 260), (fcx + 320, 260),
                (fcx + 340, 800), (fcx + 330, 1400), (fcx + 320, 1880),
                (fcx - 320, 1880), (fcx - 330, 1400), (fcx - 340, 800)
            ]
            fdraw.polygon(torso_pts, fill=color)
            # Left & Right Short Sleeves
            l_sleeve = [(fcx - 320, 260), (fcx - 540, 480), (fcx - 430, 780), (fcx - 335, 680)]
            fdraw.polygon(l_sleeve, fill=tuple(max(0, c - 10) for c in color))
            r_sleeve = [(fcx + 320, 260), (fcx + 540, 480), (fcx + 430, 780), (fcx + 335, 680)]
            fdraw.polygon(r_sleeve, fill=tuple(max(0, c - 10) for c in color))
            # Crew neck rib
            fdraw.arc([fcx - 120, 180, fcx + 120, 310], start=0, end=180, fill=tuple(max(0, c - 25) for c in color), width=18)
            # Bottom hem
            fdraw.rounded_rectangle([fcx - 325, 1840, fcx + 325, 1890], radius=8, fill=tuple(max(0, c - 15) for c in color))
            # Graphic print
            if p["has_print"]:
                fdraw.rounded_rectangle([fcx - 190, 520, fcx + 190, 1180], radius=16, fill=(15, 15, 20, 180), outline=accent, width=4)
                fdraw.polygon([(fcx, 680), (fcx + 90, 940), (fcx - 90, 940)], outline=accent, fill=accent)
                
        front_path = os.path.join(IMAGES_DIR, f"{slug}-front.webp")
        front_img.save(front_path, "WEBP", quality=90)
        
        # 3. BACK VIEW (Width 1300, Height 2000 -> aspect ratio 0.65)
        back_img = Image.new("RGBA", (fw, fh), (0, 0, 0, 0))
        bdraw = ImageDraw.Draw(back_img)
        
        draw_hanger_hook(bdraw, fcx, 0, side_view=False)
        
        if is_hoodie:
            torso_pts = [
                (fcx - 340, 270), (fcx + 340, 270),
                (fcx + 360, 800), (fcx + 350, 1400), (fcx + 340, 1920),
                (fcx - 340, 1920), (fcx - 350, 1400), (fcx - 360, 800)
            ]
            bdraw.polygon(torso_pts, fill=color)
            l_sleeve = [(fcx - 340, 270), (fcx - 560, 500), (fcx - 490, 1420), (fcx - 410, 1410), (fcx - 355, 800)]
            bdraw.polygon(l_sleeve, fill=tuple(max(0, c - 10) for c in color))
            r_sleeve = [(fcx + 340, 270), (fcx + 560, 500), (fcx + 490, 1420), (fcx + 410, 1410), (fcx + 355, 800)]
            bdraw.polygon(r_sleeve, fill=tuple(max(0, c - 10) for c in color))
            # Cuffs & waistband
            bdraw.rounded_rectangle([fcx - 490, 1410, fcx - 410, 1470], radius=8, fill=tuple(max(0, c - 20) for c in color))
            bdraw.rounded_rectangle([fcx + 410, 1410, fcx + 490, 1470], radius=8, fill=tuple(max(0, c - 20) for c in color))
            bdraw.rounded_rectangle([fcx - 345, 1870, fcx + 345, 1940], radius=12, fill=tuple(max(0, c - 20) for c in color))
            # Back of Hood
            hood_back = [(fcx - 170, 250), (fcx + 170, 250), (fcx + 190, 580), (fcx, 620), (fcx - 190, 580)]
            bdraw.polygon(hood_back, fill=tuple(min(255, c + 15) for c in color))
            # Subtle back brand text
            bdraw.rounded_rectangle([fcx - 120, 900, fcx + 120, 940], radius=6, fill=accent)
        else:
            torso_pts = [
                (fcx - 320, 260), (fcx + 320, 260),
                (fcx + 340, 800), (fcx + 330, 1400), (fcx + 320, 1880),
                (fcx - 320, 1880), (fcx - 330, 1400), (fcx - 340, 800)
            ]
            bdraw.polygon(torso_pts, fill=color)
            l_sleeve = [(fcx - 320, 260), (fcx - 540, 480), (fcx - 430, 780), (fcx - 335, 680)]
            bdraw.polygon(l_sleeve, fill=tuple(max(0, c - 10) for c in color))
            r_sleeve = [(fcx + 320, 260), (fcx + 540, 480), (fcx + 430, 780), (fcx + 335, 680)]
            bdraw.polygon(r_sleeve, fill=tuple(max(0, c - 10) for c in color))
            bdraw.arc([fcx - 120, 210, fcx + 120, 290], start=0, end=180, fill=tuple(max(0, c - 25) for c in color), width=16)
            bdraw.rounded_rectangle([fcx - 325, 1840, fcx + 325, 1890], radius=8, fill=tuple(max(0, c - 15) for c in color))
            # Minimalist back collar tag
            bdraw.rectangle([fcx - 40, 310, fcx + 40, 350], fill=accent)
            
        back_path = os.path.join(IMAGES_DIR, f"{slug}-back.webp")
        back_img.save(back_path, "WEBP", quality=90)
        
    print(f"Generated 30 rail-ready WebP images in {IMAGES_DIR}")

if __name__ == "__main__":
    generate_product_images()
