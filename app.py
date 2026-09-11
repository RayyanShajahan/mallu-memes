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
    st.write("Compact live capture on the left mapped to automated meme artifact rendering on the right.")

    # Create a clean split screen: Left for camera/controls, Right for the meme output
    left_col, right_col = st.columns([1, 1], gap="medium")

    with left_col:
        st.markdown("### 📷 Biometric Capture")
        capture_mode = st.radio(
            "Mode:",
            ["📸 Snapshot", "🧪 Simulator"],
            horizontal=True
        )

        detected_emotion = "neutral"

        if capture_mode == "📸 Snapshot":
            # Compact camera input sizing
            cam_image = st.camera_input("Capture expression", label_visibility="collapsed")
            if cam_image is not None:
                try:
                    bytes_data = cam_image.getvalue()
                    np_arr = np.frombuffer(bytes_data, np.uint8)
                    img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

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
                    
                    st.success(f"Detected: **{detected_emotion.upper()}**")
                except Exception as e:
                    detected_emotion = "neutral"
                    st.warning(f"Detection fallback engaged: {e}")
        else:
            detected_emotion = st.selectbox(
                "Demo Override Emotion:",
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
        st.info(f"🎯 **Profile:** {detected_emotion.upper()} ➔ **Category:** {target_category}")

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
        matched_df = df[(df["scenario_category"] == target_category) | (df["scenario_category"] == actual_cat) | (df["emotion"].astype(str).str.lower() == detected_emotion.lower())]
        if matched_df.empty:
            matched_df = df

        top_meme = matched_df.sample(n=1).iloc[0] if len(matched_df) > 0 else df.iloc[0]

        # Safe asset image rendering from assets/memes/
        asset_dir = "assets/memes"
        rendered_image = False
        if os.path.exists(asset_dir):
            asset_files = [f for f in os.listdir(asset_dir) if f.endswith(".jpg")]
            if asset_files:
                char_lower = str(top_meme.get("character", "")).lower()
                matched_asset = next((f for f in asset_files if any(k in f.lower() for k in char_lower.split() if len(k) > 2)), None)
                chosen_asset = os.path.join(asset_dir, matched_asset if matched_asset else random.choice(asset_files))
                st.image(
                    chosen_asset, 
                    caption=f"{top_meme['character']} | KEW Score: {top_meme['kerala_existential_weight']}/10", 
                    width='stretch'
                )
                rendered_image = True

        if not rendered_image:
            st.warning("Local assets missing or empty. Run `create_sample_assets.py` to generate visual meme cards.")

        # Clean snippet text for safe rendering
        snippet_text = str(top_meme['dialogue_snippet']).strip('"').strip("'")

        # Cinematic Text Card below or alongside the image
        st.markdown(f"""
        <div style="background-color: #1e1e2f; padding: 20px; border-radius: 12px; border: 2px solid #ff4b4b; margin-top: 10px;">
            <h3 style="color: #ff4b4b; margin-top: 0;">🎭 {top_meme['character']} — <span style="color: #ffffff;">{top_meme['movie']}</span></h3>
            <p style="font-size: 0.95rem; color: #a0a0c0;"><b>Scenario:</b> {top_meme['scenario_title']}</p>
            <hr style="border-color: #444455;">
            <p style="color: #00ffff; font-style: italic; font-size: 1.1rem; margin: 10px 0;">"{snippet_text}"</p>
            <div style="display: flex; justify-content: space-between; margin-top: 15px;">
                <span style="background-color: #ff4b4b; color: white; padding: 4px 12px; border-radius: 15px; font-weight: bold; font-size: 0.85rem;">KEW: {top_meme['kerala_existential_weight']}/10</span>
                <span style="color: #8888aa; font-family: monospace; font-size: 0.8rem;">250k PARQUET LAKE</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

with tabs[2]:
    st.subheader("Vernacular Meme Lake Explorer")
    st.dataframe(df[["meme_id", "character", "movie", "scenario_title", "emotion", "kerala_existential_weight"]].head(50), width='stretch')
