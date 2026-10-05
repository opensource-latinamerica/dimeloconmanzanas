# Skill: Dímelo-Con-Manzanas-Publisher

## Purpose
Transform raw podcast transcripts and research portfolios from Gemini Notebook into crisp, high-impact blog posts formatted natively for the Hugo Mostafa Theme. 

## Structural Constraints
- **Reading Time Guardrail**: The final blog post must be concise and tightly structured so that it **takes no more than 3 to 5 minutes to read**.
- **Tone & Style**: Direct, accessible, human-centric Latin American Spanish. Eliminate all introductory corporate AI jargon (e.g., "En el dinámico mundo de hoy", "adentrémonos").
- **Core Strategy**: Even when deep technical data or comprehensive reference sheets are supplied, the body sections must remain short, punchy, and highly scannable. Use visual tables or callouts instead of long paragraphs to keep reading time low.

## Input Parameters
- `{{EPISODE_TRANSCRIPT}}`: Spoken dialogue between Adriana and Álvaro.
- `{{SOURCE_CATALOG}}`: Curated list of original URLs, research posts, and PDF documents.
- `{{METADATA}}`: YAML Front Matter properties (Title, Date, Episode Number, Tags).

## Execution Steps

### Step 1: Strict Length & Content Pruning
1. Identify the primary narrative arc and limit the breakdown to a maximum of 4 to 5 short chapters.
2. Condense dialogue into concise explanations. If a topic requires deep data exposure, convert it into an explicit comparison block or an "🍎 Analogia Clave" to maximize clarity while minimizing reading time.

### Step 2: URL & Citation Mapping
1. Match all studies, tools, or papers mentioned during the episode with their exact link or PDF location from `{{SOURCE_CATALOG}}`.
2. Map these links into two specific output locations:
   - **Inline Hyperlinks**: Naturally wrap key entities inside the text paragraphs using descriptive anchors.
   - **Dedicated Footer**: Build a centralized resource appendix for easy listener discovery.

### Step 3: Markdown Generation
Output the post matching this strict layout template:

```yaml
---
title: "00XX - [Compelling Title Spoken with Manzanas]"
date: YYYY-MM-DD
categories: ["Episodio"]
tags: ["Tag1", "Tag2"]
---

[Insert a 2-sentence captivating hook paragraph explaining what is broken down in this episode.]

Presentado por **Adriana y Álvaro**.

## Capítulo 1: [Short Title]
[Concise text breakdown.]

🍎 Analogía Clave
### [Analogía Title]
[A crystal-clear, text-efficient analogy using apples or household concepts.]

## 📚 Enlaces de Referencia y Estudio Científico
Si deseas profundizar en el informe clínico y académico original en el que se basó este episodio:

#### [Main Paper Title]
[Brief 1-sentence context line describing the research origin.]
- [Leer publicación / Descargar PDF](URL_LINK)
- [Artículo de Referencia](URL_LINK)
```

### Step 4: Reading-Time Quality Audit
1. Execute a text density check: Ensure total word count stays under **700 to 900 words** to guarantee the 3-5 minute reading cap.
2. Scrub generic AI-isms, repetitive explanations, or filler text.
