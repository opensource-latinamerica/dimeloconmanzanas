# Regla de Arquitectura Hugo: Inmutabilidad de Submódulos en `themes/`

## 1. Principio Rector: Prohibición Absoluta de Modificar `themes/`
Los contenidos dentro del directorio `themes/` (como `themes/mostafa-hugo-theme`) son **submódulos Git externos** gestionados mediante `.gitmodules`.

Por tanto, el agente y los desarrolladores **NUNCA DEBEN modificar, editar, agregar, renombrar ni eliminar ningún archivo dentro del directorio `themes/`**.

---

## 2. Razones Técnicas
1. **Ruptura de CI/CD y Submódulos**: Modificar archivos dentro de un submódulo crea estados "dirty" en Git y divergencias de commit (SHA huérfano) que rompen los flujos de despliegue automatizado en GitHub Actions.
2. **Pérdida de Cambios**: Cualquier ejecución de `git submodule update --remote` o clonación limpia del repositorio sobreescribirá o descartará los cambios locales no versionados en el upstream del tema.
3. **Buenas Prácticas de Hugo**: Hugo cuenta con un sistema nativo de precedencia (*lookup order*) diseñado específicamente para evitar tocar el código del tema.

---

## 3. Protocolo Obligatorio para Personalizaciones (Hugo Lookup Order)

Cualquier cambio, personalización, extensión o corrección visual/estructural debe realizarse **exclusivamente en la raíz del proyecto**, sobrescribiendo la jerarquía de Hugo:

| Qué deseas personalizar | Dónde se debe crear/modificar en la raíz | 🚫 NUNCA tocar en `themes/` |
| :--- | :--- | :--- |
| **Plantillas HTML y Vistas** | `layouts/...` (ej: `layouts/_default/single.html`) | `themes/<tema>/layouts/...` |
| **Partials y Componentes** | `layouts/partials/...` | `themes/<tema>/layouts/partials/...` |
| **Shortcodes** | `layouts/shortcodes/...` | `themes/<tema>/layouts/shortcodes/...` |
| **Hojas de Estilo CSS / SASS** | `assets/css/...` o en `assets/...` | `themes/<tema>/assets/...` |
| **JavaScript** | `assets/js/...` | `themes/<tema>/assets/js/...` |
| **Archivos Estáticos / Fuentes / Logos** | `static/...` | `themes/<tema>/static/...` |
| **Arquetipos de Contenido** | `archetypes/...` | `themes/<tema>/archetypes/...` |

### Regla de Oro:
Si una plantilla del tema requiere modificación, **copia la plantilla original a la ruta equivalente dentro de `layouts/`** en la raíz del proyecto y realiza los cambios allí. Hugo le dará prioridad automáticamente sobre la versión del tema sin alterar el submódulo.
