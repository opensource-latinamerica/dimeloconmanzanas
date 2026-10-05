# Regla de Edición de Episodios del Podcast

## Fuente de Verdad: `.agents/episodes.yaml`

Antes de leer o intentar modificar cualquier archivo de episodio en `content/article/`, el agente **DEBE** consultar obligatoriamente el archivo de registro `.agents/episodes.yaml`.

## Restricciones Estrictas de Modificación

1. **Episodios Publicados (`status: published` o con `spotify_url` definida)**:
   - **NUNCA** modificar, sobreescribir ni editar los archivos asociados a estos episodios.
   - Son episodios finales ya publicados en plataformas de streaming (ejemplo: Episodio 1 y Episodio 2). Son estrictamente de **solo lectura**.

2. **Episodios Nuevos o en Borrador (`status: draft` o sin `spotify_url`)**:
   - Solo se permite modificar, enriquecer o generar contenido para episodios que figuren con `status: draft` o cuyo `spotify_url` sea `null` (como el Episodio 3).
   - Cuando se cree un nuevo episodio, se debe registrar en `.agents/episodes.yaml` con su estado correspondiente.

3. **Flujo Obligatorio de Publicación (`con-manzanas-publisher`)**:
   - Todo nuevo episodio debe redactarse siguiendo la habilidad `.agents/skills/Con-Manzanas-Publisher/SKILL.md` y su plantilla canónica `.agents/skills/Con-Manzanas-Publisher/resources/episode_template.md`.
   - Las etiquetas (`tags`) deben ser personalizadas y únicas para cada entrega (3 a 5 tags en kebab-case representativas del tema), evitando etiquetas genéricas o placeholders de plantilla.
   - Se debe validar el cumplimiento del artículo ejecutando:
     ```bash
     python3 .agents/skills/Con-Manzanas-Publisher/scripts/audit_episode.py <ruta-al-episodio>
     ```
