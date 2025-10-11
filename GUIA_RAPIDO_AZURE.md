# Guia Rápido - Deploy Azure (2 VMs)

## 🎯 Objetivo
Colocar seu site Django/Wagtail no ar usando 2 VMs Azure:
- **VM Web**: Nginx + Gunicorn + Django (IP público)
- **VM DB**: PostgreSQL (sem IP público)

## 📦 O que você tem
- ✅ 2 VMs Azure com Ubuntu 22.04 já criadas
- ✅ VM Web com IP público
- ✅ VM DB sem IP público (apenas IP privado)
- ❌ Nada instalado ainda

## ⚡ Passos Rápidos

### PARTE 1: Configurar Rede (Azure Portal ou CLI)

#### 1. Conectar VNets (se necessário)
Se suas VMs estão em VNets diferentes, crie VNet Peering:
- Azure Portal → Virtual Networks → Sua VNet → Peerings → Add
- Configure nos dois sentidos (Web ↔ DB)

#### 2. Configurar NSG da VM Web
Permitir portas: **22** (SSH), **80** (HTTP), **443** (HTTPS)

#### 3. Configurar NSG da VM DB
Permitir porta: **5432** (PostgreSQL) apenas do IP privado da VM Web

---

### PARTE 2: Configurar VM Database

```bash
# 1. Conectar via SSH Jump (da VM Web)
ssh -J azureuser@IP_PUBLICO_WEB azureuser@IP_PRIVADO_DB

# 2. Baixar e executar script de setup
wget https://raw.githubusercontent.com/DaylonCPinto/projeto_do_fim/main/scripts/setup_database.sh
chmod +x setup_database.sh
sudo ./setup_database.sh

# 3. Anotar as credenciais mostradas!
# - Banco: portaldb
# - Usuário: django_user  
# - Senha: (a que você definir)
# - Host: IP privado da VM DB
```

**⚠️ IMPORTANTE**: Anote o IP privado e as credenciais!

---

### PARTE 3: Configurar VM Web

```bash
# 1. Conectar via SSH
ssh azureuser@IP_PUBLICO_WEB

# 2. Baixar e executar script de setup
wget https://raw.githubusercontent.com/DaylonCPinto/projeto_do_fim/main/scripts/setup_web.sh
chmod +x setup_web.sh
sudo ./setup_web.sh

# 3. Configurar .env
sudo su - django
cd ~/apps/projeto_do_fim
cp .env.template .env
nano .env
```

Edite o arquivo `.env`:
```bash
SECRET_KEY=$(python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())")
DEBUG=False
ALLOWED_HOSTS=SEU_IP_PUBLICO,seu-dominio.com
CSRF_TRUSTED_ORIGINS=https://SEU_IP_PUBLICO,https://seu-dominio.com

# Usar credenciais da VM DB
DATABASE_URL=postgres://django_user:SENHA_DO_DB@IP_PRIVADO_DB:5432/portaldb

WAGTAILADMIN_BASE_URL=https://SEU_IP_PUBLICO
```

```bash
# 4. Preparar aplicação
source venv/bin/activate
python manage.py migrate
python manage.py collectstatic --noinput
python manage.py createsuperuser

# 5. Iniciar serviços
exit  # Voltar para root
sudo supervisorctl start django
sudo systemctl restart nginx
```

---

### PARTE 4: Testar

```bash
# Na VM Web, testar conectividade com DB
wget https://raw.githubusercontent.com/DaylonCPinto/projeto_do_fim/main/scripts/test_connectivity.sh
chmod +x test_connectivity.sh
./test_connectivity.sh

# Ver logs
sudo tail -f /var/log/django/gunicorn.log
sudo tail -f /var/log/nginx/django_error.log

# Verificar status
sudo supervisorctl status django
sudo systemctl status nginx
```

Acessar no navegador: `http://SEU_IP_PUBLICO`

---

## 🔧 Problemas Comuns

### ❌ Erro 502 Bad Gateway

**Causa**: Gunicorn não está rodando

**Solução**:
```bash
sudo supervisorctl status django
sudo supervisorctl start django
sudo tail -100 /var/log/django/gunicorn.log
```

---

### ❌ Erro de Conexão com Banco

**Causa**: NSG, firewall ou credenciais erradas

**Solução**:
```bash
# Testar conexão da VM Web → VM DB
psql -h IP_PRIVADO_DB -U django_user -d portaldb

# Se falhar:
# 1. Verificar NSG da VM DB (porta 5432 aberta para VM Web)
# 2. Na VM DB, verificar firewall:
sudo ufw status
sudo ufw allow 5432/tcp
```

---

### ❌ CSS/JS não carregam

**Causa**: Arquivos estáticos não coletados ou permissões

**Solução**:
```bash
sudo su - django
cd ~/apps/projeto_do_fim
source venv/bin/activate
python manage.py collectstatic --noinput
exit
sudo chown -R django:django /home/django/apps/projeto_do_fim/static_root
sudo systemctl restart nginx
```

---

## 🔄 Atualizar Código (Deploy)

```bash
# Conectar à VM Web
ssh azureuser@IP_PUBLICO_WEB

# Atualizar
sudo su - django
cd ~/apps/projeto_do_fim
git pull origin main
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --noinput
exit

# Reiniciar
sudo supervisorctl restart django
```

---

## 📊 Comandos Úteis

### Ver Logs em Tempo Real
```bash
# Gunicorn
sudo tail -f /var/log/django/gunicorn.log

# Nginx
sudo tail -f /var/log/nginx/django_error.log
sudo tail -f /var/log/nginx/django_access.log
```

### Gerenciar Serviços
```bash
# Gunicorn (via Supervisor)
sudo supervisorctl status django
sudo supervisorctl start django
sudo supervisorctl stop django
sudo supervisorctl restart django

# Nginx
sudo systemctl status nginx
sudo systemctl restart nginx
sudo systemctl reload nginx  # Sem downtime
```

### Logs do PostgreSQL (na VM DB)
```bash
sudo tail -f /var/log/postgresql/postgresql-14-main.log
sudo -u postgres psql -c "SELECT * FROM pg_stat_activity;"
```

---

## 🔒 Adicionar SSL (Opcional)

Se você tem um domínio:

```bash
# Na VM Web
sudo apt install -y certbot python3-certbot-nginx
sudo certbot --nginx -d seu-dominio.com -d www.seu-dominio.com

# Atualizar .env com o domínio
sudo su - django
cd ~/apps/projeto_do_fim
nano .env
# Atualizar ALLOWED_HOSTS e CSRF_TRUSTED_ORIGINS

# Reiniciar
exit
sudo supervisorctl restart django
```

---

## ✅ Checklist Final

Antes de considerar pronto:

### Rede
- [ ] VNets conectadas (se necessário)
- [ ] NSG da VM Web permite 22, 80, 443
- [ ] NSG da VM DB permite 5432 da VM Web
- [ ] Consegue SSH na VM Web
- [ ] Consegue SSH na VM DB via jump

### VM Database
- [ ] PostgreSQL instalado e rodando
- [ ] Banco `portaldb` criado
- [ ] Usuário `django_user` criado
- [ ] VM Web consegue conectar

### VM Web
- [ ] Python 3.12, Nginx, Supervisor instalados
- [ ] Repositório clonado
- [ ] .env configurado corretamente
- [ ] Migrações executadas
- [ ] Static files coletados
- [ ] Superusuário criado
- [ ] Gunicorn rodando
- [ ] Nginx rodando

### Testes
- [ ] Site carrega no navegador
- [ ] Admin funciona (`/admin/`)
- [ ] Wagtail CMS funciona (`/cms/`)
- [ ] CSS e JavaScript carregam
- [ ] Sem erros 502
- [ ] Logs sem erros críticos

---

## 📚 Documentação Completa

Para instruções detalhadas, consulte:
- `AZURE_VM_SETUP_COMPLETO.md` - Guia passo a passo completo
- `AZURE_DEPLOYMENT_VM.md` - Guia original com Azure CLI

---

## 🆘 Precisa de Ajuda?

1. Verifique os logs
2. Execute o script de teste de conectividade
3. Consulte a seção de Troubleshooting no `AZURE_VM_SETUP_COMPLETO.md`
4. Verifique a configuração do NSG no Azure Portal

**Principais arquivos de log**:
- `/var/log/django/gunicorn.log`
- `/var/log/nginx/django_error.log`
- `/var/log/postgresql/postgresql-14-main.log` (na VM DB)
