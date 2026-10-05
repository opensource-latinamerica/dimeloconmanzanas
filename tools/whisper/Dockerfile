FROM python:3.10-slim

# Install system dependencies for audio processing
RUN apt-get update && apt-get install -y \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install optimized faster-whisper library
RUN pip install --no-cache-dir faster-whisper

# Copy transcription script
COPY transcribe.py .

# Pre-download the Whisper small model into the image to avoid runtime downloads
RUN python -c 'from faster_whisper import WhisperModel; WhisperModel("small", device="cpu", compute_type="int8")'

# Entrypoint maps directly to python runtime execution
ENTRYPOINT ["python", "transcribe.py"]
