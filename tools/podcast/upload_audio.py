#!/usr/bin/env python3
"""
Herramienta de automatización para subir episodios de podcast a AWS S3
y actualizar automáticamente los metadatos en .agents/episodes.yaml.

Uso:
    python3 tools/podcast/upload_audio.py --episode 0003 --file /ruta/al/audio.mp3 --bucket nombre-del-bucket

Reglas de AWS:
    - Utiliza por defecto '--profile deployer' (o '--profile cloudconnect-deployer').
"""

import argparse
import os
import re
import subprocess
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    print("Error: PyYAML es requerido. Instálalo con 'pip install pyyaml'.")
    sys.exit(1)

def get_duration_from_transcript(transcript_path):
    """Intenta extraer la duración máxima del archivo de transcripción Whisper."""
    if not os.path.exists(transcript_path):
        return None
    try:
        with open(transcript_path, "r", encoding="utf-8") as f:
            lines = f.readlines()
        max_sec = 0.0
        for line in lines[-20:]:  # buscar en las últimas líneas
            match = re.search(r'->\s*([0-9\.]+)s\]', line)
            if match:
                sec = float(match.group(1))
                if sec > max_sec:
                    max_sec = sec
        if max_sec > 0:
            m = int(max_sec // 60)
            s = int(max_sec % 60)
            return f"{m:02d}:{s:02d}"
    except Exception:
        pass
    return None

def main():
    parser = argparse.ArgumentParser(description="Subir audio de episodio a S3 y registrar metadatos en episodes.yaml.")
    parser.add_argument("--episode", required=True, help="Número de episodio (ej: 0003 o 3)")
    parser.add_argument("--file", required=True, help="Ruta al archivo .mp3 local")
    parser.add_argument("--bucket", default=os.environ.get("PODCAST_S3_BUCKET", ""), help="Nombre del bucket S3")
    parser.add_argument("--profile", default="deployer", choices=["deployer", "cloudconnect-deployer"],
                        help="Perfil de AWS CLI (por defecto 'deployer')")
    parser.add_argument("--region", default="us-east-1", help="Región AWS de S3 (por defecto us-east-1)")
    parser.add_argument("--duration", help="Duración del episodio en formato MM:SS o HH:MM:SS (opcional)")
    parser.add_argument("--dry-run", action="store_true", help="Simular sin subir a S3 ni modificar archivos")

    args = parser.parse_args()

    audio_path = Path(args.file)
    if not audio_path.exists():
        print(f"Error: El archivo de audio no existe: {args.file}")
        sys.exit(1)

    ep_num = f"{int(args.episode):04d}"
    manifest_path = Path(".agents/episodes.yaml")
    if not manifest_path.exists():
        print("Error: No se encontró .agents/episodes.yaml")
        sys.exit(1)

    with open(manifest_path, "r", encoding="utf-8") as f:
        manifest = yaml.safe_load(f)

    target_ep = None
    for ep in manifest.get("episodes", []):
        if str(ep.get("number")).lstrip("0") == str(int(args.episode)):
            target_ep = ep
            break

    if not target_ep:
        print(f"Error: El episodio {ep_num} no está registrado en {manifest_path}")
        sys.exit(1)

    file_bytes = audio_path.stat().st_size
    duration = args.duration
    if not duration and target_ep.get("transcript_file"):
        duration = get_duration_from_transcript(target_ep["transcript_file"])
    if not duration:
        duration = target_ep.get("audio_duration", "20:00")

    bucket = args.bucket
    if not bucket:
        # Extraer bucket si ya existe en audio_url previa
        existing_url = target_ep.get("audio_url", "")
        m = re.search(r'https?://([^.]+)\.s3', existing_url)
        if m and m.group(1) != "TU-BUCKET-S3":
            bucket = m.group(1)
        else:
            print("Error: Debes especificar el bucket con --bucket <nombre> o definir PODCAST_S3_BUCKET.")
            sys.exit(1)

    s3_key = f"episodes/{ep_num}-{audio_path.name}"
    s3_url = f"https://{bucket}.s3.amazonaws.com/{s3_key}"

    print(f"\n🎙️  Preparando episodio {ep_num}:")
    print(f"   Archivo: {audio_path.name} ({file_bytes:,} bytes)")
    print(f"   Duración estimada: {duration}")
    print(f"   Destino S3: s3://{bucket}/{s3_key}")
    print(f"   URL pública: {s3_url}")
    print(f"   Perfil AWS: --profile {args.profile}")

    if args.dry_run:
        print("\n[DRY RUN] Operación finalizada sin cambios.")
        return

    # Comando AWS CLI
    cmd = [
        "aws", "s3", "cp",
        str(audio_path),
        f"s3://{bucket}/{s3_key}",
        "--profile", args.profile,
        "--content-type", "audio/mpeg"
    ]
    print(f"\n🚀 Subiendo audio con AWS CLI...")
    result = subprocess.run(cmd)
    if result.returncode != 0:
        print(f"Error: Falló la subida a S3 con código {result.returncode}")
        sys.exit(result.returncode)

    # Actualizar episodes.yaml
    target_ep["audio_url"] = s3_url
    target_ep["audio_bytes"] = file_bytes
    target_ep["audio_duration"] = duration

    with open(manifest_path, "w", encoding="utf-8") as f:
        yaml.dump(manifest, f, allow_unicode=True, sort_keys=False, default_flow_style=False)

    print(f"\n✓ .agents/episodes.yaml actualizado exitosamente.")

    # Recompilar con Hugo
    print("🔨 Actualizando feed de podcast con Hugo...")
    subprocess.run(["hugo", "--minify"])
    print("✓ public/podcast.xml regenerado con la nueva URL de audio.")

if __name__ == "__main__":
    main()
