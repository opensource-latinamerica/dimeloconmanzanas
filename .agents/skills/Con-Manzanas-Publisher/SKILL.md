---
name: con-manzanas-publisher
description: Transform raw podcast transcripts and research portfolios into crisp, high-impact blog posts formatted natively for the Hugo Mostafa Theme. Use when writing, publishing, or editing podcast episode blog posts for Dímelo con Manzanas.
---

# Skill: Dímelo-Con-Manzanas-Publisher

## Purpose
Transform raw podcast transcripts and research portfolios from Gemini Notebook into crisp, high-impact blog posts formatted natively for the Hugo Mostafa Theme. 

## Structural Constraints
- **Reading Time Guardrail**: The final blog post must be concise, punchy, and highly scannable so that it **takes no more than 1.5 to 2.5 minutes to read** (target 350–500 words).
- **Tone & Style**: Direct, accessible, human-centric Latin American Spanish. Eliminate all introductory corporate AI jargon (e.g., "En el dinámico mundo de hoy", "adentrémonos").
- **Core Strategy**: Even when deep technical data or comprehensive reference sheets are supplied, the body sections must remain short, punchy, and highly scannable. Use visual tables or callouts instead of long paragraphs to keep reading time low.
- **Repository Safety**: Never edit published episodes with `status: published` or existing `spotify_url`. Always register new episodes in `.agents/episodes.yaml`.
- **Dynamic Tags (Taxonomía)**: Tags are **NEVER hardcoded or generic**. They must be dynamically generated and tailored to the specific topics of each episode (3 to 5 lowercase kebab-case tags, e.g. `["ciberseguridad", "pensamiento-critico", "educacion"]`). The only fixed taxonomy property is `categories: ["episodio"]`.

## Input Parameters
- `{{EPISODE_TRANSCRIPT}}`: Spoken dialogue between the speakers (los manzaneros).
- `{{SOURCE_CATALOG}}`: Curated list of original URLs, research posts, and PDF documents.
- `{{METADATA}}`: YAML Front Matter properties (Title, Date, Episode Number, Tags).

## Execution Steps

### Step 1: Strict Length & Content Pruning
1. Identify the primary narrative arc and limit the breakdown to a maximum of 4 to 5 short chapters.
2. Condense dialogue into concise explanations. If a topic requires deep data exposure, convert it into an explicit comparison block or an "🍎 Analogía Clave" using the custom `{{< manzana >}}` shortcode to maximize clarity while minimizing reading time.

### Step 2: URL & Citation Mapping
1. Match all studies, tools, or papers mentioned during the episode with their exact link or PDF location from `{{SOURCE_CATALOG}}`.
2. Map these links into two specific output locations:
   - **Inline Hyperlinks**: Naturally wrap key entities inside the text paragraphs using descriptive anchors.
   - **Dedicated Footer**: Build a centralized resource appendix using the `{{< estudio >}}` shortcode or bulleted reference list for easy listener discovery.

### Step 3: Markdown Generation
Target file: `content/article/00XX-<slug>.es.md`

Output the post matching this strict layout template:

```markdown
---
title: "00XX - [Compelling Title Spoken with Manzanas]"
date: YYYY-MM-DDTHH:MM:SS-06:00
draft: false
categories: ["episodio"]
tags: ["[tema-central-1]", "[tema-central-2]", "[tema-central-3]"]
author: "[Autor(es) o Presentadores según la definición en episodes.yaml]"
---

[Insert a 2-sentence captivating hook paragraph explaining what is broken down in this episode.]

<!--more-->

Presentado por **[Nombre(s) de los autores / presentadores]**. [Breve contexto de la conversación].

## Capítulo 1: [Short Title]
[Concise text breakdown.]

{{< manzana title="Analogía con Manzanas: [Título]" >}}
[A crystal-clear, text-efficient analogy using apples or everyday concepts.]
{{< /manzana >}}

## Conclusión de [Nombre(s) de los autores / presentadores]
[Párrafo de cierre cálido y reflexivo.]

---

### 🎙️ Transcripción Completa del Episodio
A continuación puedes consultar la transcripción íntegra de la conversación o descargar el archivo de texto con las marcas de tiempo.

{{< transcripcion 
    titulo="Transcripción Completa: Episodio 00XX" 
    badge="Texto Íntegro · Audio Real" 
    descargar="/transcripts/00XX-<slug>.txt" >}}
{{< /transcripcion >}}

---

### 📚 Enlaces de Referencia y Estudio Científico
Si deseas profundizar en las investigaciones y reportes en los que se basó este episodio:

{{< estudio 
    titulo="[Título del Paper]"
    autores="[Autores / Institución]"
    revista="[Revista o arXiv]"
    anio="YYYY"
    url="[URL]"
    pdf="[PDF_URL]" >}}
[Resumen breve de una o dos líneas del aporte del estudio.]
{{< /estudio >}}

* [**Título del recurso** – Fuente / Medio](URL)
```

### Step 4: Manifest & Reading-Time Quality Audit
1. **Manifest Registration**: Add the new episode entry to `.agents/episodes.yaml` with `status: draft`.
2. **Text Density Check**: Ensure total body word count stays between **700 and 900 words** to guarantee the 3–5 minute reading cap.
3. **Scrub AI Jargon**: Eliminate repetitive phrasing, generic intros, or overly corporate wording.
4. **Automated Audit Execution**: Run the auditor script to verify all constraints pass:
   ```bash
   python3 .agents/skills/Con-Manzanas-Publisher/scripts/audit_episode.py content/article/00XX-<slug>.es.md
   ```
