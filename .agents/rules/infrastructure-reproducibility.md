# Regla de Infraestructura y Operaciones: Reproducibilidad Obligatoria por Scripts

## 1. Principio Rector: Infraestructura como Código y Operaciones Reproducibles
Toda configuración, recurso en la nube, política de seguridad, bucket, usuario IAM, regla CORS o servicio externo en este repositorio **DEBE ser 100% reproducible mediante scripts automatizados y versionados**.

---

## 2. Directrices Estrictas de Modificación

1. **Cero Cambios Manuales Huérfanos**:
   - Queda estrictamente prohibido aplicar configuraciones mediante clics en la consola web de AWS o mediante comandos CLI ad-hoc ejecutados de forma aislada sin quedar plasmados en el código.
   - Si se requiere un cambio en la nube, este debe codificarse primero en un script ejecutable dentro de `tools/` y en sus plantillas JSON/YAML correspondientes.

2. **Idempotencia Obligatoria**:
   - Todo script de aprovisionamiento o configuración (como `setup_aws_resources.sh` o `upload_audio.py`) debe ser **idempotente**:
     - Debe poder ejecutarse múltiples veces de manera segura.
     - Debe verificar si el recurso ya existe antes de crearlo.
     - Debe actualizar las configuraciones existentes sin interrumpir la operación ni duplicar recursos.

3. **Parametrización y Flexibilidad**:
   - Los scripts no deben hardcodear credenciales fijas.
   - Deben aceptar parámetros de línea de comandos (ej: `--profile <nombre>`, `--bucket <nombre>`, `--region <region>`).
   - Deben incluir opciones de ayuda (`--help`) y mensajes de salida claros con códigos de retorno (`exit 0` en éxito, `exit 1` en error).

4. **Sincronización de Artefactos**:
   - Cualquier modificación en una política de seguridad, política de bucket o configuración CORS debe reflejarse en dos lugares obligatorios:
     1. El archivo JSON canónico de plantilla en `tools/` (ej: `bucket-policy.json`, `iam-policy-podcaster.json`, `cors-policy.json`).
     2. El script de aprovisionamiento automatizado que lo aplica (`setup_aws_resources.sh`).

5. **Documentación de Ejecución**:
   - Cada herramienta en `tools/` debe contar con un archivo `README.md` que detalle:
     - Qué recursos crea o modifica.
     - Requisitos previos.
     - Comando exacto para ejecutarlo y reproducir el estado deseado en cualquier momento o cuenta.
