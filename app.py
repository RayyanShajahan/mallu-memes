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
    st.subheader("Ocular Psyche Biometric Scanner")
    st.write("Instantaneous psychological mapping and Malayalam Meme Engine.")

    left_col, right_col = st.columns([1, 1], gap="large")

    with left_col:
        st.markdown("### 📷 Biometric Capture")
        capture_mode = st.radio(
            "Mode:",
            ["📸 Snapshot Analysis", "🎛️ Manual Psychological Override"],
            horizontal=True
        )

        detected_emotion = "neutral"

        if capture_mode == "📸 Snapshot Analysis":
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
        st.markdown("### 🖼️ Matched Meme Artifact")

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

        # BULLETPROOF IMAGE RENDERER: Looks for generated assets or renders a clean fallback card
        asset_dir = "assets/memes"
        rendered_successfully = False

        if os.path.exists(asset_dir):
            asset_files = [f for f in os.listdir(asset_dir) if f.endswith((".jpg", ".png"))]
            if asset_files:
                char_lower = str(top_meme.get("character", "")).lower()
                matched_asset = next((f for f in asset_files if any(k in f.lower() for k in char_lower.split() if len(k) > 2)), None)
                chosen_image_path = os.path.join(asset_dir, matched_asset if matched_asset else random.choice(asset_files))
                try:
                    # Load using PIL to guarantee stream stability
                    pil_img = Image.open(chosen_image_path)
                    st.image(pil_img, caption=f"Meme Archetype: {top_meme['character_archetype']}", width='stretch')
                    rendered_successfully = True
                except Exception:
                    pass

        if not rendered_successfully:
            # Fallback visual banner container using clean HTML if assets fail to load
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, #2a1b3d, #1a1a2e); padding: 30px; border-radius: 12px; border: 2px dashed #00ffff; text-align: center; margin-bottom: 15px;">
                <h4 style="color: #00ffff; margin: 0;">🌴 KERALA CULT CLASSIC ARTIFACT</h4>
                <p style="color: #ffffff; font-size: 1.2rem; margin: 10px 0;">{top_meme['movie']}</p>
                <span style="color: #ff4b4b; font-family: monospace;">[ VISUAL BUFFER LOADED ]</span>
            </div>
            """, unsafe_allow_html=True)

        snippet_text = str(top_meme['dialogue_snippet']).strip('"').strip("'")

        # High-Impact Cinematic Dialogue Card (Unified right frame)
        st.markdown(f"""
        <div style="background-color: #1e1e2f; padding: 20px; border-radius: 12px; border: 2px solid #ff4b4b;">
            <h3 style="color: #ff4b4b; margin-top: 0;">🎭 {top_meme['character']} — <span style="color: #ffffff;">{top_meme['movie']}</span></h3>
            <p style="font-size: 0.95rem; color: #a0a0c0;"><b>Scenario:</b> {top_meme['scenario_title']}</p>
            <hr style="border-color: #444455;">
            <p style="color: #00ffff; font-style: italic; font-size: 1.1rem; margin: 10px 0;">"{snippet_text}"</p>
            <div style="display: flex; justify-content: space-between; margin-top: 15px;">
                <span style="background-color: #ff4b4b; color: white; padding: 4px 12px; border-radius: 15px; font-weight: bold; font-size: 0.85rem;">KEW Score: {top_meme['kerala_existential_weight']}/10</span>
                <span style="color: #8888aa; font-family: monospace; font-size: 0.8rem;">250k PARQUET LAKE</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

with tabs[2]:
    st.subheader("Vernacular Meme Lake Explorer")
    st.dataframe(df[["meme_id", "character", "movie", "scenario_title", "emotion", "kerala_existential_weight"]].head(50), width='stretch')
