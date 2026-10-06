# Regla de Distribución y Metadatos del Podcast RSS

## 1. Principio Rector: Integridad y Estándares de Distribución Multiplataforma
El feed oficial de sindicación (`podcast.xml`) distribuido a plataformas como **Spotify, Apple Podcasts, Amazon Music y Pocket Casts** debe cumplir estrictamente con los estándares RSS 2.0, iTunes Podcast DTD y PodcastIndex namespace.

---

## 2. Requisitos Técnicos de Audio y Enclosures (`<enclosure>`)

1. **Alojamiento y Protocolo**:
   - Todo archivo de audio referenciado en `audio_url` debe servirse exclusivamente mediante **HTTPS**.
   - El almacenamiento de origen en AWS S3 debe permitir solicitudes por rango de bytes (`Accept-Ranges: bytes`) para posibilitar el streaming y adelanto rápido en reproductores.

2. **Detección Dinámica y Estricta de MIME Types**:
   - Queda terminantemente prohibido declarar tipos MIME incorrectos o fijos. El feed debe emitir dinámicamente:
     - Archivos `.m4a` / `.mp4`: `type="audio/x-m4a"` (o `audio/mp4`).
     - Archivos `.mp3`: `type="audio/mpeg"`.
     - Archivos `.ogg`: `type="audio/ogg"`.

3. **Precisión de Metadatos Físicos**:
   - `audio_bytes`: Debe reflejar con exactitud de 1 byte el peso real del archivo subido a S3.
   - `audio_duration`: Debe formatearse en `MM:SS` (o `HH:MM:SS` para episodios largos), coincidiendo con la duración real cronometrada.

---

## 3. Jerarquía de Tres Niveles para Notas y Descripciones

Para garantizar que las notas se visualicen correctamente en todas las aplicaciones sin colapsar ni romper el formato, el feed debe generar tres niveles diferenciados de contenido:

1. **`<description>` (Compatibilidad Universal)**:
   - Texto plano formateado con saltos de línea legibles, envuelto en bloque `<![CDATA[ ... ]]>`.
2. **`<itunes:summary>` (Apple Podcasts Compliance)**:
   - Texto plano estricto (`plainify`), sanitizado de cualquier etiqueta HTML, limitado a un máximo de 4,000 caracteres.
3. **`<content:encoded>` (Spotify y Reproductores Modernos con Rich HTML)**:
   - Código HTML enriquecido envuelto en `<![CDATA[ ... ]]>`.
   - **Saltos de línea en marcas de tiempo**: Todo renglón con formato `MM:SS - Capítulo` debe conservar saltos de línea explícitos (`<br>` o sintaxis de dos espacios en Markdown) para que Spotify y Apple generen capítulos interactivos y no un bloque continuo de texto.
   - **Hipervínculos clickeables**: Los enlaces a artículos y notas web deben generarse con etiquetas HTML `<a href="..." target="_blank" rel="noopener noreferrer">`.

---

## 4. Gestión de Insignias y Recursos Gráficos

- Las insignias de plataformas (Spotify, Apple Podcasts) deben ubicarse exclusivamente en `static/images/badges/` en formatos `.svg` (vectorial web) y `.png` (transparencia fija).
- Queda prohibido comitear formatos no web (`.eps`) o archivos de metadatos de sistema operativo (`._*`, `Icon\r`).
