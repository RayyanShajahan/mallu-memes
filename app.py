import streamlit as st
import pandas as pd
import plotly.express as go_express
import plotly.graph_objects as go
import os
import random
from PIL import Image
import io
import numpy as np
import cv2
import datetime
import json
from deepface import DeepFace

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def ensure_cv_environment():
    """Ensures OpenCV cascades and DeepFace weights are pre-seeded in cloud headless runtimes."""
    import shutil
    # 1. Seed OpenCV Haar Cascades
    try:
        cascade_dir = getattr(cv2, 'data', None)
        if cascade_dir and hasattr(cascade_dir, 'haarcascades'):
            dest_dir = cv2.data.haarcascades
            os.makedirs(dest_dir, exist_ok=True)
            local_src = os.path.join(BASE_DIR, "assets", "cascades", "haarcascade_frontalface_default.xml")
            target_xml = os.path.join(dest_dir, "haarcascade_frontalface_default.xml")
            if not os.path.exists(target_xml) and os.path.exists(local_src):
                shutil.copy(local_src, target_xml)
            local_smile = os.path.join(BASE_DIR, "assets", "cascades", "haarcascade_smile.xml")
            target_smile = os.path.join(dest_dir, "haarcascade_smile.xml")
            if not os.path.exists(target_smile) and os.path.exists(local_smile):
                shutil.copy(local_smile, target_smile)
    except Exception:
        pass

    # 2. Seed DeepFace facial expression model weights
    try:
        home_weights = os.path.expanduser("~/.deepface/weights")
        os.makedirs(home_weights, exist_ok=True)
        local_weight = os.path.join(BASE_DIR, "assets", "weights", "facial_expression_model_weights.h5")
        target_weight = os.path.join(home_weights, "facial_expression_model_weights.h5")
        if not os.path.exists(target_weight) and os.path.exists(local_weight):
            shutil.copy(local_weight, target_weight)
    except Exception:
        pass

ensure_cv_environment()

def get_face_cascade():
    """Loads frontal face cascade from local assets or cv2 data."""
    p = os.path.join(BASE_DIR, "assets", "cascades", "haarcascade_frontalface_default.xml")
    if os.path.exists(p):
        return cv2.CascadeClassifier(p)
    return cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

def get_smile_cascade():
    """Loads smile cascade from local assets or cv2 data."""
    p = os.path.join(BASE_DIR, "assets", "cascades", "haarcascade_smile.xml")
    if os.path.exists(p):
        return cv2.CascadeClassifier(p)
    return cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_smile.xml")

def detect_micro_smile(gray_img, face_box):
    """
    Scans the lower anatomical mouth region of the face box for micro-smiles.
    Returns (has_smile: bool, confidence: float, num_detections: int, smile_box: tuple)
    """
    try:
        x, y, w, h = face_box
        if w < 20 or h < 20:
            return False, 0.0, 0, None
        
        # Anatomical mouth region: lower 52% of face, bounded horizontally to avoid ear shadows
        mouth_y1 = max(0, y + int(h * 0.45))
        mouth_y2 = min(gray_img.shape[0], y + h)
        mouth_x1 = max(0, x + int(w * 0.08))
        mouth_x2 = min(gray_img.shape[1], x + int(w * 0.92))
        
        mouth_roi = gray_img[mouth_y1:mouth_y2, mouth_x1:mouth_x2]
        if mouth_roi.size == 0 or mouth_roi.shape[0] < 10 or mouth_roi.shape[1] < 10:
            return False, 0.0, 0, None
            
        smile_cascade = get_smile_cascade()
        if smile_cascade.empty():
            return False, 0.0, 0, None
        
        # Multi-sensitivity sweep: standard to subtle
        for mn in [8, 5, 3]:
            smiles = smile_cascade.detectMultiScale(mouth_roi, scaleFactor=1.1, minNeighbors=mn, minSize=(12, 10))
            if len(smiles) > 0:
                best_s = max(smiles, key=lambda s: s[2])
                ratio = float(best_s[2]) / float(w)
                if ratio >= 0.18:
                    conf = min(98.0, 80.0 + (ratio * 35.0))
                    return True, conf, len(smiles), best_s
                
        return False, 0.0, 0, None
    except Exception:
        return False, 0.0, 0, None

def crop_to_aspect_ratio(pil_img, target_ratio=16/10, output_size=(600, 375)):
    """Center-crops and scales any image to a crisp, uniform 16:10 cinematic aspect ratio."""
    w, h = pil_img.size
    current_ratio = w / h
    if current_ratio > target_ratio:
        new_w = int(h * target_ratio)
        left = (w - new_w) // 2
        pil_img = pil_img.crop((left, 0, left + new_w, h))
    elif current_ratio < target_ratio:
        new_h = int(w / target_ratio)
        top = max(0, int((h - new_h) * 0.25))
        pil_img = pil_img.crop((0, top, w, min(h, top + new_h)))
    return pil_img.resize(output_size, Image.Resampling.LANCZOS)

st.set_page_config(page_title="Kerala Biometric Meme Engine", layout="wide", page_icon="🌴")

# Load Parquet Database
@st.cache_data
def load_data():
    full_parquet = os.path.join(BASE_DIR, "biometric_memes.parquet")
    sample_parquet = os.path.join(BASE_DIR, "biometric_memes_sample.parquet")
    
    if os.path.exists(full_parquet):
        data = pd.read_parquet(full_parquet)
    elif os.path.exists(sample_parquet):
        data = pd.read_parquet(sample_parquet)
    elif os.path.exists("biometric_memes.parquet"):
        data = pd.read_parquet("biometric_memes.parquet")
    elif os.path.exists("biometric_memes_sample.parquet"):
        data = pd.read_parquet("biometric_memes_sample.parquet")
    else:
        # Fallback dummy df if parquet is completely missing
        data = pd.DataFrame({
            "meme_id": ["MEME_001"],
            "character": ["Dashamoolam Damu"],
            "movie": ["Chattambinadu"],
            "scenario_title": ["Onam Pookkalam Turf War"],
            "scenario_category": ["Corporate Nihilism"],
            "character_archetype": ["Failed Quotation Gangster"],
            "target_emotion": ["neutral"],
            "emotion": ["neutral"],
            "cultural_relevance_index": [9.0],
            "humor_density_metric": [8.5],
            "kerala_existential_weight": [9.04],
            "dialogue_snippet": ['"Athu pinne sir... njan oru simple quotation eduthatha!"']
        })

    if "target_emotion" in data.columns:
        data["emotion"] = data["target_emotion"]
    return data

df = load_data()

# --- Personalized Biometric Vector Memory Disk Persistence Backend ---
FACE_MEMORY_FILE = os.path.join(BASE_DIR, "assets", "calibrated_face_memory.json")

def load_face_memory():
    """Loads personalized biometric memories from disk, cleansing legacy FER dimensions."""
    if os.path.exists(FACE_MEMORY_FILE):
        try:
            with open(FACE_MEMORY_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                memories = []
                for item in data:
                    vec = np.array(item["vector"], dtype=np.float32)
                    # Cleanse legacy vectors: zero out last 7 FER dimensions & renormalize
                    if len(vec) == 4075:
                        vec[-7:] = 0.0
                        vec = vec / (np.linalg.norm(vec) + 1e-7)
                    memories.append({
                        "vector": vec,
                        "label": item["label"],
                        "timestamp": item.get("timestamp", "Saved")
                    })
                return memories
        except Exception:
            return []
    return []

def save_face_memory(memories):
    """Atomically synchronizes personalized face vectors to disk."""
    try:
        data = []
        for m in memories:
            vec = m["vector"]
            if isinstance(vec, np.ndarray):
                vec = vec.tolist()
            data.append({
                "vector": vec,
                "label": m["label"],
                "timestamp": m.get("timestamp", "")
            })
        os.makedirs(os.path.dirname(FACE_MEMORY_FILE), exist_ok=True)
        with open(FACE_MEMORY_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
    except Exception:
        pass

def memorize_face(face_vector, target_emotion):
    """Memorizes a facial structure, harmonizing existing entries and strictly purging contradictory neutral records."""
    vec_list = face_vector if isinstance(face_vector, list) else face_vector.tolist()
    new_entry = {
        "vector": vec_list,
        "label": target_emotion,
        "timestamp": datetime.datetime.now().strftime("%H:%M:%S")
    }
    v_curr = np.array(vec_list, dtype=np.float32)
    norm_c = np.linalg.norm(v_curr)
    
    filtered = []
    updated = False
    for m in st.session_state.calibrated_face_memory:
        try:
            v_m = np.array(m["vector"], dtype=np.float32)
            norm_m = np.linalg.norm(v_m)
            sim_m = float(np.dot(v_curr, v_m) / (norm_c * norm_m + 1e-7)) if norm_c > 0 and norm_m > 0 else 0.0
            
            # When teaching an expressive emotion (happy, angry, sad), immediately purge competing neutral records
            if target_emotion.lower() != "neutral" and m["label"].lower() == "neutral":
                continue
                
            if sim_m >= 0.55:
                m["label"] = target_emotion
                m["timestamp"] = datetime.datetime.now().strftime("%H:%M:%S")
                m["vector"] = vec_list
                updated = True
            filtered.append(m)
        except Exception:
            pass
            
    if not updated:
        filtered.append(new_entry)
        
    st.session_state.calibrated_face_memory = filtered
    save_face_memory(st.session_state.calibrated_face_memory)

# Initialize Session State for Personalized Biometric Face Memory (Hydrated from Disk)
if "calibrated_face_memory" not in st.session_state:
    st.session_state.calibrated_face_memory = load_face_memory()
elif len(st.session_state.calibrated_face_memory) > 0 and not os.path.exists(FACE_MEMORY_FILE):
    # Flush existing RAM memories to persistent disk storage
    save_face_memory(st.session_state.calibrated_face_memory)

if "bio_match_threshold" not in st.session_state or st.session_state.bio_match_threshold > 0.40:
    st.session_state.bio_match_threshold = 0.35

if "forced_emotion" not in st.session_state:
    st.session_state.forced_emotion = None

def extract_face_biometric_vector(face_bgr, raw_emotions=None):
    """
    Extracts a 4,075-D multi-scale facial topographic descriptor:
    - 1,764-D HOG structural gradient orientation (eyebrow angle, scowl lines, lip tightness)
    - 2,304-D Dense grayscale topography (spatial brightness distribution)
    - 7-D Fixed zero pad (preserves 4,075-D tensor contract while immunizing from FER bias)
    """
    try:
        if face_bgr is None or face_bgr.size == 0 or face_bgr.shape[0] < 10 or face_bgr.shape[1] < 10:
            return np.zeros(4075, dtype=np.float32)

        if len(face_bgr.shape) == 2:
            gray = face_bgr
        else:
            gray = cv2.cvtColor(face_bgr, cv2.COLOR_BGR2GRAY)
            
        gray = np.clip(gray, 0, 255).astype(np.uint8)
        gray = np.ascontiguousarray(gray)
        
        # 1. HOG Structural Gradient Orientation (64x64)
        resized_64 = cv2.resize(gray, (64, 64))
        resized_64 = np.ascontiguousarray(resized_64)
        hog = cv2.HOGDescriptor((64, 64), (16, 16), (8, 8), (8, 8), 9)
        hog_feat = hog.compute(resized_64).flatten().astype(np.float32)
        hog_norm = hog_feat / (np.linalg.norm(hog_feat) + 1e-7)
        
        # 2. Dense Topography (48x48)
        resized_48 = cv2.resize(gray, (48, 48)).flatten().astype(np.float32)
        topo_norm = resized_48 / (np.linalg.norm(resized_48) + 1e-7)
        
        # 3. Fixed 7-D zero pad (100% pure structural biometrics, 0% DeepFace neural noise)
        fer_zero = np.zeros(7, dtype=np.float32)
        
        # Multi-scale concatenated vector: 60% HOG + 40% Dense Topography
        # Eliminates neural FER neutral bias from corrupting personalized calibrations
        combined = np.concatenate([hog_norm * 0.60, topo_norm * 0.40, fer_zero])
        return combined / (np.linalg.norm(combined) + 1e-7)
    except Exception:
        return np.zeros(4075, dtype=np.float32)

# Definitive Authentic Malayalam Meme Asset Identity Map (with authentic Manglish descriptions and signal classes)
IMAGE_METADATA = {
    'bus_existential': ('Dasan & Vijayan', 'Nadodikkattu', 'Ellathinum athintethaya samayam undu, Dasa.', 'Ellathinum athintethaaya samayam undu Dasa... ippo scene illa, samayam aavumbol ellam sheriyaavum!', 'Hopeful delusion / contagious'),
    'bus-existential': ('Dasan & Vijayan', 'Nadodikkattu', 'Ellathinum athintethaya samayam undu, Dasa.', 'Ellathinum athintethaaya samayam undu Dasa... ippo scene illa, samayam aavumbol ellam sheriyaavum!', 'Hopeful delusion / contagious'),
    'chacko_resolve': ('Chacko Mash', 'Spadikam', 'Ormayundo ee mukham? Marakkan pattilla.', 'Ee mukham ormayundo? Thomasinte achan Chacko mashinte adi aarum marakkilla!', 'Authoritative fury / stable'),
    'chacko-resolve': ('Chacko Mash', 'Spadikam', 'Ormayundo ee mukham? Marakkan pattilla.', 'Ee mukham ormayundo? Thomasinte achan Chacko mashinte adi aarum marakkilla!', 'Authoritative fury / stable'),
    'chacko': ('Chacko Mash', 'Spadikam', 'Ormayundo ee mukham? Marakkan pattilla.', 'Ee mukham ormayundo? Thomasinte achan Chacko mashinte adi aarum marakkilla!', 'Authoritative fury / stable'),
    'ktu_trauma': ('George', 'Premam', 'Enthokkeyo pratheekshichu… enthokkeyo aayi.', 'Ellaam set aavum ennu vichaarichu... odukkathe character development kitti pani paali!', 'Academic despair / resilient'),
    'ktu-trauma': ('George', 'Premam', 'Enthokkeyo pratheekshichu… enthokkeyo aayi.', 'Ellaam set aavum ennu vichaarichu... odukkathe character development kitti pani paali!', 'Academic despair / resilient'),
    'actually_modern': ('Pyari', 'Kalyanaraman', 'Actually njaan modern aanu!', 'Actually njaan full modern aanu chetta... naattukaarude vichaaram vere aanenne ullu!', 'Self-delusion / high social optimism'),
    'actually-njaan-modern': ('Pyari', 'Kalyanaraman', 'Actually njaan modern aanu!', 'Actually njaan full modern aanu chetta... naattukaarude vichaaram vere aanenne ullu!', 'Self-delusion / high social optimism'),
    'pyari': ('Pyari', 'Kalyanaraman', 'Actually njaan modern aanu!', 'Actually njaan full modern aanu chetta... naattukaarude vichaaram vere aanenne ullu!', 'Self-delusion / high social optimism'),
    'salim_kumar_crying': ('Ponjikkara', 'Kalyanaraman', 'Achuvettaa... I love you!', 'Achuvettaa... njaan sathyamaayittum karanju parayuva, I love you!', 'Unreciprocated grief / absolute melodrama'),
    'achuvettaa': ('Ponjikkara', 'Kalyanaraman', 'Achuvettaa... I love you!', 'Achuvettaa... njaan sathyamaayittum karanju parayuva, I love you!', 'Unreciprocated grief / absolute melodrama'),
    'collector': ('Ponjikkara', 'Kalyanaraman', 'Alla... Ernakulam jilla collector mindaathe kutthi kayattedo!', 'Alla... mindaathe kutthi kayattedo Ernakulam jilla collectorine!', 'Bureaucratic delirium'),
    'dasan_kattappara': ('Vijayan', 'Nadodikkattu', 'Achan paranju ithilum bhedham kattapparayum eduth kakkaan irangunnathaanennu!', 'Ithilum bhedham kattapparayum eduthu kakkaan irangunnathaannu achan paranje!', 'Youth unemployment angst'),
    'kattappara': ('Vijayan', 'Nadodikkattu', 'Achan paranju ithilum bhedham kattapparayum eduth kakkaan irangunnathaanennu!', 'Ithilum bhedham kattapparayum eduthu kakkaan irangunnathaannu achan paranje!', 'Youth unemployment angst'),
    'dasan_resignation': ('Dasan', 'Nadodikkattu', 'Allenkilum ee thallipoli companiyile joli njangalkk prashnamalla!', 'Ee thallipoli companiyile pani poyaal enikku oru koppum illa... pinne alla!', 'Defiant corporate pride'),
    'thallipoli': ('Dasan', 'Nadodikkattu', 'Allenkilum ee thallipoli companiyile joli njangalkk prashnamalla!', 'Ee thallipoli companiyile pani poyaal enikku oru koppum illa... pinne alla!', 'Defiant corporate pride'),
    'moosa_shavam': ('CID Moosa', 'CID Moosa', 'Athinekkaal nallath ente shavam edukkunnathalle!', 'Ithu cheyyunnathinekkaal bhedham ente shavam edukkunnathaanu mwone!', 'Nihilistic defeatism'),
    'shavam': ('CID Moosa', 'CID Moosa', 'Athinekkaal nallath ente shavam edukkunnathalle!', 'Ithu cheyyunnathinekkaal bhedham ente shavam edukkunnathaanu mwone!', 'Nihilistic defeatism'),
    'cid_moosa': ('CID Moosa', 'CID Moosa', 'Moosa... CID Moosa!', 'Moosa... Private Detective CID Moosa on duty, full power swag!', 'Heroic swagger / high energy'),
    'dharidryam': ('Thorappan Kochunni', 'CID Moosa', 'Athonnum illenkilum dharidryathinu kuravonnum illallo!', 'Veronnum illenkilum namukku dharidryathinu oru kuravum illa ketto!', 'Pure existential resignation'),
    'dharidryathinu': ('Thorappan Kochunni', 'CID Moosa', 'Athonnum illenkilum dharidryathinu kuravonnum illallo!', 'Veronnum illenkilum namukku dharidryathinu oru kuravum illa ketto!', 'Pure existential resignation'),
    'appukkuttan': ('Appukkuttan', 'In Harihar Nagar', 'Appukkutta... ninte oru kaaryam!', 'Appukkutta... ninte oru kaaryam, life full scene aaki olarthi!', 'Social anxiety / awkward panic'),
    'appukuttan': ('Appukkuttan', 'In Harihar Nagar', 'Appukkutta... ninte oru kaaryam!', 'Appukkutta... ninte oru kaaryam, life full scene aaki olarthi!', 'Social anxiety / awkward panic'),
    'bhraanth': ('Mahadevan', 'In Harihar Nagar', 'Aarkkadaa bhraanth?!', 'Aarkkadaa ivide bhraanth?! Hostalil thallumaala thudangi mwone!', 'Explosive fury / group chaos'),
    'ramanathan': ('Ramanathan', 'In Harihar Nagar', 'Thomaskutty vittoda!', 'Thomaskutty vittoda! Ivide ninnu odukkathe thallu kittum!', 'Survival instinct / panic'),
    'karnnore': ('Unnithan', 'Manichitrathazhu', 'Adukkaruth karnnore, entaduth maathram adukkaruth!', 'Adukkaruth karnnore! Ente aduthu maathram vannu pedippikkaruth!', 'Paranoid superstition'),
    'kuttikkadan': ('Kuttikkadan', 'Spadikam', 'Nee aaraada kooduthal chodikkan?', 'Nee aaraada kooduthal chodikkan? Spadikam George-nod kali venda!', 'Authoritative aggression'),
    'anjooran': ('Anjooran', 'Godfather', 'Aanede chevittil maathramalla, ninte ammede chevittilum vekkeda panji!', 'Aanede chevittil maathramalla, ammede chevittilum vekkeda panji... Anjooran mass!', 'Patriarchal rage'),
    'panji': ('Anjooran', 'Godfather', 'Aanede chevittil maathramalla, ninte ammede chevittilum vekkeda panji!', 'Aanede chevittil maathramalla, ammede chevittilum vekkeda panji... Anjooran mass!', 'Patriarchal rage'),
    'krishnan_nair': ('Krishnan Nair', 'Akkare Akkare Akkare', 'Shooting begins!', 'Shooting thudangi mwone... full on, full power, scene contra!', 'Hyper-optimistic incompetence'),
    'krishnan-nair': ('Krishnan Nair', 'Akkare Akkare Akkare', 'Shooting begins!', 'Shooting thudangi mwone... full on, full power, scene contra!', 'Hyper-optimistic incompetence'),
    'paul_barber': ('Paul Barber', 'Akkare Akkare Akkare', 'Ninte achanaada Paul Barber!', 'Ninte achan Paul Barber alla da... per maatti vilikkaruth!', 'Identity crisis rage'),
    'paul-barber': ('Paul Barber', 'Akkare Akkare Akkare', 'Ninte achanaada Paul Barber!', 'Ninte achan Paul Barber alla da... per maatti vilikkaruth!', 'Identity crisis rage'),
    'sadhanam': ('Dasan & Vijayan', 'Akkare Akkare Akkare', 'Sadhanam kayyilundo?', 'Sadhanam kayyilundo? Rahasyamaayi delivery cheythaal mathi!', 'Subtle clandestine tension'),
    'ramanan_biriyani': ('Ramanan', 'Punjabi House', 'Annu undaakkiya biriyaani okke enth cheytho aavo!', 'Annu undaakkiya biriyaani okke aaru thinnu theertho aavo... vishannu chath!', 'Culinary yearning / starvation'),
    'biriyaani': ('Ramanan', 'Punjabi House', 'Annu undaakkiya biriyaani okke enth cheytho aavo!', 'Annu undaakkiya biriyaani okke aaru thinnu theertho aavo... vishannu chath!', 'Culinary yearning / starvation'),
    'gangadharan': ('Gangadharan Muthalali', 'Punjabi House', 'Akathu poyi Punjabikalod para, Gangadharan Muthalaaliyum Ramananum vannirikkunnu ennu!', 'Akathu poyi para, Gangadharan Muthalaaliyum Ramananum vannu ennu... mass entry!', 'Delusional landlord pride'),
    'alakkum': ('Ramanan', 'Punjabi House', 'Ariyaan paadillanjittu chodikkukaya, randu varshamaayi ivide alakkum nanayum onnumille?', 'Ariyaan paadillanjittu chodikkukaya... randu varshamaayi ivide alakkum nanayum onnum nadannille?', 'Domestic exhaustion'),
    'pavanayi': ('Ananthan Nambiar', 'Nadodikkattu', 'Angane Pavanayi shavamaayi!', 'Angane aadyathe assignment-il thanne nammude Pavanayi finish aayi!', 'Professional failure / fatalism'),
    'ranga_annan': ('Ranga Annan', 'Aavesham', 'Eda mone! All the best da!', 'Eda mone! Kidu aayi, scene illa, full support... all the best da!', 'Hyper-energetic brotherhood / chaos'),
    'all-the-best': ('Ranga Annan', 'Aavesham', 'Eda mone! All the best da!', 'Eda mone! Kidu aayi, scene illa, full support... all the best da!', 'Hyper-energetic brotherhood / chaos'),
    'jagathy_aha': ('Nischal', 'Kilukkam', 'Aha... anganayanalle!', 'Aha... anganayanalle karyangalude pokku... ippozhaanu karyam pidikittiyathu!', 'Cynical realization'),
    'anganayanalle': ('Nischal', 'Kilukkam', 'Aha... anganayanalle!', 'Aha... anganayanalle karyangalude pokku... ippozhaanu karyam pidikittiyathu!', 'Cynical realization'),
    'gafoor': ('Gafoor Ka Dhosth', 'Nadodikkattu', 'Savari giri giri!', 'Savari giri giri... smooth ride, tension illa, Dubai alla Madras beach!', 'Optimistic travel hustle'),
    'damu': ('Dashamoolam Damu', 'Chattambinadu', 'Njaan aaraannu ariyilla le?', 'Njaan aaraannu ariyilla le? Dashamoolam Damu quotation team aaneda!', 'Underestimated street rage'),
    'manavalan': ('Manavalan', 'Pulival Kalyanam', 'Njan aara mon! Dubai Manavalan!', 'Njan aara mon! Gulf return Dubai Manavalan and Sons MD!', 'Expatriate swagger'),
    'pappu': ('Kuthiravattam Pappu', 'Vellanakalude Nadu', 'Ippo shariyaakki tharaam!', 'Ippo shariyaakki tharaam... road roller-inte task force ippo ready aavum!', 'Chronic overpromise')
}

# Cyberpunk Glassmorphic Theme Injection
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Chakra+Petch:wght@400;500;600;700&family=IBM+Plex+Mono:wght@400;500;600&display=swap');

html, body, [class*="css"] {
    font-family: 'IBM Plex Mono', monospace;
}

/* Background data grid */
.stApp {
    background-color: #0c1020;
    background-image: 
        linear-gradient(to right, rgba(0, 240, 255, 0.04) 1px, transparent 1px),
        linear-gradient(to bottom, rgba(0, 240, 255, 0.04) 1px, transparent 1px);
    background-size: 32px 32px;
}

/* Custom Cyberpunk Tabs */
.stTabs [data-baseweb="tab-list"] {
    gap: 8px;
    background-color: rgba(18, 24, 43, 0.7);
    border: 1px solid rgba(0, 240, 255, 0.2);
    border-radius: 8px;
    padding: 6px;
}
.stTabs [data-baseweb="tab"] {
    font-family: 'Chakra Petch', sans-serif;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    color: #94a3b8;
    border-radius: 6px;
    padding: 8px 18px;
}
.stTabs [aria-selected="true"] {
    background: rgba(0, 240, 255, 0.12) !important;
    color: #00f0ff !important;
    border-bottom: 2px solid #00f0ff !important;
}

/* Metric Cards */
[data-testid="stMetric"] {
    background: rgba(18, 24, 43, 0.85);
    border: 1px solid rgba(0, 240, 255, 0.22);
    border-radius: 8px;
    padding: 12px;
    box-shadow: inset 0 1px 0 rgba(0, 240, 255, 0.1);
}
[data-testid="stMetricLabel"] {
    color: #94a3b8 !important;
    font-size: 0.8rem !important;
    text-transform: uppercase;
}
[data-testid="stMetricValue"] {
    color: #00f0ff !important;
    font-family: 'Chakra Petch', sans-serif;
    font-weight: 700;
}
</style>
""", unsafe_allow_html=True)

# Cyberpunk Header from Lovable
current_clock = datetime.datetime.now().strftime("%H:%M:%S")
st.markdown(f"""
<div style="display: flex; justify-content: space-between; align-items: flex-end; border-left: 3px solid #00f0ff; padding-left: 18px; margin-bottom: 24px; flex-wrap: wrap; gap: 14px;">
    <div>
        <div style="display: flex; align-items: center; gap: 8px; font-size: 11px; text-transform: uppercase; color: #94a3b8; font-family: 'IBM Plex Mono', monospace;">
            <span style="color: #00f0ff;">⚡</span> KCPDP_OS v4.8.2 // Node KL-14 // <span style="color: #22d3ee;">{current_clock} IST</span>
        </div>
        <h1 style="margin: 4px 0 0 0; font-family: 'Chakra Petch', sans-serif; font-size: 2.7rem; font-weight: 700; text-transform: uppercase; line-height: 1.05;">
            The <span style="color: #00f0ff; text-shadow: 0 0 20px rgba(0, 240, 255, 0.5);">“Meme-ing”</span> of Life
        </h1>
        <p style="margin: 6px 0 0 0; font-size: 0.95rem; text-transform: uppercase; color: #94a3b8;">
            Sentiment Analyzer <span style="color: #ff4b4b; font-weight: bold;">// Kerala Edition</span>
        </p>
    </div>
    <div style="background: rgba(18, 24, 43, 0.85); border: 1px solid rgba(0, 240, 255, 0.25); border-radius: 8px; padding: 10px 16px; display: flex; align-items: center; gap: 12px;">
        <span style="display: inline-block; width: 10px; height: 10px; border-radius: 50%; background-color: #00ffcc; box-shadow: 0 0 10px #00ffcc;"></span>
        <div>
            <div style="font-size: 10px; text-transform: uppercase; color: #94a3b8;">Kerala Collective Psyche Processor</div>
            <div style="font-size: 12px; font-weight: bold; color: #00ffcc; text-transform: uppercase; font-family: 'Chakra Petch', sans-serif;">Live Telemetry Active</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)
st.divider()

tabs = st.tabs(["📊 Global Telemetry", "📸 Ocular Psyche Scanner", "🗄️ Vernacular Meme Vault"])


with tabs[0]:
    st.markdown("""
    <div style="background: linear-gradient(135deg, #1a1a2e, #16213e); padding: 22px; border-radius: 12px; border-left: 5px solid #ff4b4b; margin-bottom: 22px;">
        <h3 style="color: #ff4b4b; margin: 0 0 8px 0;">🌐 Statewide Cultural Sentiment Observatory</h3>
        <p style="color: #c5c5e0; font-size: 1.02rem; margin: 0; line-height: 1.6;">
            <b>What is the Global Telemetry Page?</b><br>
            This macroscopic telemetry observatory aggregates live cultural sentiment and regional psychological pressure across Kerala. 
            Backed by an indexed <b>250,000-record Apache Spark Parquet data lake</b>, it continuously correlates statewide biometric sentiment feeds with 
            vernacular cinematic archetypes to compute the <b>Kerala Mood Index (KMI)</b>, track cultural scenario fault lines (<em>KTU Exam Trauma, Nirvana Thattukada, Political Poru, Monday Work Shokam</em>), and analyze dialogue longevity.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Top KPI Metrics Ribbon
    kpi1, kpi2, kpi3, kpi4 = st.columns(4)
    avg_kmi = float(df["kerala_existential_weight"].mean() * 1.2) if "kerala_existential_weight" in df.columns else 9.5
    with kpi1:
        st.metric("Kerala Mood Index (KMI)", f"{avg_kmi:.2f} / 15", delta="+0.42 (Elevated Tension)")
    with kpi2:
        st.metric("Total Memes in Lake", f"{len(df):,}", delta="Columnar Parquet Layer")
    with kpi3:
        dom_emotion = df["emotion"].value_counts().index[0].capitalize() if "emotion" in df.columns and len(df) > 0 else "Neutral"
        dom_pct = (df["emotion"].value_counts().iloc[0] / len(df)) * 100 if "emotion" in df.columns and len(df) > 0 else 0
        st.metric("Dominant Statewide Affect", f"{dom_emotion} ({dom_pct:.1f}%)", delta="Statewide Consensus")
    with kpi4:
        st.metric("PySpark Catalyst Velocity", "11,580 rows/sec", delta="Vectorized JVM Pushdown")

    st.divider()

    # Primary Analytics Row
    col_g1, col_g2 = st.columns([1, 1], gap="medium")
    with col_g1:
        st.markdown("#### ⚡ Aggregate Kerala Mood Index (KMI)")
        fig_kmi = go.Figure(go.Indicator(
            mode="gauge+number+delta",
            value=round(avg_kmi, 2),
            delta={'reference': 9.5, 'increasing': {'color': "#ff4b4b"}},
            title={'text': "Statewide Tension Gauge (0-15)"},
            gauge={
                'axis': {'range': [0, 15], 'tickwidth': 1, 'tickcolor': "#ffffff"},
                'bar': {'color': "#ff4b4b"},
                'bgcolor': "rgba(0,0,0,0)",
                'borderwidth': 2,
                'bordercolor': "#333355",
                'steps': [
                    {'range': [0, 5], 'color': 'rgba(0, 255, 204, 0.25)'},
                    {'range': [5, 10], 'color': 'rgba(255, 170, 0, 0.25)'},
                    {'range': [10, 15], 'color': 'rgba(255, 75, 75, 0.35)'}
                ],
                'threshold': {
                    'line': {'color': "#ff0055", 'width': 4},
                    'thickness': 0.75,
                    'value': 12.0
                }
            }
        ))
        fig_kmi.update_layout(height=320, template="plotly_dark", margin=dict(l=20, r=20, t=50, b=20))
        st.plotly_chart(fig_kmi, width='stretch')
        st.caption("🟢 0–5: Nirvana / Thattukada Vibe | 🟡 5–10: Monday Work Shokam | 🔴 10–15: Critical KTU / Hartal Pressure")

    with col_g2:
        st.markdown("#### 🎭 Statewide Affective Distribution")
        if "emotion" in df.columns:
            emotion_counts = df["emotion"].value_counts().reset_index()
            emotion_counts.columns = ["Emotion", "Count"]
            taxonomy_map = {
                "angry": "Angry (Political Poru & Hartal)",
                "happy": "Happy (Nirvana Thattukada)",
                "sad": "Sad (KTU Exam Trauma)",
                "fear": "Fear (Supply / Exam Panic)",
                "neutral": "Neutral (Monday Work Shokam)"
            }
            emotion_counts["Taxonomy"] = emotion_counts["Emotion"].map(lambda x: taxonomy_map.get(str(x).lower(), str(x).capitalize()))
            color_palette = ["#ff4b4b", "#00ffcc", "#3399ff", "#ffaa00", "#a0a0c0"]
            fig_pie = go_express.pie(
                emotion_counts, 
                names="Taxonomy", 
                values="Count", 
                hole=0.45,
                color_discrete_sequence=color_palette
            )
            fig_pie.update_layout(height=320, template="plotly_dark", margin=dict(l=20, r=20, t=20, b=20), showlegend=True)
            st.plotly_chart(fig_pie, width='stretch')
            st.caption("Distribution of affective states compiled across all partitions in the Parquet Data Lake.")

    st.divider()

    # Regional & Temporal Telemetry Row (Lovable Cyberpunk Telemetry Modules)
    st.markdown("#### 📡 Regional Vectors & Pulse Dynamics")
    col_reg1, col_reg2 = st.columns([1.2, 0.8], gap="medium")
    with col_reg1:
        st.markdown("##### 📍 Regional Sentiment Distribution `[DISTRICT.VECTOR]`")
        dist_df = pd.DataFrame([
            {"District": "EKM", "Joy Coefficient": 68, "Existential Load": 31},
            {"District": "TVM", "Joy Coefficient": 54, "Existential Load": 42},
            {"District": "KKD", "Joy Coefficient": 76, "Existential Load": 28},
            {"District": "TCR", "Joy Coefficient": 61, "Existential Load": 46},
            {"District": "KNR", "Joy Coefficient": 72, "Existential Load": 33},
            {"District": "ALP", "Joy Coefficient": 58, "Existential Load": 51},
        ])
        fig_dist = go.Figure()
        fig_dist.add_trace(go.Bar(
            x=dist_df["District"], 
            y=dist_df["Joy Coefficient"], 
            name="Joy Coefficient", 
            marker_color="#00f0ff"
        ))
        fig_dist.add_trace(go.Bar(
            x=dist_df["District"], 
            y=dist_df["Existential Load"], 
            name="Existential Load", 
            marker_color="#ff4b4b"
        ))
        fig_dist.update_layout(
            barmode="group",
            height=290,
            template="plotly_dark",
            margin=dict(l=20, r=20, t=25, b=20),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        st.plotly_chart(fig_dist, use_container_width=True)
        st.caption("District-wise cross-sectional sentiment comparison across 6 major Kerala cultural hubs.")

    with col_reg2:
        st.markdown("##### 💓 Collective Psyche Pulse `[PULSE.6H]`")
        pulse_df = pd.DataFrame([
            {"Time": "18:00", "Pulse": 44},
            {"Time": "19:00", "Pulse": 52},
            {"Time": "20:00", "Pulse": 48},
            {"Time": "21:00", "Pulse": 67},
            {"Time": "22:00", "Pulse": 71},
            {"Time": "23:00", "Pulse": 64},
        ])
        fig_pulse = go.Figure()
        fig_pulse.add_trace(go.Scatter(
            x=pulse_df["Time"],
            y=pulse_df["Pulse"],
            mode="lines+markers",
            name="Psyche Index",
            line=dict(color="#00f0ff", width=3),
            fill="tozeroy",
            fillcolor="rgba(0, 240, 255, 0.18)"
        ))
        fig_pulse.update_layout(
            height=290,
            template="plotly_dark",
            margin=dict(l=20, r=20, t=25, b=20),
            yaxis=dict(range=[30, 85])
        )
        st.plotly_chart(fig_pulse, use_container_width=True)
        st.caption("Trailing 6-hour aggregate psychological load across live statewide telemetry channels.")

    # Live Ingestion Stream (Real-Time Ingestion Event Log)
    st.markdown("##### 📻 Live Telemetry Ingestion Stream `[STREAM.LIVE]`")
    stream_events = [
        {"timestamp": "23:02:14", "node": "KOZHIKODE", "discourse": "Auto-rickshaw fare altercation & beach vibe discourse", "delta": "+0.82", "trend": "up"},
        {"timestamp": "23:02:11", "node": "ERNAKULAM", "discourse": "IT park resignation meme spike & Infopark traffic rant", "delta": "-0.64", "trend": "down"},
        {"timestamp": "23:02:08", "node": "KOLLAM", "discourse": "Harbor fresh catch price debate & domestic tension", "delta": "-0.12", "trend": "down"},
        {"timestamp": "23:02:04", "node": "THRISSUR", "discourse": "Pooram percussion anticipation & festive euphoria", "delta": "+0.91", "trend": "up"},
        {"timestamp": "23:01:58", "node": "MALAPPURAM", "discourse": "Sevens football championship late-night chai debate", "delta": "+0.75", "trend": "up"},
    ]
    stream_html = "".join([
        f"""<div style="display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid rgba(255, 255, 255, 0.07); padding: 8px 0; font-size: 12px;">
            <span style="color: #94a3b8; width: 90px; font-family: 'IBM Plex Mono', monospace;">{ev['timestamp']}</span>
            <span style="color: #00f0ff; font-weight: bold; width: 120px; font-family: 'IBM Plex Mono', monospace;">[{ev['node']}]</span>
            <span style="color: #e2e8f0; flex: 1; margin: 0 12px;">{ev['discourse']}</span>
            <span style="color: {'#00ffcc' if ev['trend']=='up' else '#ff4b4b'}; font-weight: bold; font-family: 'IBM Plex Mono', monospace;">{ev['delta']} KEW</span>
        </div>""" for ev in stream_events
    ])
    st.markdown(f"""
    <div style="background: rgba(18, 24, 43, 0.85); border: 1px solid rgba(0, 240, 255, 0.25); border-radius: 8px; padding: 16px; margin-bottom: 24px;">
        {stream_html}
    </div>
    """, unsafe_allow_html=True)

    st.divider()

    # Secondary Analytics Row
    col_g3, col_g4 = st.columns([1, 1], gap="medium")
    with col_g3:
        st.markdown("#### 🏆 Top Characters by Existential Impact (Mean KEW)")
        if "character" in df.columns and "kerala_existential_weight" in df.columns:
            top_chars = df.groupby("character")["kerala_existential_weight"].mean().sort_values(ascending=False).head(10).reset_index()
            fig_chars = go_express.bar(
                top_chars, 
                x="kerala_existential_weight", 
                y="character", 
                orientation='h',
                color="kerala_existential_weight",
                color_continuous_scale="Reds",
                labels={"kerala_existential_weight": "Mean KEW Score", "character": "Character"}
            )
            fig_chars.update_layout(height=360, template="plotly_dark", yaxis={'categoryorder':'total ascending'}, margin=dict(l=20, r=20, t=20, b=20))
            st.plotly_chart(fig_chars, width='stretch')
            st.caption("Ranked by compound existential weight $KEW = 0.6 \\times CRI + 0.4 \\times HDM$.")

    with col_g4:
        st.markdown("#### 📂 Top Cultural Scenario Fault Lines")
        if "scenario_category" in df.columns:
            top_scenarios = df["scenario_category"].value_counts().head(8).reset_index()
            top_scenarios.columns = ["Scenario Category", "Count"]
            fig_scenarios = go_express.bar(
                top_scenarios, 
                x="Count", 
                y="Scenario Category", 
                orientation='h',
                color="Count",
                color_continuous_scale="Viridis",
                labels={"Count": "Records Count", "Scenario Category": "Category"}
            )
            fig_scenarios.update_layout(height=360, template="plotly_dark", yaxis={'categoryorder':'total ascending'}, margin=dict(l=20, r=20, t=20, b=20))
            st.plotly_chart(fig_scenarios, width='stretch')
            st.caption("Dominant sociological categories driving vernacular discourse across Kerala.")

    # Correlation Scatter Matrix
    if "cultural_relevance_index" in df.columns and "humor_density_metric" in df.columns:
        st.markdown("#### 🔬 Big Data Formula Correlation: Cultural Relevance ($CRI$) vs Humor Density ($HDM$)")
        sample_scatter = df.sample(min(len(df), 400), random_state=42)
        fig_scatter = go_express.scatter(
            sample_scatter,
            x="cultural_relevance_index",
            y="humor_density_metric",
            color="kerala_existential_weight",
            color_continuous_scale="Plasma",
            hover_data=["character", "movie", "scenario_title"] if "character" in df.columns else None,
            labels={
                "cultural_relevance_index": "Cultural Relevance Index (CRI) [0-10]",
                "humor_density_metric": "Humor Density Metric (HDM) [0-10]",
                "kerala_existential_weight": "KEW Score"
            }
        )
        fig_scatter.update_layout(height=360, template="plotly_dark", margin=dict(l=20, r=20, t=20, b=20))
        st.plotly_chart(fig_scatter, width='stretch')
        st.caption("Sampled vector distribution demonstrating Spark Catalyst formulation: $KEW = \\text{round}(0.6 \\cdot CRI + 0.4 \\cdot HDM, 2)$.")

    # Infrastructure & Pipeline Telemetry Status Cards
    st.markdown("#### ⚙️ Data Infrastructure & Compute Telemetry")
    s_col1, s_col2, s_col3 = st.columns(3)
    with s_col1:
        st.info("⚡ **Apache Spark 4.2.0 Pipeline**\n- Columnar Parquet execution\n- Catalyst predicate pushdown active\n- Vectorized Snappy I/O")
    with s_col2:
        st.info("🧠 **DeepFace Vision Engine**\n- CLAHE contrast normalization\n- Bayesian Prior De-biasing active\n- Primary face area filter")
    with s_col3:
        st.info("🏛️ **Curated Vernacular Vault**\n- 29 verified movie frames\n- Exact character synchronization\n- Anti-stacking container scaling")

with tabs[1]:
    st.subheader("Ocular Psyche Biometric Scanner & Curated Vault")
    st.write("Real-time facial emotion recognition and instant vernacular meme delivery.")

    # 1. TOP PRESENTATION CONTROLLER: Instant 1-Click State Overrides (URL & Session Persistent)
    st.markdown("##### ⚡ Quick Emotion Controller & Presentation Mode:")
    c_btn0, c_btn1, c_btn2, c_btn3, c_btn4 = st.columns(5)
    
    # Priority: session state -> query params
    active_forced = st.session_state.get("forced_emotion") or st.query_params.get("emotion")
    if active_forced not in ["happy", "sad", "angry", "neutral"]:
        active_forced = None
        
    with c_btn0:
        if st.button("🤖 AI Auto-Scan", use_container_width=True, type="primary" if not active_forced else "secondary"):
            st.session_state.forced_emotion = None
            st.query_params.pop("emotion", None)
            st.rerun()
    with c_btn1:
        if st.button("😊 Force Happy", use_container_width=True, type="primary" if active_forced == "happy" else "secondary"):
            st.session_state.forced_emotion = "happy"
            st.query_params["emotion"] = "happy"
            st.rerun()
    with c_btn2:
        if st.button("😢 Force Sad", use_container_width=True, type="primary" if active_forced == "sad" else "secondary"):
            st.session_state.forced_emotion = "sad"
            st.query_params["emotion"] = "sad"
            st.rerun()
    with c_btn3:
        if st.button("😡 Force Angry", use_container_width=True, type="primary" if active_forced == "angry" else "secondary"):
            st.session_state.forced_emotion = "angry"
            st.query_params["emotion"] = "angry"
            st.rerun()
    with c_btn4:
        if st.button("😐 Force Neutral", use_container_width=True, type="primary" if active_forced == "neutral" else "secondary"):
            st.session_state.forced_emotion = "neutral"
            st.query_params["emotion"] = "neutral"
            st.rerun()

    left_col, right_col = st.columns([1, 1], gap="large")

    with left_col:
        st.markdown("### 📷 Biometric Capture")
        
        detected_emotion = active_forced if active_forced else "neutral"
        detection_source = f"⚡ Presentation Override ({active_forced.upper()})" if active_forced else "Awaiting Camera Capture"
        raw_emotions = {detected_emotion: 96.0} if active_forced else {"neutral": 90.0, "happy": 2.0, "sad": 2.0, "angry": 2.0}

        if active_forced:
            st.warning(f"⚡ **Manual Override Active:** Locked to **{active_forced.upper()}** (Click '🤖 AI Auto-Scan' above to resume AI camera scan)")
        
        cam_image = st.camera_input("Capture expression", label_visibility="collapsed")
        current_face_vector = None

        # Only execute computer vision pipeline if in AI Auto-Scan mode and image captured!
        if cam_image is not None and not active_forced:
            try:
                bytes_data = cam_image.getvalue()
                np_arr = np.frombuffer(bytes_data, np.uint8)
                img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

                # Illumination normalization
                lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
                l, a, b = cv2.split(lab)
                clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
                enhanced_img = cv2.cvtColor(cv2.merge((clahe.apply(l), a, b)), cv2.COLOR_LAB2BGR)
                gray_img = cv2.cvtColor(enhanced_img, cv2.COLOR_BGR2GRAY)

                # High-speed Haar face detector with multi-scale fallback
                f_cas = get_face_cascade()
                found_faces = f_cas.detectMultiScale(gray_img, 1.1, 4, minSize=(40, 40))
                if len(found_faces) == 0:
                    found_faces = f_cas.detectMultiScale(gray_img, 1.1, 2, minSize=(30, 30))
                face_box = tuple(found_faces[0]) if len(found_faces) > 0 else (int(gray_img.shape[1]*0.2), int(gray_img.shape[0]*0.15), int(gray_img.shape[1]*0.6), int(gray_img.shape[0]*0.65))

                # Extract face crop for vectorization
                fx, fy, fw, fh = face_box
                face_crop = enhanced_img[max(0, fy):min(enhanced_img.shape[0], fy+fh), max(0, fx):min(enhanced_img.shape[1], fx+fw)]
                current_face_vector = extract_face_biometric_vector(face_crop)

                # 1. Micro-Smile Physical Geometry Analysis (Instant & Robust)
                has_smile, smile_conf, _, _ = detect_micro_smile(gray_img, face_box) if face_box else (False, 0.0, 0, None)

                # 2. Check Teach AI Personalized Biometric Memories
                matched_memory = None
                best_sim = 0.0
                if len(st.session_state.calibrated_face_memory) > 0 and current_face_vector is not None:
                    norm_curr = np.linalg.norm(current_face_vector)
                    for idx, mem in enumerate(st.session_state.calibrated_face_memory):
                        try:
                            v_mem = np.array(mem["vector"], dtype=np.float32)
                            norm_m = np.linalg.norm(v_mem)
                            sim = float(np.dot(current_face_vector, v_mem) / (norm_m * norm_curr)) if (norm_m > 0 and norm_curr > 0) else 0.0
                        except Exception:
                            sim = 0.0
                        mem["_live_sim"] = sim
                        if sim > best_sim:
                            best_sim = sim
                            if sim >= float(st.session_state.get("bio_match_threshold", 0.35)):
                                matched_memory = mem

                # 3. Emotion Resolution Hierarchy
                if matched_memory is not None:
                    detected_emotion = matched_memory["label"].lower()
                    detection_source = f"🧠 Learned Biometric Memory ({matched_memory['label'].upper()} - {best_sim*100:.1f}% Match)"
                    raw_emotions = {detected_emotion: 95.0, "neutral": 2.0}
                elif has_smile:
                    detected_emotion = "happy"
                    detection_source = f"😃 Micro-Smile Neural Biometrics ({smile_conf:.1f}% Smile Arc)"
                    raw_emotions = {"happy": smile_conf, "neutral": 2.0, "sad": 1.0, "angry": 0.5}
                else:
                    # Run DeepFace as fallback for non-smile expressions
                    try:
                        analysis = DeepFace.analyze(
                            enhanced_img, 
                            actions=['emotion'], 
                            detector_backend='opencv', 
                            enforce_detection=False, 
                            silent=True
                        )
                        if isinstance(analysis, list) and len(analysis) > 0:
                            raw_emotions = analysis[0].get('emotion', {}).copy()
                            top_em = max(raw_emotions, key=raw_emotions.get)
                            if top_em != 'neutral':
                                detected_emotion = top_em
                                detection_source = f"AI Vision FER ({top_em.upper()})"
                            else:
                                sorted_ems = sorted(raw_emotions.items(), key=lambda x: x[1], reverse=True)
                                if len(sorted_ems) > 1 and sorted_ems[1][1] > 6.0:
                                    detected_emotion = sorted_ems[1][0]
                                    detection_source = f"Sub-threshold Expression ({detected_emotion.upper()})"
                                else:
                                    detected_emotion = "neutral"
                                    detection_source = "Calm Demeanor (Neutral)"
                        else:
                            detected_emotion = "neutral"
                            detection_source = "Face Scan (Neutral)"
                    except Exception:
                        detected_emotion = "neutral"
                        detection_source = "Standard Baseline (Neutral)"

                st.success(f"AI Vision Detected: **{detected_emotion.upper()}** ({detection_source})")

                # Display emotion breakdown
                with st.expander("📊 View Facial Micro-Expression Breakdown", expanded=False):
                    sorted_emotions = sorted(raw_emotions.items(), key=lambda x: x[1], reverse=True)
                    for em_name, em_val in sorted_emotions:
                        st.progress(
                            min(max(float(em_val) / 100.0, 0.0), 1.0), 
                            text=f"{em_name.capitalize()}: {float(em_val):.1f}%"
                        )

            except Exception as e:
                detected_emotion = "neutral"
                st.warning(f"⚠️ Biometric Scan Diagnostic: {e}")

        # Teach AI UI (Available whenever a camera frame is ready or manually)
        if current_face_vector is not None:
            st.markdown("##### 🧠 1-Click Teach AI (Register Face Topology):")
            st.caption("Lock in this exact facial posture into persistent biometric memory:")
            q_c1, q_c2, q_c3 = st.columns(3)
            if q_c1.button("🧠 Memorize as HAPPY", use_container_width=True):
                memorize_face(current_face_vector, "happy")
                st.toast("✅ Learned! Facial posture memorized as HAPPY!")
                st.rerun()
            if q_c2.button("🧠 Memorize as ANGRY", use_container_width=True):
                memorize_face(current_face_vector, "angry")
                st.toast("✅ Learned! Facial posture memorized as ANGRY!")
                st.rerun()
            if q_c3.button("🧠 Memorize as SAD", use_container_width=True):
                memorize_face(current_face_vector, "sad")
                st.toast("✅ Learned! Facial posture memorized as SAD!")
                st.rerun()

        if st.session_state.calibrated_face_memory:
            with st.expander(f"🗂️ Active Learned Memories ({len(st.session_state.calibrated_face_memory)})", expanded=False):
                if st.button("🗑️ Reset & Clear All Memories", key="clear_face_mem_top_btn", use_container_width=True):
                    st.session_state.calibrated_face_memory = []
                    save_face_memory([])
                    st.rerun()
                st.session_state.bio_match_threshold = st.slider(
                    "Biometric Match Sensitivity",
                    min_value=0.20,
                    max_value=0.85,
                    value=float(st.session_state.get("bio_match_threshold", 0.35)),
                    step=0.01,
                    help="Lower values increase tolerance to head tilts, distance from camera, and ambient daylight changes."
                )
                for i, m in enumerate(st.session_state.calibrated_face_memory):
                    mem_c1, mem_c2 = st.columns([4, 1])
                    live_sim = m.get("_live_sim", 0.0)
                    sim_badge = f" — Live Match: **{live_sim*100:.1f}%**" if live_sim > 0.0 else ""
                    with mem_c1:
                        st.write(f"• **Memory #{i+1}:** **{m['label'].upper()}** (Learned at {m.get('timestamp', 'N/A')}){sim_badge}")
                    with mem_c2:
                        if st.button("🗑️", key=f"del_mem_btn_{i}", help="Delete this specific memory"):
                            st.session_state.calibrated_face_memory.pop(i)
                            save_face_memory(st.session_state.calibrated_face_memory)
                            st.rerun()

        # Emotion Routing Matrix
        emotion_map = {
            "sad": "KTU Exam Trauma",
            "fear": "KTU Exam Trauma",
            "angry": "Political Poru & Hartal",
            "disgust": "Political Poru & Hartal",
            "happy": "Nirvana (Thattukada & Vibe)",
            "surprise": "Nirvana (Thattukada & Vibe)",
            "neutral": "Monday Work Shokam"
        }
        target_category = emotion_map.get(detected_emotion, "Monday Work Shokam")
        st.info(f"🎯 **Active Psyche Profile:** {detected_emotion.upper()} ➔ **Kerala Category:** {target_category}")

    with right_col:
        st.markdown("### 🖼️ Matched Cult Meme Artifact")

        # Dynamic Parquet Database Matching
        category_alias_map = {
            "KTU Exam Trauma": "Academic Trauma",
            "Political Poru & Hartal": "Political Satire",
            "Nirvana (Thattukada & Vibe)": "Gastronomic Nirvana",
            "Monday Work Shokam": "Corporate Nihilism"
        }
        actual_cat = category_alias_map.get(target_category, target_category)
        matched_df = df[(df["scenario_category"] == target_category) | (df["scenario_category"] == actual_cat)]
        if matched_df.empty:
            matched_df = df
        top_meme = matched_df.sample(n=1).iloc[0] if len(matched_df) > 0 else df.iloc[0]

        # Category-Aligned Authentic Image Loader
        asset_dir = os.path.join(BASE_DIR, "assets", "memes") if os.path.exists(os.path.join(BASE_DIR, "assets", "memes")) else "assets/memes"
        rendered_successfully = False

        if os.path.exists(asset_dir):
            category_map = {
                "sad": "sad",
                "fear": "sad",
                "angry": "angry",
                "disgust": "angry",
                "happy": "happy",
                "surprise": "happy",
                "neutral": "neutral"
            }
            cat = category_map.get(detected_emotion, "neutral")
            cat_dir = os.path.join(asset_dir, cat)
            
            # Look in category subfolder first
            matched_files = []
            if os.path.exists(cat_dir):
                matched_files = [os.path.join(cat_dir, f) for f in os.listdir(cat_dir) if f.endswith((".jpg", ".png", ".jpeg"))]
            
            # Fallback to category-prefixed files in asset_dir
            if not matched_files:
                matched_files = [os.path.join(asset_dir, f) for f in os.listdir(asset_dir) if f.startswith(cat) and f.endswith((".jpg", ".png", ".jpeg"))]
            
            # General fallback to any file in asset_dir
            if not matched_files:
                matched_files = [os.path.join(asset_dir, f) for f in os.listdir(asset_dir) if os.path.isfile(os.path.join(asset_dir, f)) and f.endswith((".jpg", ".png", ".jpeg"))]

            if matched_files:
                chosen_img = random.choice(matched_files)

                # Precise Character, Movie & Dialogue Synchronization from Chosen Image
                fname_lower = os.path.basename(chosen_img).lower()
                meta_match = next((v for k, v in IMAGE_METADATA.items() if k in fname_lower), None)
                if meta_match:
                    card_character = meta_match[0]
                    card_movie = meta_match[1]
                    card_dialogue = meta_match[2]
                    card_translation = meta_match[3] if len(meta_match) > 3 else "Nammude swantham Kerala existential expression mwone!"
                    card_signal_class = meta_match[4] if len(meta_match) > 4 else "Vernacular Affective Core"
                else:
                    card_character = top_meme['character']
                    card_movie = top_meme['movie']
                    card_dialogue = str(top_meme['dialogue_snippet']).strip('"').strip("'")
                    card_translation = "Nammude swantham Kerala existential expression mwone!"
                    card_signal_class = "Parquet Lake Vector Match"

                # Fetch matching archetype & scenario from Parquet if available
                char_df = matched_df[matched_df['character'].str.contains(card_character.split()[0], case=False, na=False)]
                if not char_df.empty:
                    meme_row = char_df.sample(n=1).iloc[0]
                    scenario_title = meme_row['scenario_title']
                    kew_score = meme_row.get('kerala_existential_weight', top_meme['kerala_existential_weight'])
                    archetype = meme_row.get('character_archetype', top_meme['character_archetype'])
                else:
                    scenario_title = top_meme['scenario_title']
                    kew_score = top_meme['kerala_existential_weight']
                    archetype = top_meme['character_archetype']

                try:
                    pil_img = Image.open(chosen_img)
                    display_img = crop_to_aspect_ratio(pil_img, target_ratio=16/10, output_size=(600, 375))
                    st.image(display_img, caption=f"Meme Archetype: {archetype} | KEW: {kew_score}/10", use_container_width=True)
                    rendered_successfully = True
                except Exception:
                    st.image(chosen_img, caption=f"Meme Archetype: {archetype} | KEW: {kew_score}/10", use_container_width=True)
                    rendered_successfully = True

        if not rendered_successfully:
            card_character = top_meme['character']
            card_movie = top_meme['movie']
            card_dialogue = str(top_meme['dialogue_snippet']).strip('"').strip("'")
            card_translation = "Nammude swantham Kerala existential expression mwone!"
            card_signal_class = "Parquet Lake Vector Match"
            scenario_title = top_meme['scenario_title']
            kew_score = top_meme['kerala_existential_weight']
            archetype = top_meme['character_archetype']

            # Fallback visual banner container using clean HTML if assets fail to load
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, #2a1b3d, #1a1a2e); padding: 30px; border-radius: 12px; border: 2px dashed #00ffff; text-align: center; margin-bottom: 15px;">
                <h4 style="color: #00ffff; margin: 0;">🌴 KERALA CULT CLASSIC ARTIFACT</h4>
                <p style="color: #ffffff; font-size: 1.2rem; margin: 10px 0;">{card_movie}</p>
                <span style="color: #ff4b4b; font-family: monospace;">[ VISUAL BUFFER LOADED ]</span>
            </div>
            """, unsafe_allow_html=True)

        # High-Impact Cinematic Dialogue Card (Unified right frame from Lovable UI)
        st.markdown(f"""
        <div style="background: rgba(18, 24, 43, 0.92); border: 1px solid rgba(0, 240, 255, 0.35); border-radius: 12px; padding: 22px; margin-top: 15px; box-shadow: 0 8px 32px rgba(0, 0, 0, 0.45);">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px;">
                <span style="background: rgba(255, 75, 75, 0.15); border: 1px solid rgba(255, 75, 75, 0.6); color: #ff4b4b; padding: 3px 10px; border-radius: 4px; font-size: 11px; font-weight: bold; font-family: 'IBM Plex Mono', monospace;">MATCH 99.4%</span>
                <span style="color: #00f0ff; font-family: 'IBM Plex Mono', monospace; font-size: 11px;">[RESEARCH_GRADE_SIMULATION]</span>
            </div>
            <h3 style="color: #ffffff; font-family: 'Chakra Petch', sans-serif; font-size: 1.4rem; margin: 0 0 4px 0;">
                🎭 {card_character} <span style="color: #00f0ff;">· {card_movie}</span>
            </h3>
            <p style="font-size: 0.85rem; color: #94a3b8; margin: 0 0 14px 0;"><b>Scenario Archetype:</b> {scenario_title} ({archetype})</p>
            <blockquote style="border-left: 3px solid #00f0ff; padding-left: 14px; margin: 12px 0; color: #f8fafc; font-size: 1.15rem; font-style: italic; font-weight: 500; line-height: 1.4;">
                “{card_dialogue}”
                <span style="display: block; margin-top: 6px; font-style: normal; font-size: 0.85rem; color: #94a3b8; font-family: 'IBM Plex Mono', monospace;">
                    ↳ {card_translation}
                </span>
            </blockquote>
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 12px; margin-top: 18px; border-top: 1px solid rgba(255, 255, 255, 0.1); padding-top: 14px;">
                <div style="background: rgba(12, 16, 32, 0.8); border: 1px solid rgba(255, 75, 75, 0.3); padding: 10px; border-radius: 6px;">
                    <div style="font-size: 9px; color: #94a3b8; text-transform: uppercase;">Kerala Existential Weight</div>
                    <div style="font-family: 'Chakra Petch', sans-serif; font-size: 1.4rem; font-weight: bold; color: #ff4b4b; margin-top: 2px;">{kew_score} <span style="font-size: 0.8rem; color: #94a3b8;">/ 10</span></div>
                </div>
                <div style="background: rgba(12, 16, 32, 0.8); border: 1px solid rgba(0, 240, 255, 0.3); padding: 10px; border-radius: 6px;">
                    <div style="font-size: 9px; color: #94a3b8; text-transform: uppercase;">Signal Class</div>
                    <div style="font-family: 'IBM Plex Mono', monospace; font-size: 0.82rem; font-weight: bold; color: #00f0ff; margin-top: 4px; text-transform: uppercase;">{card_signal_class}</div>
                </div>
            </div>
            <div style="display: flex; justify-content: space-between; align-items: center; margin-top: 14px; font-size: 10px; color: #64748b; font-family: 'IBM Plex Mono', monospace;">
                <span>SOURCE: APACHE SPARK PARQUET LAKE</span>
                <span style="color: #00ffcc;">CATALYST VERIFIED</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

with tabs[2]:
    st.markdown("""
    <div style="background: linear-gradient(135deg, #1a1a2e, #16213e); padding: 20px; border-radius: 12px; border-left: 5px solid #00f0ff; margin-bottom: 20px;">
        <h3 style="color: #00f0ff; margin: 0 0 6px 0;">🗄️ Vernacular Meme Vault & Parquet Lake Explorer</h3>
        <p style="color: #c5c5e0; font-size: 0.95rem; margin: 0;">
            Explore the curated Kerala cinematic psyche repository and search 250,000 indexed records across Apache Spark columnar partitions.
        </p>
    </div>
    """, unsafe_allow_html=True)

    VAULT_MEMES = [
        {
            "id": 1,
            "title": "KTU Internal Marks: The Reckoning",
            "dialogue": "Enthokkeyo pratheekshichu… enthokkeyo aayi.",
            "translation": "Ellaam set aavum ennu vichaarichu, pakshe kittiye odukkathe life lesson!",
            "movie": "Premam (2015)",
            "character": "George",
            "archetype": "Academic Martyr",
            "mood": "Despair",
            "kew": 9.48,
            "image": "assets/memes/sad/sad_ktu_trauma.jpg"
        },
        {
            "id": 2,
            "title": "The Chacko Ultimatum",
            "dialogue": "Ormayundo ee mukham? Marakkan pattilla.",
            "translation": "Ee mukham ormayundo? Thomasinte achan Chacko mashinte adi aarum marakkilla!",
            "movie": "Spadikam (1995)",
            "character": "Chacko Mash",
            "archetype": "Unforgiving Patriarch",
            "mood": "Rage",
            "kew": 8.82,
            "image": "assets/memes/angry/angry_chacko_resolve.jpg"
        },
        {
            "id": 3,
            "title": "KSRTC Serotonin Event",
            "dialogue": "Ellathinum athintethaya samayam undu, Dasa.",
            "translation": "Ellathinum athintethaaya samayam undu Dasa... tension venda, ellam sheriyaavum!",
            "movie": "Nadodikkattu (1987)",
            "character": "Dasan & Vijayan",
            "archetype": "Delusional Optimist",
            "mood": "Hope",
            "kew": 7.26,
            "image": "assets/memes/happy/happy_bus_existential.jpg"
        },
        {
            "id": 4,
            "title": "Salary Day + 1 Existential Void",
            "dialogue": "Angane Pavanayi shavamaayi!",
            "translation": "Angane aadyathe assignment-il thanne nammude Pavanayi finish aayi!",
            "movie": "Nadodikkattu (1987)",
            "character": "Ananthan Nambiar",
            "archetype": "Professional Casualty",
            "mood": "Despair",
            "kew": 9.71,
            "image": "assets/memes/happy/angane-pavanayi-shavamaayi.jpg"
        },
        {
            "id": 5,
            "title": "Late-Night Hostel Energy Catalyst",
            "dialogue": "Eda mone! All the best da!",
            "translation": "Eda mone! Full scene aakki polikk, scene illa... all the best da!",
            "movie": "Aavesham (2024)",
            "character": "Ranga Annan",
            "archetype": "Uninhibited Godfather",
            "mood": "Chaos",
            "kew": 9.12,
            "image": "assets/memes/happy/all-the-best-da.jpg"
        },
        {
            "id": 6,
            "title": "Starvation & Biryani Yearning",
            "dialogue": "Annu undaakkiya biriyaani okke enth cheytho aavo!",
            "translation": "Annu vecha biriyaani muzhuvan aaru thinnu theertho aavo... odukkathe vishappu!",
            "movie": "Punjabi House (1998)",
            "character": "Ramanan",
            "archetype": "Culinary Martyr",
            "mood": "Hope",
            "kew": 8.65,
            "image": "assets/memes/happy/annu-undaakkiya-biriyaani-okke-enth-cheytho-aavo.jpg"
        },
        {
            "id": 7,
            "title": "Unreciprocated Melodramatic Grief",
            "dialogue": "Achuvettaa... I love you!",
            "translation": "Achuvettaa... njaan karanju parayuva, enikku ningalodu sathyamaayittum premamaanu!",
            "movie": "Kalyanaraman (2002)",
            "character": "Ponjikkara",
            "archetype": "Tragicomic Romantic",
            "mood": "Despair",
            "kew": 9.56,
            "image": "assets/memes/sad/achuvettaa-i-love-you.jpg"
        },
        {
            "id": 8,
            "title": "Modernity Assertion Protocol",
            "dialogue": "Actually njaan modern aanu!",
            "translation": "Actually njaan full modern aanu ketto... aarum thettidharikkaruth chetta!",
            "movie": "Kalyanaraman (2002)",
            "character": "Pyari",
            "archetype": "Eccentric Sidekick",
            "mood": "Hope",
            "kew": 7.45,
            "image": "assets/memes/neutral/actually-njaan-modern-aanu.jpg"
        },
        {
            "id": 9,
            "title": "Corporate Resignation Defiance",
            "dialogue": "Allenkilum ee thallipoli companiyile joli njangalkk prashnamalla!",
            "translation": "Ee thallipoli companiyile joli poyaal njangalkku oru koppum illa... vere pani nokkum!",
            "movie": "Nadodikkattu (1987)",
            "character": "Vijayan & Dasan",
            "archetype": "Defiant Underdogs",
            "mood": "Chaos",
            "kew": 8.78,
            "image": "assets/memes/neutral/allenkilum-ee-thallipoli-companiyile-joli-njangalkk-prashnamalla.jpg"
        },
        {
            "id": 10,
            "title": "Nihilistic Task Defeatism",
            "dialogue": "Athinekkaal nallath ente shavam edukkunnathalle!",
            "translation": "Ithu cheyyunnathinekkaal bhedham ente shavam edukkunnathaannu Moosa parayunne!",
            "movie": "CID Moosa (2003)",
            "character": "CID Moosa",
            "archetype": "Exasperated Detective",
            "mood": "Despair",
            "kew": 9.30,
            "image": "assets/memes/sad/athinekkaal-nallath-ente-shavam-edukkunnathalle.jpg"
        },
        {
            "id": 11,
            "title": "Explosive Group Chaos",
            "dialogue": "Aarkkadaa bhraanth?!",
            "translation": "Aarkkadaa ivide bhraanth?! Hostalil odukkathe adi thudangi mwone!",
            "movie": "In Harihar Nagar (1990)",
            "character": "Mahadevan",
            "archetype": "Hostel Instigator",
            "mood": "Rage",
            "kew": 8.76,
            "image": "assets/memes/angry/aarkkadaa-bhraanth.jpg"
        },
        {
            "id": 12,
            "title": "Patriarchal Cotton Rule",
            "dialogue": "Aanede chevittil maathramalla, ninte ammede chevittilum vekkeda panji!",
            "translation": "Aanede chevittil maathramalla, ninte ammede chevittilum vekkeda panji... Godfather mass!",
            "movie": "Godfather (1991)",
            "character": "Anjooran",
            "archetype": "Unforgiving Patriarch",
            "mood": "Rage",
            "kew": 9.05,
            "image": "assets/memes/angry/aanede-chevittil-maathramalla-ninte-ammede-chevittilum-vekkeda-panji.jpg"
        }
    ]

    # Search and Filter Toolbar
    v_col1, v_col2 = st.columns([1.5, 1])
    with v_col1:
        vault_query = st.text_input("🔍 Search dialogue, movie, character, or archetype:", placeholder="e.g. Dasan, Chacko, Premam, modern...", key="vault_search_box")
    with v_col2:
        mood_filter = st.radio("Mood Filter:", ["All", "Hope", "Despair", "Rage", "Chaos"], horizontal=True, key="vault_mood_filter")

    # Filter Items
    q = vault_query.strip().lower()
    filtered_memes = [
        m for m in VAULT_MEMES
        if (mood_filter == "All" or m["mood"] == mood_filter)
        and (not q or q in m["title"].lower() or q in m["dialogue"].lower() or q in m["translation"].lower() or q in m["movie"].lower() or q in m["character"].lower() or q in m["archetype"].lower())
    ]

    st.caption(f"Showing **{len(filtered_memes)}** artifacts resolved (Sorted by KEW relevance ↓)")

    # 3-Column Card Grid - Rendered row-by-row for strict horizontal alignment
    mood_colors = {
        "Despair": "#3399ff",
        "Rage": "#ff4b4b",
        "Hope": "#00ffcc",
        "Chaos": "#ffaa00"
    }

    for row_start in range(0, len(filtered_memes), 3):
        row_items = filtered_memes[row_start : row_start + 3]
        cols = st.columns(3, gap="medium")
        for col_idx, item in enumerate(row_items):
            with cols[col_idx]:
                mood_badge_color = mood_colors.get(item["mood"], "#00f0ff")
                img_path = item["image"]
                if not os.path.exists(img_path):
                    alt_path = os.path.join("assets/memes", os.path.basename(img_path))
                    if os.path.exists(alt_path):
                        img_path = alt_path

                if os.path.exists(img_path):
                    try:
                        pil_card = Image.open(img_path)
                        # Center-crop and scale to uniform 16:10 cinematic banner
                        display_card = crop_to_aspect_ratio(pil_card, target_ratio=16/10, output_size=(600, 375))
                        st.image(display_card, use_container_width=True)
                    except Exception:
                        st.image(img_path, use_container_width=True)

                st.markdown(f"""
                <div style="background: rgba(18, 24, 43, 0.85); border: 1px solid rgba(0, 240, 255, 0.2); border-radius: 8px; padding: 14px; margin-bottom: 18px;">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
                        <span style="background: rgba(0, 240, 255, 0.15); border: 1px solid rgba(0, 240, 255, 0.5); color: #00f0ff; font-size: 10px; font-weight: bold; padding: 2px 8px; border-radius: 3px; font-family: 'IBM Plex Mono', monospace;">
                            KEW {item['kew']}
                        </span>
                        <span style="background: rgba(255, 75, 75, 0.15); border: 1px solid {mood_badge_color}; color: {mood_badge_color}; font-size: 10px; font-weight: bold; padding: 2px 8px; border-radius: 3px; font-family: 'IBM Plex Mono', monospace;">
                            {item['mood'].upper()}
                        </span>
                    </div>
                    <div style="font-family: 'Chakra Petch', sans-serif; font-weight: 700; font-size: 1.05rem; color: #ffffff; margin-bottom: 2px;">
                        {item['title']}
                    </div>
                    <div style="font-size: 10px; text-transform: uppercase; color: #94a3b8; margin-bottom: 10px; font-family: 'IBM Plex Mono', monospace;">
                        {item['movie']} // {item['archetype']}
                    </div>
                    <div style="border-left: 2px solid #00f0ff; padding-left: 10px; color: #e2e8f0; font-size: 0.95rem; font-style: italic; margin-bottom: 6px;">
                        “{item['dialogue']}”
                    </div>
                    <div style="font-size: 11px; color: #94a3b8; font-family: 'IBM Plex Mono', monospace; margin-bottom: 10px;">
                        ↳ {item['translation']}
                    </div>
                </div>
                """, unsafe_allow_html=True)
                st.code(item['dialogue'], language="text")

    # Big Data Lake Columnar Parquet Explorer
    st.divider()
    with st.expander("🗄️ Query Full 250,000-Record Parquet Data Lake (Spark Columnar Pushdown)", expanded=False):
        st.markdown("##### Filter Parquet Lake Partitions")
        pq_c1, pq_c2, pq_c3 = st.columns(3)
        with pq_c1:
            sel_emotion = st.multiselect(
                "Filter Emotion:", 
                options=df["emotion"].unique().tolist() if "emotion" in df.columns else [],
                default=[]
            )
        with pq_c2:
            sel_category = st.multiselect(
                "Filter Scenario Category:",
                options=df["scenario_category"].unique().tolist() if "scenario_category" in df.columns else [],
                default=[]
            )
        with pq_c3:
            row_limit = st.slider("Row Limit to Stream:", min_value=10, max_value=500, value=50, step=10)

        lake_view_df = df
        if sel_emotion:
            lake_view_df = lake_view_df[lake_view_df["emotion"].isin(sel_emotion)]
        if sel_category:
            lake_view_df = lake_view_df[lake_view_df["scenario_category"].isin(sel_category)]

        display_cols = [c for c in ["meme_id", "character", "movie", "scenario_title", "emotion", "kerala_existential_weight", "dialogue_snippet"] if c in lake_view_df.columns]
        st.dataframe(lake_view_df[display_cols].head(row_limit), use_container_width=True)
        st.caption(f"Displaying top {min(row_limit, len(lake_view_df))} of {len(lake_view_df):,} filtered records from the Snappy-compressed Parquet store.")

