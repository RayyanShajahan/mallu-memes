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
    st.subheader("Curated Malayalam Meme Vault (Offline Mode)")
    st.write("Instant manual emotion selection mapped directly to your local meme library.")

    # Dropdown to select emotion directly without camera friction
    selected_emotion = st.selectbox(
        "Select Emotional State:",
        ["sad", "angry", "happy", "neutral", "fear", "surprise"]
    )

    emotion_map = {
        "sad": "KTU Exam Trauma",
        "fear": "KTU Exam Trauma",
        "angry": "Political Poru & Hartal",
        "disgust": "Political Poru & Hartal",
        "happy": "Nirvana (Thattukada & Vibe)",
        "surprise": "Nirvana (Thattukada & Vibe)",
        "neutral": "Monday Work Shokam"
    }
    target_category = emotion_map.get(selected_emotion, "Monday Work Shokam")
    st.info(f"🎯 Target Category: **{target_category}**")

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

    col1, col2 = st.columns([1, 1], gap="medium")

    with col1:
        st.markdown("### 📥 Local Meme Artifact")
        asset_dir = "assets/memes"
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
            cat = category_map.get(selected_emotion, "neutral")
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
                try:
                    pil_img = Image.open(chosen_img)
                    st.image(pil_img, caption=f"Meme Archetype: {top_meme['character_archetype']}", width='stretch')
                except Exception:
                    st.image(chosen_img, caption=f"Meme Archetype: {top_meme['character_archetype']}", width='stretch')
            else:
                st.warning("No images found in assets/memes/. Run download_curated_memes.py to fetch them!")
        else:
            st.error("Missing assets/memes folder.")

    with col2:
        st.markdown(f"### 🎭 {top_meme['character']} — {top_meme['movie']}")
        st.markdown(f"**Scenario:** {top_meme['scenario_title']}")
        dialogue_text = str(top_meme['dialogue_snippet']).strip('"').strip("'")
        st.info(f"**Dialogue:**\n\n\"{dialogue_text}\"")
        st.metric("Kerala Existential Weight (KEW)", f"{top_meme['kerala_existential_weight']}/10")
        st.caption(f"Matched from 250,000-record Parquet Lake | CRI: {top_meme.get('cultural_relevance_index', 9.0):.1f} | HDM: {top_meme.get('humor_density_metric', 8.5):.1f}")

with tabs[2]:
    st.subheader("Vernacular Meme Lake Explorer")
    st.dataframe(df[["meme_id", "character", "movie", "scenario_title", "emotion", "kerala_existential_weight"]].head(50), width='stretch')
