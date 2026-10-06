# Reglas del Proyecto: Dímelo con Manzanas

## Política de Edición de Episodios
- **Fuente de verdad**: Antes de interactuar con o modificar episodios en `content/article/`, consulta siempre `.agents/episodes.yaml`.
- **Episodios con `status: published` o con `spotify_url`**:
  - NUNCA modificar ni alterar archivos de episodios existentes marcados como publicados (como el Episodio 1 o el Episodio 2). Son definitivos e intocables.
- **Episodios nuevos o en desarrollo (`status: draft` o sin `spotify_url`)**:
  - Solo se permite editar, actualizar y agregar contenido en episodios que **NO** tengan una URL de Spotify o estén marcados en borrador (`status: draft`).
  - La generación de nuevos contenidos, notas del episodio y referencias académicas aplica exclusivamente a episodios nuevos.

## Política de Transcripciones y Veracidad de Contenido
- **Prohibición absoluta de alucinación**:
  - NUNCA inventar, simular, redactar ni generar transcripciones sintéticas o ficticias simulando ser las palabras de Adriana y Álvaro. Generar transcripciones artificiales está estrictamente prohibido.
- **Flujo de trabajo para transcripciones con Whisper (`tools/whisper/`)**:
  - Las transcripciones oficiales provienen única y exclusivamente de los archivos de audio reales procesados a través del pipeline Whisper en `tools/whisper/`.
  - Solo cuando el usuario proporcione el archivo `.txt` real generado por Whisper se podrá integrar la transcripción al episodio y subir el archivo raw descargable a la página.
  - Si un episodio no cuenta con un archivo real de transcripción, se deja sin transcripción.

## Política de Publicación de Nuevos Episodios (Con-Manzanas-Publisher)
- **Activación obligatoria de la habilidad**: Al redactar, estructurar o publicar un nuevo episodio de podcast, el agente **DEBE** activar y aplicar estrictamente la habilidad `con-manzanas-publisher` ([`.agents/skills/Con-Manzanas-Publisher/SKILL.md`](.agents/skills/Con-Manzanas-Publisher/SKILL.md)).
- **Límite de lectura (Guardrail)**: El texto del artículo debe ser ágil y estructurado para leerse en **3 a 5 minutos** (límite estricto de **700 a 900 palabras** en el cuerpo editorial).
- **Uso obligatorio de shortcodes nativos**:
  - `{{< manzana title="Analogía con Manzanas: ..." >}}`: Al menos una analogía visual cotidiana.
  - `{{< transcripcion titulo="..." badge="..." descargar="..." >}}`: Transcripción accesible enlazando al archivo en `static/transcripts/`.
  - `{{< estudio ... >}}`: Ficha interactiva para citas de investigaciones académicas.
- **Taxonomía estricta y etiquetas dinámicas**:
  - Frontmatter obligatorio con `categories: ["episodio"]` (minúsculas) y el campo `author` según la definición del episodio en `.agents/episodes.yaml` (ej: "Manzaneros", "Adriana y Alvaro", etc.).
  - Las etiquetas (`tags`) **NUNCA son fijas ni genéricas**: deben crearse a la medida de cada entrega (de 3 a 5 tags en kebab-case, ej: `["ciberseguridad", "pensamiento-critico"]`).
- **Auditoría automatizada obligatoria**: Ningún episodio se considerará completado sin haber ejecutado exitosamente el auditor editorial:
  ```bash
  python3 .agents/skills/Con-Manzanas-Publisher/scripts/audit_episode.py <ruta-al-episodio>
  ```
- **Formato Estricto de Título ('00XX - Título')**: Todos los títulos de episodios en el frontmatter (`content/article/`), en el manifiesto `.agents/episodes.yaml` y en el feed RSS (`podcast.xml`) **DEBEN** iniciar obligatoriamente con el prefijo numérico de 4 dígitos seguido de guion y espacio: `0001 - ...`, `0002 - ...`, `0003 - ...` ([`.agents/rules/episode-titling.md`](.agents/rules/episode-titling.md)).
- **Registro en manifiesto**: Todo episodio nuevo debe registrarse de inmediato en `.agents/episodes.yaml` con `status: draft`.

## Política de Seguridad: Hardening y Menor Privilegio (Least Privilege)
- **Principio Rector**: Toda infraestructura, bucket S3, rol IAM, endpoint o URL web debe seguir estrictamente el Principio de Menor Privilegio ([`.agents/rules/security-hardening.md`](.agents/rules/security-hardening.md)).
- **Almacenamiento y Nube**:
  - Perfiles operativos (como `podcaster`) tienen prohibidos los permisos de eliminación (`DeleteObject`, `DeleteBucket`) y alteración de configuraciones. Sus permisos de escritura están confinados a prefijos exactos (`arn:aws:s3:::conmanzanas/episodes/*`).
  - El acceso anónimo público está limitado con exclusividad a `s3:GetObject` en `/episodes/*`. Listar el bucket (`ListBucket`), la raíz o directorios privados está estrictamente bloqueado.
  - Cifrado en tránsito forzado: toda política de bucket debe incluir denegación explícita (`Effect: Deny`) si la solicitud no viaja por HTTPS (`aws:SecureTransport: false`).
  - Resiliencia obligatoria: buckets de entrega multimedia deben mantener S3 Versioning habilitado.
- **URLs Web y Navegación**:
  - **HTTPS 100% obligatorio**: Toda URL expuesta en el sitio web, feed RSS (`podcast.xml`), metadatos o enlaces debe usar `https://`. Queda prohibido el uso de `http://` en texto claro.
  - Enlaces externos deben implementar `rel="noopener noreferrer"`.

## Política de Infraestructura: Reproducibilidad Obligatoria por Scripts
- **Principio Rector**: Toda infraestructura en la nube, bucket, política de seguridad, usuario IAM, endpoint o configuración externa **DEBE ser 100% reproducible mediante scripts automatizados y versionados** ([`.agents/rules/infrastructure-reproducibility.md`](.agents/rules/infrastructure-reproducibility.md)).
- **Cero Cambios Manuales Huérfanos**:
  - Queda prohibido realizar modificaciones manuales desde consolas web o CLI sin que queden inmediatamente reflejadas y parametrizadas en los scripts ejecutables dentro de `tools/` y en sus plantillas canónicas JSON/YAML.
- **Idempotencia y Parametrización**:
  - Todos los scripts operativos deben ser idempotentes (capaces de ejecutarse repetidamente sin romper el estado) y aceptar parámetros configurables (`--profile`, `--bucket`, `--region`) sin credenciales hardcodeadas.

## Política de Submódulos y Temas Hugo (Inmutabilidad de themes/)
- **Principio Rector**: Los contenidos dentro de `themes/` son submódulos Git externos ([`.agents/rules/theme-submodules.md`](.agents/rules/theme-submodules.md)).
- **Prohibición Estricta**: **NUNCA modificar, editar, agregar ni borrar archivos dentro de `themes/`**.
- **Precedencia Hugo (Lookup Order)**: Toda personalización, override de plantilla, shortcode, estilo CSS, script o recurso estático debe implementarse en los directorios raíz (`layouts/`, `assets/`, `static/`, `archetypes/`). Hugo prioriza automáticamente los archivos de la raíz sobre los del submódulo sin romper el repositorio upstream.

