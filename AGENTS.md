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
