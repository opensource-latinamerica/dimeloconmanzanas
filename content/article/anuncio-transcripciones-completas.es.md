---
title: "¡Llegaron las Transcripciones Completas a Dímelo con Manzanas!"
date: 2026-10-04T16:30:00-06:00
draft: false
tags: ["anuncio", "accesibilidad", "transcripciones", "comunidad"]
categories: ["anuncio"]
author: "Adriana y Alvaro"
---

Nos emociona anunciar una gran mejora para nuestra comunidad: a partir de ahora, nuestros episodios incluirán la transcripción íntegra y pública de todo lo conversado en cabina.

<!--more-->

Adriana y Álvaro te cuentan por qué decidimos hacer públicas las transcripciones y cómo utilizarlas para estudiar, buscar conceptos o acompañar tu escucha.

En *Dímelo con Manzanas*, nuestra misión siempre ha sido **democratizar el conocimiento y hacer que el aprendizaje sea accesible para todos**. Creemos firmemente que las ideas complejas no deben quedarse encerradas en tecnicismos ni limitarse a un solo formato.

Por eso, tomamos la decisión de hacer las transcripciones de nuestros episodios **100% públicas, abiertas y disponibles directamente en nuestro blog**.

---

### ¿Por qué decidimos hacerlas públicas?

1. **Accesibilidad e Inclusión Real**:  
   Queremos que cualquier persona, incluyendo oyentes con discapacidad auditiva o personas sordas, pueda disfrutar y aprender con cada uno de los temas que desglosamos.

2. **Facilidad de Estudio y Búsqueda**:  
   ¿Recuerdas una frase, un autor o una analogía genial pero no sabes en qué minuto exacto del podcast lo dijimos? Con las transcripciones de texto completo, basta con presionar `Ctrl + F` (o `Cmd + F`) en tu navegador para encontrar al instante conceptos clave como *"loros estocásticos"*, *"vigilancia epistémica"* o *"TCP/IP"*.

3. **Lectura Acompañada (*Read-Along*)**:  
   Muchos de ustedes nos escuchan mientras conducen, caminan o entrenan, pero al llegar a casa o a la oficina desean repasar con calma las referencias académicas o citar partes de la conversación.

---

### 🛠️ Generación Automática desde el Audio Real con Whisper

Una duda común al ver transcripciones en la web es si están generadas artificialmente o si reflejan con exactitud lo que se dijo en cabina. En *Dímelo con Manzanas* seguimos una política de veracidad inquebrantable:

* **Cero transcripciones sintéticas o inventadas**: Cada transcripción proviene directamente del archivo de audio real grabado durante la sesión.
* **Procesamiento automatizado con Whisper**: Implementamos una herramienta local y abierta basada en `faster-whisper` (optimizada con cuantización `int8` sobre contenedores Podman/Docker). Esto nos permite transcribir el audio en español con marcas de tiempo precisas segundo a segundo, sin depender de nubes propietarias y garantizando la privacidad de las grabaciones.
* **Archivo Raw Descargable**: Además de leer la transcripción en el blog, los oyentes pueden descargar el archivo `.txt` original con las marcas de tiempo exactas para sus propios análisis o proyectos de accesibilidad.

---

### 🎙️ Detrás de Cámaras: El Flujo de Creación de un Episodio

Compartir el proceso abierto forma parte del espíritu de nuestro proyecto. Así nace cada entrega de *Dímelo con Manzanas*:

1. **Curaduría e Investigación Académica**: Seleccionamos temas de frontera tecnológica y exploramos publicaciones de instituciones líderes (como el MIT, Stanford o la Wharton School).
2. **Estructuración con Manzanas**: Diseñamos los capítulos traduciendo conceptos abstractos a metáforas cotidianas y analogías visuales que cualquiera pueda disfrutar.
3. **Grabación en Cabina**: Adriana y Álvaro graban la conversación de forma cercana, amena y espontánea.
4. **Procesamiento de Audio y Transcripción Automática**: El audio master se procesa a través de nuestro pipeline de Whisper en `tools/whisper/`, generando el registro textual con marcas de tiempo.
5. **Publicación Abierta**: El episodio se lanza en Spotify, mientras que en [conmanzanas.lat](https://conmanzanas.lat) se publican las notas completas, el reproductor embebido, las fichas interactivas de los estudios científicos citados y la transcripción íntegra descargable.

¡Esperamos que esta nueva herramienta enriquezca su experiencia de aprendizaje! Si tienes comentarios, sugerencias o ideas sobre cómo seguir mejorando el podcast, no dudes en escribirnos a través del buzón de la comunidad al final de cada página.
