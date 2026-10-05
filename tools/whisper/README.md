# Local Whisper Transcription Podman Platform

An optimized, containerized execution environment for converting Spanish audio files (`.mp3`, `.m4a`) into structured text transcripts using `faster-whisper`. 

This setup leverages **CTranslate2 with `int8` quantization** to execute efficiently on low-power or resource-constrained host hardware (such as dual-core/4-thread CPUs without a dedicated GPU).

---

## 🏗️ Project Architecture

The solution consists of three main operational files:
1. `transcribe.py`: Python script utilizing `faster-whisper` forced to Spanish (`es`) to eliminate language-detection latency.
2. `Dockerfile`: Sets up standard system libraries (`ffmpeg`), installs runtime frameworks, and pre-caches the Whisper model inside the image layer during build-time to allow **100% offline runtime execution**.
3. `run_transcribe.sh`: A helper automation shell wrapper that resolves paths and maps filesystem volumes cleanly into the isolated container space via Podman.

---

## ⚡ Setup & Installation

### 1. Build the Container Image
Run the build engine inside the root folder containing your `Dockerfile` and Python script. The installer will download the `small` model weight configuration file and pack it directly into the image structure:

```bash
# Using Podman (recommended):
podman build -t local-whisper .

# Or using Docker:
docker build -t local-whisper .
```

### 2. Configure Execution Permissions
Make the automation shell wrapper executable on your host system:

```bash
chmod +x run_transcribe.sh
```

---

## 🚀 Execution Guide

The helper script `run_transcribe.sh` automatically detects if **Podman** is available, and cleanly falls back to **Docker** if Podman is not found. It also manages volume mounting (`:Z` flags for SELinux/rootless Podman) without requiring manual container arguments.

Invoke the helper shell wrapper with two functional arguments:

```bash
./run_transcribe.sh <path_to_input_audio> <path_to_output_txt>
```

### Production Examples:
* **Processing an audio file to static transcripts directory:**
  ```bash
  ./run_transcribe.sh ./audio/episodio3.m4a ./static/transcripts/0003-inteligencia-artificial-y-rendicion-cognitiva.txt
  ```

* **Processing with local paths:**
  ```bash
  ./run_transcribe.sh ./audio/test_audio.mp3 ./output/result.txt
  ```

---

## 🎯 Verification & Validation

To ensure your container environment is running smoothly and managing computing thresholds appropriately, execute these validation layers:

### 1. Functional Integrity Verification
Check that the transcription output file was compiled successfully and contains the correct formatted elements.
```bash
# Verify the output document exists on the local file system
ls -lh ./output/result.txt

# Inspect the head records to check time-segment mapping and Spanish text resolution
head -n 5 ./output/result.txt
```
*Expected Format Snapshot:*
```text
[0.00s -> 4.12s] Bienvenidos a la primera sesión del curso.
[4.12s -> 8.50s] Hoy vamos a hablar sobre el procesamiento de datos distribuidos.
```

### 2. Runtime Resource Threshold Audit
Because this script runs multi-threaded matrix operations on standard consumer CPUs without hardware acceleration pipelines, you must monitor memory consumption and thread activity during a live run. 

Open a separate terminal window and execute:
```bash
# General real-time memory and core consumption view
top

# Or use a container-specific telemetry sweep
podman stats
```
*Validation Benchmarks:*
* **Memory Limits:** Memory footprint should stabilize under **~2GB RAM**, cleanly within your system availability boundaries.
* **CPU Core Distribution:** Thread utilization across your available processing cores should maintain steady consumption rates during computational loops without exhausting host resource availability.
