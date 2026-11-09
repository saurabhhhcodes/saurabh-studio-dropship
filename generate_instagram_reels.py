#!/usr/bin/env python3
"""
Instagram Reels & Video Ads Generator for Saurabh Studio Dropshipping
Generates 1080x1920 (9:16 vertical) MP4 videos with animated kinetic typography,
zoom motion, luxury branding, and viral Instagram captions.
"""

import os
import sys
import json
import shutil
import subprocess
from PIL import Image, ImageDraw, ImageFont

BASE_DIR = "/Users/saurabhkumarbajpaiai/.gemini/antigravity/scratch/saurabh-studio-dropship"
ASSETS_DIR = os.path.join(BASE_DIR, "assets")
OUTPUT_DIR = os.path.join(BASE_DIR, "instagram_content")
os.makedirs(OUTPUT_DIR, exist_ok=True)

REELS_CONFIG = [
    {
        "id": "reel_canvas_dragon",
        "title": "Neo-Tokyo Cyberpunk Dragon Canvas",
        "product_id": "prod-canvas-dragon",
        "mockup": "mockup_canvas_dragon.png",
        "price_usd": "$69.99",
        "price_inr": "₹5,799",
        "category": "MUSEUM CANVAS ART",
        "hook_title": "STOP BUYING BORING POSTERS.",
        "hook_sub": "This is Museum-Grade 12-Color Archival Canvas.",
        "feature_1": "100% Solid FSC-Certified Wood Bars",
        "feature_2": "Archival UV-Resistant Giclée Ink",
        "feature_3": "Lifetime Anti-Fade Guarantee",
        "cta": "LINK IN BIO • EXPRESS FEDEX DISPATCH",
        "caption": """Stop buying cheap, paper-thin posters that wrinkle in a month. 🐉✨

Introducing the 'Neo-Tokyo Cyberpunk Dragon & Sacred Mt. Fuji' Museum Stretched Canvas.
• Printed with archival 12-color giclée ink on heavy poly-cotton canvas
• Hand-stretched over 1.25" sustainable solid wood bars
• Pre-installed brass hanging hardware included
• Shipped worldwide in reinforced protective crating

🚨 Limited Batch Production for November.
Direct from Saurabh Studio: Zero middlemen, pure museum quality.

👉 Tap the link in our bio to order yours with Free Express Delivery!
.
.
#canvasart #wallartdecor #cyberpunkart #neotokyo #japandecor #luxuryinterior #homedecorgoals #artcollector #hypebeastinterior #saurabhstudiostore""",
        "hashtags": ["#canvasart", "#wallartdecor", "#cyberpunkart", "#neotokyo", "#luxuryinterior", "#artcollector"]
    },
    {
        "id": "reel_hoodie_cyberpunk",
        "title": "Neo-Tokyo French Terry 400 GSM Hoodie",
        "product_id": "prod-hoodie-cyberpunk",
        "mockup": "mockup_hoodie_cyberpunk.png",
        "price_usd": "$54.99",
        "price_inr": "₹3,699",
        "category": "LUXURY STREETWEAR",
        "hook_title": "400 GSM HEAVYWEIGHT HOODIE.",
        "hook_sub": "Zero Shrinking. Pure Streetwear Silhouette.",
        "feature_1": "Custom Engraved Silver Aglets",
        "feature_2": "Seamless Double-Lined Hood & Kangaroo Pocket",
        "feature_3": "High-Definition DTG Dragon Print",
        "cta": "TAP LINK IN BIO • SHIPS WORLDWIDE",
        "caption": """Most hoodies lose their shape after two washes. Ours is built like armor. ⚡️

The Neo-Tokyo Cyberpunk Dragon Heavy French Terry Hoodie:
• 400 GSM ultra-heavyweight cotton fleece
• Custom engraved metal hardware & silver aglets
• Boxy drop-shoulder aesthetic streetwear cut
• Won't shrink or fade

Made-to-order individually. Zero fast-fashion waste.

👉 Tap the link in bio to cop before this batch closes!
.
.
#streetwear #heavyweighthoodie #hypebeast #streetwearoutfit #vintagefashion #cyberpunkfashion #dropshouldertshirt #luxuryapparel #tokyostyle #saurabhstudiostore""",
        "hashtags": ["#streetwear", "#heavyweighthoodie", "#hypebeast", "#cyberpunkfashion", "#luxuryapparel"]
    },
    {
        "id": "reel_canvas_zen",
        "title": "Aesthetic Zen Mountain Museum Canvas",
        "product_id": "prod-canvas-zen",
        "mockup": "mockup_canvas_zen.png",
        "price_usd": "$64.99",
        "price_inr": "₹5,399",
        "category": "JAPANDI FINE ART",
        "hook_title": "UPGRADE YOUR SANCTUARY.",
        "hook_sub": "Minimalist Japandi Art For Creative Spaces.",
        "feature_1": "Warm Archival Matte Texture",
        "feature_2": "High-Contrast Charcoal & Radiant Gold",
        "feature_3": "Crafted to Resist Sagging Permanently",
        "cta": "ORDER NOW • ZERO INVENTORY OVERHEAD",
        "caption": """Create a space that inspires calm and deep focus. 🧘‍♂️🏔️

The 'Aesthetic Zen Mountain & Golden Sun' Canvas:
A timeless balance of traditional Japanese ink landscapes and Scandinavian minimalism.
• Printed on museum-grade textured archival canvas
• Delivered ready-to-hang right out of the box
• Shipped via express courier with real-time tracking

Available now at Saurabh Studio.
👉 Tap link in bio to transform your living room or creative studio.
.
.
#japandistyle #minimalisthome #zenart #livingroomdecor #aestheticroom #interiordesignideas #scandinavianhome #artprints #saurabhstudiostore""",
        "hashtags": ["#japandistyle", "#minimalisthome", "#zenart", "#livingroomdecor", "#aestheticroom"]
    }
]

def get_font(size):
    font_paths = [
        "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
        "/System/Library/Fonts/Supplemental/Arial.ttf",
        "/System/Library/Fonts/Helvetica.ttc",
        "/Library/Fonts/Arial.ttf"
    ]
    for p in font_paths:
        if os.path.exists(p):
            try:
                return ImageFont.truetype(p, size)
            except Exception:
                continue
    return ImageFont.load_default()

def render_reel_video(config):
    reel_id = config["id"]
    print(f"[*] Rendering Instagram Reel: {config['title']} ({reel_id})")
    
    mockup_path = os.path.join(ASSETS_DIR, config["mockup"])
    if not os.path.exists(mockup_path):
        print(f"[!] Error: Mockup not found at {mockup_path}")
        return None
        
    mockup_img = Image.open(mockup_path).convert("RGBA")
    
    # We will generate 8 seconds of video at 30 fps = 240 frames
    temp_frames_dir = os.path.join(OUTPUT_DIR, f"frames_{reel_id}")
    if os.path.exists(temp_frames_dir):
        shutil.rmtree(temp_frames_dir)
    os.makedirs(temp_frames_dir, exist_ok=True)
    
    WIDTH = 1080
    HEIGHT = 1920
    FPS = 30
    DURATION_SEC = 8
    TOTAL_FRAMES = FPS * DURATION_SEC
    
    font_badge = get_font(28)
    font_hook = get_font(56)
    font_sub = get_font(34)
    font_feature = get_font(36)
    font_price = get_font(52)
    font_cta = get_font(38)
    font_brand = get_font(30)
    
    print(f"[*] Generating {TOTAL_FRAMES} frames (1080x1920) for {reel_id}...")
    
    for frame_idx in range(TOTAL_FRAMES):
        t = frame_idx / FPS  # Current time in seconds
        
        # Base background: Dark luxury gradient with subtle blue/emerald tint
        base = Image.new("RGBA", (WIDTH, HEIGHT), (11, 15, 25, 255))
        draw = ImageDraw.Draw(base)
        
        # Draw background radial ambient gradient
        for r in range(400, 0, -20):
            alpha = int(35 * (r / 400.0))
            draw.ellipse([WIDTH//2 - r, 750 - r, WIDTH//2 + r, 750 + r], fill=(16, 185, 129, alpha))
            
        # Subtle grid / boundary accents
        draw.rectangle([40, 40, WIDTH - 40, HEIGHT - 40], outline=(255, 255, 255, 25), width=2)
        
        # Header Brand Pill
        brand_text = "SAURABH BAJPAI STUDIO  •  OFFICIAL POD"
        draw.text((WIDTH//2, 90), brand_text, fill=(16, 185, 129, 255), font=font_brand, anchor="mm")
        
        # Category Badge
        cat_box = [WIDTH//2 - 220, 140, WIDTH//2 + 220, 195]
        draw.rounded_rectangle(cat_box, radius=28, fill=(17, 24, 39, 230), outline=(52, 211, 153, 180), width=2)
        draw.text((WIDTH//2, 168), config["category"], fill=(255, 255, 255, 255), font=font_badge, anchor="mm")
        
        # Animated Product Zoom (Slow cinematic breathing / Ken Burns zoom from 1.0 to 1.15)
        zoom_factor = 1.0 + 0.12 * (frame_idx / TOTAL_FRAMES)
        m_w = int(820 * zoom_factor)
        m_h = int(820 * zoom_factor)
        resized_mockup = mockup_img.resize((m_w, m_h), Image.Resampling.LANCZOS)
        
        # Center coordinates for product
        m_x = (WIDTH - m_w) // 2
        m_y = 480 - (m_h - 820) // 2
        
        # Product drop shadow
        draw.ellipse([WIDTH//2 - 380, 1150, WIDTH//2 + 380, 1230], fill=(0, 0, 0, 160))
        
        base.paste(resized_mockup, (m_x, m_y), resized_mockup)
        
        # Price Floating Pill over image
        price_text = f"{config['price_usd']}  /  {config['price_inr']}"
        draw.rounded_rectangle([WIDTH//2 - 230, 1120, WIDTH//2 + 230, 1195], radius=24, fill=(5, 150, 105, 245), outline=(255, 255, 255, 200), width=2)
        draw.text((WIDTH//2, 1158), price_text, fill=(255, 255, 255, 255), font=font_price, anchor="mm")
        
        # KINETIC TEXT PHASES
        # Phase 1: 0s - 2.5s (Hook)
        if t < 2.5:
            hook_alpha = min(255, int(t * 300))
            draw.text((WIDTH//2, 1280), config["hook_title"], fill=(255, 255, 255, hook_alpha), font=font_hook, anchor="mm")
            draw.text((WIDTH//2, 1360), config["hook_sub"], fill=(156, 163, 175, hook_alpha), font=font_sub, anchor="mm")
            draw.text((WIDTH//2, 1430), "Handcrafted on Museum Archival Material", fill=(52, 211, 153, hook_alpha), font=font_sub, anchor="mm")
        
        # Phase 2: 2.5s - 5.5s (Feature Bullets)
        elif t < 5.5:
            # Bullet 1
            b1_box = [100, 1250, WIDTH - 100, 1315]
            draw.rounded_rectangle(b1_box, radius=16, fill=(17, 24, 39, 220), outline=(52, 211, 153, 120), width=1)
            draw.text((WIDTH//2, 1282), f"✓ {config['feature_1']}", fill=(255, 255, 255, 255), font=font_feature, anchor="mm")
            
            # Bullet 2
            b2_box = [100, 1335, WIDTH - 100, 1400]
            draw.rounded_rectangle(b2_box, radius=16, fill=(17, 24, 39, 220), outline=(52, 211, 153, 120), width=1)
            draw.text((WIDTH//2, 1367), f"✓ {config['feature_2']}", fill=(255, 255, 255, 255), font=font_feature, anchor="mm")
            
            # Bullet 3
            b3_box = [100, 1420, WIDTH - 100, 1485]
            draw.rounded_rectangle(b3_box, radius=16, fill=(17, 24, 39, 220), outline=(52, 211, 153, 120), width=1)
            draw.text((WIDTH//2, 1452), f"✓ {config['feature_3']}", fill=(255, 255, 255, 255), font=font_feature, anchor="mm")
            
        # Phase 3: 5.5s - 8s (Call to Action & Dispatch Guarantee)
        else:
            pulse = int(220 + 35 * abs((frame_idx % 30) - 15) / 15.0)
            draw.text((WIDTH//2, 1270), "DIRECT ZERO-INVENTORY DISPATCH", fill=(52, 211, 153, 255), font=font_brand, anchor="mm")
            draw.text((WIDTH//2, 1330), "SHIPPED WORLDWIDE WITH FEDEX", fill=(255, 255, 255, 255), font=font_hook, anchor="mm")
            draw.text((WIDTH//2, 1400), "Doorstep Delivery • 30-Day Total Guarantee", fill=(209, 213, 219, 255), font=font_sub, anchor="mm")
            
            cta_box = [80, 1470, WIDTH - 80, 1570]
            draw.rounded_rectangle(cta_box, radius=24, fill=(16, 185, 129, pulse), outline=(255, 255, 255, 240), width=3)
            draw.text((WIDTH//2, 1520), config["cta"], fill=(11, 15, 25, 255), font=font_cta, anchor="mm")

        # Bottom Bar Guarantee
        bottom_box = [60, HEIGHT - 180, WIDTH - 60, HEIGHT - 80]
        draw.rounded_rectangle(bottom_box, radius=20, fill=(17, 24, 39, 240), outline=(75, 85, 99, 120), width=1)
        draw.text((WIDTH//2, HEIGHT - 145), "Secure Checkout • Verified UPI & Stripe • 24/7 Tracking", fill=(156, 163, 175, 255), font=font_badge, anchor="mm")
        draw.text((WIDTH//2, HEIGHT - 105), "saurabhhhcodes.github.io/saurabh-studio-dropship", fill=(52, 211, 153, 255), font=font_badge, anchor="mm")
        
        # Save frame
        frame_filename = os.path.join(temp_frames_dir, f"frame_{frame_idx:04d}.png")
        base.convert("RGB").save(frame_filename, "PNG")
        
    print(f"[*] Frames generated. Compiling MP4 via ffmpeg...")
    output_mp4 = os.path.join(OUTPUT_DIR, f"{reel_id}.mp4")
    
    ffmpeg_cmd = [
        "/opt/homebrew/bin/ffmpeg",
        "-y",
        "-r", str(FPS),
        "-i", os.path.join(temp_frames_dir, "frame_%04d.png"),
        "-c:v", "libx264",
        "-pix_fmt", "yuv420p",
        "-crf", "18",
        "-preset", "fast",
        output_mp4
    ]
    
    res = subprocess.run(ffmpeg_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if res.returncode == 0:
        print(f"[✓] Success: Generated Reel {output_mp4} ({os.path.getsize(output_mp4)//1024} KB)")
        # Clean up frames
        shutil.rmtree(temp_frames_dir)
        return output_mp4
    else:
        print(f"[!] FFmpeg error: {res.stderr.decode('utf-8')[:300]}")
        return None

def main():
    print("=== Saurabh Studio: Instagram Reels & Ad Pipeline ===")
    generated_reels = []
    
    for config in REELS_CONFIG:
        mp4_path = render_reel_video(config)
        if mp4_path:
            generated_reels.append({
                "id": config["id"],
                "title": config["title"],
                "video_path": mp4_path,
                "video_filename": os.path.basename(mp4_path),
                "duration_seconds": 8,
                "aspect_ratio": "9:16 (1080x1920)",
                "caption": config["caption"],
                "hashtags": config["hashtags"],
                "status": "Ready for Instagram / Meta Ads"
            })
            
    # Save Instagram Campaign JSON
    campaign_file = os.path.join(OUTPUT_DIR, "instagram_campaign.json")
    with open(campaign_file, "w") as f:
        json.dump({
            "brand": "Saurabh Studio & Apparel",
            "founder": "Saurabh Bajpai",
            "store_url": "https://saurabhhhcodes.github.io/saurabh-studio-dropship/",
            "generated_at": "2026-11-09T13:15:00Z",
            "reels_count": len(generated_reels),
            "reels": generated_reels,
            "scheduled_posting_times": [
                {"time": "11:30 AM IST", "purpose": "Morning Discovery & Commute Browse"},
                {"time": "03:15 PM IST", "purpose": "Afternoon Lifestyle Engagement"},
                {"time": "08:00 PM IST", "purpose": "Prime Impulse Purchasing Peak"}
            ]
        }, f, indent=2)
    print(f"[✓] Instagram Campaign manifest written to {campaign_file}")

if __name__ == "__main__":
    main()
