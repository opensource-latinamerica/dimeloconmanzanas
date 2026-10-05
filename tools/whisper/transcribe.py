import sys
import os
from faster_whisper import WhisperModel

if len(sys.argv) < 3:
    print("Error: Missing arguments.")
    print("Usage: python transcribe.py <input_audio_path> <output_txt_path>")
    sys.exit(1)

audio_path = sys.argv[1]
output_path = sys.argv[2]

if not os.path.exists(audio_path):
    print(f"Error: Input file {audio_path} does not exist.")
    sys.exit(1)

print(f"Loading Whisper 'small' model on CPU (int8)...")
# Force CPU and optimized int8 math execution
model = WhisperModel("small", device="cpu", compute_type="int8")

print(f"Transcribing {audio_path} (Forced Language: Spanish)...")
# language="es" eliminates language detection latency
segments, info = model.transcribe(audio_path, language="es", beam_size=5)

# Ensure the output directory exists
os.makedirs(os.path.dirname(output_path), exist_ok=True)

with open(output_path, "w", encoding="utf-8") as f:
    for segment in segments:
        timestamp = f"[{segment.start:.2f}s -> {segment.end:.2f}s]"
        line = f"{timestamp} {segment.text}\n"
        print(line, end="")
        f.write(line)

print(f"\nTranscription successfully saved to: {output_path}")
