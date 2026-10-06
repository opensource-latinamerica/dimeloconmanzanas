# Herramientas de Publicación y Distribución de Podcast (100% Gratuito)

Este módulo gestiona la distribución automatizada de episodios de audio para el podcast **"Dímelo con Manzanas"** utilizando **Hugo RSS** y **AWS S3**.

---

## 1. Arquitectura de Distribución

```
1. Audio .mp3  ──>  AWS S3 Bucket (Público / CloudFront)
2. episodes.yaml ──> Registra audio_url, bytes y duration
3. git push     ──> GitHub Actions compila Hugo y genera https://conmanzanas.lat/podcast.xml
4. Spotify      ──> Lee podcast.xml y actualiza catálogo automáticamente
```

---

## 2. Configuración del Bucket en AWS S3

1. Crea tu bucket en AWS S3 (ej: `dimeloconmanzanas-audio`).
2. Desactiva el bloqueo de acceso público para objetos si vas a servir las descargas directas desde S3 (o configura una distribución en CloudFront).
3. Agrega la siguiente política de bucket para permitir la lectura pública de los episodios:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "PublicReadGetObject",
      "Effect": "Allow",
      "Principal": "*",
      "Action": "s3:GetObject",
      "Resource": "arn:aws:s3:::TU-BUCKET-S3/episodes/*"
    }
  ]
}
```

---

## 3. Subir un Episodio y Actualizar Metadatos

Ejecuta el script de automatización:

```bash
# Ejemplo: Subir episodio 3 usando el perfil por defecto 'podcaster'
python3 tools/podcast/upload_audio.py \
    --episode 0003 \
    --file /ruta/al/archivo-0003.mp3 \
    --bucket TU-BUCKET-S3
```

El script:
* Sube el `.mp3` a `s3://TU-BUCKET-S3/episodes/0003-<nombre>.mp3` usando `--profile podcaster` por defecto.
* Calcula el tamaño exacto en bytes (`audio_bytes`).
* Extrae la duración estimada desde la transcripción Whisper o parámetro `--duration`.
* Actualiza `.agents/episodes.yaml` automáticamente.
* Recompila `public/podcast.xml` con Hugo.

---

## 4. Conectar el Feed en Spotify for Podcasters (Paso Único)

Solo una vez debes registrar la URL del feed:
1. Inicia sesión en [podcasters.spotify.com](https://podcasters.spotify.com).
2. Ve a los ajustes del show / disponibilidad del podcast.
3. Ingresa la URL oficial del feed RSS generado por Hugo:
   ```
   https://conmanzanas.lat/podcast.xml
   ```
4. A partir de ese momento, cualquier cambio que hagas en `.agents/episodes.yaml` se sincroniza automáticamente con Spotify al hacer `git push`.
