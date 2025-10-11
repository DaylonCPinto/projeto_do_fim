# Guia de Deploy em VMs Isoladas no Azure

Este documento descreve como fazer o deploy desta aplicação Django/Wagtail em máquinas virtuais isoladas no Azure com PostgreSQL.

## 🆕 NOVOS GUIAS DISPONÍVEIS

**Se você já tem 2 VMs prontas (Web + Database)**, use os novos guias simplificados:

- 📘 **[GUIA_RAPIDO_AZURE.md](GUIA_RAPIDO_AZURE.md)** - Guia rápido e objetivo
- 📗 **[AZURE_VM_SETUP_COMPLETO.md](AZURE_VM_SETUP_COMPLETO.md)** - Guia completo passo a passo
- 🔧 **[TROUBLESHOOTING_NGINX_GUNICORN.md](TROUBLESHOOTING_NGINX_GUNICORN.md)** - Soluções para problemas comuns
- 🤖 **[scripts/](scripts/)** - Scripts de automação para facilitar o deploy

**Este guia abaixo é para criar VMs do zero usando Azure CLI.**

---

## 📋 Visão Geral da Arquitetura

Esta configuração cria:
- 1 ou mais VMs Linux para a aplicação
- 1 VM PostgreSQL ou Azure Database for PostgreSQL
- Load Balancer (opcional, para múltiplas VMs)
- Virtual Network (VNet) com subnets isoladas
- Network Security Groups (NSG) para firewall

## 🔧 Pré-requisitos

1. **Conta no Azure** com permissões para criar recursos
2. **Azure CLI instalado** localmente
3. **Conhecimento básico** de Linux e redes
4. **SSH Key** para acesso às VMs

### Instalar Azure CLI

```bash
# Linux/MacOS
curl -sL https://aka.ms/InstallAzureCLIDeb | sudo bash

# Windows (PowerShell)
Invoke-WebRequest -Uri https://aka.ms/installazurecliwindows -OutFile .\AzureCLI.msi
Start-Process msiexec.exe -Wait -ArgumentList '/I AzureCLI.msi /quiet'
```

## 🚀 Passo 1: Configuração Inicial

### 1.1 Login no Azure

```bash
# Login interativo
az login

# Listar assinaturas disponíveis
az account list --output table

# Selecionar assinatura (se tiver múltiplas)
az account set --subscription "NOME_OU_ID_DA_ASSINATURA"
```

### 1.2 Definir Variáveis de Ambiente

```bash
# Configurações do projeto
export RESOURCE_GROUP="projeto-portal-rg"
export LOCATION="brazilsouth"  # ou eastus
export PROJECT_NAME="portal-analise"

# Configurações de rede
export VNET_NAME="${PROJECT_NAME}-vnet"
export SUBNET_APP_NAME="${PROJECT_NAME}-subnet-app"
export SUBNET_DB_NAME="${PROJECT_NAME}-subnet-db"
export NSG_NAME="${PROJECT_NAME}-nsg"

# Configurações da VM de aplicação
export VM_NAME="${PROJECT_NAME}-vm"
export VM_SIZE="Standard_B2s"  # 2 vCPUs, 4GB RAM
export VM_IMAGE="Canonical:0001-com-ubuntu-server-jammy:22_04-lts-gen2:latest"

# Configurações do PostgreSQL
export DB_SERVER_NAME="${PROJECT_NAME}-pgserver"
export DB_NAME="portaldb"
export DB_ADMIN_USER="pgadmin"
export DB_ADMIN_PASSWORD="SuaSenhaForte123!"  # MUDAR!
export DB_SKU="GP_Gen5_2"  # General Purpose, 2 vCores
```

## 🌐 Passo 2: Criar Infraestrutura de Rede

### 2.1 Criar Resource Group

```bash
az group create \
  --name $RESOURCE_GROUP \
  --location $LOCATION
```

### 2.2 Criar Virtual Network e Subnets

```bash
# Criar VNet
az network vnet create \
  --resource-group $RESOURCE_GROUP \
  --name $VNET_NAME \
  --address-prefix 10.0.0.0/16 \
  --subnet-name $SUBNET_APP_NAME \
  --subnet-prefix 10.0.1.0/24

# Criar subnet para banco de dados
az network vnet subnet create \
  --resource-group $RESOURCE_GROUP \
  --vnet-name $VNET_NAME \
  --name $SUBNET_DB_NAME \
  --address-prefix 10.0.2.0/24
```

### 2.3 Criar Network Security Group

```bash
# Criar NSG
az network nsg create \
  --resource-group $RESOURCE_GROUP \
  --name $NSG_NAME

# Permitir SSH (porta 22)
az network nsg rule create \
  --resource-group $RESOURCE_GROUP \
  --nsg-name $NSG_NAME \
  --name AllowSSH \
  --priority 1000 \
  --source-address-prefixes '*' \
  --source-port-ranges '*' \
  --destination-address-prefixes '*' \
  --destination-port-ranges 22 \
  --access Allow \
  --protocol Tcp

# Permitir HTTP (porta 80)
az network nsg rule create \
  --resource-group $RESOURCE_GROUP \
  --nsg-name $NSG_NAME \
  --name AllowHTTP \
  --priority 1001 \
  --source-address-prefixes '*' \
  --source-port-ranges '*' \
  --destination-address-prefixes '*' \
  --destination-port-ranges 80 \
  --access Allow \
  --protocol Tcp

# Permitir HTTPS (porta 443)
az network nsg rule create \
  --resource-group $RESOURCE_GROUP \
  --nsg-name $NSG_NAME \
  --name AllowHTTPS \
  --priority 1002 \
  --source-address-prefixes '*' \
  --source-port-ranges '*' \
  --destination-address-prefixes '*' \
  --destination-port-ranges 443 \
  --access Allow \
  --protocol Tcp

# Associar NSG à subnet de aplicação
az network vnet subnet update \
  --resource-group $RESOURCE_GROUP \
  --vnet-name $VNET_NAME \
  --name $SUBNET_APP_NAME \
  --network-security-group $NSG_NAME
```

## 💾 Passo 3: Criar PostgreSQL Database

### Opção A: Azure Database for PostgreSQL (Recomendado)

```bash
# Criar servidor PostgreSQL
az postgres server create \
  --resource-group $RESOURCE_GROUP \
  --name $DB_SERVER_NAME \
  --location $LOCATION \
  --admin-user $DB_ADMIN_USER \
  --admin-password "$DB_ADMIN_PASSWORD" \
  --sku-name $DB_SKU \
  --storage-size 51200 \
  --version 14

# Configurar firewall para permitir acesso da subnet de aplicação
az postgres server vnet-rule create \
  --resource-group $RESOURCE_GROUP \
  --server-name $DB_SERVER_NAME \
  --name AllowAppSubnet \
  --vnet-name $VNET_NAME \
  --subnet $SUBNET_APP_NAME

# Criar banco de dados
az postgres db create \
  --resource-group $RESOURCE_GROUP \
  --server-name $DB_SERVER_NAME \
  --name $DB_NAME

# Habilitar SSL (obrigatório)
az postgres server update \
  --resource-group $RESOURCE_GROUP \
  --name $DB_SERVER_NAME \
  --ssl-enforcement Enabled
```

### Opção B: PostgreSQL em VM (Para controle total)

```bash
# Criar VM para PostgreSQL
az vm create \
  --resource-group $RESOURCE_GROUP \
  --name "${PROJECT_NAME}-db-vm" \
  --vnet-name $VNET_NAME \
  --subnet $SUBNET_DB_NAME \
  --size Standard_B2s \
  --image $VM_IMAGE \
  --admin-username azureuser \
  --generate-ssh-keys

# Conectar via SSH e instalar PostgreSQL
# (ver seção de instalação do PostgreSQL abaixo)
```

## 🖥️ Passo 4: Criar VM de Aplicação

### 4.1 Criar IP Público

```bash
az network public-ip create \
  --resource-group $RESOURCE_GROUP \
  --name "${VM_NAME}-ip" \
  --allocation-method Static \
  --sku Standard
```

### 4.2 Criar VM

```bash
az vm create \
  --resource-group $RESOURCE_GROUP \
  --name $VM_NAME \
  --vnet-name $VNET_NAME \
  --subnet $SUBNET_APP_NAME \
  --nsg $NSG_NAME \
  --public-ip-address "${VM_NAME}-ip" \
  --size $VM_SIZE \
  --image $VM_IMAGE \
  --admin-username azureuser \
  --generate-ssh-keys \
  --verbose

# Obter IP público
VM_PUBLIC_IP=$(az vm show -d \
  --resource-group $RESOURCE_GROUP \
  --name $VM_NAME \
  --query publicIps -o tsv)

echo "VM criada com IP público: $VM_PUBLIC_IP"
```

## 📦 Passo 5: Configurar VM de Aplicação

### 5.1 Conectar via SSH

```bash
ssh azureuser@$VM_PUBLIC_IP
```

### 5.2 Instalar Dependências do Sistema

```bash
# Atualizar sistema
sudo apt update && sudo apt upgrade -y

# Instalar Python 3.12 e dependências
sudo apt install -y python3.12 python3.12-venv python3-pip
sudo apt install -y postgresql-client libpq-dev
sudo apt install -y nginx git curl

# Instalar supervisord para gerenciar processos
sudo apt install -y supervisor

# Criar usuário para a aplicação
sudo useradd -m -s /bin/bash django
sudo usermod -aG sudo django
```

### 5.3 Configurar Aplicação Django

```bash
# Mudar para usuário django
sudo su - django

# Criar diretório da aplicação
mkdir -p ~/apps
cd ~/apps

# Clonar repositório (substituir pela URL do seu repo)
git clone https://github.com/DaylonCPinto/projeto_do_fim.git
cd projeto_do_fim

# Criar ambiente virtual
python3.12 -m venv venv
source venv/bin/activate

# Instalar dependências
pip install --upgrade pip
pip install -r requirements.txt

# Criar arquivo .env
cat > .env << EOF
SECRET_KEY=$(python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())")
DEBUG=False
ALLOWED_HOSTS=${VM_PUBLIC_IP},${PROJECT_NAME}.com
CSRF_TRUSTED_ORIGINS=https://${VM_PUBLIC_IP},https://${PROJECT_NAME}.com

# Database Configuration
DATABASE_URL=postgres://${DB_ADMIN_USER}:${DB_ADMIN_PASSWORD}@${DB_SERVER_NAME}.postgres.database.azure.com:5432/${DB_NAME}?sslmode=require

# Wagtail Configuration
WAGTAILADMIN_BASE_URL=https://${VM_PUBLIC_IP}
EOF

# Executar migrações
python manage.py migrate

# Coletar arquivos estáticos
python manage.py collectstatic --noinput

# Criar superusuário
python manage.py createsuperuser
```

### 5.4 Configurar Gunicorn com Supervisor

```bash
# Voltar para usuário root
exit

# Criar configuração do supervisor
sudo tee /etc/supervisor/conf.d/django.conf > /dev/null << EOF
[program:django]
command=/home/django/apps/projeto_do_fim/venv/bin/gunicorn core.wsgi:application --bind 127.0.0.1:8000 --workers 4 --timeout 600
directory=/home/django/apps/projeto_do_fim
user=django
autostart=true
autorestart=true
redirect_stderr=true
stdout_logfile=/var/log/django/gunicorn.log
EOF

# Criar diretório de logs
sudo mkdir -p /var/log/django
sudo chown django:django /var/log/django

# Recarregar supervisor
sudo supervisorctl reread
sudo supervisorctl update
sudo supervisorctl start django
```

### 5.5 Configurar Nginx

```bash
# Remover configuração padrão
sudo rm /etc/nginx/sites-enabled/default

# Criar configuração do Django
sudo tee /etc/nginx/sites-available/django > /dev/null << EOF
upstream django {
    server 127.0.0.1:8000;
}

server {
    listen 80;
    server_name ${VM_PUBLIC_IP} ${PROJECT_NAME}.com;

    client_max_body_size 100M;

    location /static/ {
        alias /home/django/apps/projeto_do_fim/static_root/;
        expires 30d;
        add_header Cache-Control "public, immutable";
    }

    location /media/ {
        alias /home/django/apps/projeto_do_fim/media/;
        expires 7d;
        add_header Cache-Control "public";
    }

    location / {
        proxy_pass http://django;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
        proxy_redirect off;
    }
}
EOF

# Ativar site
sudo ln -s /etc/nginx/sites-available/django /etc/nginx/sites-enabled/

# Testar configuração
sudo nginx -t

# Reiniciar Nginx
sudo systemctl restart nginx
sudo systemctl enable nginx
```

## 🔒 Passo 6: Configurar SSL com Let's Encrypt

```bash
# Instalar Certbot
sudo apt install -y certbot python3-certbot-nginx

# Obter certificado SSL (substituir pelo seu domínio)
sudo certbot --nginx -d ${PROJECT_NAME}.com -d www.${PROJECT_NAME}.com

# Renovação automática já está configurada via cron
# Testar renovação
sudo certbot renew --dry-run
```

## 🔄 Passo 7: Configurar Backup Automático

### Backup do Banco de Dados

```bash
# Criar script de backup
sudo tee /home/django/backup.sh > /dev/null << 'EOF'
#!/bin/bash
BACKUP_DIR="/home/django/backups"
DATE=$(date +%Y%m%d_%H%M%S)
DB_NAME="portaldb"
DB_HOST="SERVIDOR.postgres.database.azure.com"
DB_USER="pgadmin"
DB_PASSWORD="SuaSenha"

mkdir -p $BACKUP_DIR

# Backup do banco de dados
PGPASSWORD=$DB_PASSWORD pg_dump -h $DB_HOST -U $DB_USER -d $DB_NAME | gzip > $BACKUP_DIR/db_backup_$DATE.sql.gz

# Manter apenas últimos 7 dias
find $BACKUP_DIR -name "db_backup_*.sql.gz" -mtime +7 -delete

echo "Backup concluído: $DATE"
EOF

sudo chmod +x /home/django/backup.sh
sudo chown django:django /home/django/backup.sh

# Adicionar ao crontab (backup diário às 2 AM)
(crontab -l 2>/dev/null; echo "0 2 * * * /home/django/backup.sh >> /var/log/django/backup.log 2>&1") | crontab -
```

## 📊 Passo 8: Monitoramento e Logs

### Visualizar Logs

```bash
# Logs do Gunicorn
sudo tail -f /var/log/django/gunicorn.log

# Logs do Nginx
sudo tail -f /var/log/nginx/access.log
sudo tail -f /var/log/nginx/error.log

# Logs do Supervisor
sudo supervisorctl tail -f django

# Logs do sistema
sudo journalctl -u nginx -f
```

### Comandos Úteis

```bash
# Reiniciar aplicação
sudo supervisorctl restart django

# Reiniciar Nginx
sudo systemctl restart nginx

# Verificar status
sudo supervisorctl status
sudo systemctl status nginx

# Atualizar código
cd /home/django/apps/projeto_do_fim
git pull
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --noinput
sudo supervisorctl restart django
```

## 🔧 Troubleshooting

### Erro de conexão com banco de dados

1. Verificar firewall do PostgreSQL:
```bash
az postgres server firewall-rule list \
  --resource-group $RESOURCE_GROUP \
  --server-name $DB_SERVER_NAME
```

2. Testar conexão:
```bash
psql -h ${DB_SERVER_NAME}.postgres.database.azure.com -U ${DB_ADMIN_USER} -d ${DB_NAME}
```

### Erro 502 Bad Gateway

1. Verificar se Gunicorn está rodando:
```bash
sudo supervisorctl status django
```

2. Verificar logs:
```bash
sudo tail -100 /var/log/django/gunicorn.log
```

### Permissões de arquivo

```bash
# Corrigir permissões
sudo chown -R django:django /home/django/apps/projeto_do_fim
sudo chmod -R 755 /home/django/apps/projeto_do_fim
```

## 🎯 Configuração de Load Balancer (Múltiplas VMs)

Para alta disponibilidade, crie múltiplas VMs e um Load Balancer:

```bash
# Criar Load Balancer
az network lb create \
  --resource-group $RESOURCE_GROUP \
  --name "${PROJECT_NAME}-lb" \
  --sku Standard \
  --public-ip-address "${PROJECT_NAME}-lb-ip" \
  --frontend-ip-name "${PROJECT_NAME}-frontend" \
  --backend-pool-name "${PROJECT_NAME}-backend"

# Criar health probe
az network lb probe create \
  --resource-group $RESOURCE_GROUP \
  --lb-name "${PROJECT_NAME}-lb" \
  --name http-probe \
  --protocol http \
  --port 80 \
  --path /

# Criar regra de balanceamento
az network lb rule create \
  --resource-group $RESOURCE_GROUP \
  --lb-name "${PROJECT_NAME}-lb" \
  --name http-rule \
  --protocol tcp \
  --frontend-port 80 \
  --backend-port 80 \
  --frontend-ip-name "${PROJECT_NAME}-frontend" \
  --backend-pool-name "${PROJECT_NAME}-backend" \
  --probe-name http-probe
```

## 📚 Recursos Adicionais

- [Azure Virtual Machines Documentation](https://docs.microsoft.com/azure/virtual-machines/)
- [Azure Database for PostgreSQL](https://docs.microsoft.com/azure/postgresql/)
- [Nginx Documentation](https://nginx.org/en/docs/)
- [Supervisor Documentation](http://supervisord.org/)
- [Django Deployment Checklist](https://docs.djangoproject.com/en/stable/howto/deployment/checklist/)

## 💰 Estimativa de Custos (Brasil Sul)

| Recurso | Especificação | Custo Mensal (USD) |
|---------|---------------|-------------------|
| VM App | Standard_B2s | ~$30 |
| PostgreSQL | GP_Gen5_2 | ~$100 |
| Load Balancer | Standard (opcional) | ~$20 |
| IP Público | Standard | ~$3 |
| Bandwidth | 100 GB | ~$5 |
| **Total** | | **~$158/mês** |

*Valores aproximados, consulte o Azure Pricing Calculator para estimativa precisa.*

## ✅ Checklist de Deploy

- [ ] Resource Group criado
- [ ] Virtual Network e Subnets configuradas
- [ ] Network Security Group com regras de firewall
- [ ] PostgreSQL Database criado e configurado
- [ ] VM de aplicação criada
- [ ] Python 3.12 e dependências instaladas
- [ ] Código da aplicação clonado
- [ ] Arquivo .env configurado
- [ ] Migrações executadas
- [ ] Arquivos estáticos coletados
- [ ] Superusuário criado
- [ ] Gunicorn configurado com Supervisor
- [ ] Nginx configurado e funcionando
- [ ] SSL configurado com Let's Encrypt (se usando domínio)
- [ ] Backup automático configurado
- [ ] Logs verificados e funcionando
- [ ] Testes de carga realizados
- [ ] Documentação atualizada

---

**Última atualização:** Outubro 2025
