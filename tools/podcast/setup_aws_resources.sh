#!/usr/bin/env bash
#
# setup_aws_resources.sh
# Valida y crea los recursos necesarios en AWS para el podcast 'Dímelo con Manzanas':
# - Bucket S3 ('conmanzanas') con permisos públicos para 'episodes/*' y CORS.
# - Usuario IAM ('podcaster') con política de privilegios mínimos.
# - Genera y configura automáticamente el perfil local 'podcaster'.
#
# Uso:
#   ./tools/podcast/setup_aws_resources.sh --profile <admin_profile> [--bucket conmanzanas] [--region us-east-1]
#

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/../.." && pwd)"

# Colores para salida de terminal
GREEN="\033[92m"
YELLOW="\033[93m"
RED="\033[91m"
BLUE="\033[94m"
BOLD="\033[1m"
RESET="\033[0m"

# Valores por defecto
ADMIN_PROFILE=""
BUCKET_NAME="conmanzanas"
AWS_REGION="us-east-1"
PODCASTER_USER="podcaster"
POLICY_NAME="DimeloConManzanasPodcasterPolicy"

usage() {
    local exit_code="${1:-1}"
    echo -e "${BOLD}Uso:${RESET} $0 --profile <admin_profile> [opciones]"
    echo ""
    echo "Opciones requeridas:"
    echo "  --profile <nombre>    Nombre del perfil de AWS CLI con permisos de administración (ej: deployer, default, root)"
    echo ""
    echo "Opciones adicionales:"
    echo "  --bucket <nombre>     Nombre del bucket S3 (por defecto: conmanzanas)"
    echo "  --region <region>     Región de AWS (por defecto: us-east-1)"
    echo "  -h, --help            Mostrar esta ayuda"
    exit "$exit_code"
}

# Parsear argumentos
while [[ $# -gt 0 ]]; do
    case "$1" in
        --profile)
            ADMIN_PROFILE="$2"
            shift 2
            ;;
        --bucket)
            BUCKET_NAME="$2"
            shift 2
            ;;
        --region)
            AWS_REGION="$2"
            shift 2
            ;;
        -h|--help)
            usage 0
            ;;
        *)
            echo -e "${RED}Opción no reconocida:${RESET} $1"
            usage
            ;;
    esac
done

if [[ -z "$ADMIN_PROFILE" ]]; then
    echo -e "${RED}Error: Debes especificar el perfil de administrador con --profile <nombre>${RESET}"
    echo "Ejemplo: $0 --profile deployer"
    exit 1
fi

echo -e "\n${BOLD}${BLUE}======================================================${RESET}"
echo -e "${BOLD}Aprovisionamiento de Recursos AWS: Podcast 'Dímelo con Manzanas'${RESET}"
echo -e "${BLUE}======================================================${RESET}"
echo -e "Perfil Administrador: ${BOLD}${ADMIN_PROFILE}${RESET}"
echo -e "Bucket S3:            ${BOLD}${BUCKET_NAME}${RESET}"
echo -e "Región AWS:           ${BOLD}${AWS_REGION}${RESET}"
echo -e "Usuario IAM:          ${BOLD}${PODCASTER_USER}${RESET}\n"

# 1. Verificar identidad del administrador
echo -e "🔍 Verificando credenciales del perfil '${ADMIN_PROFILE}'..."
ACCOUNT_ID=$(aws sts get-caller-identity --profile "$ADMIN_PROFILE" --query "Account" --output text 2>/dev/null || true)
if [[ -z "$ACCOUNT_ID" ]]; then
    echo -e "${RED}✗ Error: No se pudo autenticar con el perfil '${ADMIN_PROFILE}'. Revisa tus credenciales en ~/.aws/credentials.${RESET}"
    exit 1
fi
echo -e "${GREEN}✓ Autenticado como cuenta AWS ID: ${ACCOUNT_ID}${RESET}\n"

# 2. Validar o crear el Bucket S3
echo -e "📦 ${BOLD}[1/4] Verificando Bucket S3: '${BUCKET_NAME}'...${RESET}"
if aws s3api head-bucket --bucket "$BUCKET_NAME" --profile "$ADMIN_PROFILE" 2>/dev/null; then
    echo -e "${GREEN}✓ El bucket '${BUCKET_NAME}' ya existe y tienes acceso.${RESET}"
else
    echo -e "⚙️  Creando bucket '${BUCKET_NAME}' en región '${AWS_REGION}'..."
    if [[ "$AWS_REGION" == "us-east-1" ]]; then
        aws s3api create-bucket \
            --bucket "$BUCKET_NAME" \
            --profile "$ADMIN_PROFILE"
    else
        aws s3api create-bucket \
            --bucket "$BUCKET_NAME" \
            --region "$AWS_REGION" \
            --create-bucket-configuration LocationConstraint="$AWS_REGION" \
            --profile "$ADMIN_PROFILE"
    fi
    echo -e "${GREEN}✓ Bucket '${BUCKET_NAME}' creado exitosamente.${RESET}"
fi

# Configurar Block Public Access
echo -e "⚙️  Configurando Block Public Access para permitir lectura de podcast..."
aws s3api put-public-access-block \
    --bucket "$BUCKET_NAME" \
    --public-access-block-configuration "BlockPublicAcls=true,IgnorePublicAcls=true,BlockPublicPolicy=false,RestrictPublicBuckets=false" \
    --profile "$ADMIN_PROFILE"
echo -e "${GREEN}✓ Block Public Access configurado.${RESET}"

# Habilitar Versioning
echo -e "⚙️  Habilitando S3 Versioning para resiliencia y protección contra eliminación accidental..."
aws s3api put-bucket-versioning \
    --bucket "$BUCKET_NAME" \
    --versioning-configuration Status=Enabled \
    --profile "$ADMIN_PROFILE"
echo -e "${GREEN}✓ S3 Versioning activado.${RESET}"

# Aplicar Bucket Policy
echo -e "⚙️  Aplicando política de lectura pública para 'episodes/*' con TLS/HTTPS forzado..."
BUCKET_POLICY_FILE="${SCRIPT_DIR}/bucket-policy.json"
# Asegurar que el archivo de política tenga el nombre del bucket correcto
sed -i "s|arn:aws:s3:::.*\/episodes\/\*|arn:aws:s3:::${BUCKET_NAME}/episodes/*|g" "$BUCKET_POLICY_FILE"
aws s3api put-bucket-policy \
    --bucket "$BUCKET_NAME" \
    --policy "file://${BUCKET_POLICY_FILE}" \
    --profile "$ADMIN_PROFILE"
echo -e "${GREEN}✓ Política de bucket aplicada.${RESET}"

# Aplicar CORS
echo -e "⚙️  Aplicando configuración CORS para streaming de audio..."
CORS_POLICY_FILE="${SCRIPT_DIR}/cors-policy.json"
aws s3api put-bucket-cors \
    --bucket "$BUCKET_NAME" \
    --cors-configuration "file://${CORS_POLICY_FILE}" \
    --profile "$ADMIN_PROFILE"
echo -e "${GREEN}✓ Configuración CORS aplicada exitosamente.${RESET}\n"

# 3. Validar o crear Usuario IAM 'podcaster'
echo -e "👤 ${BOLD}[2/4] Verificando Usuario IAM: '${PODCASTER_USER}'...${RESET}"
if aws iam get-user --user-name "$PODCASTER_USER" --profile "$ADMIN_PROFILE" 2>/dev/null; then
    echo -e "${GREEN}✓ El usuario IAM '${PODCASTER_USER}' ya existe.${RESET}"
else
    echo -e "⚙️  Creando usuario IAM '${PODCASTER_USER}'..."
    aws iam create-user --user-name "$PODCASTER_USER" --profile "$ADMIN_PROFILE"
    echo -e "${GREEN}✓ Usuario '${PODCASTER_USER}' creado.${RESET}"
fi

# 4. Validar o crear Política IAM para 'podcaster'
echo -e "\n🛡️  ${BOLD}[3/4] Verificando Política IAM: '${POLICY_NAME}'...${RESET}"
POLICY_ARN="arn:aws:iam::${ACCOUNT_ID}:policy/${POLICY_NAME}"
IAM_POLICY_FILE="${SCRIPT_DIR}/iam-policy-podcaster.json"

# Asegurar que el archivo de política tenga el nombre del bucket correcto
sed -i "s|arn:aws:s3:::[^\/\"]*\"|arn:aws:s3:::${BUCKET_NAME}\"|g" "$IAM_POLICY_FILE"
sed -i "s|arn:aws:s3:::[^\/\"]*\/episodes\/\*|arn:aws:s3:::${BUCKET_NAME}/episodes/*|g" "$IAM_POLICY_FILE"

if aws iam get-policy --policy-arn "$POLICY_ARN" --profile "$ADMIN_PROFILE" 2>/dev/null; then
    echo -e "${GREEN}✓ La política IAM ya existe (${POLICY_ARN}).${RESET}"
else
    echo -e "⚙️  Creando política IAM '${POLICY_NAME}'..."
    aws iam create-policy \
        --policy-name "$POLICY_NAME" \
        --policy-document "file://${IAM_POLICY_FILE}" \
        --description "Permisos de gestion de audios para el podcast Dimelo con Manzanas" \
        --profile "$ADMIN_PROFILE"
    echo -e "${GREEN}✓ Política IAM creada.${RESET}"
fi

# Adjuntar política al usuario
echo -e "⚙️  Adjuntando política al usuario '${PODCASTER_USER}'..."
aws iam attach-user-policy \
    --user-name "$PODCASTER_USER" \
    --policy-arn "$POLICY_ARN" \
    --profile "$ADMIN_PROFILE"
echo -e "${GREEN}✓ Política adjuntada al usuario.${RESET}\n"

# 5. Gestionar Credenciales y Perfil Local 'podcaster'
echo -e "🔑 ${BOLD}[4/4] Verificando credenciales locales para perfil 'podcaster'...${RESET}"

EXISTING_KEYS=$(aws iam list-access-keys --user-name "$PODCASTER_USER" --profile "$ADMIN_PROFILE" --query "AccessKeyMetadata[].AccessKeyId" --output text)

if [[ -n "$EXISTING_KEYS" ]]; then
    echo -e "${YELLOW}ℹ️  El usuario '${PODCASTER_USER}' ya cuenta con Access Keys activas: ${EXISTING_KEYS}${RESET}"
    echo -e "Si ya configuraste el perfil local en ~/.aws/credentials, está listo para usarse."
else
    echo -e "⚙️  Generando nuevas Access Keys para '${PODCASTER_USER}'..."
    KEY_JSON=$(aws iam create-access-key --user-name "$PODCASTER_USER" --profile "$ADMIN_PROFILE")
    NEW_KEY_ID=$(echo "$KEY_JSON" | grep -o '"AccessKeyId": "[^"]*' | cut -d'"' -f4)
    NEW_SECRET=$(echo "$KEY_JSON" | grep -o '"SecretAccessKey": "[^"]*' | cut -d'"' -f4)

    echo -e "⚙️  Configurando automáticamente el perfil local 'podcaster' en AWS CLI..."
    aws configure set aws_access_key_id "$NEW_KEY_ID" --profile "$PODCASTER_USER"
    aws configure set aws_secret_access_key "$NEW_SECRET" --profile "$PODCASTER_USER"
    aws configure set region "$AWS_REGION" --profile "$PODCASTER_USER"
    aws configure set output "json" --profile "$PODCASTER_USER"
    echo -e "${GREEN}✓ Perfil local 'podcaster' configurado en ~/.aws/credentials.${RESET}"
fi

# 6. Prueba de verificación con el perfil 'podcaster'
echo -e "\n🧪 ${BOLD}Verificación final con el perfil '${PODCASTER_USER}':${RESET}"
if aws s3 ls "s3://${BUCKET_NAME}" --profile "$PODCASTER_USER" >/dev/null 2>&1; then
    echo -e "${GREEN}✓ ¡Éxito! El perfil '${PODCASTER_USER}' puede listar el bucket s3://${BUCKET_NAME}.${RESET}"
else
    echo -e "${YELLOW}⚠ Nota: El perfil '${PODCASTER_USER}' puede tardar unos segundos en propagar los permisos IAM en AWS.${RESET}"
fi

echo -e "\n${BOLD}${GREEN}======================================================${RESET}"
echo -e "${BOLD}${GREEN}¡Aprovisionamiento completado con éxito!${RESET}"
echo -e "${BOLD}${GREEN}======================================================${RESET}"
echo -e "Ahora puedes subir episodios usando simplemente:"
echo -e "  ${BOLD}python3 tools/podcast/upload_audio.py --episode 0003 --file /ruta/al/audio.mp3${RESET}\n"
