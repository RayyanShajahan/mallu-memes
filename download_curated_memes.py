import os
import urllib.request
import urllib.parse
from PIL import Image

# Curated, authentic Malayalam movie meme archive
MEME_CATALOG = {
    'sad': [
        ('Kalyanaraman', 'achuvettaa-i-love-you.jpg', 'sad_salim_kumar_crying.jpg'),
        ('Nadodikkattu', 'achan-paranju-ithilum-bhedham-kattapparayum-eduth-kakkaan-irangunnathaanennu.jpg', 'sad_dasan_kattappara.jpg'),
        ('CID Moosa', 'athinekkaal-nallath-ente-shavam-edukkunnathalle.jpg', 'sad_moosa_shavam.jpg'),
        ('In Harihar Nagar', 'appukkuttan-expression.jpg', 'sad_appukkuttan_expression.jpg'),
        ('Manichitrathazhu', 'adukkaruth-karnnore-entaduth-maathram-adukkaruth.jpg', 'sad_karnnore_adukkaruth.jpg'),
    ],
    'angry': [
        ('Spadikam', 'kuttikkadan-expression.jpg', 'angry_kuttikkadan_spadikam.jpg'),
        ('Godfather', 'aanede-chevittil-maathramalla-ninte-ammede-chevittilum-vekkeda-panji.jpg', 'angry_anjooran_panji.jpg'),
        ('Akkare Akkare Akkare', 'krishnan-nair-shooting.jpg', 'angry_krishnan_nair_gun.jpg'),
        ('Akkare Akkare Akkare', 'ninte-achanaada-paul-barber.jpg', 'angry_paul_barber.jpg'),
        ('In Harihar Nagar', 'aarkkadaa-bhraanth.jpg', 'angry_aarkkada_bhraanth.jpg'),
    ],
    'happy': [
        ('Punjabi House', 'annu-undaakkiya-biriyaani-okke-enth-cheytho-aavo.jpg', 'happy_ramanan_biriyani.jpg'),
        ('Punjabi House', 'akathu-poyi-punjabikalod-para-gangadharan-mothalaaliyum-ramananum-vannirikkunnu-ennu.jpg', 'happy_gangadharan_mothalali.jpg'),
        ('Akkare Akkare Akkare', 'sadhanam-kayyilundo.jpg', 'happy_sadhanam_kayyilundo.jpg'),
        ('Nadodikkattu', 'angane-pavanayi-shavamaayi.jpg', 'happy_pavanayi_shavamaayi.jpg'),
        ('Aavesham', 'all-the-best-da.jpg', 'happy_ranga_annan_aavesham.jpg'),
        ('Kilukkam', 'aha-anganayanalle.jpg', 'happy_jagathy_aha.jpg'),
    ],
    'neutral': [
        ('Nadodikkattu', 'allenkilum-ee-thallipoli-companiyile-joli-njangalkk-prashnamalla.jpg', 'neutral_dasan_resignation.jpg'),
        ('CID Moosa', 'athonnum-illenkilum-dharidryathinu-kuravonnum-illallo.jpg', 'neutral_dharidryam.jpg'),
        ('Punjabi House', 'ariyaan-paadillanjittu-chodikkukaya-randu-varshamaayi-ivide-alakkum-nanayum-onnumille.jpg', 'neutral_alakkum_nanayum.jpg'),
        ('Kalyanaraman', 'alla-ernakulam-jilla-collector-mindaathe-kutthi-kayattedo.jpg', 'neutral_collector_kutthi.jpg'),
        ('Kalyanaraman', 'actually-njaan-modern-aanu.jpg', 'neutral_actually_modern.jpg'),
    ]
}

BASE_URL = 'https://raw.githubusercontent.com/arunpt/malayalam-plain-memes-archive/main/malayalam'
ASSET_BASE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'assets', 'memes')

def download_memes():
    os.makedirs(ASSET_BASE, exist_ok=True)
    download_count = 0

    for category, items in MEME_CATALOG.items():
        cat_dir = os.path.join(ASSET_BASE, category)
        os.makedirs(cat_dir, exist_ok=True)

        for movie, remote_fname, local_alias in items:
            encoded_movie = urllib.parse.quote(movie)
            remote_url = f'{BASE_URL}/{encoded_movie}/{remote_fname}'
            
            subfolder_path = os.path.join(cat_dir, remote_fname)
            root_path = os.path.join(ASSET_BASE, local_alias)

            try:
                req = urllib.request.Request(remote_url, headers={'User-Agent': 'Mozilla/5.0'})
                with urllib.request.urlopen(req) as resp:
                    data = resp.read()
                    if len(data) > 1000:
                        # Save in subfolder
                        with open(subfolder_path, 'wb') as f:
                            f.write(data)
                        # Save also in root of assets/memes for flat searches
                        with open(root_path, 'wb') as f:
                            f.write(data)
                        
                        # Validate with PIL
                        with Image.open(root_path) as img:
                            w, h = img.size
                        print(f"Downloaded [{category.upper()}]: {local_alias} ({len(data)} bytes, {w}x{h})")
                        download_count += 1
                    else:
                        print(f"Skipping tiny file: {remote_fname}")
            except Exception as e:
                print(f"Error downloading {remote_fname}: {e}")

    print(f"\nSuccessfully downloaded and validated {download_count} real Malayalam meme artifacts!")

if __name__ == '__main__':
    download_memes()
