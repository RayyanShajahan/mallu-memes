# ==============================================================================
# Dockerfile for Hugging Face Spaces (Docker SDK Runtime)
# Port: 7860 | User: 1000 (Non-root user required by Hugging Face)
# ==============================================================================
FROM python:3.11-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONIOENCODING=utf-8 \
    DEBIAN_FRONTEND=noninteractive \
    HOME=/home/user \
    PATH=/home/user/.local/bin:$PATH \
    STREAMLIT_SERVER_PORT=7860 \
    STREAMLIT_SERVER_HEADLESS=true

# Install essential Linux packages for OpenCV and video processing
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    ffmpeg \
    libgl1 \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender1 \
    && rm -rf /var/lib/apt/lists/*

# Set up non-root user required by Hugging Face Spaces
RUN useradd -m -u 1000 user
USER user
WORKDIR /home/user/app

# Copy requirements and install dependencies into user environment
COPY --chown=user:user requirements.txt .
RUN pip install --no-cache-dir --upgrade --only-binary=:all: pip && \
    pip install --no-cache-dir --only-binary=:all: -r requirements.txt

# Pre-seed weights directly from local bundled assets (zero build-time network downloads)
RUN mkdir -p /home/user/.deepface/weights
COPY --chown=user:user assets/weights/facial_expression_model_weights.h5 /home/user/.deepface/weights/facial_expression_model_weights.h5

# Copy explicit application source files (prevents inadvertent sensitive data leakage)
COPY --chown=user:user app.py spark_processor.py generate_v2_corpus.py packages.txt biometric_memes_sample.parquet ./
COPY --chown=user:user assets/ ./assets/
COPY --chown=user:user demo/ ./demo/
COPY --chown=user:user screenshots/ ./screenshots/

# Expose default Hugging Face Spaces port
EXPOSE 7860

# Launch Streamlit dashboard
CMD ["streamlit", "run", "app.py"]
