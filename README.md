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

# 🌴 Kerala Biometric Meme Engine (Mallu Memes V2)
**Real-Time Computer Vision, PySpark Distributed Telemetry, and Vernacular Cultural Intelligence**

An over-engineered, hyper-local biometric cultural intelligence dashboard that pairs **real-time computer vision (DeepFace)** with an enterprise **columnar Parquet data lake** processed via **Apache Spark** to map human facial micro-expressions into existentially heavy Malayalam cinema memes.

---

## ☁️ Deploying to Streamlit Community Cloud (Recommended)

This repository is pre-configured for turnkey 1-click deployment on **Streamlit Community Cloud** ([share.streamlit.io](https://share.streamlit.io/)).

### Step-by-Step Deployment Guide:
1. **Sign in**: Log in to [share.streamlit.io](https://share.streamlit.io/) with your GitHub account.
2. **Deploy an App**: Click **"New app"** (or **"Create app"**).
3. **Repository Configuration**:
   - **Repository**: `RayyanShajahan/mallu-memes`
   - **Branch**: `main`
   - **Main file path**: `app.py`
   - **App URL**: Choose your custom URL or keep the default.
4. **Advanced Settings (Optional)**:
   - **Python Version**: `3.11` (recommended)
5. **Click Deploy**: Streamlit Cloud automatically:
   - Reads [packages.txt](file:///c:/Users/ra416/OneDrive/Desktop/mallu-memes/packages.txt) to install Debian dependencies (`libgl1`, `libglib2.0-0`) for headless OpenCV.
   - Installs Python dependencies from [requirements.txt](file:///c:/Users/ra416/OneDrive/Desktop/mallu-memes/requirements.txt).
   - Ingests the optimized [biometric_memes_sample.parquet](file:///c:/Users/ra416/OneDrive/Desktop/mallu-memes/biometric_memes_sample.parquet) (5,000 records, 55 characters, 29 categories, < 1 MB) adhering strictly to GitHub's 100MB file limit.
   - Serves the live application instantly!

---

## ⚡ Key Architecture & Features

### 1. 📷 Ocular Psyche Biometric Scanner (Tab 2)
- **Native Browser Camera Input**: Uses Streamlit's native `st.camera_input` for zero-configuration webcam access on desktop and mobile without requiring WebRTC STUN/TURN server handshakes.
- **CLAHE Contrast Normalization**: Applies Contrast-Limited Adaptive Histogram Equalization to normalize facial lighting across dark rooms, high-backlight settings, and low-fidelity laptop cameras.
- **Primary Foreground Face Selection**: Automatically extracts the dominant face (`max(w * h)`) to prevent background bystanders from corrupting emotion analysis.
- **Intelligent Neutral-Dampened Affective Detection**: Standard Facial Expression Recognition (FER) neural networks disproportionately skew toward "neutral" (often 40%+ even during genuine laughter or distress). The engine implements an affective dampener: if any expressive emotion exceeds 15% confidence and is at least 45% of the neutral signal, the human expression is actively promoted.
- **Curated Malayalam Meme Vault**: Serves 29 high-resolution authentic Malayalam movie frames (*Kalyanaraman, Nadodikkattu, CID Moosa, Punjabi House, Spadikam, Godfather, Akkare Akkare Akkare, In Harihar Nagar, Aavesham*) mapped directly to psychological categories (*KTU Exam Trauma, Nirvana Thattukada, Political Poru, Monday Work Shokam*).
- **Exact Character & Dialogue Synchronization**: Eliminates character-image mismatches by linking images to canonical identities in `IMAGE_METADATA` and querying matching dialogue snippets and Kerala Existential Weight (KEW) scores.

### 2. 📊 Global Telemetry & KMI Index (Tab 1)
- **Aggregate Kerala Mood Index (KMI)**: Real-time Plotly gauge chart visualizing statewide existential tension.
- **Telemetry Indicators**: Displays total meme lake count, dominant cultural states, and Spark Parquet partition health.

### 3. 📂 Vernacular Meme Lake Explorer (Tab 3)
- Interactive high-performance dataframe explorer querying the columnar Parquet lake.

### 4. 🗄️ Big Data Architecture (PySpark Catalyst)
- Evaluates the **Cultural Relevance Index ($CRI$)**, **Humor Density Metric ($HDM$)**, and compound **Kerala Existential Weight ($KEW$)** across **250,000 records** in **21.57 seconds** using native JVM Catalyst expressions.
- The cloud frontend is decoupled from runtime JVM/Spark requirements, querying the pre-computed Parquet lake through `pyarrow` and `pandas`.

---

## 🚀 Local Quickstart

### Prerequisites
- Python 3.10 or 3.11
- Webcam for biometric capture

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
| **Streamlit Community Cloud** | `app.py` | ✅ Turnkey Ready | `packages.txt` (`libgl1`, `libglib2.0-0`) + `requirements.txt` |
| **Hugging Face Spaces** | Streamlit SDK / Docker | ✅ Turnkey Ready | Configured via `README.md` YAML frontmatter & `Dockerfile` |
| **Local Environment** | Windows / Linux / macOS | ✅ Tested | Python 3.10-3.11 with `.venv` |

---

## 🛠️ Pre-Demo Diagnostic Verification

Run the included hardware and asset diagnostic suite:
```powershell
.venv\Scripts\python.exe verify_environment.py
```

---

## 📜 License
MIT License. Dedicated to the Kerala internet collective consciousness.

