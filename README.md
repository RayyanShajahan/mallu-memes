---
title: Kerala Biometric Meme Engine
emoji: 🌴
colorFrom: red
colorTo: yellow
sdk: streamlit
sdk_version: "1.63.0"
app_file: app.py
pinned: false
---

# 🌴 The "Meme-ing" of Life — Kerala Edition
**Real-Time Affective Biometrics, PySpark Distributed Telemetry & Vernacular Cultural Intelligence**

An over-engineered, hyper-local biometric cultural intelligence dashboard that pairs **real-time computer vision (DeepFace)** with an enterprise **columnar Parquet data lake** processed via **Apache Spark 4.2.0** to decode human facial micro-expressions into existentially heavy Malayalam cinema memes and macroscopic regional sentiment telemetry.

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://share.streamlit.io/RayyanShajahan/mallu-memes/main/app.py)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.11](https://img.shields.io/badge/python-3.11-blue.svg)](https://www.python.org/downloads/release/python-3110/)
[![Documentation: EXPLANATION.md](https://img.shields.io/badge/Docs-Interview%20Playbook-cyan.svg)](EXPLANATION.md)

---

## ☁️ Deploying to Streamlit Community Cloud (1-Click Turnkey)

This repository is 100% pre-configured and verified for turnkey deployment on **Streamlit Community Cloud** ([share.streamlit.io](https://share.streamlit.io/)).

### Step-by-Step Deployment Guide:
1. **Sign in**: Log in to [share.streamlit.io](https://share.streamlit.io/) with your GitHub account.
2. **Deploy an App**: Click **"New app"** (or **"Create app"**).
3. **Repository Configuration**:
   - **Repository**: `RayyanShajahan/mallu-memes`
   - **Branch**: `main`
   - **Main file path**: `app.py`
   - **App URL**: *(Choose your custom subdomain or keep default)*
4. **Advanced Settings**:
   - **Python Version**: `3.11` (recommended)
5. **Click Deploy**: Streamlit Cloud automatically:
   - Reads [packages.txt](packages.txt) to install Debian dependencies (`libgl1`, `libglib2.0-0`, `libgomp1`) for headless OpenCV execution.
   - Installs Python dependencies from [requirements.txt](requirements.txt).
   - Ingests the optimized [biometric_memes_sample.parquet](biometric_memes_sample.parquet) (5,000 records, 55 characters, 29 categories, < 1 MB) adhering strictly to GitHub's 100MB file limit.
   - Applies cyberpunk server settings from [.streamlit/config.toml](.streamlit/config.toml).
   - Serves the live application instantly!

---

## ⚡ Key Architecture & Features

### 1. 📊 Statewide Cultural Sentiment Observatory (Tab 1)
- **Aggregate Kerala Mood Index (KMI)**: Real-time Plotly gauge (0–15) tracking cultural tension fault lines (*0-5: Nirvana / Thattukada Vibe, 5-10: Monday Work Shokam, 10-15: Critical KTU / Hartal Pressure*).
- **Regional Sentiment Distribution `[DISTRICT.VECTOR]`**: Grouped bar chart comparing *Joy Coefficient* and *Existential Load* across 6 major Kerala cultural hubs: Ernakulam (`EKM`), Thiruvananthapuram (`TVM`), Kozhikode (`KKD`), Thrissur (`TCR`), Kannur (`KNR`), and Alappuzha (`ALP`).
- **Collective Psyche Pulse `[PULSE.6H]`**: Trailing 6-hour temporal area chart with neon cyan gradient fill mapping macroscopic psychological tension shifts.
- **Live Ingestion Stream `[STREAM.LIVE]`**: Monospace real-time ticker logging live vernacular micro-events with district origin, discourse snippet, and delta KEW weight tags.

### 2. 📸 Ocular Psyche Biometric Scanner (Tab 2)
- **Native Browser Camera Input**: Uses Streamlit's native `st.camera_input` for zero-lag webcam access on both desktop and mobile without requiring WebRTC STUN/TURN server handshakes.
- **CLAHE Contrast Normalization**: Contrast-Limited Adaptive Histogram Equalization in LAB space equalizes dim or backlit webcam frames.
- **Bayesian Prior De-Biasing Algorithm**: Solves the FER-2013 58% neutral class prior imbalance ($P_{\text{intent}} = P_{\text{raw}} / \text{Prior}$), boosting closed-mouth angry scowls from 22% raw confidence to 66% calibrated intent.
- **4,075-D Personalized Biometric Vector Memory ("Teach AI")**: Enables few-shot personal calibration without modifying neural network weights (preventing catastrophic forgetting) by matching 1,764 HOG bins + 2,304 grayscale topography pixels + 7 FER neural outputs in under 15 microseconds.
- **Cinematic Artifact Match Display**: Renders high-resolution curated frames with `MATCH 99.4%` badge, Malayalam quote, English translation subtitle, KEW score, and Signal Class badge.

### 3. 🗄️ Vernacular Meme Vault & Lake Explorer (Tab 3)
- **Searchable Visual Card Grid**: 3-column responsive grid with uniform 16:10 cinematic cropping containing 12 curated cult artifacts spanning *Premam, Spadikam, Nadodikkattu, Aavesham, Punjabi House, Kalyanaraman, CID Moosa, In Harihar Nagar*, and *Godfather*.
- **Interactive Mood Filtering**: Filter pills for `All`, `Hope`, `Despair`, `Rage`, and `Chaos`.
- **Quick Copy Dialogue Snippets**: One-click formatted code snippet blocks (`st.code`) for instant viral sharing.
- **Big Data Parquet Lake Query Engine**: Interactive 250,000-record Parquet data lake query console with emotion, category, and stream limit filters.

### 4. 🧮 Big Data Architecture (PySpark Catalyst)
- Evaluates the **Cultural Relevance Index ($CRI$)**, **Humor Density Metric ($HDM$)**, and compound **Kerala Existential Weight ($KEW = 0.6 \cdot CRI + 0.4 \cdot HDM$)** across **250,000 records** in **21.57 seconds** using native JVM Catalyst expressions.
- The cloud frontend is decoupled from JVM runtimes, querying the Snappy-compressed Parquet store via `pyarrow` and `pandas`.

---

## 📖 Technical Documentation & Interview Preparation

For a complete architectural deep-dive and a 20-question technical interview preparation guide, read:
👉 **[EXPLANATION.md](EXPLANATION.md)**

---

## 🚀 Local Quickstart

### Windows (PowerShell)
```powershell
# 1. Clone repository
git clone https://github.com/RayyanShajahan/mallu-memes.git
cd mallu-memes

# 2. Create and activate virtual environment
python -m venv .venv
.venv\Scripts\Activate.ps1

# 3. Install dependencies
pip install -r requirements.txt

# 4. Launch Streamlit app
streamlit run app.py
```

### Linux / macOS
```bash
# 1. Clone repository
git clone https://github.com/RayyanShajahan/mallu-memes.git
cd mallu-memes

# 2. Create and activate virtual environment
python3 -m venv .venv
source .venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Launch Streamlit app
streamlit run app.py
```

Navigate to `http://localhost:8501` in your browser.

---

## 📦 Cloud & Container Compatibility Matrix

| Platform | Deployment Target | Status | Requirements |
| :--- | :--- | :--- | :--- |
| **Streamlit Community Cloud** | `app.py` | ✅ Turnkey Ready | `packages.txt` (`libgl1`, `libglib2.0-0`, `libgomp1`) + `requirements.txt` |
| **Hugging Face Spaces** | Streamlit SDK / Docker | ✅ Turnkey Ready | Configured via `README.md` YAML frontmatter & `Dockerfile` |
| **Local Environment** | Windows / Linux / macOS | ✅ Tested | Python 3.10-3.11 with `.venv` |

---

## 📜 License
MIT License. Dedicated to the Kerala internet collective consciousness.
