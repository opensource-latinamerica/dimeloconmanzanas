# Regla de Transcripciones y Veracidad de Contenido

## Prohibición Absoluta de Transcripciones Simuladas o Alucinadas

1. **Cero Tolerancia a Transcripciones Sintéticas / Inventadas**:
   - **NUNCA** inventar, generar, simular o redactar diálogos ficticios simulando ser la transcripción de un episodio de Álvaro y Adriana.
   - Generar diálogos artificiales simulando transcripciones reales es considerado una alucinación grave y está estrictamente prohibido en este repositorio.

2. **Fuente Exclusiva para Transcripciones: Whisper (`tools/whisper`)**:
   - Las transcripciones oficiales provienen única y exclusivamente de archivos reales de audio procesados a través del entorno local de Whisper ubicado en `tools/whisper/`.
   - El pipeline de Whisper genera archivos de texto (`.txt`) con marcas de tiempo reales a partir del audio emitido en cabina.

3. **Ubicación y Convención de Nombres**:
   - **Carpeta estándar**: `static/transcripts/`
   - **Convención de nombres**: `<numero-episodio>-<slug-del-episodio>.txt` (debe coincidir con el prefijo y slug del archivo en `content/article/`).
     - Ejemplo: `static/transcripts/0003-inteligencia-artificial-y-rendicion-cognitiva.txt`
   - **Ejecución con Whisper**:
     ```bash
     ./tools/whisper/run_transcribe.sh <ruta-del-audio> ./static/transcripts/0003-inteligencia-artificial-y-rendicion-cognitiva.txt
     ```

4. **Protocolo para Incorporar Transcripciones al Sitio**:
   - Solo se puede incorporar una transcripción en un episodio cuando el archivo `.txt` real generado por Whisper exista en `static/transcripts/`.
   - Se enlaza el archivo descargable en el shortcode: `{{< transcripcion descargar="/transcripts/0003-inteligencia-artificial-y-rendicion-cognitiva.txt" >}}`
   - Si no se dispone del archivo real de transcripción para un episodio, el episodio se deja sin transcripción hasta que el audio sea procesado.
