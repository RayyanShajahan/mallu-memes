# PROJECT MASTER SUMMARY & SYSTEM COMPENDIUM
**Mallu Memes: Kerala Collective Psyche Distributed Processor & Biometric Meme Engine**  
*Document Version:* `3.1.0-BIOMETRIC-ENGINE-OPTIMIZED`  
*Last Synchronized:* September 2026  
*Target Hardware:* ASUS TUF F16 (Local Multi-Core CPU + Integrated IR/Webcam)  
*Status:* Active / V2 Biometric Engine, 150MB+ PySpark Parquet Lake, DeepFace Vision & WebP Lazy Feed Operational  

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
8. [Developer Quickstart & Execution Runbook](#8-developer-quickstart--execution-runbook)
9. [Downstream Roadmap & Future Phases](#9-downstream-roadmap--future-phases)

---

## 1. PROJECT MISSION, VERNACULAR PHILOSOPHY & ARCHITECTURAL INVARIANTS

The **Mallu Memes Analytics Platform (V2 Biometric Meme Engine)** is an enterprise-grade vernacular cultural intelligence, sentiment analysis, and real-time computer vision system designed to quantify the existential absurdities of Malayalam internet culture and mirror them directly onto user facial micro-expressions.

By intentionally scaling up to a **150MB+ (250,000 records) raw Parquet corpus**, processing it through **PySpark Catalyst distributed compute engines in local mode**, and serving an **ocular Streamlit dashboard** powered by **DeepFace neural facial expression inference** and **automated Pillow-to-WebP backend compression**, the system achieves maximum architectural pretentiousness and sub-millisecond local latency on consumer laptop hardware (ASUS TUF F16).

### The 6 Inviolable Architectural Invariants

1. **Massive Columnar Parquet Lake (150MB+ / 250,000 Records)**:
   - All vernacular meme transcripts must be stored and manipulated in columnar Apache Parquet format (`raw_meme_corpus.parquet` and `biometric_memes.parquet`) rather than bloated JSON to prevent browser and frontend memory leaks.
   - The corpus includes 55+ distinct Malayalam cinematic characters and 35+ hyper-specific regional scenarios.
2. **Distributed Compute via PySpark Catalyst Engine**:
   - Every raw OCR text extracted from Malayalam social media memes undergoes distributed transformation via Apache Spark (`pyspark.sql`).
   - Scoring heuristics and emotion categorizations are implemented using vectorized Spark Catalyst expressions (`when`, `regexp_extract_all`, `least`) executing directly within the JVM for maximum throughput.
3. **Deterministic Cultural Quantification**:
   - Satire, cinematic archetypes, and societal anxieties are codified into weighted anchor vectors.
   - Every meme resolves into a deterministic triad of scores:
     - `cultural_relevance_index` $\in [0.0, 10.0]$
     - `humor_density_metric` $\in [0.0, 10.0]$
     - `kerala_existential_weight` $\in [0.0, 10.0]$
4. **Biometric Face-to-Meme Mapping via DeepFace**:
   - The user's live facial expression is captured via `st.camera_input()` and evaluated using `deepface.DeepFace.analyze(actions=['emotion'], detector_backend='opencv')`.
   - The dominant emotion strictly maps to one of the 5 canonical DeepFace buckets: `happy`, `sad`, `angry`, `fear`, `neutral`.
   - The system performs a sub-millisecond columnar scan on the Parquet dataframe to extract high Kerala Existential Weight (KEW $\ge 90$th percentile) memes matching that exact affective state.
5. **Automated Pillow-to-WebP Compression (Backend)**:
   - High-resolution meme images are intercepted by Pillow, proportionally downscaled (`max_width=600`) using `Image.Resampling.LANCZOS`, and converted to in-memory WebP buffers (`quality=60`).
   - Slashes image payload sizes by **80% to 96%** compared to standard uncompressed JPEGs.
6. **Frontend Lazy Loading & CDN Edge Bypassing**:
   - Progressive batch rendering in Streamlit is governed via `st.session_state.feed_limit` and a "Load More Chaos" trigger.
   - Remote URL requests support instant Cloudinary/Cloudflare CDN transformation (`w_600,f_webp`).

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

    subgraph Phase3["Phase 3: The Biometric Streamlit Dashboard & WebP Engine"]
        App["Streamlit Dashboard\n(app.py : Port 8501)"]
        
        subgraph Tab1["Tab 1: Global Telemetry"]
            Gauge["Plotly go.Indicator KMI Gauge"]
            BarChart["Plotly Express Emotion Volume"]
            Leaderboard["Top Existential Artifacts"]
        end

        subgraph Tab2["Tab 2: The Biometric Scanner"]
            Camera["st.camera_input() Frame Capture"]
            DeepFace["DeepFace.analyze()\nOpenCV Detector Backend"]
            Matcher["Sub-ms Parquet Scanner\n(Top 10% KEW Filter)"]
            MemeCard["Matched Meme HTML Card"]
            WebPBanner["On-the-Fly WebP Banner"]
            Camera --> DeepFace --> Matcher --> MemeCard & WebPBanner
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
├── LICENSE                                 # MIT Open Source License
├── README.md                               # Project intro & vernacular manifest
├── app.py                                  # Phase 3 V2 Biometric Streamlit Application + WebP Feed
├── biometric_memes.parquet                 # 195.81 MB pre-computed Parquet dataset (250,000 records)
├── create_sample_assets.py                 # Generates sample high-res meme JPEG banners
├── generate_v2_corpus.py                   # V2 massive streaming corpus generator (150MB+ / 250k rec)
├── PROJECT_MASTER_SUMMARY.md               # [THIS FILE] Single Source of Truth Compendium
├── raw_meme_corpus.parquet                 # 187.97 MB raw Parquet corpus (250,000 records)
├── requirements.txt                        # Pinned dependencies (deepface, pyspark, opencv, etc.)
└── spark_processor.py                      # V2 PySpark Distributed Emotion Mapping Engine
```

### Detailed Component Inventory

| File / Component | Primary Technology | Purpose & Responsibility |
| :--- | :--- | :--- |
| `app.py` | Python 3.11, Streamlit 1.63, DeepFace 0.0.100, OpenCV 5.0, Pillow 12.3, Plotly 7.0 | V2 Biometric Meme Engine frontend. Features 3 tabs: Global Telemetry gauge, IR/webcam biometric face scanner with DeepFace emotion inference, and lazy-loaded WebP feed with Pillow compression. |
| `spark_processor.py` | Python 3.11, PySpark 4.2.0, PyArrow 25.0 | V2 distributed ETL processor (`KeralaBiometricMemeProcessor`). Ingests `raw_meme_corpus.parquet`, applies vectorized Spark Catalyst expressions for CRI, HDM, and DeepFace emotion classification, and writes `biometric_memes.parquet`. |
| `generate_v2_corpus.py` | Python 3.11, PyArrow 25.0 | Streaming synthesizer that generates 250,000 authentic vernacular meme records (187.97 MB Parquet) across 55 cinematic characters and 35 cultural scenarios. |
| `create_sample_assets.py` | Python 3.11, Pillow 12.3 | Generates sample uncompressed 900x500 JPEG meme banners in `assets/memes/` to validate backend WebP compression and lazy loading. |
| `raw_meme_corpus.parquet` | Apache Parquet (Uncompressed) | 187.97 MB raw ingestion corpus with 250,000 rows, 18 columns, and rich Manglish OCR text dialogues. |
| `biometric_memes.parquet` | Apache Parquet (Uncompressed) | 195.81 MB indexed analytical data plane with 250,000 rows and 22 columns including `cultural_relevance_index`, `humor_density_metric`, `emotion`, and `kerala_existential_weight`. |
| `requirements.txt` | Pip | Dependency manifest pinned with `deepface`, `opencv-python`, `fastparquet`, `pyarrow`, `pyspark`, `streamlit`, `pillow`, `plotly`, and `nltk`. |

---

## 4. WHAT HAS BEEN DONE SO FAR (MILESTONES & CHANGELOG)

### Milestone 1: Distributed Infrastructure Provisioning (September 2026)
- **Microsoft OpenJDK 17 LTS Installed**: Provisioned through `winget` (`Microsoft.OpenJDK.17` version `17.0.20.101`). Permanent system `JAVA_HOME` configured at `C:\Program Files\Microsoft\jdk-17.0.20.101-hotspot\` with JVM binaries in system `Path`.
- **Virtual Environment Rebuild**: Migrated environment to Python 3.11.9 (`C:\Users\ra416\AppData\Local\Programs\Python\Python311\python.exe`) to guarantee binary wheel compatibility with `tensorflow` and `deepface`.

### Milestone 2–5: V1 Distributed Pipeline, NLP Model & KMI Dashboard (Archived)
- Built and validated pilot pipeline on the 85-record test corpus. Superseded by the V2 150MB+ columnar Parquet and computer vision architecture.

### Milestone 6: V2 Biometric Meme Engine & 150MB+ Corpus Architecture
- **Corpus Scaling (`generate_v2_corpus.py`)**: Built a high-throughput streaming Parquet writer utilizing `pyarrow.parquet.ParquetWriter`. Synthesized **250,000 records** in 2.09 seconds, producing `raw_meme_corpus.parquet` at **187.97 MB** physical disk size.
- **Content Diversity Expansion**: Added 55 iconic characters (from Dashamoolam Damu, Manavalan, and CID Moosa to Shammi, Ramanathan, Gafoor, and Kuthiravattam Pappu) and 35 regional scenarios (KTU exam hall panic, Bangalore sleeper bus delays, Kochi water metro selfies, thattukada beef fry queues).
- **Catalyst-Vectorized PySpark Engine (`spark_processor.py`)**:
  - Eliminated slow Python UDF socket serialization by engineering pure Spark Catalyst expressions using `when`, `rlike`, `regexp_extract_all(..., lit(0))`, `least`, and `spark_round`.
  - Configured PyArrow-based local collection to bypass Windows Hadoop `winutils.exe` committer restrictions.
  - Processed all 250,000 records across 4 local CPU cores in **21.57 seconds**, outputting `biometric_memes.parquet` (**195.81 MB** uncompressed).

### Milestone 7: Automated Pillow-to-WebP Compression, Lazy Loading & CDN Routing
- **Automated Backend Compression (`compress_image()`)**:
  - Implemented Pillow-based image interception in `app.py`.
  - Resizes images proportionally (`max_width=600`) using `Image.Resampling.LANCZOS` and converts them to in-memory WebP buffers (`quality=60`).
  - Benchmarked on sample assets: slashes uncompressed JPEG files from **91.5 KB to 3.8 KB (95.9% bandwidth reduction)** in **~3.2 ms**.
- **Lazy Loading & Session State Pagination**:
  - Implemented viewport chunking via `st.session_state.feed_limit` (initial limit: 5).
  - Added interactive "🔥 Load More Chaos (+5 Memes)" button triggering `st.rerun()`.
- **CDN Edge Transformation**:
  - Added `get_cdn_url()` routing remote URLs through Cloudinary fetch transforms (`https://res.cloudinary.com/demo/image/fetch/w_600,f_webp/...`) to demonstrate zero-CPU edge optimization.
- **Biometric Face-to-Meme Pipeline**:
  - Integrated `st.camera_input()` with `deepface.DeepFace.analyze(actions=['emotion'], detector_backend='opencv')`.
  - Sub-millisecond Parquet querying for $\ge 90$th percentile KEW memes matching the detected micro-expression.
  - Renders both rich HTML card and on-the-fly WebP banner artifact.

### Milestone 8: Decommissioning of Legacy V1 Artifacts & Architecture Consolidation
- **Purged Obsolete V1 Artifacts**: Permanently removed legacy prototype scripts and redundant JSON data planes (`generate_corpus.py`, `meme_corpus.json`, `phase2_pyspark_pipeline.py`, `processed_memes.json`, `phase3_sentiment_model.py`, `mood_indexed_memes.json`, `phase4_dashboard.py`).
- **Single-Stack Parquet Consolidation**: Refactored `app.py` data ingestion to strictly rely on `biometric_memes.parquet` (with raw Parquet fallback), fully eliminating obsolete JSON fallbacks.
- **Git Ignore Safeguard**: Configured `*.parquet` in `.gitignore` to prevent GitHub 100MB file push rejections while maintaining deterministic 20-second reproducibility from source scripts.

---

## 5. PROPRIETARY SCORING ALGORITHMS & MATHEMATICAL FORMULATIONS

### 1. Cultural Relevance Index ($CRI$)
Quantifies cultural resonance against the shared consciousness of Kerala cinema, political discourse, and regional academic struggles:

$$\text{CRI}(\text{text}) = \min\left( \sum_{k \in \mathcal{A}} w_k \cdot \mathbb{I}(k \in \text{lower}(\text{text})), \; 10.0 \right)$$

Evaluated inside Spark Catalyst via stacked `when(lower(col("raw_ocr_text")).contains(k), lit(w)).otherwise(lit(0.0))` expressions.

### 2. Humor Density Metric ($HDM$)
Quantifies comedic hysteria based on punctuation clustering, phonetic laughter, and all-caps shouty energy:

$$HDM = \min\left( 1.0 + \min(N_{\text{punc}} \times 0.3, 3.0) + \min(N_{\text{laugh}} \times 1.2, 4.0) + 2.0 \cdot \mathbb{I}\left(\frac{N_{\text{caps}}}{L} > 0.25\right), \; 10.0 \right)$$

Spark implementation utilizes `regexp_extract_all(col("raw_ocr_text"), lit(r"[!?.]"), lit(0))` with group index `0` to execute without Python UDF overhead.

### 3. Kerala Existential Weight ($KEW$)
$$KEW = \text{round}(0.6 \times CRI + 0.4 \times HDM, \; 2)$$

### 4. DeepFace Emotion Mapping Taxonomy
The Spark pipeline categorizes every meme text transcript directly into one of the 5 canonical DeepFace facial expression buckets:

| DeepFace Emotion | Vernacular Semantic Triggers & Regional Nuances |
| :--- | :--- |
| **`happy`** | `swargam`, `bliss`, `adipoli`, `porotta`, `beef`, `celebration`, `milk abhishekam`, `set vibe`, `vibe` |
| **`sad`** | `theppu`, `sad`, `supply`, `tholi`, `fail`, `karayunnu`, `breakup`, `tears`, `shokam` |
| **`angry`** | `block`, `traffic`, `fight`, `scuffle`, `overtake`, `shouting`, `pinarayi`, `bjp`, `congress`, `kseb`, `dispute` |
| **`fear`** | `drift`, `danger`, `whistle`, `police`, `threat`, `kettle`, `inspection`, `raid`, `panic`, `fear` |
| **`neutral`** | Fallback for stoic dialogue, administrative announcements, and observations. |

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
- `deepface==0.0.100`
- `opencv-python==5.0.0.93`
- `tensorflow==2.21.0`
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

## 8. DEVELOPER QUICKSTART & EXECUTION RUNBOOK

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

### 5. Launching the V2 Biometric Streamlit Dashboard (Phase 3)
```powershell
.venv\Scripts\streamlit.exe run app.py
```
- **Access Endpoints**:
  - Local URL: `http://localhost:8501`
  - Features:
    - **Tab 1**: Global Telemetry KMI Gauge & Emotion Volume
    - **Tab 2**: Real-Time IR/Webcam Biometric Facial Scanner with DeepFace
    - **Tab 3**: Lazy-Loaded Vernacular Feed with Automated WebP Compression & CDN Toggle

---

## 9. DOWNSTREAM ROADMAP & FUTURE PHASES

1. **Phase 1 Pipeline Formalization (OCR & Web Scraper)**:
   - Integrate Tesseract OCR & OpenCV for direct image-to-text extraction from Malayalam meme JPEG/PNG files.
2. **Phase 2 & 3 Biometric Parquet Matrix**: [COMPLETED]
   - Scaled corpus to 250k records (195MB+ Parquet lake) with PySpark Catalyst execution and DeepFace real-time vision.
3. **Phase 4 Visual Optimization (WebP & Lazy Loading)**: [COMPLETED]
   - Built Pillow-to-WebP automated compression engine (-95.9% size reduction) and session-state progressive feed.
4. **Phase 5 Real-Time Kafka / Spark Streaming**:
   - Stream live social media posts directly into the PySpark Catalyst engine for continuous telemetry updates.
