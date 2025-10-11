#!/bin/bash
# Script para configurar Network Security Groups no Azure
# Execute este script no seu computador local (com Azure CLI instalado)

set -e

echo "=============================================="
echo "Configuração de NSG - Azure VMs"
echo "=============================================="
echo ""

# Cores
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Verificar se Azure CLI está instalado
if ! command -v az &> /dev/null; then
    echo -e "${RED}Azure CLI não está instalado!${NC}"
    echo "Instale em: https://docs.microsoft.com/cli/azure/install-azure-cli"
    exit 1
fi

# Verificar se está logado
if ! az account show &> /dev/null; then
    echo -e "${YELLOW}Você não está logado no Azure CLI${NC}"
    echo "Fazendo login..."
    az login
fi

echo -e "${GREEN}✓ Azure CLI configurado${NC}"
echo ""

# Solicitar informações
echo -e "${BLUE}=== Informações da VM Web ===${NC}"
read -p "Resource Group da VM Web: " RG_WEB
read -p "Nome do NSG da VM Web: " NSG_WEB
read -p "Nome da VM Web: " VM_WEB_NAME

echo ""
echo -e "${BLUE}=== Informações da VM Database ===${NC}"
read -p "Resource Group da VM Database: " RG_DB
read -p "Nome do NSG da VM Database: " NSG_DB

echo ""
echo -e "${YELLOW}Obtendo IP privado da VM Web...${NC}"

# Obter IP privado da VM Web
VM_WEB_PRIVATE_IP=$(az vm show -d \
    --resource-group "$RG_WEB" \
    --name "$VM_WEB_NAME" \
    --query privateIps -o tsv)

if [ -z "$VM_WEB_PRIVATE_IP" ]; then
    echo -e "${RED}Não foi possível obter o IP privado da VM Web${NC}"
    exit 1
fi

echo -e "${GREEN}IP privado da VM Web: $VM_WEB_PRIVATE_IP${NC}"
echo ""

# Confirmar
echo -e "${YELLOW}Este script irá:${NC}"
echo "1. Configurar NSG da VM Web para permitir:"
echo "   - SSH (porta 22)"
echo "   - HTTP (porta 80)"
echo "   - HTTPS (porta 443)"
echo ""
echo "2. Configurar NSG da VM Database para permitir:"
echo "   - PostgreSQL (porta 5432) apenas do IP $VM_WEB_PRIVATE_IP"
echo ""
read -p "Deseja continuar? (s/n): " CONFIRM

if [ "$CONFIRM" != "s" ] && [ "$CONFIRM" != "S" ]; then
    echo "Operação cancelada."
    exit 0
fi

echo ""
echo -e "${GREEN}Configurando NSGs...${NC}"
echo ""

# Configurar NSG da VM Web
echo -e "${BLUE}[1/4] Configurando NSG da VM Web - Porta SSH (22)...${NC}"
az network nsg rule create \
    --resource-group "$RG_WEB" \
    --nsg-name "$NSG_WEB" \
    --name AllowSSH \
    --priority 100 \
    --source-address-prefixes '*' \
    --source-port-ranges '*' \
    --destination-address-prefixes '*' \
    --destination-port-ranges 22 \
    --access Allow \
    --protocol Tcp \
    --description "Allow SSH from anywhere" \
    --output none 2>/dev/null || echo "  (Regra já existe ou erro)"

echo -e "${BLUE}[2/4] Configurando NSG da VM Web - Porta HTTP (80)...${NC}"
az network nsg rule create \
    --resource-group "$RG_WEB" \
    --nsg-name "$NSG_WEB" \
    --name AllowHTTP \
    --priority 110 \
    --source-address-prefixes '*' \
    --source-port-ranges '*' \
    --destination-address-prefixes '*' \
    --destination-port-ranges 80 \
    --access Allow \
    --protocol Tcp \
    --description "Allow HTTP from anywhere" \
    --output none 2>/dev/null || echo "  (Regra já existe ou erro)"

echo -e "${BLUE}[3/4] Configurando NSG da VM Web - Porta HTTPS (443)...${NC}"
az network nsg rule create \
    --resource-group "$RG_WEB" \
    --nsg-name "$NSG_WEB" \
    --name AllowHTTPS \
    --priority 120 \
    --source-address-prefixes '*' \
    --source-port-ranges '*' \
    --destination-address-prefixes '*' \
    --destination-port-ranges 443 \
    --access Allow \
    --protocol Tcp \
    --description "Allow HTTPS from anywhere" \
    --output none 2>/dev/null || echo "  (Regra já existe ou erro)"

# Configurar NSG da VM Database
echo -e "${BLUE}[4/4] Configurando NSG da VM Database - PostgreSQL (5432)...${NC}"
az network nsg rule create \
    --resource-group "$RG_DB" \
    --nsg-name "$NSG_DB" \
    --name AllowPostgreSQLFromWeb \
    --priority 100 \
    --source-address-prefixes "$VM_WEB_PRIVATE_IP" \
    --source-port-ranges '*' \
    --destination-address-prefixes '*' \
    --destination-port-ranges 5432 \
    --access Allow \
    --protocol Tcp \
    --description "Allow PostgreSQL from Web VM" \
    --output none 2>/dev/null || echo "  (Regra já existe ou erro)"

echo ""
echo -e "${GREEN}=============================================="
echo "Configuração de NSG concluída!"
echo "==============================================${NC}"
echo ""

# Mostrar regras criadas
echo -e "${YELLOW}Regras do NSG da VM Web:${NC}"
az network nsg rule list \
    --resource-group "$RG_WEB" \
    --nsg-name "$NSG_WEB" \
    --query "[?direction=='Inbound'].{Name:name, Priority:priority, Port:destinationPortRange, Access:access}" \
    --output table

echo ""
echo -e "${YELLOW}Regras do NSG da VM Database:${NC}"
az network nsg rule list \
    --resource-group "$RG_DB" \
    --nsg-name "$NSG_DB" \
    --query "[?direction=='Inbound'].{Name:name, Priority:priority, Port:destinationPortRange, Access:access}" \
    --output table

echo ""
echo -e "${GREEN}✓ NSGs configurados com sucesso!${NC}"
echo ""
echo -e "${YELLOW}Próximos passos:${NC}"
echo "1. Configurar a VM Database (executar setup_database.sh)"
echo "2. Configurar a VM Web (executar setup_web.sh)"
echo "3. Testar conectividade (executar test_connectivity.sh na VM Web)"
echo ""
