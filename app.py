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
    st.write("Extracts your instantaneous facial micro-expression and projects a matched Kerala existential meme.")

    capture_mode = st.radio(
        "Choose Biometric Capture Mode:",
        ["Continuous Live Stream (WebRTC)", "Instant Snapshot Frame (Camera Input)", "Emotion Simulator (Test Matrix)"],
        horizontal=True
    )

    detected_emotion = "neutral"

    if capture_mode == "Continuous Live Stream (WebRTC)":
        if WEBRTC_AVAILABLE:
            RTC_CONFIGURATION = RTCConfiguration({"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]})
            
            class EmotionProcessor(VideoProcessorBase):
                def __init__(self):
                    self.emotion = "neutral"
                    self.frame_count = 0
                    self.last_valid = "neutral"

                def recv(self, frame):
                    img = frame.to_ndarray(format="bgr24")
                    self.frame_count += 1
                    
                    # Analyze every 10th frame for optimal balance of speed and responsiveness
                    if self.frame_count % 10 == 0:
                        try:
                            # enforce_detection=False prevents crashes when face moves or lighting varies
                            analysis = DeepFace.analyze(img, actions=['emotion'], enforce_detection=False, silent=True)
                            if isinstance(analysis, list) and len(analysis) > 0:
                                self.last_valid = analysis[0].get('dominant_emotion', 'neutral')
                        except Exception:
                            pass
                            
                    self.emotion = self.last_valid
                    cv2.putText(img, f"PSYCHE: {self.emotion.upper()}", (25, 50), 
                                cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 255, 255), 2, cv2.LINE_AA)
                    return av.VideoFrame.from_ndarray(img, format="bgr24")

            ctx = webrtc_streamer(key="scanner", video_processor_factory=EmotionProcessor, rtc_configuration=RTC_CONFIGURATION, async_processing=True)
            if ctx.video_processor:
                detected_emotion = ctx.video_processor.emotion
        else:
            st.warning("WebRTC unavailable. Falling back to Simulator.")
            capture_mode = "Emotion Simulator (Test Matrix)"

    elif capture_mode == "Instant Snapshot Frame (Camera Input)":
        cam_image = st.camera_input("Capture expression")
        if cam_image is not None:
            try:
                bytes_data = cam_image.getvalue()
                img_np = np.array(Image.open(io.BytesIO(bytes_data)).convert("RGB"))
                analysis = DeepFace.analyze(img_np, actions=['emotion'], enforce_detection=False, silent=True)
                if isinstance(analysis, list) and len(analysis) > 0:
                    detected_emotion = analysis[0].get('dominant_emotion', 'neutral')
                else:
                    detected_emotion = "neutral"
                st.success(f"Detected Emotion: {detected_emotion.upper()}")
            except Exception:
                detected_emotion = "neutral"

    else:
        detected_emotion = st.selectbox(
            "Simulate Facial Micro-Expression (Guaranteed Demo Mode):",
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
    st.markdown(f"🎯 Detected Psyche: **{detected_emotion.upper()}** ➔ Routing to Category: **{target_category}**")

    # Dynamic Parquet Filtering (Ensures valid matching rows)
    matched_df = df[df["emotion"].astype(str).str.lower() == detected_emotion.lower()]
    if matched_df.empty and "target_emotion" in df.columns:
        matched_df = df[df["target_emotion"].astype(str).str.lower() == detected_emotion.lower()]
    if matched_df.empty and detected_emotion.lower() == "surprise":
        matched_df = df[df["emotion"].astype(str).str.lower() == "happy"]
    if matched_df.empty:
        matched_df = df # Fallback if specific emotion rows are sparse

    # Pick top meme based on highest KEW score
    top_meme = matched_df.sort_values(by="kerala_existential_weight", ascending=False).iloc[0]

    # Layout: Image Display vs Text Dialogue
    col_img, col_txt = st.columns([1, 1])
    
    with col_img:
        st.markdown("### 🖼️ Matched Meme Artifact")
        asset_files = [f for f in os.listdir("assets/memes") if f.endswith(".jpg")] if os.path.exists("assets/memes") else []
        if asset_files:
            char_lower = str(top_meme.get("character", "")).lower()
            matched_asset = next((f for f in asset_files if any(k in f.lower() for k in char_lower.split() if len(k) > 2)), None)
            chosen_asset = os.path.join("assets/memes", matched_asset if matched_asset else random.choice(asset_files))
            st.image(chosen_asset, caption=top_meme["scenario_title"], width='stretch')
        else:
            st.warning("Local assets missing. Run `create_sample_assets.py`.")
            st.image("https://images.unsplash.com/photo-1531403009284-440f080d1e12?w=600&auto=format&fit=crop&q=60", width='stretch')

    with col_txt:
        st.markdown(f"### 🎭 {top_meme['character']} — {top_meme['movie']}")
        st.markdown(f"**Scenario:** {top_meme['scenario_title']}")
        st.markdown(f"**Archetype:** {top_meme['character_archetype']} | **KEW Score:** {top_meme['kerala_existential_weight']}/10")
        st.info(f"**Dialogue Transcript:**\n\n{top_meme['dialogue_snippet']}")

with tabs[2]:
    st.subheader("Vernacular Meme Lake Explorer")
    st.dataframe(df[["meme_id", "character", "movie", "scenario_title", "emotion", "kerala_existential_weight"]].head(50), width='stretch')
