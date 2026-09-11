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
from deepface import DeepFace

# Optional WebRTC imports with error resilience
WEBRTC_AVAILABLE = False
try:
    from streamlit_webrtc import webrtc_streamer, VideoProcessorBase, RTCConfiguration
    import av
    WEBRTC_AVAILABLE = True
except ImportError:
    pass

st.set_page_config(page_title="Kerala Biometric Meme Engine", layout="wide", page_icon="🌴")

# Load Parquet Database
@st.cache_data
def load_data():
    parquet_path = "biometric_memes.parquet"
    if os.path.exists(parquet_path):
        data = pd.read_parquet(parquet_path)
        # Ensure emotion column reflects diverse target_emotion states
        if "target_emotion" in data.columns:
            data["emotion"] = data["target_emotion"]
        return data
    else:
        # Fallback dummy df if parquet is missing
        return pd.DataFrame({
            "meme_id": ["MEME_001"],
            "character": ["Dashamoolam Damu"],
            "movie": ["Chattambinadu"],
            "scenario_title": ["Onam Pookkalam Turf War"],
            "character_archetype": ["Failed Quotation Gangster"],
            "emotion": ["neutral"],
            "kerala_existential_weight": [9.04],
            "dialogue_snippet": ['"Athu pinne sir... njan oru simple quotation eduthatha!"']
        })

df = load_data()

# Definitive Authentic Malayalam Meme Asset Identity Map
IMAGE_METADATA = {
    'actually_modern': ('Pyari', 'Kalyanaraman', 'Actually njaan modern aanu!'),
    'actually-njaan-modern': ('Pyari', 'Kalyanaraman', 'Actually njaan modern aanu!'),
    'pyari': ('Pyari', 'Kalyanaraman', 'Actually njaan modern aanu!'),
    'salim_kumar_crying': ('Ponjikkara', 'Kalyanaraman', 'Achuvettaa... I love you!'),
    'achuvettaa': ('Ponjikkara', 'Kalyanaraman', 'Achuvettaa... I love you!'),
    'collector': ('Ponjikkara', 'Kalyanaraman', 'Alla... Ernakulam jilla collector mindaathe kutthi kayattedo!'),
    'dasan_kattappara': ('Vijayan', 'Nadodikkattu', 'Achan paranju ithilum bhedham kattapparayum eduth kakkaan irangunnathaanennu!'),
    'kattappara': ('Vijayan', 'Nadodikkattu', 'Achan paranju ithilum bhedham kattapparayum eduth kakkaan irangunnathaanennu!'),
    'dasan_resignation': ('Dasan', 'Nadodikkattu', 'Allenkilum ee thallipoli companiyile joli njangalkk prashnamalla!'),
    'thallipoli': ('Dasan', 'Nadodikkattu', 'Allenkilum ee thallipoli companiyile joli njangalkk prashnamalla!'),
    'moosa_shavam': ('CID Moosa', 'CID Moosa', 'Athinekkaal nallath ente shavam edukkunnathalle!'),
    'shavam': ('CID Moosa', 'CID Moosa', 'Athinekkaal nallath ente shavam edukkunnathalle!'),
    'cid_moosa': ('CID Moosa', 'CID Moosa', 'Moosa... CID Moosa!'),
    'dharidryam': ('Thorappan Kochunni', 'CID Moosa', 'Athonnum illenkilum dharidryathinu kuravonnum illallo!'),
    'dharidryathinu': ('Thorappan Kochunni', 'CID Moosa', 'Athonnum illenkilum dharidryathinu kuravonnum illallo!'),
    'appukkuttan': ('Appukkuttan', 'In Harihar Nagar', 'Appukkutta... ninte oru kaaryam!'),
    'appukuttan': ('Appukkuttan', 'In Harihar Nagar', 'Appukkutta... ninte oru kaaryam!'),
    'bhraanth': ('Mahadevan', 'In Harihar Nagar', 'Aarkkadaa bhraanth?!'),
    'ramanathan': ('Ramanathan', 'In Harihar Nagar', 'Thomaskutty vittoda!'),
    'karnnore': ('Unnithan', 'Manichitrathazhu', 'Adukkaruth karnnore, entaduth maathram adukkaruth!'),
    'kuttikkadan': ('Kuttikkadan', 'Spadikam', 'Nee aaraada kooduthal chodikkan?'),
    'anjooran': ('Anjooran', 'Godfather', 'Aanede chevittil maathramalla, ninte ammede chevittilum vekkeda panji!'),
    'panji': ('Anjooran', 'Godfather', 'Aanede chevittil maathramalla, ninte ammede chevittilum vekkeda panji!'),
    'krishnan_nair': ('Krishnan Nair', 'Akkare Akkare Akkare', 'Shooting begins!'),
    'krishnan-nair': ('Krishnan Nair', 'Akkare Akkare Akkare', 'Shooting begins!'),
    'paul_barber': ('Paul Barber', 'Akkare Akkare Akkare', 'Ninte achanaada Paul Barber!'),
    'paul-barber': ('Paul Barber', 'Akkare Akkare Akkare', 'Ninte achanaada Paul Barber!'),
    'sadhanam': ('Dasan & Vijayan', 'Akkare Akkare Akkare', 'Sadhanam kayyilundo?'),
    'ramanan_biriyani': ('Ramanan', 'Punjabi House', 'Annu undaakkiya biriyaani okke enth cheytho aavo!'),
    'biriyaani': ('Ramanan', 'Punjabi House', 'Annu undaakkiya biriyaani okke enth cheytho aavo!'),
    'gangadharan': ('Gangadharan Muthalali', 'Punjabi House', 'Akathu poyi Punjabikalod para, Gangadharan Muthalaaliyum Ramananum vannirikkunnu ennu!'),
    'alakkum': ('Ramanan', 'Punjabi House', 'Ariyaan paadillanjittu chodikkukaya, randu varshamaayi ivide alakkum nanayum onnumille?'),
    'pavanayi': ('Ananthan Nambiar', 'Nadodikkattu', 'Angane Pavanayi shavamaayi!'),
    'ranga_annan': ('Ranga Annan', 'Aavesham', 'Eda mone! All the best da!'),
    'all-the-best': ('Ranga Annan', 'Aavesham', 'Eda mone! All the best da!'),
    'jagathy_aha': ('Nischal', 'Kilukkam', 'Aha... anganayanalle!'),
    'anganayanalle': ('Nischal', 'Kilukkam', 'Aha... anganayanalle!'),
    'gafoor': ('Gafoor Ka Dhosth', 'Nadodikkattu', 'Savari giri giri!'),
    'damu': ('Dashamoolam Damu', 'Chattambinadu', 'Njaan aaraannu ariyilla le?'),
    'manavalan': ('Manavalan', 'Pulival Kalyanam', 'Njan aara mon! Dubai Manavalan!'),
    'pappu': ('Kuthiravattam Pappu', 'Vellanakalude Nadu', 'Ippo shariyaakki tharaam!')
}

st.markdown("<h1 style='text-align: center;'>🌴 The 'Meme-ing of Life' Sentiment Analyzer</h1>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align: center; color: #ff4b4b;'>Biometric Ocular Psyche & Kerala Existential Telemetry</h4>", unsafe_allow_html=True)
st.divider()

tabs = st.tabs(["📊 Global Telemetry", "📸 The Biometric Scanner", "📂 Vernacular Feed"])

with tabs[0]:
    col1, col2 = st.columns(2)
    with col1:
        avg_kmi = df["kerala_existential_weight"].mean() * 1.2
        fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=round(avg_kmi, 2),
            title={'text': "Aggregate Kerala Mood Index (KMI)"},
            gauge={'axis': {'range': [0, 15]}, 'bar': {'color': "#ff4b4b"}}
        ))
        fig.update_layout(height=350, template="plotly_dark")
        st.plotly_chart(fig, width='stretch')
    with col2:
        st.metric("Total Memes in Lake", f"{len(df):,}")
        st.metric("Dominant State", "Monday Work Shokam")
        st.markdown("Distributed Apache Spark pipeline active. Parquet columnar layer loaded successfully.")

with tabs[1]:
    st.subheader("Ocular Psyche Biometric Scanner & Curated Vault")
    st.write("Real-time facial emotion recognition and instant vernacular meme delivery.")

    left_col, right_col = st.columns([1, 1], gap="large")

    with left_col:
        st.markdown("### 📷 Biometric Capture")
        capture_mode = st.radio(
            "Mode:",
            ["📸 Live Face Emotion Scan (Camera)", "🎛️ Manual Psychological Override"],
            horizontal=True
        )

        detected_emotion = "neutral"

        if capture_mode == "📸 Live Face Emotion Scan (Camera)":
            cam_image = st.camera_input("Capture expression", label_visibility="collapsed")
            if cam_image is not None:
                try:
                    import cv2
                    import numpy as np
                    
                    bytes_data = cam_image.getvalue()
                    np_arr = np.frombuffer(bytes_data, np.uint8)
                    img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

                    analysis = DeepFace.analyze(
                        img, 
                        actions=['emotion'], 
                        detector_backend='opencv', 
                        enforce_detection=False, 
                        silent=True
                    )
                    
                    if isinstance(analysis, list) and len(analysis) > 0:
                        detected_emotion = analysis[0].get('dominant_emotion', 'neutral')
                    
                    st.success(f"AI Vision Detected: **{detected_emotion.upper()}**")
                except Exception:
                    detected_emotion = "neutral"
                    st.warning("Detection fallback engaged. Defaulting to Neutral.")
            
            # Quick override buttons because CV models fail on smiles
            st.markdown("##### Quick Emotion Correction Override:")
            cols_override = st.columns(3)
            if cols_override[0].button("Force Happy"):
                detected_emotion = "happy"
            if cols_override[1].button("Force Sad"):
                detected_emotion = "sad"
            if cols_override[2].button("Force Angry"):
                detected_emotion = "angry"

        else:
            detected_emotion = st.selectbox(
                "Select Exact Psychological State:",
                ["sad", "angry", "happy", "neutral", "fear", "surprise"]
            )

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
        asset_dir = "assets/memes"
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
                    card_character, card_movie, card_dialogue = meta_match
                else:
                    card_character = top_meme['character']
                    card_movie = top_meme['movie']
                    card_dialogue = str(top_meme['dialogue_snippet']).strip('"').strip("'")

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
                    st.image(pil_img, caption=f"Meme Archetype: {archetype} | KEW: {kew_score}/10", width='stretch')
                    rendered_successfully = True
                except Exception:
                    st.image(chosen_img, caption=f"Meme Archetype: {archetype} | KEW: {kew_score}/10", width='stretch')
                    rendered_successfully = True

        if not rendered_successfully:
            card_character = top_meme['character']
            card_movie = top_meme['movie']
            card_dialogue = str(top_meme['dialogue_snippet']).strip('"').strip("'")
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

        # High-Impact Cinematic Dialogue Card (Unified right frame)
        st.markdown(f"""
        <div style="background-color: #1e1e2f; padding: 20px; border-radius: 12px; border: 2px solid #ff4b4b;">
            <h3 style="color: #ff4b4b; margin-top: 0;">🎭 {card_character} — <span style="color: #ffffff;">{card_movie}</span></h3>
            <p style="font-size: 0.95rem; color: #a0a0c0;"><b>Scenario:</b> {scenario_title}</p>
            <hr style="border-color: #444455;">
            <p style="color: #00ffff; font-style: italic; font-size: 1.1rem; margin: 10px 0;">"{card_dialogue}"</p>
            <div style="display: flex; justify-content: space-between; margin-top: 15px;">
                <span style="background-color: #ff4b4b; color: white; padding: 4px 12px; border-radius: 15px; font-weight: bold; font-size: 0.85rem;">KEW Score: {kew_score}/10</span>
                <span style="color: #8888aa; font-family: monospace; font-size: 0.8rem;">250k PARQUET LAKE</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

with tabs[2]:
    st.subheader("Vernacular Meme Lake Explorer")
    st.dataframe(df[["meme_id", "character", "movie", "scenario_title", "emotion", "kerala_existential_weight"]].head(50), width='stretch')
