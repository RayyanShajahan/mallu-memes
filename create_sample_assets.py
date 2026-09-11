"""
create_sample_assets.py
=======================
Generates high-resolution sample JPEG meme banners in assets/memes/
to demonstrate automated Pillow-to-WebP compression and lazy loading.
"""

import os
from PIL import Image, ImageDraw, ImageFont

ASSETS_DIR = os.path.join(os.path.dirname(__file__), "assets", "memes")
os.makedirs(ASSETS_DIR, exist_ok=True)

SAMPLE_MEMES = [
    {
        "filename": "damu_choodu.jpg",
        "character": "Dashamoolam Damu",
        "actor": "Suraj Venjaramoodu",
        "movie": "Chattambinaadu",
        "quote": "Evidennu varunnu ithra choodu?! Ente thalakkakathu theepori!",
        "punchline": "Thalakkakathu full spark!",
        "accent_color": (255, 75, 75),
        "emotion": "angry"
    },
    {
        "filename": "manavalan_royal.jpg",
        "character": "Manavalan",
        "actor": "Salim Kumar",
        "movie": "Pulival Kalyanam",
        "quote": "Njan aara mon! Gulf return Manavalan and Sons Managing Director!",
        "punchline": "Aara mon!",
        "accent_color": (245, 166, 35),
        "emotion": "happy"
    },
    {
        "filename": "cid_moosa_sadhanam.jpg",
        "character": "CID Moosa",
        "actor": "Dileep",
        "movie": "CID Moosa",
        "quote": "Sadhanam kayyil undo mwone? Private Detective Moosa on duty!",
        "punchline": "Sadhanam kayyil undo?!",
        "accent_color": (0, 200, 255),
        "emotion": "happy"
    },
    {
        "filename": "ramanathan_malappuram.jpg",
        "character": "Ramanathan",
        "actor": "Mohanlal / Jagathy",
        "movie": "Manichitrathazhu",
        "quote": "Enthoke aayirunnu... Malappuram kathi, bomb, vedi... Oduvil Gangayude dance kandu njetti!",
        "punchline": "Vedi vazhipaadu aayi!",
        "accent_color": (180, 80, 255),
        "emotion": "fear"
    },
    {
        "filename": "pyari_rasikan.jpg",
        "character": "Pyari",
        "actor": "Salim Kumar",
        "movie": "Kalyanaraman",
        "quote": "Njan oru rasikan aanu chetta... Njanum ente oru potti chiriyum!",
        "punchline": "Full chiri haha!",
        "accent_color": (100, 220, 80),
        "emotion": "happy"
    },
    {
        "filename": "pappu_shariyaakkam.jpg",
        "character": "Kuthiravattam Pappu",
        "actor": "Pappu",
        "movie": "Vellanakalude Naadu",
        "quote": "Ippo sheriyaakki tharaam! Task force vannal road roller engottum maaranilla!",
        "punchline": "Ippo sheriyaakki tharaam!",
        "accent_color": (255, 120, 0),
        "emotion": "neutral"
    },
    {
        "filename": "mamukoya_gafoor.jpg",
        "character": "Gafoor Ka Dost",
        "actor": "Mamukoya",
        "movie": "Nadodikkattu",
        "quote": "Gafoor ka dost aanu! Dubai ennu paranju Madras beach-il erakkiya mahaprathibha!",
        "punchline": "Dubai alla Madras beach!",
        "accent_color": (220, 50, 120),
        "emotion": "sad"
    },
    {
        "filename": "harisree_appukuttan.jpg",
        "character": "Appukuttan",
        "actor": "Harisree Ashokan",
        "movie": "In Harihar Nagar",
        "quote": "Ente oru karyam... Maya vannappol muthal life full trap aayi!",
        "punchline": "Trap aayi mwone!",
        "accent_color": (255, 215, 0),
        "emotion": "fear"
    }
]

def generate_meme_image(meme_data, width=1000, height=600):
    """
    Creates an uncompressed high-res JPEG card with cinematic styling,
    ideal for demonstrating the 80%+ WebP compression savings.
    """
    img = Image.new("RGB", (width, height), color=(18, 22, 28))
    draw = ImageDraw.Draw(img)

    # Filmic gradient simulation
    accent = meme_data["accent_color"]
    for y in range(height):
        alpha = y / float(height)
        r = int(18 * (1 - alpha) + (accent[0] * 0.15) * alpha)
        g = int(22 * (1 - alpha) + (accent[1] * 0.15) * alpha)
        b = int(28 * (1 - alpha) + (accent[2] * 0.15) * alpha)
        draw.line([(0, y), (width, y)], fill=(r, g, b))

    # Outer border
    draw.rectangle([(15, 15), (width - 15, height - 15)], outline=accent, width=3)
    draw.rectangle([(22, 22), (width - 22, height - 22)], outline=(50, 55, 65), width=1)

    # Header Badges
    draw.rectangle([(40, 40), (280, 80)], fill=accent)
    draw.text((55, 50), "KERALA CULT CLASSIC", fill=(255, 255, 255))

    draw.rectangle([(width - 220, 40), (width - 40, 80)], outline=accent, width=2)
    draw.text((width - 200, 52), f"EMOTION: {meme_data['emotion'].upper()}", fill=accent)

    # Character and Movie
    draw.text((45, 120), meme_data["character"].upper(), fill=(255, 255, 255))
    draw.text((45, 175), f"Actor: {meme_data['actor']} | Movie: '{meme_data['movie']}'", fill=(170, 180, 195))

    # Quote Box
    draw.rectangle([(45, 240), (width - 45, 430)], fill=(10, 12, 16), outline=(60, 65, 75), width=2)
    draw.line([(45, 240), (45, 430)], fill=accent, width=8)

    # Quote text
    draw.text((65, 270), f"\"{meme_data['quote']}\"", fill=(240, 245, 250))
    draw.text((65, 365), f"🔥 PUNCHLINE: {meme_data['punchline']}", fill=accent)

    # Footer Metadata
    draw.line([(45, 470), (width - 45, 470)], fill=(40, 45, 55), width=1)
    draw.text((45, 510), "BIOMETRIC MEME MATRIX V2 | ASUS TUF F16 STREAMLIT DATA PLANE", fill=(120, 130, 145))
    draw.text((width - 320, 510), "TELEMETRY: 250,000 MEMES INDEXED", fill=(100, 200, 120))

    return img


def main():
    print(f"[ASSETS] Generating sample high-res meme images in '{ASSETS_DIR}'...")
    for meme in SAMPLE_MEMES:
        path = os.path.join(ASSETS_DIR, meme["filename"])
        img = generate_meme_image(meme)
        # Save as uncompressed JPEG (sub-sampling disabled, quality 95) to simulate realistic photo capture
        img.save(path, format="JPEG", quality=95, subsampling=0)
        size_kb = os.path.getsize(path) / 1024
        print(f"  * Generated {meme['filename']} ({size_kb:.1f} KB)")

    print(f"[SUCCESS] {len(SAMPLE_MEMES)} sample meme assets ready for lazy-loaded WebP compression.")

if __name__ == "__main__":
    main()
