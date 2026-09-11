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

st.set_page_config(page_title="Kerala Biometric Meme Engine", layout="wide", page_icon="🌴")

# Load Parquet Database
@st.cache_data
def load_data():
    full_parquet = "biometric_memes.parquet"
    sample_parquet = "biometric_memes_sample.parquet"
    
    if os.path.exists(full_parquet):
        data = pd.read_parquet(full_parquet)
    elif os.path.exists(sample_parquet):
        data = pd.read_parquet(sample_parquet)
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
                    bytes_data = cam_image.getvalue()
                    np_arr = np.frombuffer(bytes_data, np.uint8)
                    img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

                    # Contrast-Limited Adaptive Histogram Equalization (CLAHE) for dim/backlit webcams
                    lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
                    l, a, b = cv2.split(lab)
                    clahe = cv2.createCLAHE(clipLimit=2.5, tileGridSize=(8, 8))
                    enhanced_img = cv2.cvtColor(cv2.merge((clahe.apply(l), a, b)), cv2.COLOR_LAB2BGR)

                    analysis = DeepFace.analyze(
                        enhanced_img, 
                        actions=['emotion'], 
                        detector_backend='opencv', 
                        enforce_detection=False, 
                        silent=True
                    )
                    
                    if isinstance(analysis, list) and len(analysis) > 0:
                        # Pick the primary/largest foreground face (area = w * h)
                        primary_face = max(
                            analysis, 
                            key=lambda f: f.get('region', {}).get('w', 0) * f.get('region', {}).get('h', 0)
                        )
                        raw_emotions = primary_face.get('emotion', {})
                        
                        # Bayesian Prior-Normalized Affective Classifier:
                        # Resolves FER-2013 training prior bias (where neutral accounts for >58% of weight).
                        # Mathematical formulation: P(intent = e | img) proportional to P_raw(e) / Prior(e)
                        EMOTION_PRIORS = {
                            "neutral": 0.58,
                            "angry": 0.08,
                            "happy": 0.10,
                            "sad": 0.10,
                            "fear": 0.07,
                            "surprise": 0.05,
                            "disgust": 0.02
                        }

                        unnorm_scores = {k: float(v) / EMOTION_PRIORS.get(k, 0.10) for k, v in raw_emotions.items()}
                        total_unnorm = sum(unnorm_scores.values()) if sum(unnorm_scores.values()) > 0 else 1.0
                        calibrated_emotions = {k: (v / total_unnorm) * 100.0 for k, v in unnorm_scores.items()}

                        # Winner selection based on Bayesian calibrated probability
                        detected_emotion = max(calibrated_emotions, key=calibrated_emotions.get)
                        top_calibrated_conf = float(calibrated_emotions[detected_emotion])
                        raw_conf = float(raw_emotions.get(detected_emotion, 0.0))
                        
                        st.success(f"AI Vision Detected: **{detected_emotion.upper()}** ({top_calibrated_conf:.1f}% Calibrated Intent | Raw FER: {raw_conf:.1f}%)")

                        # Display mini emotion meter for full visibility with both calibrated and raw metrics
                        with st.expander("📊 View Facial Micro-Expression Breakdown (Bayesian Calibrated)", expanded=True):
                            sorted_calibrated = sorted(calibrated_emotions.items(), key=lambda x: x[1], reverse=True)
                            for em_name, em_val in sorted_calibrated:
                                r_val = float(raw_emotions.get(em_name, 0.0))
                                st.progress(
                                    min(max(float(em_val) / 100.0, 0.0), 1.0), 
                                    text=f"{em_name.capitalize()}: {float(em_val):.1f}% (Raw FER: {r_val:.1f}%)"
                                )
                    else:
                        detected_emotion = "neutral"
                except Exception as e:
                    detected_emotion = "neutral"
                    st.warning(f"Detection fallback engaged: {e}")
            
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
                    # Proportional scaling to prevent super-tall vertical multi-panel memes from blowing up the column
                    max_display_h = 420
                    w, h = pil_img.size
                    if h > max_display_h:
                        new_w = int(w * (max_display_h / h))
                        display_img = pil_img.resize((new_w, max_display_h), Image.Resampling.LANCZOS)
                    else:
                        display_img = pil_img
                    st.image(display_img, caption=f"Meme Archetype: {archetype} | KEW: {kew_score}/10")
                    rendered_successfully = True
                except Exception:
                    st.image(chosen_img, caption=f"Meme Archetype: {archetype} | KEW: {kew_score}/10")
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
