# Guia Completo: Deploy em VMs Azure Separadas (Web + Database)

## 📋 Visão Geral

Este guia foi criado especificamente para configurar duas VMs Azure já provisionadas:
- **VM Web (porta_web)**: Ubuntu 22.04 com IP público - rodará Django + Nginx + Gunicorn
- **VM Database (porta_db)**: Ubuntu 22.04 SEM IP público - rodará PostgreSQL 14

## 🎯 Arquitetura da Solução

```
Internet
    ↓
[NSG - Portas 22, 80, 443]
    ↓
VM Web (10.0.1.x) ←→ VNet ←→ VM Database (10.0.2.x)
    ↓                              ↓
Nginx → Gunicorn → Django    PostgreSQL 14
```

## 🚀 Passo 1: Configuração de Rede no Azure Portal

### 1.1 Conectar as VNets (se estiverem em VNets diferentes)

Se suas VMs estão em VNets diferentes, você precisa criar um VNet Peering:

#### Via Azure Portal:
1. Acesse **Virtual networks**
2. Selecione a VNet da VM Web
3. Clique em **Peerings** → **+ Add**
4. Configure:
   - Nome: `web-to-db-peering`
   - VNet remota: Selecione a VNet da VM Database
   - Permita tráfego entre as VNets: **Enabled**
   - Permita tráfego encaminhado: **Enabled**
5. Repita o processo na direção oposta (DB → Web)

#### Via Azure CLI:
```bash
# Obter IDs das VNets
VNET_WEB_ID=$(az network vnet show --resource-group NOME_RG_WEB --name NOME_VNET_WEB --query id -o tsv)
VNET_DB_ID=$(az network vnet show --resource-group NOME_RG_DB --name NOME_VNET_DB --query id -o tsv)

# Criar peering Web → DB
az network vnet peering create \
  --name web-to-db \
  --resource-group NOME_RG_WEB \
  --vnet-name NOME_VNET_WEB \
  --remote-vnet $VNET_DB_ID \
  --allow-vnet-access \
  --allow-forwarded-traffic

# Criar peering DB → Web
az network vnet peering create \
  --name db-to-web \
  --resource-group NOME_RG_DB \
  --vnet-name NOME_VNET_DB \
  --remote-vnet $VNET_WEB_ID \
  --allow-vnet-access \
  --allow-forwarded-traffic
```

### 1.2 Configurar NSG da VM Web

A VM Web precisa aceitar tráfego SSH, HTTP e HTTPS da internet.

#### Via Azure Portal:
1. Acesse **Network Security Groups**
2. Selecione o NSG da VM Web
3. Vá em **Inbound security rules** → **+ Add**
4. Adicione as seguintes regras:

| Nome | Prioridade | Porta | Protocolo | Origem | Ação |
|------|-----------|-------|-----------|--------|------|
| AllowSSH | 100 | 22 | TCP | * | Allow |
| AllowHTTP | 110 | 80 | TCP | * | Allow |
| AllowHTTPS | 120 | 443 | TCP | * | Allow |

#### Via Azure CLI:
```bash
# Definir variáveis
NSG_WEB="nome-nsg-web"
RG_WEB="nome-resource-group-web"

# Permitir SSH
az network nsg rule create \
  --resource-group $RG_WEB \
  --nsg-name $NSG_WEB \
  --name AllowSSH \
  --priority 100 \
  --source-address-prefixes '*' \
  --destination-port-ranges 22 \
  --access Allow \
  --protocol Tcp

# Permitir HTTP
az network nsg rule create \
  --resource-group $RG_WEB \
  --nsg-name $NSG_WEB \
  --name AllowHTTP \
  --priority 110 \
  --source-address-prefixes '*' \
  --destination-port-ranges 80 \
  --access Allow \
  --protocol Tcp

# Permitir HTTPS
az network nsg rule create \
  --resource-group $RG_WEB \
  --nsg-name $NSG_WEB \
  --name AllowHTTPS \
  --priority 120 \
  --source-address-prefixes '*' \
  --destination-port-ranges 443 \
  --access Allow \
  --protocol Tcp
```

### 1.3 Configurar NSG da VM Database

A VM Database deve aceitar apenas conexões PostgreSQL da VM Web.

#### Via Azure Portal:
1. Acesse **Network Security Groups**
2. Selecione o NSG da VM Database
3. Vá em **Inbound security rules** → **+ Add**
4. Adicione:

| Nome | Prioridade | Porta | Protocolo | Origem | Ação |
|------|-----------|-------|-----------|--------|------|
| AllowPostgreSQL | 100 | 5432 | TCP | IP_PRIVADO_VM_WEB | Allow |

**Nota**: Se não souber o IP privado da VM Web, obtenha com:
```bash
az vm show -d --resource-group NOME_RG_WEB --name NOME_VM_WEB --query privateIps -o tsv
```

#### Via Azure CLI:
```bash
# Obter IP privado da VM Web
VM_WEB_PRIVATE_IP=$(az vm show -d --resource-group $RG_WEB --name NOME_VM_WEB --query privateIps -o tsv)

# Definir variáveis
NSG_DB="nome-nsg-db"
RG_DB="nome-resource-group-db"

# Permitir PostgreSQL apenas da VM Web
az network nsg rule create \
  --resource-group $RG_DB \
  --nsg-name $NSG_DB \
  --name AllowPostgreSQLFromWeb \
  --priority 100 \
  --source-address-prefixes $VM_WEB_PRIVATE_IP \
  --destination-port-ranges 5432 \
  --access Allow \
  --protocol Tcp
```

## 🗄️ Passo 2: Configurar VM Database (PostgreSQL)

### 2.1 Conectar à VM Database via SSH Jump

Como a VM Database não tem IP público, conecte através da VM Web:

```bash
# Método 1: SSH Jump direto
ssh -J azureuser@IP_PUBLICO_VM_WEB azureuser@IP_PRIVADO_VM_DB

# Método 2: SSH ProxyJump (adicione ao ~/.ssh/config)
cat >> ~/.ssh/config << EOF
Host azure-web
    HostName IP_PUBLICO_VM_WEB
    User azureuser
    IdentityFile ~/.ssh/id_rsa

Host azure-db
    HostName IP_PRIVADO_VM_DB
    User azureuser
    ProxyJump azure-web
    IdentityFile ~/.ssh/id_rsa
EOF

# Depois disso, conecte simplesmente com:
ssh azure-db
```

### 2.2 Executar Script de Configuração do PostgreSQL

Após conectar à VM Database, execute:

```bash
# Baixar o script de setup
curl -o setup_database.sh https://raw.githubusercontent.com/DaylonCPinto/projeto_do_fim/main/scripts/setup_database.sh

# Tornar executável
chmod +x setup_database.sh

# Executar (ATENÇÃO: Defina uma senha forte!)
sudo ./setup_database.sh
```

O script irá:
1. Instalar PostgreSQL 14
2. Configurar para aceitar conexões da VM Web
3. Criar banco de dados e usuário
4. Configurar firewall local (ufw)
5. Habilitar PostgreSQL para iniciar automaticamente

**IMPORTANTE**: Anote as credenciais que o script gerar!

### 2.3 Configuração Manual do PostgreSQL (alternativa)

Se preferir configurar manualmente:

```bash
# Atualizar sistema
sudo apt update && sudo apt upgrade -y

# Instalar PostgreSQL 14
sudo apt install -y postgresql-14 postgresql-contrib-14

# Configurar PostgreSQL para aceitar conexões remotas
sudo sed -i "s/#listen_addresses = 'localhost'/listen_addresses = '*'/" /etc/postgresql/14/main/postgresql.conf

# Configurar autenticação (pg_hba.conf)
# Substitua 10.0.1.0/24 pela subnet da sua VM Web
sudo tee -a /etc/postgresql/14/main/pg_hba.conf > /dev/null << EOF

# Permitir conexões da VM Web
host    portaldb        django_user     10.0.1.0/24            scram-sha-256
EOF

# Reiniciar PostgreSQL
sudo systemctl restart postgresql

# Criar banco de dados e usuário
sudo -u postgres psql << EOF
CREATE DATABASE portaldb;
CREATE USER django_user WITH PASSWORD 'SUA_SENHA_FORTE_AQUI';
ALTER ROLE django_user SET client_encoding TO 'utf8';
ALTER ROLE django_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE django_user SET timezone TO 'America/Sao_Paulo';
GRANT ALL PRIVILEGES ON DATABASE portaldb TO django_user;
\q
EOF

# Configurar firewall
sudo ufw allow 5432/tcp
sudo ufw allow OpenSSH
sudo ufw --force enable

# Verificar status
sudo systemctl status postgresql
```

### 2.4 Testar Conexão do Database

```bash
# Na VM Database, verificar se PostgreSQL está rodando
sudo systemctl status postgresql

# Verificar se está escutando na porta 5432
sudo netstat -plnt | grep 5432

# Testar conexão local
psql -U django_user -d portaldb -h localhost
```

## 🌐 Passo 3: Configurar VM Web (Django + Nginx + Gunicorn)

### 3.1 Conectar à VM Web via SSH

```bash
ssh azureuser@IP_PUBLICO_VM_WEB
```

### 3.2 Executar Script de Configuração Automática

```bash
# Baixar o script de setup
curl -o setup_web.sh https://raw.githubusercontent.com/DaylonCPinto/projeto_do_fim/main/scripts/setup_web.sh

# Tornar executável
chmod +x setup_web.sh

# Executar
sudo ./setup_web.sh
```

O script irá:
1. Instalar Python 3.12, pip, venv
2. Instalar e configurar Nginx
3. Instalar Supervisor para gerenciar Gunicorn
4. Criar usuário `django`
5. Clonar o repositório
6. Configurar ambiente virtual
7. Instalar dependências
8. Configurar arquivos de configuração
9. Preparar diretórios de logs e static

### 3.3 Configurar Variáveis de Ambiente

Após o script rodar, você precisará configurar o arquivo `.env`:

```bash
# Conectar como usuário django
sudo su - django

# Navegar até o diretório da aplicação
cd ~/apps/projeto_do_fim

# Criar arquivo .env
cat > .env << EOF
# Django Settings
SECRET_KEY=$(python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())")
DEBUG=False
ALLOWED_HOSTS=IP_PUBLICO_VM_WEB,seu-dominio.com
CSRF_TRUSTED_ORIGINS=https://IP_PUBLICO_VM_WEB,https://seu-dominio.com

# Database Configuration
# Formato: postgres://usuario:senha@host:porta/banco
DATABASE_URL=postgres://django_user:SUA_SENHA@IP_PRIVADO_VM_DB:5432/portaldb

# Wagtail Configuration
WAGTAILADMIN_BASE_URL=https://IP_PUBLICO_VM_WEB
EOF
```

### 3.4 Preparar Aplicação Django

```bash
# Ativar ambiente virtual
source venv/bin/activate

# Executar migrações
python manage.py migrate

# Coletar arquivos estáticos
python manage.py collectstatic --noinput

# Criar superusuário (interativo)
python manage.py createsuperuser
```

### 3.5 Iniciar Serviços

```bash
# Voltar para usuário root
exit

# Iniciar Gunicorn via Supervisor
sudo supervisorctl reread
sudo supervisorctl update
sudo supervisorctl start django

# Verificar status
sudo supervisorctl status django

# Reiniciar Nginx
sudo systemctl restart nginx
sudo systemctl status nginx
```

## 🔍 Passo 4: Verificação e Testes

### 4.1 Testar Conexão entre VMs

Na VM Web, teste a conexão com o PostgreSQL:

```bash
# Instalar cliente PostgreSQL (se ainda não tiver)
sudo apt install -y postgresql-client

# Testar conexão
psql -h IP_PRIVADO_VM_DB -U django_user -d portaldb

# Se conectar, digite \q para sair
```

### 4.2 Verificar Logs

```bash
# Logs do Gunicorn
sudo tail -f /var/log/django/gunicorn.log

# Logs do Nginx
sudo tail -f /var/log/nginx/error.log
sudo tail -f /var/log/nginx/access.log

# Status do Supervisor
sudo supervisorctl status
```

### 4.3 Testar Aplicação Web

```bash
# Testar Gunicorn diretamente
curl http://localhost:8000

# Testar Nginx
curl http://localhost

# Do seu computador local
curl http://IP_PUBLICO_VM_WEB
```

Abra o navegador e acesse:
- Site: `http://IP_PUBLICO_VM_WEB`
- Admin: `http://IP_PUBLICO_VM_WEB/admin/`
- Wagtail: `http://IP_PUBLICO_VM_WEB/cms/`

## 🔧 Troubleshooting - Problemas Comuns

### Problema 1: Erro 502 Bad Gateway (Nginx)

**Causa**: Gunicorn não está rodando ou não consegue se comunicar com Nginx.

**Solução**:
```bash
# Verificar status do Gunicorn
sudo supervisorctl status django

# Se não estiver rodando, iniciar
sudo supervisorctl start django

# Verificar logs
sudo tail -100 /var/log/django/gunicorn.log

# Verificar se está escutando na porta 8000
sudo netstat -plnt | grep 8000

# Reiniciar serviço
sudo supervisorctl restart django
```

### Problema 2: Erro de Conexão com Database

**Causa**: Firewall bloqueando, credenciais erradas, ou PostgreSQL não configurado.

**Solução**:
```bash
# Na VM Web, testar conexão
psql -h IP_PRIVADO_VM_DB -U django_user -d portaldb

# Verificar variável DATABASE_URL no .env
cat /home/django/apps/projeto_do_fim/.env | grep DATABASE_URL

# Na VM DB, verificar PostgreSQL
sudo systemctl status postgresql

# Verificar se está escutando
sudo netstat -plnt | grep 5432

# Verificar logs do PostgreSQL
sudo tail -100 /var/log/postgresql/postgresql-14-main.log

# Verificar pg_hba.conf
sudo cat /etc/postgresql/14/main/pg_hba.conf | grep django_user
```

### Problema 3: Static Files (CSS/JS) não carregam

**Causa**: Arquivos estáticos não coletados ou permissões erradas.

**Solução**:
```bash
# Conectar como usuário django
sudo su - django
cd ~/apps/projeto_do_fim
source venv/bin/activate

# Coletar arquivos estáticos novamente
python manage.py collectstatic --noinput

# Verificar permissões
ls -la static_root/

# Corrigir permissões se necessário
exit
sudo chown -R django:django /home/django/apps/projeto_do_fim/static_root
sudo chmod -R 755 /home/django/apps/projeto_do_fim/static_root
```

### Problema 4: Gunicorn não inicia

**Causa**: Erro no código Python, ambiente virtual incorreto, ou caminho errado.

**Solução**:
```bash
# Testar Gunicorn manualmente
sudo su - django
cd ~/apps/projeto_do_fim
source venv/bin/activate
gunicorn core.wsgi:application --bind 127.0.0.1:8000

# Se houver erros, corrija-os antes de usar o Supervisor
# Verificar configuração do Supervisor
cat /etc/supervisor/conf.d/django.conf

# Recarregar Supervisor
exit
sudo supervisorctl reread
sudo supervisorctl update
```

### Problema 5: Permissões Negadas

**Causa**: Arquivos ou diretórios com permissões incorretas.

**Solução**:
```bash
# Corrigir permissões do diretório da aplicação
sudo chown -R django:django /home/django/apps/projeto_do_fim
sudo chmod -R 755 /home/django/apps/projeto_do_fim

# Corrigir permissões de logs
sudo chown -R django:django /var/log/django
sudo chmod -R 755 /var/log/django

# Criar diretório media se não existir
sudo mkdir -p /home/django/apps/projeto_do_fim/media
sudo chown django:django /home/django/apps/projeto_do_fim/media
sudo chmod 755 /home/django/apps/projeto_do_fim/media
```

## 🔒 Passo 5: SSL com Let's Encrypt (Opcional)

Se você tem um domínio apontando para sua VM Web:

```bash
# Na VM Web
sudo apt install -y certbot python3-certbot-nginx

# Obter certificado (substitua seu-dominio.com)
sudo certbot --nginx -d seu-dominio.com -d www.seu-dominio.com

# Testar renovação automática
sudo certbot renew --dry-run
```

Atualizar o arquivo `.env`:
```bash
sudo su - django
cd ~/apps/projeto_do_fim
nano .env

# Atualizar:
ALLOWED_HOSTS=IP_PUBLICO_VM_WEB,seu-dominio.com,www.seu-dominio.com
CSRF_TRUSTED_ORIGINS=https://seu-dominio.com,https://www.seu-dominio.com
WAGTAILADMIN_BASE_URL=https://seu-dominio.com
```

Reiniciar aplicação:
```bash
exit
sudo supervisorctl restart django
```

## 🔄 Passo 6: Deploy de Atualizações

Quando fizer mudanças no código e quiser atualizar:

```bash
# Conectar à VM Web
ssh azureuser@IP_PUBLICO_VM_WEB

# Mudar para usuário django
sudo su - django
cd ~/apps/projeto_do_fim

# Atualizar código
git pull origin main

# Ativar ambiente virtual
source venv/bin/activate

# Instalar novas dependências (se houver)
pip install -r requirements.txt

# Executar migrações (se houver)
python manage.py migrate

# Coletar arquivos estáticos
python manage.py collectstatic --noinput

# Voltar para root e reiniciar
exit
sudo supervisorctl restart django

# Verificar status
sudo supervisorctl status django
```

## 📊 Monitoramento

### Ver logs em tempo real:

```bash
# Gunicorn
sudo tail -f /var/log/django/gunicorn.log

# Nginx Access
sudo tail -f /var/log/nginx/access.log

# Nginx Error
sudo tail -f /var/log/nginx/error.log

# PostgreSQL (na VM DB)
sudo tail -f /var/log/postgresql/postgresql-14-main.log

# Supervisor
sudo supervisorctl tail -f django
```

## 📦 Backup e Restauração

### Backup do Banco de Dados:

```bash
# Na VM Web (conectando ao DB)
pg_dump -h IP_PRIVADO_VM_DB -U django_user -d portaldb > backup_$(date +%Y%m%d).sql

# Ou na VM DB
sudo -u postgres pg_dump portaldb > /tmp/backup_$(date +%Y%m%d).sql
```

### Backup dos Arquivos Media:

```bash
# Na VM Web
tar -czf media_backup_$(date +%Y%m%d).tar.gz /home/django/apps/projeto_do_fim/media/
```

## ✅ Checklist Final

Antes de considerar o deploy completo, verifique:

### Rede e Conectividade:
- [ ] VNets conectadas (se necessário)
- [ ] NSG da VM Web permite 22, 80, 443
- [ ] NSG da VM DB permite 5432 apenas da VM Web
- [ ] Consegue fazer SSH na VM Web
- [ ] Consegue fazer SSH na VM DB via jump da VM Web
- [ ] VM Web consegue conectar ao PostgreSQL na VM DB

### VM Database:
- [ ] PostgreSQL 14 instalado e rodando
- [ ] Banco `portaldb` criado
- [ ] Usuário `django_user` criado com senha forte
- [ ] PostgreSQL configurado para aceitar conexões remotas
- [ ] pg_hba.conf permite conexões da subnet da VM Web
- [ ] Firewall (ufw) permite porta 5432

### VM Web:
- [ ] Python 3.12 instalado
- [ ] Nginx instalado e rodando
- [ ] Supervisor instalado e rodando
- [ ] Repositório clonado em /home/django/apps/projeto_do_fim
- [ ] Ambiente virtual criado e dependências instaladas
- [ ] Arquivo .env configurado com DATABASE_URL correto
- [ ] Migrações executadas sem erros
- [ ] Arquivos estáticos coletados
- [ ] Superusuário criado
- [ ] Gunicorn rodando via Supervisor
- [ ] Site acessível via navegador

### Segurança:
- [ ] DEBUG=False no .env
- [ ] SECRET_KEY forte e único gerado
- [ ] Senhas do banco de dados são fortes
- [ ] SSL configurado (se tem domínio)
- [ ] Firewall configurado em ambas VMs

### Funcionalidade:
- [ ] Site carrega no navegador
- [ ] Admin Django acessível
- [ ] Wagtail CMS acessível
- [ ] CSS e JavaScript carregam corretamente
- [ ] Upload de imagens funciona
- [ ] Não há erros 502 Bad Gateway
- [ ] Não há erros de conexão com banco

## 📞 Suporte e Recursos

- **Documentação Django**: https://docs.djangoproject.com/
- **Documentação Wagtail**: https://docs.wagtail.org/
- **Documentação Nginx**: https://nginx.org/en/docs/
- **Documentação PostgreSQL**: https://www.postgresql.org/docs/
- **Azure Documentation**: https://docs.microsoft.com/azure/

## 🎉 Próximos Passos

Após o deploy inicial:
1. Configure backup automático do banco de dados
2. Configure monitoramento (Azure Monitor, Application Insights)
3. Configure alertas para quando o site ficar fora do ar
4. Documente suas senhas em um gerenciador seguro
5. Configure CI/CD para deploys automáticos (GitHub Actions + Azure)

---

**Importante**: Este guia foi criado para minimizar configurações manuais futuras. Se seguir todos os passos corretamente, seu site estará no ar de forma estável e profissional!
