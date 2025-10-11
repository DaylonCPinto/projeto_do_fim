#!/bin/bash
# Script de configuração automática do PostgreSQL na VM Database
# Ubuntu 22.04 - Azure VM
# Execute como root: sudo ./setup_database.sh

set -e  # Parar em caso de erro

echo "=============================================="
echo "Configuração PostgreSQL - VM Database"
echo "=============================================="
echo ""

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Verificar se está rodando como root
if [ "$EUID" -ne 0 ]; then 
   echo -e "${RED}Por favor, execute como root: sudo ./setup_database.sh${NC}"
   exit 1
fi

# Solicitar informações necessárias
echo -e "${YELLOW}Este script irá instalar e configurar PostgreSQL 14${NC}"
echo ""
read -p "Nome do banco de dados [portaldb]: " DB_NAME
DB_NAME=${DB_NAME:-portaldb}

read -p "Nome do usuário do banco [django_user]: " DB_USER
DB_USER=${DB_USER:-django_user}

read -sp "Senha do usuário (IMPORTANTE - anote!): " DB_PASSWORD
echo ""
if [ -z "$DB_PASSWORD" ]; then
    echo -e "${RED}Senha não pode ser vazia!${NC}"
    exit 1
fi

read -p "Subnet da VM Web (ex: 10.0.1.0/24): " WEB_SUBNET
if [ -z "$WEB_SUBNET" ]; then
    echo -e "${RED}Subnet é obrigatória!${NC}"
    exit 1
fi

echo ""
echo -e "${GREEN}Iniciando configuração...${NC}"
echo ""

# 1. Atualizar sistema
echo "[1/8] Atualizando sistema..."
apt update && apt upgrade -y

# 2. Instalar PostgreSQL 14
echo "[2/8] Instalando PostgreSQL 14..."
apt install -y postgresql-14 postgresql-contrib-14 postgresql-client-14

# 3. Configurar PostgreSQL para aceitar conexões remotas
echo "[3/8] Configurando PostgreSQL para conexões remotas..."
sed -i "s/#listen_addresses = 'localhost'/listen_addresses = '*'/" /etc/postgresql/14/main/postgresql.conf

# Configurações adicionais de performance
cat >> /etc/postgresql/14/main/postgresql.conf << EOF

# Configurações de performance
max_connections = 100
shared_buffers = 256MB
effective_cache_size = 1GB
maintenance_work_mem = 64MB
checkpoint_completion_target = 0.9
wal_buffers = 16MB
default_statistics_target = 100
random_page_cost = 1.1
effective_io_concurrency = 200
work_mem = 2621kB
min_wal_size = 1GB
max_wal_size = 4GB
EOF

# 4. Configurar autenticação (pg_hba.conf)
echo "[4/8] Configurando autenticação..."
cat >> /etc/postgresql/14/main/pg_hba.conf << EOF

# Permitir conexões da VM Web
host    $DB_NAME    $DB_USER    $WEB_SUBNET    scram-sha-256
host    all         all         $WEB_SUBNET    scram-sha-256
EOF

# 5. Reiniciar PostgreSQL
echo "[5/8] Reiniciando PostgreSQL..."
systemctl restart postgresql
systemctl enable postgresql

# 6. Criar banco de dados e usuário
echo "[6/8] Criando banco de dados e usuário..."
sudo -u postgres psql << EOF
CREATE DATABASE $DB_NAME;
CREATE USER $DB_USER WITH PASSWORD '$DB_PASSWORD';
ALTER ROLE $DB_USER SET client_encoding TO 'utf8';
ALTER ROLE $DB_USER SET default_transaction_isolation TO 'read committed';
ALTER ROLE $DB_USER SET timezone TO 'America/Sao_Paulo';
GRANT ALL PRIVILEGES ON DATABASE $DB_NAME TO $DB_USER;
\c $DB_NAME
GRANT ALL ON SCHEMA public TO $DB_USER;
\q
EOF

# 7. Configurar firewall (ufw)
echo "[7/8] Configurando firewall..."
ufw allow 5432/tcp comment 'PostgreSQL'
ufw allow OpenSSH
ufw --force enable

# 8. Verificar instalação
echo "[8/8] Verificando instalação..."
if systemctl is-active --quiet postgresql; then
    echo -e "${GREEN}✓ PostgreSQL está rodando${NC}"
else
    echo -e "${RED}✗ PostgreSQL não está rodando${NC}"
    exit 1
fi

if sudo -u postgres psql -lqt | cut -d \| -f 1 | grep -qw $DB_NAME; then
    echo -e "${GREEN}✓ Banco de dados '$DB_NAME' criado${NC}"
else
    echo -e "${RED}✗ Banco de dados não foi criado${NC}"
    exit 1
fi

# Salvar informações em arquivo
CREDS_FILE="/root/db_credentials.txt"
cat > $CREDS_FILE << EOF
===========================================
Credenciais do PostgreSQL
===========================================
Banco de dados: $DB_NAME
Usuário: $DB_USER
Senha: $DB_PASSWORD
Host: $(hostname -I | awk '{print $1}')
Porta: 5432
Subnet permitida: $WEB_SUBNET

String de conexão Django:
DATABASE_URL=postgres://$DB_USER:$DB_PASSWORD@$(hostname -I | awk '{print $1}'):5432/$DB_NAME

String de conexão psql:
psql -h $(hostname -I | awk '{print $1}') -U $DB_USER -d $DB_NAME

===========================================
Data de criação: $(date)
===========================================
EOF

chmod 600 $CREDS_FILE

echo ""
echo -e "${GREEN}=============================================="
echo "Configuração concluída com sucesso!"
echo "==============================================${NC}"
echo ""
echo -e "Credenciais salvas em: ${YELLOW}$CREDS_FILE${NC}"
echo ""
echo "Informações importantes:"
echo "  - Banco de dados: $DB_NAME"
echo "  - Usuário: $DB_USER"
echo "  - Host: $(hostname -I | awk '{print $1}')"
echo "  - Porta: 5432"
echo ""
echo -e "${YELLOW}IMPORTANTE: Anote essas credenciais! Você precisará delas na VM Web.${NC}"
echo ""
echo "Para testar a conexão localmente:"
echo "  psql -U $DB_USER -d $DB_NAME -h localhost"
echo ""
echo "Status do PostgreSQL:"
systemctl status postgresql --no-pager -l
echo ""
