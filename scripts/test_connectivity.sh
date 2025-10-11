#!/bin/bash
# Script para testar conectividade entre VM Web e VM Database
# Execute na VM Web: ./test_connectivity.sh

echo "=============================================="
echo "Teste de Conectividade - VM Web → VM Database"
echo "=============================================="
echo ""

# Cores
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Solicitar informações
read -p "IP Privado da VM Database: " DB_HOST
read -p "Porta do PostgreSQL [5432]: " DB_PORT
DB_PORT=${DB_PORT:-5432}
read -p "Nome do banco [portaldb]: " DB_NAME
DB_NAME=${DB_NAME:-portaldb}
read -p "Usuário do banco [django_user]: " DB_USER
DB_USER=${DB_USER:-django_user}

echo ""
echo "Executando testes..."
echo ""

# Teste 1: Ping
echo -n "[1/5] Teste de ping... "
if ping -c 3 -W 2 $DB_HOST > /dev/null 2>&1; then
    echo -e "${GREEN}✓ OK${NC}"
    PING_OK=true
else
    echo -e "${RED}✗ FALHOU${NC}"
    echo "      A VM Database não responde ao ping"
    PING_OK=false
fi

# Teste 2: Porta TCP
echo -n "[2/5] Teste de porta $DB_PORT... "
if timeout 5 bash -c "cat < /dev/null > /dev/tcp/$DB_HOST/$DB_PORT" 2>/dev/null; then
    echo -e "${GREEN}✓ OK${NC}"
    PORT_OK=true
else
    echo -e "${RED}✗ FALHOU${NC}"
    echo "      A porta $DB_PORT não está acessível"
    echo "      Verifique o NSG e firewall (ufw) da VM Database"
    PORT_OK=false
fi

# Teste 3: PostgreSQL client
echo -n "[3/5] Verificando cliente PostgreSQL... "
if command -v psql &> /dev/null; then
    echo -e "${GREEN}✓ OK${NC}"
    PSQL_OK=true
else
    echo -e "${YELLOW}✗ NÃO INSTALADO${NC}"
    echo "      Instalando postgresql-client..."
    sudo apt update > /dev/null 2>&1
    sudo apt install -y postgresql-client > /dev/null 2>&1
    if command -v psql &> /dev/null; then
        echo -e "      ${GREEN}✓ Instalado com sucesso${NC}"
        PSQL_OK=true
    else
        echo -e "      ${RED}✗ Falha na instalação${NC}"
        PSQL_OK=false
    fi
fi

# Teste 4: Conexão PostgreSQL
if [ "$PSQL_OK" = true ] && [ "$PORT_OK" = true ]; then
    echo -n "[4/5] Teste de conexão PostgreSQL... "
    read -sp "Senha do banco: " DB_PASSWORD
    echo ""
    
    export PGPASSWORD="$DB_PASSWORD"
    
    if psql -h $DB_HOST -p $DB_PORT -U $DB_USER -d $DB_NAME -c "SELECT 1;" > /dev/null 2>&1; then
        echo -e "${GREEN}✓ OK${NC}"
        echo "      Conexão com banco de dados estabelecida com sucesso!"
        DB_CONN_OK=true
    else
        echo -e "${RED}✗ FALHOU${NC}"
        echo "      Não foi possível conectar ao banco de dados"
        echo "      Verifique:"
        echo "      - Credenciais (usuário/senha)"
        echo "      - Configuração do pg_hba.conf"
        echo "      - Se o banco de dados existe"
        DB_CONN_OK=false
    fi
    
    unset PGPASSWORD
else
    echo "[4/5] Teste de conexão PostgreSQL... ${YELLOW}PULADO${NC}"
    DB_CONN_OK=false
fi

# Teste 5: String de conexão Django
echo -n "[5/5] Gerando string de conexão... "
if [ "$DB_CONN_OK" = true ]; then
    CONNECTION_STRING="postgres://$DB_USER:SUA_SENHA@$DB_HOST:$DB_PORT/$DB_NAME"
    echo -e "${GREEN}✓ OK${NC}"
    echo ""
    echo -e "${GREEN}================================${NC}"
    echo -e "${GREEN}String de conexão para .env:${NC}"
    echo -e "${GREEN}================================${NC}"
    echo ""
    echo "DATABASE_URL=$CONNECTION_STRING"
    echo ""
else
    echo -e "${YELLOW}PULADO${NC}"
fi

# Resumo
echo ""
echo "=============================================="
echo "Resumo dos Testes"
echo "=============================================="
echo ""

if [ "$PING_OK" = true ]; then
    echo -e "${GREEN}✓${NC} Ping: OK"
else
    echo -e "${RED}✗${NC} Ping: FALHOU"
fi

if [ "$PORT_OK" = true ]; then
    echo -e "${GREEN}✓${NC} Porta $DB_PORT: Acessível"
else
    echo -e "${RED}✗${NC} Porta $DB_PORT: Bloqueada"
fi

if [ "$PSQL_OK" = true ]; then
    echo -e "${GREEN}✓${NC} Cliente PostgreSQL: Instalado"
else
    echo -e "${RED}✗${NC} Cliente PostgreSQL: Não disponível"
fi

if [ "$DB_CONN_OK" = true ]; then
    echo -e "${GREEN}✓${NC} Conexão com Banco: Estabelecida"
else
    echo -e "${RED}✗${NC} Conexão com Banco: Falhou"
fi

echo ""

# Sugestões de correção
if [ "$PING_OK" = false ] || [ "$PORT_OK" = false ]; then
    echo -e "${YELLOW}Sugestões de correção:${NC}"
    echo ""
    echo "1. Verificar se as VNets estão conectadas (VNet Peering)"
    echo ""
    echo "2. Verificar NSG da VM Database:"
    echo "   - Deve permitir porta 5432 da subnet da VM Web"
    echo "   - No Azure Portal: Network Security Groups → Inbound rules"
    echo ""
    echo "3. Verificar firewall na VM Database:"
    echo "   sudo ufw status"
    echo "   sudo ufw allow from $(/sbin/ip -o -4 addr list eth0 | awk '{print $4}') to any port 5432"
    echo ""
fi

if [ "$DB_CONN_OK" = false ] && [ "$PORT_OK" = true ]; then
    echo -e "${YELLOW}Sugestões de correção para conexão:${NC}"
    echo ""
    echo "1. Verificar credenciais do banco de dados"
    echo ""
    echo "2. Verificar pg_hba.conf na VM Database:"
    echo "   sudo cat /etc/postgresql/14/main/pg_hba.conf"
    echo "   Deve conter linha permitindo sua subnet"
    echo ""
    echo "3. Verificar se PostgreSQL está escutando em todas interfaces:"
    echo "   sudo grep listen_addresses /etc/postgresql/14/main/postgresql.conf"
    echo "   Deve ser: listen_addresses = '*'"
    echo ""
    echo "4. Reiniciar PostgreSQL na VM Database:"
    echo "   sudo systemctl restart postgresql"
    echo ""
fi

echo ""
echo "Para mais informações, consulte:"
echo "  /home/runner/work/projeto_do_fim/projeto_do_fim/AZURE_VM_SETUP_COMPLETO.md"
echo ""
