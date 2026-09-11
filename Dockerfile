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
    PATH=/home/user/.local/bin:$PATH

# Install essential Linux packages for OpenCV, WebRTC (av/ffmpeg), and audio/video codecs
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    ffmpeg \
    libgl1 \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    && rm -rf /var/lib/apt/lists/*

# Set up non-root user required by Hugging Face Spaces
RUN useradd -m -u 1000 user
USER user
WORKDIR /home/user/app

# Pre-create DeepFace weights directory and download model during build (Cold-Start Bypass)
RUN mkdir -p /home/user/.deepface/weights && \
    curl -L -o /home/user/.deepface/weights/facial_expression_model_weights.h5 \
    https://github.com/serengil/deepface_models/releases/download/v1.0/facial_expression_model_weights.h5

# Copy requirements and install dependencies into user environment
COPY --chown=user:user requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Download OpenCV haarcascades directly into Python site-packages
RUN python -c "import urllib.request, os, cv2; \
dest = cv2.data.haarcascades; os.makedirs(dest, exist_ok=True); \
for f in ['haarcascade_frontalface_default.xml', 'haarcascade_eye.xml']: \
    urllib.request.urlretrieve(f'https://raw.githubusercontent.com/opencv/opencv/master/data/haarcascades/{f}', os.path.join(dest, f))"

# Copy application artifacts and code
COPY --chown=user:user . .

# Expose default Hugging Face Spaces port
EXPOSE 7860

# Launch Streamlit dashboard
CMD ["streamlit", "run", "app.py", "--server.port=7860", "--server.address=0.0.0.0"]
