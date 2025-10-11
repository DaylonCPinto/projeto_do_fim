#!/bin/bash
# Script de configuração automática da VM Web
# Ubuntu 22.04 - Azure VM
# Execute como root: sudo ./setup_web.sh

set -e  # Parar em caso de erro

echo "=============================================="
echo "Configuração Django + Nginx + Gunicorn"
echo "VM Web - Ubuntu 22.04"
echo "=============================================="
echo ""

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Verificar se está rodando como root
if [ "$EUID" -ne 0 ]; then 
   echo -e "${RED}Por favor, execute como root: sudo ./setup_web.sh${NC}"
   exit 1
fi

echo -e "${YELLOW}Este script irá instalar e configurar:${NC}"
echo "  - Python 3.12"
echo "  - Nginx"
echo "  - Supervisor"
echo "  - Repositório do projeto"
echo "  - Ambiente virtual Python"
echo ""

# Solicitar informações
read -p "URL do repositório Git [https://github.com/DaylonCPinto/projeto_do_fim.git]: " REPO_URL
REPO_URL=${REPO_URL:-https://github.com/DaylonCPinto/projeto_do_fim.git}

read -p "Branch do Git [main]: " GIT_BRANCH
GIT_BRANCH=${GIT_BRANCH:-main}

# Obter IP público da VM
PUBLIC_IP=$(curl -s http://ifconfig.me || curl -s http://icanhazip.com)
echo ""
echo -e "${BLUE}IP Público detectado: $PUBLIC_IP${NC}"
echo ""

echo -e "${GREEN}Iniciando configuração...${NC}"
echo ""

# 1. Atualizar sistema
echo "[1/12] Atualizando sistema..."
apt update && apt upgrade -y

# 2. Instalar dependências do sistema
echo "[2/12] Instalando dependências do sistema..."
apt install -y software-properties-common

# Adicionar PPA do Python 3.12
add-apt-repository -y ppa:deadsnakes/ppa
apt update

# Instalar Python 3.12 e ferramentas
apt install -y python3.12 python3.12-venv python3.12-dev python3-pip
apt install -y postgresql-client libpq-dev
apt install -y nginx git curl wget

# 3. Instalar Supervisor
echo "[3/12] Instalando Supervisor..."
apt install -y supervisor
systemctl enable supervisor
systemctl start supervisor

# 4. Criar usuário django
echo "[4/12] Criando usuário django..."
if id "django" &>/dev/null; then
    echo "Usuário django já existe"
else
    useradd -m -s /bin/bash django
    echo "Usuário django criado"
fi

# 5. Clonar repositório
echo "[5/12] Clonando repositório..."
sudo -u django bash << EOF
cd /home/django
mkdir -p apps
cd apps

if [ -d "projeto_do_fim" ]; then
    echo "Repositório já existe, atualizando..."
    cd projeto_do_fim
    git pull origin $GIT_BRANCH
else
    echo "Clonando repositório..."
    git clone $REPO_URL
    cd projeto_do_fim
    git checkout $GIT_BRANCH
fi
EOF

# 6. Criar ambiente virtual e instalar dependências
echo "[6/12] Criando ambiente virtual e instalando dependências..."
sudo -u django bash << 'EOF'
cd /home/django/apps/projeto_do_fim

# Criar ambiente virtual
python3.12 -m venv venv

# Ativar ambiente virtual
source venv/bin/activate

# Atualizar pip
pip install --upgrade pip

# Instalar dependências
pip install -r requirements.txt

echo "Dependências instaladas com sucesso"
EOF

# 7. Criar diretórios necessários
echo "[7/12] Criando diretórios de logs e static..."
mkdir -p /var/log/django
chown django:django /var/log/django

mkdir -p /home/django/apps/projeto_do_fim/static_root
mkdir -p /home/django/apps/projeto_do_fim/media
chown -R django:django /home/django/apps/projeto_do_fim

# 8. Criar arquivo .env template
echo "[8/12] Criando template do arquivo .env..."
cat > /home/django/apps/projeto_do_fim/.env.template << EOF
# Django Settings
SECRET_KEY=CHANGE_THIS_TO_A_RANDOM_SECRET_KEY
DEBUG=False
ALLOWED_HOSTS=$PUBLIC_IP,seu-dominio.com,localhost
CSRF_TRUSTED_ORIGINS=https://$PUBLIC_IP,https://seu-dominio.com

# Database Configuration
# Formato: postgres://usuario:senha@host:porta/banco
DATABASE_URL=postgres://django_user:SUA_SENHA@IP_PRIVADO_VM_DB:5432/portaldb

# Wagtail Configuration
WAGTAILADMIN_BASE_URL=https://$PUBLIC_IP
EOF

chown django:django /home/django/apps/projeto_do_fim/.env.template

echo -e "${YELLOW}Template .env criado em /home/django/apps/projeto_do_fim/.env.template${NC}"
echo -e "${YELLOW}Você precisará copiar e editar este arquivo depois!${NC}"

# 9. Configurar Supervisor para Gunicorn
echo "[9/12] Configurando Supervisor para Gunicorn..."
cat > /etc/supervisor/conf.d/django.conf << 'EOF'
[program:django]
command=/home/django/apps/projeto_do_fim/venv/bin/gunicorn core.wsgi:application --bind 127.0.0.1:8000 --workers 4 --timeout 600 --access-logfile /var/log/django/access.log --error-logfile /var/log/django/error.log
directory=/home/django/apps/projeto_do_fim
user=django
autostart=true
autorestart=true
redirect_stderr=true
stdout_logfile=/var/log/django/gunicorn.log
stderr_logfile=/var/log/django/gunicorn_err.log
environment=PATH="/home/django/apps/projeto_do_fim/venv/bin"
EOF

# 10. Configurar Nginx
echo "[10/12] Configurando Nginx..."

# Remover configuração padrão
rm -f /etc/nginx/sites-enabled/default

# Criar configuração do Django
cat > /etc/nginx/sites-available/django << EOF
upstream django {
    server 127.0.0.1:8000 fail_timeout=0;
}

server {
    listen 80;
    server_name $PUBLIC_IP _;
    
    client_max_body_size 100M;
    client_body_timeout 120s;
    
    # Logs
    access_log /var/log/nginx/django_access.log;
    error_log /var/log/nginx/django_error.log;
    
    # Static files
    location /static/ {
        alias /home/django/apps/projeto_do_fim/static_root/;
        expires 30d;
        add_header Cache-Control "public, immutable";
        access_log off;
    }
    
    # Media files
    location /media/ {
        alias /home/django/apps/projeto_do_fim/media/;
        expires 7d;
        add_header Cache-Control "public";
    }
    
    # Django application
    location / {
        proxy_pass http://django;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
        proxy_redirect off;
        proxy_connect_timeout 600s;
        proxy_send_timeout 600s;
        proxy_read_timeout 600s;
    }
    
    # Health check endpoint
    location /health/ {
        access_log off;
        return 200 "healthy\n";
        add_header Content-Type text/plain;
    }
}
EOF

# Ativar site
ln -sf /etc/nginx/sites-available/django /etc/nginx/sites-enabled/

# Testar configuração do Nginx
nginx -t

# 11. Ajustar permissões finais
echo "[11/12] Ajustando permissões..."
chown -R django:django /home/django/apps/projeto_do_fim
chmod -R 755 /home/django/apps/projeto_do_fim

# 12. Iniciar serviços
echo "[12/12] Iniciando serviços..."
systemctl restart nginx
systemctl enable nginx

supervisorctl reread
supervisorctl update

echo ""
echo -e "${GREEN}=============================================="
echo "Configuração concluída com sucesso!"
echo "==============================================${NC}"
echo ""
echo -e "${YELLOW}PRÓXIMOS PASSOS IMPORTANTES:${NC}"
echo ""
echo "1. Configure o arquivo .env:"
echo -e "   ${BLUE}sudo su - django${NC}"
echo -e "   ${BLUE}cd ~/apps/projeto_do_fim${NC}"
echo -e "   ${BLUE}cp .env.template .env${NC}"
echo -e "   ${BLUE}nano .env${NC}"
echo ""
echo "   Edite especialmente:"
echo "   - SECRET_KEY (gere uma nova chave)"
echo "   - DATABASE_URL (com credenciais do PostgreSQL)"
echo ""
echo "2. Execute as migrações e colete arquivos estáticos:"
echo -e "   ${BLUE}source venv/bin/activate${NC}"
echo -e "   ${BLUE}python manage.py migrate${NC}"
echo -e "   ${BLUE}python manage.py collectstatic --noinput${NC}"
echo -e "   ${BLUE}python manage.py createsuperuser${NC}"
echo ""
echo "3. Inicie o Gunicorn:"
echo -e "   ${BLUE}exit${NC} (voltar para root)"
echo -e "   ${BLUE}sudo supervisorctl start django${NC}"
echo ""
echo "4. Verifique o status:"
echo -e "   ${BLUE}sudo supervisorctl status${NC}"
echo -e "   ${BLUE}sudo systemctl status nginx${NC}"
echo ""
echo -e "IP Público: ${GREEN}http://$PUBLIC_IP${NC}"
echo ""
echo "Para ver logs:"
echo "  - Gunicorn: sudo tail -f /var/log/django/gunicorn.log"
echo "  - Nginx: sudo tail -f /var/log/nginx/django_error.log"
echo ""
