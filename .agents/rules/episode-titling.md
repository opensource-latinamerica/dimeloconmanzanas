# Regla de Nomenclatura Editorial: Formato Obligatorio de Títulos `00XX - Título`

## 1. Principio Rector: Uniformidad Canónica de Títulos
Todos los episodios del podcast "Dímelo con Manzanas" **DEBEN** mantener una nomenclatura idéntica y estandarizada en todas las capas del proyecto:
1. **Frontmatter del artículo Markdown** en `content/article/<slug>.es.md`.
2. **Manifiesto central de episodios** en `.agents/episodes.yaml`.
3. **Feed RSS de distribución** en `podcast.xml` (`<title>` e `<itunes:title>`).

---

## 2. Estructura Obligatoria del Título

El título de cada episodio debe iniciar estrictamente con un prefijo numérico de cuatro dígitos, seguido de un espacio, un guion corto (`-`), otro espacio y el título editorial:

```text
00XX - Título Completo del Episodio
```

### Ejemplos Canónicos:
-  `0001 - Internet para Todos: De Postales Digitales a la Seguridad Online`
-  `0002 - Inteligencia Artificial y Salud Mental: ¿Compañía Real o Espejismo Digital?`
-  `0003 - ¿Tu Cerebro en Pausa? Inteligencia Artificial y Rendición Cognitiva`

### Formatos Prohibidos:
- ❌ `Internet para Todos` *(Falta el prefijo numérico)*
- ❌ `Episodio 1: Internet para Todos` *(Uso de texto en vez del formato 00XX -)*
- ❌ `01 - Internet para Todos` *(Menos de cuatro dígitos)*
- ❌ `0001: Internet para Todos` *(Uso de dos puntos en vez de guion)*

---

## 3. Implementación y Salvaguardas en Código

1. **Auditoría Editorial (`audit_episode.py`)**:
   - Todo episodio auditado debe superar la comprobación de expresión regular:
     ```python
     re.match(r"^[0-9]{4}\s*-\s*.+", title)
     ```
2. **Plantilla Hugo RSS (`layouts/index.podcast.xml`)**:
   - El compilador de Hugo aplica formato defensivo en tiempo de generación: si por error humano un título en el YAML o frontmatter omitiese el prefijo, la plantilla prependeará automáticamente `$epNum - `:
     ```go
     {{- if and $epNum (not (findRE "^[0-9]{4}\\s*-\\s*" $title)) -}}
       {{- $title = printf "%s - %s" $epNum $title -}}
     {{- end -}}
     ```
3. **Manifiesto `.agents/episodes.yaml`**:
   - El campo `title` de cada episodio registrado debe incluir siempre el prefijo canónico `00XX - `.
