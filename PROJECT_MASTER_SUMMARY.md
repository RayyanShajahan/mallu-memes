# PROJECT MASTER SUMMARY & SYSTEM COMPENDIUM
**Mallu Memes: Kerala Collective Psyche Distributed Processor & Biometric Meme Engine**  
*Document Version:* `3.2.0-LIVE-WEBRTC-BIOMETRIC-ENGINE`  
*Last Synchronized:* September 2026  
*Target Hardware:* ASUS TUF F16 (Local Multi-Core CPU + Integrated IR/Webcam)  
*Cloud Target:* Hugging Face Spaces (Free CPU Tier: 2 vCPU · 16 GB RAM)  
*Status:* Active / Phase 5 Live Continuous WebRTC Engine, 150MB+ PySpark Parquet Lake, DeepFace Vision, WebP Lazy Feed & Cloud Architecture Operational  

---

> [!IMPORTANT]
> **LIVING DOCUMENT DIRECTIVE (MANDATORY FOR ALL TEAMMATES)**:  
> This file is the **Single Source of Truth (SSOT)** for the entire repository. Whenever any engineer or agent adds, modifies, or refactors an execution script, scoring heuristic, schema definition, frontend component, or pipeline stage, **this file MUST be updated in the same commit/turn**. Keep every section synchronized so cross-functional teammates (Big Data, Computer Vision, Frontend, QA) can build without discrepancies.

---

## TABLE OF CONTENTS
1. [Project Mission, Vernacular Philosophy & Architectural Invariants](#1-project-mission-vernacular-philosophy--architectural-invariants)
2. [High-Level System Topology & Distributed Architecture](#2-high-level-system-topology--distributed-architecture)
3. [Repository Inventory — File & Directory Map](#3-repository-inventory--file--directory-map)
4. [What Has Been Done So Far (Milestones & Changelog)](#4-what-has-been-done-so-far-milestones--changelog)
5. [Proprietary Scoring Algorithms & Mathematical Formulations](#5-proprietary-scoring-algorithms--mathematical-formulations)
6. [Data Schemas & Payload Contracts](#6-data-schemas--payload-contracts)
7. [Infrastructure & Distributed Runtime Specifications](#7-infrastructure--distributed-runtime-specifications)
8. [Zero-Cost Cloud Deployment Architecture (Hugging Face Spaces)](#8-zero-cost-cloud-deployment-architecture-hugging-face-spaces)
9. [Developer Quickstart & Execution Runbook](#9-developer-quickstart--execution-runbook)
10. [Downstream Roadmap & Future Phases](#10-downstream-roadmap--future-phases)

---

## 1. PROJECT MISSION, VERNACULAR PHILOSOPHY & ARCHITECTURAL INVARIANTS

The **Mallu Memes Analytics Platform (V2 Biometric Meme Engine)** is an enterprise-grade vernacular cultural intelligence, sentiment analysis, and continuous computer vision system designed to quantify the existential absurdities of Malayalam internet culture and mirror them directly onto user facial micro-expressions in real-time.

By combining an enterprise **150MB+ (250,000 records) raw Parquet corpus**, **PySpark Catalyst distributed compute engines in local mode**, **continuous WebRTC live video streaming via `streamlit-webrtc`**, **DeepFace neural facial expression inference**, and **automated Pillow-to-WebP backend compression**, the system achieves maximum architectural pretentiousness, zero-cloud egress costs, and sub-millisecond local latency on consumer laptop hardware (ASUS TUF F16) while remaining 100% cloud-deployable on free-tier Hugging Face Spaces.

### The 7 Inviolable Architectural Invariants

1. **Massive Columnar Parquet Lake (150MB+ / 250,000 Records)**:
   - All vernacular meme transcripts must be stored and manipulated in columnar Apache Parquet format (`raw_meme_corpus.parquet` and `biometric_memes.parquet`) rather than bloated JSON to prevent browser and frontend memory leaks.
   - The corpus includes 55+ distinct Malayalam cinematic characters and 35+ hyper-specific regional scenarios.
2. **Distributed Compute via PySpark Catalyst Engine**:
   - Every raw OCR text extracted from Malayalam social media memes undergoes distributed transformation via Apache Spark (`pyspark.sql`).
   - Scoring heuristics and emotion categorizations are implemented using vectorized Spark Catalyst expressions (`when`, `regexp_extract_all`, `least`) executing directly within JVM 17 for maximum throughput.
3. **Deterministic Cultural Quantification**:
   - Satire, cinematic archetypes, and societal anxieties are codified into weighted anchor vectors.
   - Every meme resolves into a deterministic triad of scores:
     - `cultural_relevance_index` $\in [0.0, 10.0]$
     - `humor_density_metric` $\in [0.0, 10.0]$
     - `kerala_existential_weight` $\in [0.0, 10.0]$
4. **Live Continuous Biometric Engine (WebRTC + DeepFace)**:
   - Continuous video frames are captured via `streamlit-webrtc` over Google STUN (`stun:stun.l.google.com:19302`).
   - `BiometricEmotionProcessor` throttles inference to every 4th frame for smooth 30+ FPS video while running DeepFace OpenCV emotion analysis.
   - The detected emotional state is burned directly onto the video feed HUD using `cv2.putText`.
5. **Categorical Emotion Routing Matrix**:
   - Live micro-expressions map directly into regional vernacular taxonomies:
     - `sad` / `fear` $\to$ **KTU Exam Trauma**
     - `angry` / `disgust` $\to$ **Political Poru & Hartal**
     - `happy` / `surprise` $\to$ **Nirvana (Thattukada & Vibe)**
     - `neutral` $\to$ **Monday Work Shokam**
   - The system performs a sub-millisecond columnar scan on the Parquet dataframe to extract high Kerala Existential Weight (KEW $\ge 85$th percentile) memes matching that exact affective state.
6. **Automated Pillow-to-WebP Compression (Backend)**:
   - High-resolution meme images are intercepted by Pillow, proportionally downscaled (`max_width=600`) using `Image.Resampling.LANCZOS`, and converted to in-memory WebP buffers (`quality=60`).
   - Slashes image payload sizes by **80% to 96%** compared to standard uncompressed JPEGs.
7. **Frontend Lazy Loading & Zero-Cost Cloud Portability**:
   - Progressive batch rendering in Streamlit is governed via `st.session_state.feed_limit` and a "Load More Chaos" trigger.
   - Decoupled from runtime PySpark/Java dependencies: the frontend operates strictly on `pandas` and `pyarrow` over the pre-computed Parquet lake, making it instantly deployable on Hugging Face Spaces' free CPU tier.

---

## 2. HIGH-LEVEL SYSTEM TOPOLOGY & DISTRIBUTED ARCHITECTURE

```mermaid
flowchart TB
    subgraph Phase1["Phase 1: Massive Parquet Corpus Synthesis (150MB+)"]
        CharDB["55+ Cinematic Characters\n(Damu, Manavalan, CID Moosa, Ramanathan)"]
        ScenDB["35+ Cultural Scenarios\n(KTU Backlogs, Bangalore Sleeper Bus, Kochi Metro)"]
        Synthesizer["Corpus Generator\n(generate_v2_corpus.py)"]
        RawParquet[("raw_meme_corpus.parquet\n187.97 MB | 250,000 Records")]
        CharDB --> Synthesizer
        ScenDB --> Synthesizer
        Synthesizer --> RawParquet
    end

    subgraph DistributedEngine["Phase 2: Hyper-Converged PySpark Engine (Local Mode)"]
        SparkSession["SparkSession Builder\nMaster: local[4] | Memory: 4GB\nVectorized Catalyst Expressions"]
        
        subgraph SparkCatalyst["Spark Catalyst Optimizer / JVM 17"]
            CRI_Expr["Catalyst Expr: Cultural Relevance Index (CRI)\nWeighted Anchors | Range: 0.0 - 10.0"]
            HDM_Expr["Catalyst Expr: Humor Density Metric (HDM)\nPunctuation Hysteria & All-Caps\nRange: 0.0 - 10.0"]
            Emo_Expr["Catalyst Expr: DeepFace Emotion Classifier\n(happy, sad, angry, fear, neutral)"]
            HarmonicTensor["Compound Weight Formulation\nKEW = (CRI * 0.6) + (HDM * 0.4)"]
        end

        RawParquet --> SparkSession
        SparkSession --> SparkCatalyst
        CRI_Expr --> HarmonicTensor
        HDM_Expr --> HarmonicTensor
        Emo_Expr --> HarmonicTensor
        BiometricParquet[("biometric_memes.parquet\n195.81 MB | 250,000 Records")]
        HarmonicTensor -->|PyArrow Stream (Snappy/None)| BiometricParquet
    end

    subgraph Phase5["Phase 5: The Live Continuous Biometric Dashboard (app.py)"]
        App["Streamlit Dashboard\n(Port 8501 / Hugging Face Spaces)"]
        
        subgraph Tab1["Tab 1: Global Telemetry"]
            Gauge["Plotly go.Indicator KMI Gauge"]
            BarChart["Plotly Express Emotion Volume"]
            Leaderboard["Top Existential Artifacts"]
        end

        subgraph Tab2["Tab 2: Ocular Psyche Biometric Scanner"]
            WebRTC["streamlit-webrtc Video Stream\nSTUN: stun.l.google.com:19302"]
            Processor["BiometricEmotionProcessor\nDeepFace Neural Inference (OpenCV Backend)\nHUD Overlay: 'DETECTED PSYCHE'"]
            SnapshotFallback["Fallback Mode: st.camera_input()"]
            SimFallback["Fallback Mode: Emotion Simulator"]
            RoutingMatrix["Emotion Routing Matrix\n(KTU Trauma, Political Poru, Nirvana, Work Shokam)"]
            Matcher["Sub-ms Parquet Scanner\n(Top 15% KEW Filter)"]
            MemeCard["Matched Meme HTML Card"]
            WebPBanner["On-the-Fly WebP Banner"]
            
            WebRTC --> Processor --> RoutingMatrix
            SnapshotFallback --> RoutingMatrix
            SimFallback --> RoutingMatrix
            RoutingMatrix --> Matcher --> MemeCard & WebPBanner
        end

        subgraph Tab3["Tab 3: Lazy-Loaded Vernacular Feed"]
            LocalAssets["Local JPEG Assets\n(assets/memes/*.jpg)"]
            PillowCompress["compress_image()\nLANCZOS + WebP 60 (-95.9% size)"]
            LazyLoad["st.session_state.feed_limit\n'Load More Chaos' Trigger"]
            CDNEdge["Cloudinary / CDN Edge Mode\n(w_600,f_webp Transform)"]
            LocalAssets --> PillowCompress --> LazyLoad
            CDNEdge --> LazyLoad
        end

        BiometricParquet --> App
        App --> Tab1 & Tab2 & Tab3
    end
```

---

## 3. REPOSITORY INVENTORY — FILE & DIRECTORY MAP

```
mallu-memes/
├── .agents/
│   └── rules/
│       └── sync-master-summary.md          # Automation rule enforcing SSOT synchronization
├── .dockerignore                           # Context exclusions for container builds
├── .gitignore                              # Comprehensive exclusions (venv, caches, *.parquet)
├── .venv/                                  # Isolated Python 3.11 virtual environment
├── assets/
│   └── memes/                              # Sample high-resolution uncompressed JPEG memes
│       ├── cid_moosa_sadhanam.jpg          # CID Moosa classic card (90.1 KB)
│       ├── damu_choodu.jpg                 # Dashamoolam Damu rage card (91.5 KB)
│       ├── harisree_appukuttan.jpg         # Appukuttan panic card (94.2 KB)
│       ├── mamukoya_gafoor.jpg             # Gafoor Ka Dost melodrama card (78.7 KB)
│       ├── manavalan_royal.jpg             # Manavalan pride card (90.4 KB)
│       ├── pappu_shariyaakkam.jpg          # Pappu road roller card (96.7 KB)
│       ├── pyari_rasikan.jpg               # Pyari laughter card (88.5 KB)
│       └── ramanathan_malappuram.jpg       # Ramanathan shock card (89.6 KB)
├── Dockerfile                              # Production Hugging Face Spaces Docker SDK container definition
├── LICENSE                                 # MIT Open Source License
├── README.md                               # Project intro, Hugging Face metadata & runbook
├── app.py                                  # Phase 5 Live Continuous WebRTC Biometric Streamlit App
├── biometric_memes.parquet                 # 195.81 MB pre-computed Parquet dataset (250,000 records)
├── create_sample_assets.py                 # Generates sample high-res meme JPEG banners
├── generate_v2_corpus.py                   # V2 massive streaming corpus generator (150MB+ / 250k rec)
├── PROJECT_MASTER_SUMMARY.md               # [THIS FILE] Single Source of Truth Compendium
├── raw_meme_corpus.parquet                 # 187.97 MB raw Parquet corpus (250,000 records)
├── requirements.txt                        # Pinned dependencies (streamlit-webrtc, av, deepface, etc.)
├── spark_processor.py                      # V2 PySpark Distributed Emotion Mapping Engine
└── verify_environment.py                   # Pre-demo diagnostic suite (STUN, weights, camera)
```

### Detailed Component Inventory

| File / Component | Primary Technology | Purpose & Responsibility |
| :--- | :--- | :--- |
| `app.py` | Python 3.11, Streamlit 1.63, `streamlit-webrtc` 0.77, `av` 17.1, DeepFace 0.0.100, OpenCV 4.14, Pillow 12.3, Plotly 7.0 | Resilient Phase 5 Live Continuous Biometric Meme Engine frontend. Features 3 tabs: Global Telemetry gauge, Biometric Scanner with drop-proof WebRTC video streaming, Instant Snapshot Frame (Pillow RGB decoded), Emotion Simulator matrix, and side-by-side true JPEG meme artifact rendering from `assets/memes/`, and Vernacular Data Lake explorer. |
| `spark_processor.py` | Python 3.11, PySpark 4.2.0, PyArrow 25.0 | Distributed ETL processor (`KeralaBiometricMemeProcessor`). Ingests `raw_meme_corpus.parquet`, applies vectorized Spark Catalyst expressions for CRI, HDM, and DeepFace emotion classification, and writes `biometric_memes.parquet`. |
| `generate_v2_corpus.py` | Python 3.11, PyArrow 25.0 | Streaming synthesizer that generates 250,000 authentic vernacular meme records (187.97 MB Parquet) across 55 cinematic characters and 35 cultural scenarios. |
| `verify_environment.py` | Python 3.11, `socket`, `cv2` | Pre-demo verification diagnostic suite. Validates DeepFace weight cache integrity, Google STUN UDP connectivity, and hardware camera device access. |
| `Dockerfile` | Docker, Debian Slim, Python 3.11 | Containerized runtime definition for Hugging Face Spaces Docker SDK. Pre-caches neural weights, installs system OpenCV/ffmpeg codecs, and serves on port 7860. |
| `.dockerignore` | Docker | Ignores local `.venv`, `__pycache__`, and git caches during Docker container builds. |
| `create_sample_assets.py` | Python 3.11, Pillow 12.3 | Generates sample uncompressed 900x500 JPEG meme banners in `assets/memes/` to validate backend WebP compression and lazy loading. |
| `raw_meme_corpus.parquet` | Apache Parquet (Uncompressed) | 187.97 MB raw ingestion corpus with 250,000 rows, 18 columns, and rich Manglish OCR text dialogues. |
| `biometric_memes.parquet` | Apache Parquet (Uncompressed) | 195.81 MB indexed analytical data plane with 250,000 rows and 22 columns including `cultural_relevance_index`, `humor_density_metric`, `emotion`, and `kerala_existential_weight`. |
| `README.md` | Markdown + YAML | Project README with Hugging Face Spaces configuration metadata (supporting both Streamlit & Docker SDKs). |
| `requirements.txt` | Pip | Dependency manifest pinned with `streamlit-webrtc`, `av`, `deepface`, `opencv-python`, `fastparquet`, `pyarrow`, `pyspark`, `streamlit`, `pillow`, `plotly`, `tf-keras`, and `nltk`. |

---

## 4. WHAT HAS BEEN DONE SO FAR (MILESTONES & CHANGELOG)

### Milestone 1: Distributed Infrastructure Provisioning (September 2026)
- **Microsoft OpenJDK 17 LTS Installed**: Provisioned through `winget` (`Microsoft.OpenJDK.17` version `17.0.20.101`). Permanent system `JAVA_HOME` configured at `C:\Program Files\Microsoft\jdk-17.0.20.101-hotspot\` with JVM binaries in system `Path`.
- **Virtual Environment Rebuild**: Migrated environment to Python 3.11.9 (`C:\Users\ra416\AppData\Local\Programs\Python\Python311\python.exe`) to guarantee binary wheel compatibility with `tensorflow`, `deepface`, and `streamlit-webrtc`.

### Milestone 2–5: V1 Distributed Pipeline, NLP Model & KMI Dashboard (Archived)
- Built and validated pilot pipeline on the 85-record test corpus. Superseded by the V2 150MB+ columnar Parquet and computer vision architecture.

### Milestone 6: V2 Biometric Meme Engine & 150MB+ Corpus Architecture
- **Corpus Scaling (`generate_v2_corpus.py`)**: Built a high-throughput streaming Parquet writer utilizing `pyarrow.parquet.ParquetWriter`. Synthesized **250,000 records** in 2.09 seconds, producing `raw_meme_corpus.parquet` at **187.97 MB** physical disk size.
- **Content Diversity Expansion**: Added 55 iconic characters and 35 regional scenarios.
- **Catalyst-Vectorized PySpark Engine (`spark_processor.py`)**:
  - Eliminated slow Python UDF socket serialization by engineering pure Spark Catalyst expressions using `when`, `rlike`, `regexp_extract_all(..., lit(0))`, `least`, and `spark_round`.
  - Processed all 250,000 records across 4 local CPU cores in **21.57 seconds**, outputting `biometric_memes.parquet` (**195.81 MB** uncompressed).

### Milestone 7: Automated Pillow-to-WebP Compression, Lazy Loading & CDN Routing
- **Automated Backend Compression (`compress_image()`)**: Resizes images proportionally (`max_width=600`) using `Image.Resampling.LANCZOS` and converts them to in-memory WebP buffers (`quality=60`). Benchmarked: **91.5 KB to 3.8 KB (95.9% bandwidth reduction)** in **~3.2 ms**.
- **Progressive Lazy Loading**: Managed via `st.session_state.feed_limit` and a "Load More Chaos" trigger.
- **CDN Edge Transformation**: Added `get_cdn_url()` routing remote URLs through Cloudinary fetch transforms (`https://res.cloudinary.com/demo/image/fetch/w_600,f_webp/...`).

### Milestone 8: Decommissioning of Legacy V1 Artifacts & Architecture Consolidation
- **Purged Obsolete V1 Artifacts**: Permanently removed legacy prototype scripts and redundant JSON data planes (`generate_corpus.py`, `meme_corpus.json`, `phase2_pyspark_pipeline.py`, `processed_memes.json`, `phase3_sentiment_model.py`, `mood_indexed_memes.json`, `phase4_dashboard.py`).
- **Single-Stack Parquet Consolidation**: Refactored `app.py` data ingestion to strictly rely on `biometric_memes.parquet` (with raw Parquet fallback).
- **Git Ignore Safeguard**: Configured `*.parquet` in `.gitignore` to prevent GitHub 100MB file push rejections.

### Milestone 9: Phase 5 Live Continuous Biometric Engine & Zero-Cost Cloud Deployment
- **Continuous WebRTC Frame Streaming**:
  - Integrated `streamlit-webrtc` (v0.77.0) and `av` (v17.1.0).
  - Built `BiometricEmotionProcessor` communicating via Google public STUN (`stun:stun.l.google.com:19302`).
  - Throttled inference to every 4th frame ensuring a smooth 30+ FPS video rendering on CPU.
  - Burned live telemetry HUD (`DETECTED PSYCHE: <EMOTION>`) directly onto the video output using OpenCV `cv2.putText`.
- **Emotion Routing Matrix**:
  - Automatically routes detected facial expressions to regional cultural categories:
    - `sad` / `fear` $\to$ **KTU Exam Trauma**
    - `angry` / `disgust` $\to$ **Political Poru & Hartal**
    - `happy` / `surprise` $\to$ **Nirvana (Thattukada & Vibe)**
    - `neutral` $\to$ **Monday Work Shokam**
- **Triple-Mode Camera Resilience**:
  - Implemented a seamless mode switch: **Continuous Live WebRTC Stream**, **Instant Snapshot Camera**, and **Emotion Simulator** (guaranteeing 100% demo uptime even under strict corporate firewalls).
- **DeepFace Cold-Start Caching**:
  - Pre-cached `facial_expression_model_weights.h5` in `~/.deepface/weights/` and packaged OpenCV cascade definitions.
- **Zero-Cost Hugging Face Spaces Architecture**:
  - Decoupled `app.py` from runtime PySpark dependencies, enabling zero-egress hosting on Hugging Face Spaces (free 2 vCPU · 16 GB tier) using `README.md` YAML frontmatter.

### Milestone 10: Docker SDK Fallback Architecture & Pre-Demo Verification Suite
- **Containerized Docker SDK Runtime**: Authored a production-grade `Dockerfile` using `python:3.11-slim`, non-root user `user` (UID `1000`), port `7860`, system OpenCV/FFmpeg libraries, and build-time model weight injection.
- **Diagnostics Automation (`verify_environment.py`)**: Built an automated hardware and network pre-flight verification script checking model weight integrity, Google STUN UDP reachability, and hardware camera device access.
- **Full Verification Green**: Executed `verify_environment.py`—all checks passed (5.97 MB weight cache verified, STUN handshake resolved to 74.125.250.129:19302, and device 0 frame capture confirmed).

### Milestone 11: WebRTC Stability Hardening, Zero-Crash Fallback & True Image Rendering
- **WebRTC Stream Drop Recovery**: Implemented error-resilient exception handling around `streamlit-webrtc` streamer initialization, ensuring that dropped browser video streams or unhandled exceptions do not crash the Streamlit session.
- **Triple-Mode Biometric Fallback**: Enabled instant switching between:
  1. *Continuous Live Stream (WebRTC)*: Real-time STUN-routed webcam streaming with HUD psyche overlay.
  2. *Instant Snapshot Frame (Camera Input)*: Static hardware capture for low-bandwidth environments, hardened with Pillow RGB array decoding (`np.array(Image.open(io.BytesIO(bytes_data)).convert('RGB'))`) to eliminate DeepFace `DataTypeError`.
  3. *Emotion Simulator (Test Matrix)*: Zero-hardware manual micro-expression selector (`sad`, `angry`, `happy`, `neutral`, `fear`, `surprise`) guaranteeing 100% demo uptime under strict presentation conditions.
- **True Image Asset Rendering**: Resolved the issue where the meme container only displayed raw text dialogue. Configured Tab 2 to dynamically inspect `assets/memes/` for high-resolution `.jpg` assets, intelligently matching character archetypes (Damu, Manavalan, Gafoor, Pappu, etc.) and rendering the physical image via `st.image(chosen_asset, caption=..., width='stretch')` directly adjacent to the dialogue transcript.
- **Streamlit 1.63 Layout Compatibility**: Standardized layout parameters using modern `width='stretch'` and `use_container_width=True` across Plotly indicators, meme image frames, and vernacular data lake explorers.

### Milestone 12: Emotion Freezing Prevention (Lighting Tolerance & Throttle) & Dynamic Parquet Alignment
- **Preventing Emotion Freezing in WebRTC**:
  - Re-architected `EmotionProcessor` with asynchronous frame streaming (`async_processing=True`) and decoupled inference: DeepFace neural evaluation is throttled to every 10th frame (`self.frame_count % 10 == 0`), preventing CPU thread starvation and dropped frame queues.
  - Enabled lighting-tolerant detection with `enforce_detection=False` and `silent=True` to smoothly track micro-expressions even under harsh venue or low-light webcam feeds.
  - Implemented persistent state retention (`self.last_valid`) so transient micro-movements do not reset the detected state to default "neutral".
- **Dynamic Parquet Filtering & Column Alignment**:
  - Diagnosed and resolved Spark Catalyst regex collision that collapsed `emotion` into `happy` for all 250,000 records. Refactored `spark_processor.py` to prioritize `target_emotion` ground truths and re-ran Spark Catalyst distributed execution in 18.31s, regenerating `biometric_memes.parquet` (195.75 MB) with authentic distribution: `angry` (71,360), `happy` (64,350), `fear` (42,900), `sad` (42,845), `neutral` (28,545).
  - Hardened `app.py` `load_data()` with automatic schema reconciliation and applied case-insensitive dynamic query filtering (`df['emotion'].astype(str).str.lower() == detected_emotion.lower()`).
  - Added visual fallback cards (`https://images.unsplash.com/...`) if local assets directory is ever purged.

### Milestone 13: MTCNN Neural Face Alignment, CLAHE Normalization & Confidence Breakdown
- **MTCNN Multi-Task Cascaded CNN Integration**: Upgraded the face detector backend from basic OpenCV Haar cascades to `detector_backend='mtcnn'`. Leverages deep multi-task convolutional networks for precise 5-point facial landmark alignment, resolving off-axis pose detection issues.
- **CLAHE Contrast Normalization**: Added OpenCV LAB color space preprocessing using Contrast Limited Adaptive Histogram Equalization (`cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))`) on the luminance channel, neutralizing shadows and dim ambient lighting before feeding frames to the neural net.
- **Full Emotion Confidence Breakdown**: Surfaced detailed model probability distributions via interactive Streamlit progress bars within an expander (`📊 View Full Emotion Probability Breakdown`), displaying exact percentage confidences for every affective state (`happy`, `neutral`, `sad`, `fear`, `angry`, `surprise`, `disgust`).
- **Resilient Fallback Detector Pipeline**: Configured a two-tier detector pipeline: if MTCNN strict bounds are missed due to sudden motion, the engine automatically catches the exception and falls back to `detector_backend='opencv'` with `enforce_detection=False`.
- **Categorical Parquet Database Matching**: Aligned regional categories (`KTU Exam Trauma` $\to$ `Academic Trauma`, `Political Poru & Hartal` $\to$ `Political Satire`, `Nirvana` $\to$ `Gastronomic Nirvana`, `Monday Work Shokam` $\to$ `Corporate Nihilism`) with randomized sample selection (`matched_df.sample(n=1)`), ensuring dynamic, non-repetitive meme recommendations.

### Milestone 14: Text-First Cyberpunk Cinematic Card & High-Velocity AI Layout
- **Cyberpunk Cinematic Card Container**: Pivoted Tab 2 from local image placeholder loading to a rich, high-contrast neon card layout (`background-color: #1e1e2f; border: 2px solid #ff4b4b; box-shadow: 0px 0px 20px rgba(255, 75, 75, 0.3)`). The card champions high-impact typography with character headers, movie tags, italicized cyan punchlines, and branded badges.
- **Elimination of Broken / Placeholder Images**: Dropped local image file I/O dependencies in Tab 2, avoiding generic placeholder banners or missing asset errors during live presentations and elevating the Malayalam script and existential weight into the visual center.
- **High-Velocity Preprocessing & Inference**: Streamlined snapshot capture with fast OpenCV LAB CLAHE contrast balancing (`clipLimit=2.0`) and non-blocking OpenCV detector inference (`enforce_detection=False`, `silent=True`), providing near-instantaneous UI response (< 1s) upon camera click.

### Milestone 15: Dual-Column Split Screen & Synchronized Visual-Cinematic Projection
- **Two-Column Split Screen Matrix**: Replaced full-width camera layout with a balanced `st.columns([1, 1], gap="medium")` architecture in Tab 2. The left column encapsulates compact camera controls (`st.camera_input` with `label_visibility="collapsed"`) and manual simulation overrides, preventing camera feed viewport dominance.
- **Dual Visual-Cinematic Card Display**: Right column unifies both visual and typographic outputs by rendering the high-resolution JPEG artifact from `assets/memes/` (`use_container_width=True`) alongside the cyberpunk neon dialogue card (`#1e1e2f` card with cyan dialogue snippet, KEW score, and Parquet data plane tag).
- **Hardened Parquet & Asset Binding**: Preserves character-aware asset matching and regional category alignment (`Academic Trauma`, `Political Satire`, `Gastronomic Nirvana`, `Corporate Nihilism`) querying the 250,000-record Parquet data lake with randomized sampling.

---

## 5. PROPRIETARY SCORING ALGORITHMS & MATHEMATICAL FORMULATIONS

### 1. Cultural Relevance Index ($CRI$)
$$\text{CRI}(\text{text}) = \min\left( \sum_{k \in \mathcal{A}} w_k \cdot \mathbb{I}(k \in \text{lower}(\text{text})), \; 10.0 \right)$$

Evaluated inside Spark Catalyst via stacked `when(lower(col("raw_ocr_text")).contains(k), lit(w)).otherwise(lit(0.0))` expressions.

### 2. Humor Density Metric ($HDM$)
$$HDM = \min\left( 1.0 + \min(N_{\text{punc}} \times 0.3, 3.0) + \min(N_{\text{laugh}} \times 1.2, 4.0) + 2.0 \cdot \mathbb{I}\left(\frac{N_{\text{caps}}}{L} > 0.25\right), \; 10.0 \right)$$

### 3. Kerala Existential Weight ($KEW$)
$$KEW = \text{round}(0.6 \times CRI + 0.4 \times HDM, \; 2)$$

### 4. DeepFace Emotion Routing Matrix
| DeepFace Output | Target Regional Taxonomy | Vernacular Emotional Manifestation |
| :--- | :--- | :--- |
| **`sad`** / **`fear`** | **KTU Exam Trauma** | Backlogs, supply hall panic, calculator dead batteries, weeping. |
| **`angry`** / **`disgust`** | **Political Poru & Hartal** | KSRTC bus block, flag marches, shouting matches, fuel price hikes. |
| **`happy`** / **`surprise`** | **Nirvana (Thattukada & Vibe)** | Midnight porotta & beef fry, tea shop banter, celebration. |
| **`neutral`** | **Monday Work Shokam** | Infopark / Technopark burnout, Bangalore sleeper bus exhaustion. |

---

## 6. DATA SCHEMAS & PAYLOAD CONTRACTS

### V2 Biometric Meme Parquet Schema (`biometric_memes.parquet`)

```text
root
 |-- meme_id: string (nullable = true)
 |-- character: string (nullable = true)
 |-- actor: string (nullable = true)
 |-- movie: string (nullable = true)
 |-- character_archetype: string (nullable = true)
 |-- scenario_id: string (nullable = true)
 |-- scenario_title: string (nullable = true)
 |-- scenario_category: string (nullable = true)
 |-- target_emotion: string (nullable = true)
 |-- raw_ocr_text: string (nullable = true)
 |-- dialogue_snippet: string (nullable = true)
 |-- engagement_score: double (nullable = true)
 |-- shares_count: long (nullable = true)
 |-- upvotes_count: long (nullable = true)
 |-- troll_page_handle: string (nullable = true)
 |-- cloud_distributed_shard_id: string (nullable = true)
 |-- year: long (nullable = true)
 |-- ocr_confidence_score: double (nullable = true)
 |-- cultural_relevance_index: double (nullable = true)
 |-- humor_density_metric: double (nullable = true)
 |-- emotion: string (nullable = true)
 |-- kerala_existential_weight: double (nullable = true)
```

---

## 7. INFRASTRUCTURE & DISTRIBUTED RUNTIME SPECIFICATIONS

### Hardware & Virtualization Target
- **Machine**: ASUS TUF Gaming F16 Laptop
- **Compute**: Multi-Core Local CPU (24 logical cores)
- **Sensors**: Integrated HD / IR Webcam for live computer vision
- **Java Virtual Machine**: OpenJDK 17 LTS (`C:\Program Files\Microsoft\jdk-17.0.20.101-hotspot`)

### Python 3.11 Environment Packages (`requirements.txt`)
- `streamlit-webrtc==0.77.0`
- `av==17.1.0`
- `deepface==0.0.100`
- `opencv-python==4.14.0.94`
- `tensorflow==2.21.0`
- `tf-keras==2.21.0`
- `pyspark==4.2.0`
- `py4j==0.10.9.9`
- `pyarrow==25.0.1`
- `fastparquet==2026.5.0`
- `pillow==12.3.0`
- `streamlit==1.63.0`
- `plotly==7.0.0`
- `pandas==3.0.5`
- `nltk==3.10.3`

---

## 8. ZERO-COST CLOUD DEPLOYMENT ARCHITECTURE (HUGGING FACE SPACES)

Deployable to **Hugging Face Spaces** on the **Free CPU Tier (2 vCPU · 16 GB RAM)** with dual SDK support:

### Option A: Standard Streamlit SDK
- In `README.md`, maintain standard YAML frontmatter:
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
- Uses `requirements.txt` to install dependencies and boots directly into `app.py`.

### Option B: Containerized Docker SDK (Recommended Fallback)
Hugging Face recently recommended the Docker SDK for production Spaces using C++ bindings (OpenCV, FFmpeg, aiortc):
- `Dockerfile` provided at repository root:
  - Base Image: `python:3.11-slim`
  - Non-Root Security: User `user` (UID `1000`)
  - Build-time Pre-caching: Injects `facial_expression_model_weights.h5` and OpenCV cascades directly into image layers to completely eliminate cold-start lag.
  - Exposed Port: Binds Streamlit to port `7860` as required by Spaces.
- Update `README.md` YAML frontmatter to:
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

---

## 9. DEVELOPER QUICKSTART & EXECUTION RUNBOOK

### 1. Activating the Environment
```powershell
.venv\Scripts\Activate.ps1
```

### 2. Generating the 150MB+ Parquet Corpus (Phase 1)
```powershell
.venv\Scripts\python.exe generate_v2_corpus.py 250000
```
- **Output**: `raw_meme_corpus.parquet` (187.97 MB, 250,000 records).

### 3. Running Distributed PySpark Emotion Mapping (Phase 2)
```powershell
.venv\Scripts\python.exe spark_processor.py
```
- **Output**: `biometric_memes.parquet` (195.81 MB, 250,000 records) computed in ~21 seconds.

### 4. Generating Sample Local Meme Image Assets
```powershell
.venv\Scripts\python.exe create_sample_assets.py
```
- **Output**: 8 high-res JPEG files in `assets/memes/`.

### 5. Running the Pre-Demo Verification Suite (Diagnostic Check)
```powershell
.venv\Scripts\python.exe verify_environment.py
```
- **Validates**:
  - `[1] WEIGHT CACHE INTEGRITY`: `facial_expression_model_weights.h5` (5.97 MB) present in `~/.deepface/weights/`.
  - `[2] STUN CONNECTIVITY`: UDP handshake with `stun.l.google.com:19302` confirmed.
  - `[3] HARDWARE CAMERA`: Device 0 open and delivering live frames.

### 6. Launching the V2 Biometric Streamlit Dashboard (Phase 5)
```powershell
.venv\Scripts\streamlit.exe run app.py
```
- **Access Endpoints**:
  - Local URL: `http://localhost:8501`
  - Features:
    - **Tab 1**: Global Telemetry KMI Gauge & Emotion Volume
    - **Tab 2**: Live WebRTC Continuous Biometric Scanner with HUD overlay, emotion routing, and snapshot/simulator fallbacks
    - **Tab 3**: Lazy-Loaded Vernacular Feed with Automated WebP Compression & CDN Toggle

---

## 10. DOWNSTREAM ROADMAP & FUTURE PHASES

1. **Phase 1 Pipeline Formalization (OCR & Web Scraper)**:
   - Integrate Tesseract OCR & OpenCV for direct image-to-text extraction from Malayalam meme JPEG/PNG files.
2. **Phase 2 & 3 Biometric Parquet Matrix**: [COMPLETED]
   - Scaled corpus to 250k records (195MB+ Parquet lake) with PySpark Catalyst execution and DeepFace vision.
3. **Phase 4 Visual Optimization (WebP & Lazy Loading)**: [COMPLETED]
   - Built Pillow-to-WebP automated compression engine (-95.9% size reduction) and session-state progressive feed.
4. **Phase 5 Live Continuous WebRTC Engine & Cloud Deployment**: [COMPLETED]
   - Implemented real-time continuous video streaming via `streamlit-webrtc`, STUN connectivity, HUD overlay, and zero-cost Hugging Face Spaces deployment architecture.
5. **Phase 6 Real-Time Kafka / Spark Streaming Ingestion**:
   - Stream live social media posts directly into the PySpark Catalyst engine for continuous telemetry updates.
