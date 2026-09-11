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

This repository supports both **Streamlit SDK** and the recommended **Docker SDK** for Hugging Face Spaces:

### Option A: Standard Streamlit SDK
1. Create a Space on [Hugging Face](https://huggingface.co/spaces), select **Streamlit** SDK, and choose **Free CPU Tier (2 vCPU · 16 GB RAM)**.
2. In `README.md`, ensure the header is:
   ```yaml
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
   ```

### Option B: Containerized Docker SDK (Recommended Fallback)
Hugging Face recently transitioned Spaces toward the Docker runtime. A production-ready `Dockerfile` is provided in the repository root:
1. When creating or configuring the Space, select **Docker** as the SDK.
2. Update the `README.md` YAML header to:
   ```yaml
   ---
   title: Kerala Biometric Meme Engine
   emoji: 🌴
   colorFrom: red
   colorTo: yellow
   sdk: docker
   pinned: false
   ---
   ```
3. The container automatically installs OpenCV system libraries, pre-caches `facial_expression_model_weights.h5` during build, and binds Streamlit to port `7860`.

---

## 🛠️ Pre-Demo Verification Suite

Run the diagnostic tool before live presentations:
```powershell
.venv\Scripts\python.exe verify_environment.py
```
Checks:
- **Weight Cache Integrity**: Confirms `facial_expression_model_weights.h5` (~5.97 MB) is present in `~/.deepface/weights/`.
- **STUN Connectivity**: Tests UDP ping to `stun.l.google.com:19302` to ensure venue firewalls allow WebRTC handshakes.
- **Hardware Camera**: Confirms device index 0 is open and accessible.

---

## 📜 License
MIT License. Built for the Kerala internet collective consciousness.
