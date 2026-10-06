# Regla de Seguridad: Hardening y Principio de Menor Privilegio (Least Privilege)

## 1. Principio Fundamental
Todos los recursos de infraestructura en la nube, flujos de almacenamiento, endpoints, archivos estáticos y URLs web en este repositorio **DEBEN** adherirse de manera estricta al **Principio de Menor Privilegio (Least Privilege)** y a directrices de endurecimiento (*security hardening*).

---

## 2. Recursos de Almacenamiento e Infraestructura Nube (AWS S3, IAM, CDN)

1. **Permisos IAM Estrictamente Delimitados (Zero Excess Privileges)**:
   - Toda identidad programática (como el perfil `podcaster`) solo debe contar con los permisos mínimos indispensables para sus tareas habituales (`s3:PutObject`, `s3:GetObject` en prefijos específicos).
   - **Prohibición de permisos destructivos**: Los roles operativos cotidianos **NUNCA** deben tener privilegios de eliminación (`s3:DeleteObject`, `s3:DeleteBucket`) ni de alteración de configuraciones (`s3:PutBucketPolicy`, `s3:PutBucketCors`).
   - Los recursos en las políticas IAM deben delimitarse a nivel de prefijo exacto (ejemplo: `arn:aws:s3:::<bucket>/episodes/*`), nunca conceder comodines amplios a la raíz ni a otros buckets de la cuenta.

2. **Acceso Público Acotado y Restrictivo**:
   - Únicamente los activos destinados al consumo público de la audiencia (ej: `/episodes/*` para streaming) pueden tener `s3:GetObject` público.
   - Todo lo demás (listado del bucket `s3:ListBucket`, directorios de trabajo, respaldos, metadatos internos) debe estar **bloqueado para acceso anónimo** (`403 Forbidden`).
   - Mantener siempre activos los controles de bloqueo de ACLs públicas (`BlockPublicAcls=true`, `IgnorePublicAcls=true`).

3. **Cifrado Obligatorio en Tránsito (Enforce TLS / HTTPS)**:
   - Todo bucket con objetos públicos debe incluir una regla de política con denegación explícita (`Effect: Deny`) cuando la petición no use HTTPS:
     ```json
     {
       "Sid": "EnforceTLSRequestsOnly",
       "Effect": "Deny",
       "Principal": "*",
       "Action": "s3:*",
       "Resource": ["arn:aws:s3:::<bucket>", "arn:aws:s3:::<bucket>/*"],
       "Condition": { "Bool": { "aws:SecureTransport": "false" } }
     }
     ```
   - Cero tolerancia al tráfico en texto claro (HTTP sin cifrar).

4. **Resiliencia de Datos y Versionado (S3 Object Versioning)**:
   - Los buckets de producción que alojen entregas multimedia o archivos de episodios deben tener **S3 Versioning activado**.
   - Esto previene pérdidas irreversibles en caso de sobreescrituras involuntarias o incidentes operativos.

5. **CORS con Menor Privilegio**:
   - Solo se permiten métodos de lectura (`GET`, `HEAD`).
   - Métodos con efectos secundarios (`POST`, `PUT`, `DELETE`) están estrictamente deshabilitados en CORS para clientes web.

---

## 3. URLs Web, Enlaces y Frontend (Hugo, Feeds, Plantillas)

1. **HTTPS Obligatorio en Todas las URLs**:
   - **Toda** URL interna o externa en el sitio (`https://conmanzanas.lat`), feeds RSS (`podcast.xml`), sitemaps, shortcodes, esquemas estructurados y referencias de medios **DEBE** utilizar exclusivamente `https://`.
   - Queda terminantemente prohibido incluir URLs en texto claro `http://` (salvo declaraciones de esquemas XML / namespaces como `xmlns`, donde sea estándar técnico inmutable).

2. **Seguridad en Hipervínculos Externos**:
   - Todo enlace a sitios de terceros (`target="_blank"`) debe incorporar los atributos de seguridad `rel="noopener noreferrer"` para mitigar ataques de navegación reversa (*reverse tabnabbing*).

3. **Validación Previa a Producción**:
   - Antes de cerrar cualquier tarea que involucre infraestructura, credenciales, plantillas de salida o URLs de distribución, se debe validar:
     - Que los endpoints respondan de manera segura bajo HTTPS con las cabeceras requeridas.
     - Que ningún archivo con credenciales secretas, tokens ni claves de acceso se agregue al control de versiones (`.gitignore`).
