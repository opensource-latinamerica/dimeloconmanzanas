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
