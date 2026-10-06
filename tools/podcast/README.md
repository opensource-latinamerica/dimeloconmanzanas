# Herramientas de Publicación y Distribución de Podcast (100% Gratuito)

Este módulo gestiona la distribución automatizada de episodios de audio para el podcast **"Dímelo con Manzanas"** utilizando **Hugo RSS** y **AWS S3**.

---

## 1. Arquitectura de Distribución y Permisos

```
┌─────────────────────────────────────────────────────────────┐
│ 1. Creador / Agente (Perfil IAM: 'podcaster')               │
│    Permisos: Subir, listar y gestionar .mp3 en S3           │
└──────────────────────────────┬──────────────────────────────┘
                               │ aws s3 cp (upload_audio.py)
                               ▼
┌─────────────────────────────────────────────────────────────┐
│ 2. AWS S3 Bucket (p. ej. 'dimeloconmanzanas-audio')         │
│    Permisos del Bucket:                                     │
│    - Lectura pública en 'episodes/*' (para Spotify y oyentes)│
│    - CORS habilitado (para reproductores web y streaming)   │
└──────────────────────────────┬──────────────────────────────┘
                               │ Streaming vía <enclosure>
                               ▼
┌──────────────────────────────┬──────────────────────────────┐
│ 3. Hugo Engine (podcast.xml) │ 4. Agregadores (Spotify, etc)│
│    Genera feed RSS estándar  │    Leen podcast.xml y        │
│    en conmanzanas.lat        │    reproducen audio de S3    │
└──────────────────────────────┴──────────────────────────────┘
```

---

## 2. Aprovisionamiento Automático en un Solo Paso (`setup_aws_resources.sh`)

Puedes crear y validar todos los recursos (Bucket S3, Block Public Access, Bucket Policy, CORS, Usuario IAM `podcaster`, política IAM y configuración del perfil local) ejecutando un único comando con tu perfil administrador:

```bash
# Ejecutar con tu perfil administrador (ej: deployer, default, etc.)
./tools/podcast/setup_aws_resources.sh --profile TU_PERFIL_ADMIN

# Opcional: Especificar región si es distinta a us-east-1
./tools/podcast/setup_aws_resources.sh --profile TU_PERFIL_ADMIN --bucket conmanzanas --region us-east-1
```

El script es **100% idempotente**: comprueba qué recursos ya existen y sólo crea o configura lo que haga falta, configurando automáticamente el perfil `podcaster` en tu máquina local.

---

## 3. Configuración Manual y Detalle de Permisos (Referencia)

Si prefieres realizar los pasos manualmente o auditar las políticas:

### A. Archivo de Política IAM: [`iam-policy-podcaster.json`](iam-policy-podcaster.json)

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "PodcasterBucketManagement",
      "Effect": "Allow",
      "Action": [
        "s3:ListBucket",
        "s3:GetBucketLocation"
      ],
      "Resource": "arn:aws:s3:::conmanzanas"
    },
    {
      "Sid": "PodcasterObjectManagement",
      "Effect": "Allow",
      "Action": [
        "s3:PutObject",
        "s3:GetObject",
        "s3:DeleteObject"
      ],
      "Resource": "arn:aws:s3:::conmanzanas/*"
    }
  ]
}
```

> **Nota**: Reemplaza `conmanzanas` con el nombre real de tu bucket.

### B. Pasos para crear el perfil `podcaster` en AWS:

1. **Crear el usuario IAM**:
   * En la consola de AWS -> **IAM** -> **Users** -> **Create user** -> Nombre: `podcaster`.
   * (O vía CLI con `--profile deployer`):
     ```bash
     aws iam create-user --user-name podcaster --profile deployer
     ```

2. **Crear y adjuntar la política**:
   * Reemplaza el nombre de tu bucket en `iam-policy-podcaster.json`.
   * Crea la política en IAM:
     ```bash
     aws iam create-policy \
       --policy-name DimeloConManzanasPodcasterPolicy \
       --policy-document file://tools/podcast/iam-policy-podcaster.json \
       --profile deployer
     ```
   * Adjunta la política al usuario `podcaster`:
     ```bash
     aws iam attach-user-policy \
       --user-name podcaster \
       --policy-arn arn:aws:iam::TU_ACCOUNT_ID:policy/DimeloConManzanasPodcasterPolicy \
       --profile deployer
     ```

3. **Generar Access Keys y configurar el perfil local**:
   * Genera las credenciales en la consola de IAM para el usuario `podcaster`.
   * En tu terminal local, configura el perfil:
     ```bash
     aws configure --profile podcaster
     # Ingresa tu AWS Access Key ID
     # Ingresa tu AWS Secret Access Key
     # Default region name: us-east-1 (o tu región preferida)
     # Default output format: json
     ```

---

## 3. Configuración de Permisos del Bucket S3

Para que Spotify, Apple Podcasts y los oyentes puedan reproducir los audios, el bucket debe permitir la descarga pública directa y solicitudes de streaming (HTTP Range requests).

### A. Desactivar "Block Public Access" (Específico para Bucket Policy)
En la consola de S3 -> Tu bucket -> Pestaña **Permissions** -> **Block public access (bucket settings)**:
* Desmarca **"Block all public access"** (específicamente desmarca las opciones relacionadas con Bucket Policies públicas).
* (O vía CLI):
  ```bash
  aws s3api put-public-access-block \
    --bucket conmanzanas \
    --public-access-block-configuration "BlockPublicAcls=true,IgnorePublicAcls=true,BlockPublicPolicy=false,RestrictPublicBuckets=false" \
    --profile deployer
  ```

### B. Aplicar Política de Bucket: [`bucket-policy.json`](bucket-policy.json)
Permite a cualquier cliente HTTP (Spotify, Apple Podcasts, navegadores) descargar y reproducir los audios bajo la ruta `episodes/*`:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "PublicPodcastEpisodeRead",
      "Effect": "Allow",
      "Principal": "*",
      "Action": "s3:GetObject",
      "Resource": "arn:aws:s3:::conmanzanas/episodes/*"
    }
  ]
}
```

* Aplicar vía CLI:
  ```bash
  aws s3api put-bucket-policy \
    --bucket conmanzanas \
    --policy file://tools/podcast/bucket-policy.json \
    --profile deployer
  ```

### C. Configuración CORS para Streaming Web: [`cors-policy.json`](cors-policy.json)
Esencial para que reproductores web (reproductores HTML5 en navegadores o Spotify Web) puedan hacer peticiones `Range` sin bloqueos de origen cruzado:

```json
{
  "CORSRules": [
    {
      "AllowedHeaders": ["*"],
      "AllowedMethods": ["GET", "HEAD"],
      "AllowedOrigins": ["*"],
      "ExposeHeaders": [
        "ETag",
        "Content-Length",
        "Content-Type",
        "Content-Range",
        "Accept-Ranges"
      ],
      "MaxAgeSeconds": 3600
    }
  ]
}
```

* Aplicar vía CLI:
  ```bash
  aws s3api put-bucket-cors \
    --bucket conmanzanas \
    --cors-configuration file://tools/podcast/cors-policy.json \
    --profile deployer
  ```

---

## 4. Subir un Episodio y Actualizar Metadatos

Una vez configurado tu bucket y perfil `podcaster`, sube el audio con un solo comando:

```bash
# Ejemplo: Subir episodio 3 usando el perfil por defecto 'podcaster'
python3 tools/podcast/upload_audio.py \
    --episode 0003 \
    --file /ruta/al/archivo-0003.mp3 \
    --bucket conmanzanas
```

El script automáticamente:
1. Sube el `.mp3` a `s3://conmanzanas/episodes/0003-<archivo>.mp3` usando `--profile podcaster`.
2. Calcula el tamaño exacto en bytes (`audio_bytes`).
3. Extrae la duración estimada desde la transcripción Whisper o parámetro `--duration`.
4. Actualiza `.agents/episodes.yaml` con la nueva `audio_url`.
5. Recompila `public/podcast.xml` con Hugo.

---

## 5. Conectar el Feed en Spotify for Podcasters (Paso Único)

Solo una vez debes registrar la URL del feed:
1. Inicia sesión en [podcasters.spotify.com](https://podcasters.spotify.com).
2. Ve a los ajustes del show / disponibilidad del podcast.
3. Ingresa la URL oficial del feed RSS generado por Hugo:
   ```
   https://conmanzanas.lat/podcast.xml
   ```
4. A partir de ese momento, cualquier cambio que hagas en `.agents/episodes.yaml` se sincroniza automáticamente con Spotify al hacer `git push origin main`.
