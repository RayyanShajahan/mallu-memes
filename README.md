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

An over-engineered, hyper-local biometric cultural intelligence system that uses **continuous computer vision (WebRTC + DeepFace)** and an enterprise **150MB+ columnar Parquet data lake (250,000 records)** processed via **PySpark** to match user facial micro-expressions with existentially heavy Malayalam cinema memes.

---

## ⚡ Key Features

1. **Live Continuous Biometric Engine (WebRTC + DeepFace)**:
   - Streams 30+ FPS video directly from the user's camera via `streamlit-webrtc` using Google STUN (`stun:stun.l.google.com:19302`).
   - DeepFace extracts real-time micro-expressions and burns a cyberpunk telemetry HUD (`DETECTED PSYCHE`) directly onto the live video feed.
   - Maps emotions (`happy`, `sad`, `angry`, `fear`, `neutral`, `surprise`, `disgust`) to regional cultural buckets (*KTU Exam Trauma, Nirvana Thattukada, Political Poru, Monday Work Shokam*).
   - Instantly scans the 195MB Parquet lake in **< 5 ms** to project a matching high-KEW meme.

2. **Automated Pillow-to-WebP Compression Engine**:
   - Intercepts uncompressed JPEG meme banners, scales them proportionally (`max_width=600`) using `Image.Resampling.LANCZOS`, and converts to in-memory WebP buffers (`quality=60`).
   - Slashes image sizes from **91.5 KB to 3.8 KB (95.9% bandwidth reduction)** in **~3.2 ms**.

3. **Progressive Lazy Loading**:
   - Prevents browser tab crashes by paginating through `st.session_state.feed_limit` and a "Load More Chaos" trigger.
   - Includes an Edge CDN transform toggle (`https://res.cloudinary.com/.../w_600,f_webp/...`) for zero-CPU remote image optimization.

4. **Distributed Big Data Engine (PySpark Catalyst)**:
   - Evaluates the **Cultural Relevance Index ($CRI$)**, **Humor Density Metric ($HDM$)**, and compound **Kerala Existential Weight ($KEW$)** across **250,000 records** in **21.57 seconds** using native JVM Catalyst expressions.

---

## 🚀 Local Quickstart

```powershell
# 1. Clone & activate virtual environment
git clone https://github.com/RayyanShajahan/mallu-memes.git
cd mallu-memes
.venv\Scripts\Activate.ps1

# 2. Install dependencies
pip install -r requirements.txt

# 3. Launch the Streamlit Biometric Dashboard
streamlit run app.py
```
Open `http://localhost:8501` in your browser and grant webcam permissions when prompted.

---

## ☁️ Zero-Cost Hugging Face Spaces Deployment

This repository is pre-configured for free deployment on **Hugging Face Spaces**:
1. Go to [Hugging Face](https://huggingface.co/spaces) and click **"Create New Space"**.
2. Space Name: `kerala-biometric-meme-engine`
3. SDK: Select **Streamlit**.
4. Hardware: Choose **Free CPU Tier (2 vCPU · 16 GB RAM)**.
5. Push repository files:
   - `app.py`
   - `biometric_memes.parquet` (or run `generate_v2_corpus.py` & `spark_processor.py`)
   - `assets/`
   - `requirements.txt`
   - `README.md`
6. Hugging Face will automatically detect the YAML frontmatter and boot the application. The frontend uses `pandas` and `pyarrow` to read the pre-computed Parquet data plane with zero Java/PySpark cluster dependencies at runtime.

---

## 📜 License
MIT License. Built for the Kerala internet collective consciousness.
