#!/usr/bin/env python3
"""
Auditor automatizado de episodios para Dímelo con Manzanas.
Verifica que los artículos de episodios cumplan con los estándares de la habilidad
'Con-Manzanas-Publisher':
- Límite de tiempo de lectura (700-900 palabras en el cuerpo editorial).
- Uso de shortcodes nativos: {{< manzana >}}, {{< transcripcion >}}, {{< estudio >}}.
- Taxonomía estricta: categories: ["episodio"], author: "Manzaneros".
- Registro en .agents/episodes.yaml.
"""

import sys
import os
import re
from pathlib import Path

try:
    import yaml
except ImportError:
    yaml = None

# Códigos de color ANSI para terminal
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
BLUE = "\033[94m"
BOLD = "\033[1m"
RESET = "\033[0m"

def load_manifest(manifest_path=".agents/episodes.yaml"):
    """Carga el manifiesto de episodios."""
    if not os.path.exists(manifest_path):
        return None
    try:
        with open(manifest_path, "r", encoding="utf-8") as f:
            if yaml:
                return yaml.safe_load(f)
            else:
                # Parser rudimentario si PyYAML no está presente
                content = f.read()
                episodes = []
                for block in content.split("- number:"):
                    if not block.strip():
                        continue
                    m_num = re.search(r'^\s*["\']?([0-9]+)["\']?', block)
                    m_file = re.search(r'file:\s*["\']?([^"\'\n]+)["\']?', block)
                    m_status = re.search(r'status:\s*["\']?([^"\'\n]+)["\']?', block)
                    if m_num and m_file:
                        episodes.append({
                            "number": m_num.group(1),
                            "file": m_file.group(1).strip(),
                            "status": m_status.group(1).strip() if m_status else "unknown"
                        })
                return {"episodes": episodes}
    except Exception as e:
        print(f"{YELLOW}[ADVERTENCIA] No se pudo parsear {manifest_path}: {e}{RESET}")
        return None

def extract_frontmatter(content):
    """Extrae el frontmatter YAML y el cuerpo Markdown."""
    match = re.match(r"^---\r?\n(.*?)\r?\n---\r?\n(.*)$", content, re.DOTALL)
    if not match:
        return {}, content
    raw_fm = match.group(1)
    body = match.group(2)
    fm = {}
    if yaml:
        try:
            fm = yaml.safe_load(raw_fm) or {}
        except Exception:
            fm = {}
    if not fm:
        for line in raw_fm.splitlines():
            parts = line.split(":", 1)
            if len(parts) == 2:
                key = parts[0].strip()
                val = parts[1].strip().strip('"\'')
                fm[key] = val
    return fm, body

def calculate_editorial_word_count(body):
    """
    Calcula el conteo de palabras del cuerpo editorial excluyendo
    la transcripción larga y los enlaces de referencia.
    """
    # Eliminar bloques de transcripción embebidos si los hay
    clean = re.sub(r"\{\{<\s*transcripcion[\s\S]*?\{\{<\s*/transcripcion\s*>}}", "", body)
    clean = re.sub(r"\{\{<\s*transcripcion[^\n>]*>}}", "", clean)
    # Eliminar shortcodes de estudio para el conteo de narrativa
    clean = re.sub(r"\{\{<\s*estudio[\s\S]*?\{\{<\s*/estudio\s*>}}", "", clean)
    # Eliminar llamadas HTML y comentarios
    clean = re.sub(r"<!--[\s\S]*?-->", "", clean)
    # Extraer palabras
    words = re.findall(r"\b[^\W\d_]+(?:'[^\W\d_]+)?\b", clean, re.UNICODE)
    return len(words)

def audit_episode(file_path, manifest=None):
    """Audita un único archivo de episodio."""
    path = Path(file_path)
    print(f"\n{BOLD}{BLUE}======================================================{RESET}")
    print(f"{BOLD}Auditoría Editorial: {path.name}{RESET}")
    print(f"{BLUE}======================================================{RESET}")

    if not path.exists():
        print(f"  {RED}[FAIL] El archivo no existe: {file_path}{RESET}")
        return False

    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    fm, body = extract_frontmatter(content)
    errors = []
    warnings = []
    passes = []

    # 1. Validación de Formato de Título
    title = str(fm.get("title", ""))
    if re.match(r"^[0-9]{4}\s*-\s*.+", title):
        passes.append(f"Título estructurado con número de episodio: «{title[:45]}...»")
    else:
        errors.append(f"El título debe iniciar con formato '00XX - Título': actual '{title}'")

    # 2. Validación de Categoría
    cats = fm.get("categories", [])
    if isinstance(cats, str):
        cats = [cats]
    if "episodio" in cats:
        passes.append("Categoría correcta: 'episodio' (minúsculas)")
    elif "Episodio" in cats:
        errors.append("La categoría 'Episodio' tiene mayúscula; debe ser 'episodio' para alinearse con los templates")
    else:
        errors.append("Falta la categoría obligatoria: 'episodio'")

    # 3. Validación de Autoría
    author = str(fm.get("author", ""))
    if author in ["Manzaneros", "Adriana y Alvaro", "Adriana y Álvaro"]:
        passes.append(f"Autor válido: '{author}'")
    else:
        warnings.append(f"Se recomienda 'author: \"Manzaneros\"' (actual: '{author}')")

    # 4. Conteo de Palabras y Tiempo de Lectura
    word_count = calculate_editorial_word_count(body)
    est_reading_time = round(word_count / 200, 1)

    if 650 <= word_count <= 950:
        passes.append(f"Densidad de lectura óptima: {word_count} palabras (~{est_reading_time} min)")
    elif word_count < 650:
        warnings.append(f"Contenido breve: {word_count} palabras (~{est_reading_time} min). Meta recomendada: 700-900 palabras.")
    else:
        warnings.append(f"Contenido extenso: {word_count} palabras (~{est_reading_time} min). El guardrail de la habilidad sugiere podar a 700-900 palabras.")

    # 5. Shortcode Obligatorio: Analogía con Manzanas ({{< manzana >}})
    if re.search(r"\{\{<\s*manzana\b", body):
        passes.append("Shortcode de analogía presente: {{< manzana >}}")
    else:
        errors.append("Falta el shortcode obligatorio de analogía: {{< manzana title=\"...\" >}}")

    # 6. Shortcode de Transcripción ({{< transcripcion >}})
    if re.search(r"\{\{<\s*transcripcion\b", body):
        passes.append("Shortcode de transcripción presente: {{< transcripcion >}}")
        # Verificar si apunta a un archivo existente
        m_dl = re.search(r'descargar=["\'](/transcripts/[^"\']+)["\']', body)
        if m_dl:
            disk_path = "static" + m_dl.group(1)
            if os.path.exists(disk_path):
                passes.append(f"Archivo de transcripción verificado en disco: {disk_path}")
            else:
                warnings.append(f"El archivo referenciado no existe aún en disco: {disk_path}")
    else:
        warnings.append("No se encontró el shortcode {{< transcripcion >}} (debe añadirse al contar con el archivo de audio transcrito)")

    # 7. Shortcode de Estudio Científico (Recomendado para episodios analíticos)
    if re.search(r"\{\{<\s*estudio\b", body):
        passes.append("Ficha interactiva de estudio científico presente: {{< estudio >}}")
    else:
        passes.append("Sin ficha {{< estudio >}} (permitido si el episodio se basa en fuentes directas en lista)")

    # 8. Verificación en .agents/episodes.yaml
    if manifest and "episodes" in manifest:
        ep_num_match = re.search(r"^0*([0-9]+)", path.name)
        ep_num = ep_num_match.group(1) if ep_num_match else None
        found_in_manifest = False
        for ep in manifest.get("episodes", []):
            if str(ep.get("number", "")).lstrip("0") == ep_num or ep.get("file", "").endswith(path.name):
                found_in_manifest = True
                status = ep.get("status", "desconocido")
                passes.append(f"Registrado en .agents/episodes.yaml (Estado: {status})")
                break
        if not found_in_manifest:
            errors.append(f"El episodio {path.name} NO está registrado en .agents/episodes.yaml")

    # Imprimir resultados
    for p in passes:
        print(f"  {GREEN}✓ [PASS]{RESET} {p}")
    for w in warnings:
        print(f"  {YELLOW}⚠ [WARN]{RESET} {w}")
    for e in errors:
        print(f"  {RED}✗ [FAIL]{RESET} {e}")

    print(f"\nResumen: {len(passes)} pasadas, {len(warnings)} advertencias, {len(errors)} errores críticos.")
    return len(errors) == 0

def main():
    manifest = load_manifest()
    target_files = sys.argv[1:]

    # Si no se pasan archivos, auditar todos los borradores del manifiesto
    if not target_files:
        if not manifest or "episodes" not in manifest:
            print(f"{RED}No se especificaron archivos y no se pudo cargar .agents/episodes.yaml{RESET}")
            sys.exit(1)
        print(f"{BOLD}Modo automático: auditando episodios marcados como 'status: draft'...{RESET}")
        target_files = []
        for ep in manifest["episodes"]:
            if ep.get("status") == "draft":
                target_files.append(ep.get("file"))
        if not target_files:
            print(f"{GREEN}No hay episodios marcados en borrador actualmente.{RESET}")
            sys.exit(0)

    all_passed = True
    for f in target_files:
        success = audit_episode(f, manifest=manifest)
        if not success:
            all_passed = False

    if all_passed:
        print(f"\n{BOLD}{GREEN}✓ Todos los episodios auditados cumplen con los estándares de Con-Manzanas-Publisher.{RESET}\n")
        sys.exit(0)
    else:
        print(f"\n{BOLD}{RED}✗ Se encontraron fallos críticos de cumplimiento. Por favor corrige los errores antes de publicar.{RESET}\n")
        sys.exit(1)

if __name__ == "__main__":
    main()
