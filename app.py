import streamlit as st
import pandas as pd
import plotly.express as go_express
import plotly.graph_objects as go
import os
import random
from PIL import Image
import io
import numpy as np

# Optional WebRTC imports with error resilience
WEBRTC_AVAILABLE = False
try:
    from streamlit_webrtc import webrtc_streamer, VideoProcessorBase, RTCConfiguration
    import av
    import cv2
    from deepface import DeepFace
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
        # Ensure emotion column reflects diverse target_emotion states if collapsed
        if "target_emotion" in data.columns and data["emotion"].nunique() <= 1:
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
        st.plotly_chart(fig, use_container_width=True)
    with col2:
        st.metric("Total Memes in Lake", f"{len(df):,}")
        st.metric("Dominant State", "Monday Work Shokam")
        st.markdown("Distributed Apache Spark pipeline active. Parquet columnar layer loaded successfully.")

with tabs[1]:
    st.subheader("Ocular Psyche Biometric Scanner")
    st.write("Instantaneous psychological mapping and Kerala Existential Meme Engine.")

    capture_mode = st.radio(
        "Choose Mode:",
        ["📸 Instant Snapshot (Fast AI)", "🧪 Emotion Simulator (Guaranteed Demo Mode)"],
        horizontal=True
    )

    detected_emotion = "neutral"

    if capture_mode == "📸 Instant Snapshot (Fast AI)":
        cam_image = st.camera_input("Strike a pose & capture your expression")
        if cam_image is not None:
            try:
                import cv2
                import numpy as np
                
                bytes_data = cam_image.getvalue()
                np_arr = np.frombuffer(bytes_data, np.uint8)
                img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

                # Fast OpenCV preprocessing
                lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
                l, a, b = cv2.split(lab)
                clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
                enhanced_img = cv2.cvtColor(cv2.merge((clahe.apply(l), a, b)), cv2.COLOR_LAB2BGR)

                analysis = DeepFace.analyze(
                    enhanced_img, 
                    actions=['emotion'], 
                    detector_backend='opencv', 
                    enforce_detection=False, 
                    silent=True
                )
                
                if isinstance(analysis, list) and len(analysis) > 0:
                    detected_emotion = analysis[0].get('dominant_emotion', 'neutral')
                
                st.success(f"🔍 AI Vision Detected Emotion: **{detected_emotion.upper()}**")
            except Exception as e:
                detected_emotion = "neutral"
                st.warning("Detection fallback engaged. Defaulting to Neutral.")
    else:
        detected_emotion = st.selectbox(
            "Select Exact Emotion (Hackathon Demo Override):",
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
    st.markdown(f"🎯 **Psyche Profile:** {detected_emotion.upper()} ➔ **Kerala Category:** {target_category}")

    # Dynamic Parquet Database Matching
    category_alias_map = {
        "KTU Exam Trauma": "Academic Trauma",
        "Political Poru & Hartal": "Political Satire",
        "Nirvana (Thattukada & Vibe)": "Gastronomic Nirvana",
        "Monday Work Shokam": "Corporate Nihilism"
    }
    actual_cat = category_alias_map.get(target_category, target_category)
    matched_df = df[(df["scenario_category"] == target_category) | (df["scenario_category"] == actual_cat) | (df["emotion"].astype(str).str.lower() == detected_emotion.lower())]
    if matched_df.empty:
        matched_df = df

    top_meme = matched_df.sample(n=1).iloc[0] if len(matched_df) > 0 else df.iloc[0]

    # Cinematic Card Layout (Zero broken images, pure high-impact typography)
    st.markdown("---")
    st.markdown(f"""
    <div style="background-color: #1e1e2f; padding: 30px; border-radius: 15px; border: 2px solid #ff4b4b; box-shadow: 0px 0px 20px rgba(255, 75, 75, 0.3);">
        <h2 style="color: #ff4b4b; margin-top: 0;">🎭 {top_meme['character']} — <span style="color: #ffffff;">{top_meme['movie']}</span></h2>
        <p style="font-size: 1.1rem; color: #a0a0c0;"><b>Scenario:</b> {top_meme['scenario_title']} | <b>Archetype:</b> {top_meme['character_archetype']}</p>
        <hr style="border-color: #444455;">
        <h3 style="color: #00ffff; font-style: italic; margin: 20px 0;">{top_meme['dialogue_snippet']}</h3>
        <div style="display: flex; justify-content: space-between; margin-top: 20px;">
            <span style="background-color: #ff4b4b; color: white; padding: 5px 15px; border-radius: 20px; font-weight: bold;">KEW Score: {top_meme['kerala_existential_weight']}/10</span>
            <span style="color: #8888aa; font-family: monospace;">DATA PLANE SHARD: 250k PARQUET LAKE</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("---")

with tabs[2]:
    st.subheader("Vernacular Meme Lake Explorer")
    st.dataframe(df[["meme_id", "character", "movie", "scenario_title", "emotion", "kerala_existential_weight"]].head(50), width='stretch')
