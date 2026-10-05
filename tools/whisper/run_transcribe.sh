#!/bin/bash

# Check parameters
if [ "$#" -ne 2 ]; then
    echo "Usage: $0 <path_to_audio_file> <path_to_output_txt>"
    exit 1
fi

INPUT_FILE=$(realpath "$1")
OUTPUT_FILE=$(realpath "$2")

INPUT_DIR=$(dirname "$INPUT_FILE")
OUTPUT_DIR=$(dirname "$OUTPUT_FILE")

INPUT_BASE=$(basename "$INPUT_FILE")
OUTPUT_BASE=$(basename "$OUTPUT_FILE")

# Detect container engine: prefer Podman, fallback to Docker
if command -v podman >/dev/null 2>&1; then
    CONTAINER_ENGINE="podman"
    MOUNT_OPTS=":Z"
elif command -v docker >/dev/null 2>&1; then
    CONTAINER_ENGINE="docker"
    MOUNT_OPTS=""
else
    echo "Error: Neither 'podman' nor 'docker' was found on your system PATH." >&2
    echo "Please install Podman or Docker to execute transcription." >&2
    exit 1
fi

echo "Using container engine: ${CONTAINER_ENGINE}"

# Run container engine, mounting directories safely
"$CONTAINER_ENGINE" run --rm \
  -v "${INPUT_DIR}:/input${MOUNT_OPTS}" \
  -v "${OUTPUT_DIR}:/output${MOUNT_OPTS}" \
  local-whisper "/input/${INPUT_BASE}" "/output/${OUTPUT_BASE}"
