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
  - Frontmatter obligatorio con `categories: ["episodio"]` (minúsculas) y `author: "Manzaneros"`.
  - Las etiquetas (`tags`) **NUNCA son fijas ni genéricas**: deben crearse a la medida de cada entrega (de 3 a 5 tags en kebab-case, ej: `["ciberseguridad", "pensamiento-critico"]`).
- **Auditoría automatizada obligatoria**: Ningún episodio se considerará completado sin haber ejecutado exitosamente el auditor editorial:
  ```bash
  python3 .agents/skills/Con-Manzanas-Publisher/scripts/audit_episode.py <ruta-al-episodio>
  ```
- **Registro en manifiesto**: Todo episodio nuevo debe registrarse de inmediato en `.agents/episodes.yaml` con `status: draft`.
