# Guia de Troubleshooting - Nginx e Gunicorn

Este guia resolve os problemas mais comuns com Nginx e Gunicorn em deploys Azure.

## 🔴 Erro 502 Bad Gateway

### Sintoma
Ao acessar o site, aparece "502 Bad Gateway" do Nginx.

### Causas Possíveis

#### 1. Gunicorn não está rodando

**Verificar**:
```bash
sudo supervisorctl status django
```

**Se mostrar "STOPPED" ou "FATAL"**:
```bash
# Ver logs do erro
sudo supervisorctl tail django

# Ou ver arquivo de log
sudo tail -100 /var/log/django/gunicorn.log

# Tentar iniciar
sudo supervisorctl start django
```

**Erros comuns no log**:

- **"ModuleNotFoundError: No module named 'core'"**
  - **Causa**: Caminho errado no supervisor.conf ou venv não ativado
  - **Solução**:
    ```bash
    # Verificar configuração
    cat /etc/supervisor/conf.d/django.conf
    
    # O caminho deve estar correto:
    # command=/home/django/apps/projeto_do_fim/venv/bin/gunicorn ...
    # directory=/home/django/apps/projeto_do_fim
    ```

- **"django.core.exceptions.ImproperlyConfigured: The SECRET_KEY setting must not be empty"**
  - **Causa**: Arquivo .env não configurado ou SECRET_KEY vazio
  - **Solução**:
    ```bash
    sudo su - django
    cd ~/apps/projeto_do_fim
    
    # Verificar se .env existe
    ls -la .env
    
    # Verificar SECRET_KEY
    cat .env | grep SECRET_KEY
    
    # Se vazio, gerar nova chave
    python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
    
    # Editar .env e adicionar a chave
    nano .env
    ```

- **"psycopg2.OperationalError: could not connect to server"**
  - **Causa**: Problema de conexão com banco de dados
  - **Solução**: Ver seção "Erro de Conexão com Banco de Dados" abaixo

#### 2. Gunicorn rodando mas Nginx não consegue conectar

**Verificar se Gunicorn está escutando**:
```bash
sudo netstat -plnt | grep 8000
```

Deve mostrar algo como:
```
tcp  0  0 127.0.0.1:8000  0.0.0.0:*  LISTEN  12345/gunicorn
```

**Se não mostrar nada**:
```bash
# Verificar configuração do Gunicorn
cat /etc/supervisor/conf.d/django.conf | grep bind

# Deve ter: --bind 127.0.0.1:8000
```

**Verificar configuração do Nginx**:
```bash
sudo nginx -t
cat /etc/nginx/sites-available/django | grep proxy_pass

# Deve ter: proxy_pass http://django;
# E upstream definido como: server 127.0.0.1:8000;
```

**Se configuração estiver correta**:
```bash
# Reiniciar ambos os serviços
sudo supervisorctl restart django
sudo systemctl restart nginx
```

#### 3. Socket ou permissões

**Verificar permissões do socket (se usar unix socket)**:
```bash
ls -la /run/gunicorn.sock
```

**Melhor usar TCP (porta 8000) em vez de socket Unix** para evitar problemas de permissão.

---

## 🔴 Erro de Conexão com Banco de Dados

### Sintoma
```
django.db.utils.OperationalError: could not connect to server: Connection refused
```
ou
```
psycopg2.OperationalError: connection to server at "IP" port 5432 failed
```

### Diagnóstico

**Na VM Web, testar conexão**:
```bash
psql -h IP_PRIVADO_DB -U django_user -d portaldb
```

### Causas e Soluções

#### 1. NSG bloqueando

**Verificar**: No Azure Portal → Network Security Groups → NSG da VM DB → Inbound rules

**Deve ter regra**:
- Nome: AllowPostgreSQL
- Porta: 5432
- Protocolo: TCP
- Origem: IP privado da VM Web ou subnet da VM Web
- Ação: Allow

**Criar regra via CLI**:
```bash
az network nsg rule create \
  --resource-group NOME_RG \
  --nsg-name NOME_NSG_DB \
  --name AllowPostgreSQLFromWeb \
  --priority 100 \
  --source-address-prefixes IP_PRIVADO_VM_WEB \
  --destination-port-ranges 5432 \
  --access Allow \
  --protocol Tcp
```

#### 2. Firewall (ufw) na VM DB bloqueando

**Na VM DB**:
```bash
sudo ufw status

# Se 5432 não estiver permitido:
sudo ufw allow 5432/tcp
sudo ufw reload
```

#### 3. PostgreSQL não está escutando em todas interfaces

**Na VM DB, verificar**:
```bash
sudo grep listen_addresses /etc/postgresql/14/main/postgresql.conf
```

**Deve ser**:
```
listen_addresses = '*'
```

**Se for 'localhost', mudar**:
```bash
sudo sed -i "s/listen_addresses = 'localhost'/listen_addresses = '*'/" /etc/postgresql/14/main/postgresql.conf
sudo systemctl restart postgresql
```

#### 4. pg_hba.conf não permite conexão da VM Web

**Na VM DB, verificar**:
```bash
sudo cat /etc/postgresql/14/main/pg_hba.conf
```

**Deve ter linha permitindo a subnet da VM Web**:
```
host    portaldb    django_user    10.0.1.0/24    scram-sha-256
```

**Se não tiver, adicionar**:
```bash
sudo tee -a /etc/postgresql/14/main/pg_hba.conf > /dev/null << EOF
host    portaldb    django_user    10.0.1.0/24    scram-sha-256
EOF

sudo systemctl restart postgresql
```

**Nota**: Substitua `10.0.1.0/24` pela subnet real da sua VM Web.

#### 5. Credenciais erradas no .env

**Na VM Web, verificar**:
```bash
sudo su - django
cd ~/apps/projeto_do_fim
cat .env | grep DATABASE_URL
```

**Formato correto**:
```
DATABASE_URL=postgres://django_user:SENHA@IP_PRIVADO_DB:5432/portaldb
```

**Testar credenciais manualmente**:
```bash
export DATABASE_URL="postgres://django_user:SENHA@IP_PRIVADO_DB:5432/portaldb"
psql $DATABASE_URL
```

#### 6. VNets não conectadas

Se as VMs estão em VNets diferentes, precisam de VNet Peering.

**Verificar**: Azure Portal → Virtual Networks → Peerings

**Criar peering**: Ver `AZURE_VM_SETUP_COMPLETO.md` seção 1.1

---

## 🔴 Static Files (CSS/JS/Imagens) não carregam

### Sintoma
Site abre mas sem estilos, ou erro 404 em arquivos `/static/`

### Soluções

#### 1. Coletar arquivos estáticos

```bash
sudo su - django
cd ~/apps/projeto_do_fim
source venv/bin/activate
python manage.py collectstatic --noinput
```

#### 2. Verificar permissões

```bash
ls -la /home/django/apps/projeto_do_fim/static_root/

# Se permissões estiverem erradas:
exit
sudo chown -R django:django /home/django/apps/projeto_do_fim/static_root
sudo chmod -R 755 /home/django/apps/projeto_do_fim/static_root
```

#### 3. Verificar configuração do Nginx

```bash
sudo cat /etc/nginx/sites-available/django | grep -A 4 "location /static"
```

**Deve ter**:
```nginx
location /static/ {
    alias /home/django/apps/projeto_do_fim/static_root/;
    expires 30d;
    add_header Cache-Control "public, immutable";
}
```

**Reiniciar Nginx**:
```bash
sudo nginx -t
sudo systemctl restart nginx
```

#### 4. Verificar settings.py

```bash
sudo su - django
cd ~/apps/projeto_do_fim
source venv/bin/activate
python manage.py shell
```

```python
from django.conf import settings
print(settings.STATIC_ROOT)
print(settings.STATIC_URL)
```

Deve mostrar:
```
STATIC_ROOT: /home/django/apps/projeto_do_fim/static_root
STATIC_URL: /static/
```

---

## 🔴 Erro de Permissão (Permission Denied)

### Sintoma
```
PermissionError: [Errno 13] Permission denied
```

### Solução Geral

```bash
# Corrigir todas as permissões
sudo chown -R django:django /home/django/apps/projeto_do_fim
sudo chmod -R 755 /home/django/apps/projeto_do_fim

# Logs
sudo chown -R django:django /var/log/django
sudo chmod -R 755 /var/log/django

# Media files
sudo chown django:django /home/django/apps/projeto_do_fim/media
sudo chmod 755 /home/django/apps/projeto_do_fim/media

# Reiniciar Gunicorn
sudo supervisorctl restart django
```

---

## 🔴 Gunicorn Timeout

### Sintoma
```
[CRITICAL] WORKER TIMEOUT
```

### Causa
Requests demorando muito (migrações, processamento pesado, etc.)

### Solução

**Aumentar timeout**:
```bash
sudo nano /etc/supervisor/conf.d/django.conf

# Mudar linha command para incluir timeout maior:
command=/home/django/apps/projeto_do_fim/venv/bin/gunicorn core.wsgi:application --bind 127.0.0.1:8000 --workers 4 --timeout 600

# Recarregar
sudo supervisorctl reread
sudo supervisorctl update
sudo supervisorctl restart django
```

---

## 🔴 Mudanças no código não aparecem

### Sintoma
Fiz `git pull` mas o site continua igual

### Solução

```bash
sudo su - django
cd ~/apps/projeto_do_fim
git pull origin main
source venv/bin/activate

# Se teve mudança em dependências
pip install -r requirements.txt

# Se teve mudança em models
python manage.py migrate

# Se teve mudança em static files
python manage.py collectstatic --noinput

# Voltar e reiniciar
exit
sudo supervisorctl restart django
sudo systemctl reload nginx  # Reload sem downtime
```

---

## 🔴 Nginx não inicia

### Sintoma
```
sudo systemctl status nginx
● nginx.service - A high performance web server and a reverse proxy server
   Loaded: loaded
   Active: failed
```

### Diagnóstico

```bash
# Ver erro específico
sudo nginx -t

# Ver logs
sudo tail -50 /var/log/nginx/error.log
sudo journalctl -u nginx -n 50
```

### Erros Comuns

#### "Address already in use"
```bash
# Verificar o que está usando porta 80
sudo netstat -plnt | grep :80

# Se for outro nginx ou apache
sudo systemctl stop apache2
sudo systemctl disable apache2

# Se for processo desconhecido, matar
sudo kill -9 PID
```

#### "nginx: [emerg] unknown directive"
```bash
# Erro de sintaxe no arquivo de configuração
sudo nginx -t

# Ver arquivo com erro
sudo nano /etc/nginx/sites-available/django

# Procurar por:
# - Diretivas erradas
# - Falta de ponto e vírgula
# - Variáveis não escapadas (usar \$host em vez de $host)
```

---

## 🔴 DEBUG=True em Produção

### Problema
DEBUG=True expõe informações sensíveis e desabilita WhiteNoise.

### Solução

```bash
sudo su - django
cd ~/apps/projeto_do_fim
nano .env

# Mudar para:
DEBUG=False

# Salvar e sair
exit
sudo supervisorctl restart django
```

**Com DEBUG=False, você precisa**:
- Ter `ALLOWED_HOSTS` configurado corretamente
- Ter coletado static files (`collectstatic`)
- Ter Nginx servindo arquivos estáticos

---

## 🛠️ Comandos de Diagnóstico Úteis

### Ver todos os logs em uma janela
```bash
# Terminal 1: Gunicorn
sudo tail -f /var/log/django/gunicorn.log

# Terminal 2: Nginx Error
sudo tail -f /var/log/nginx/django_error.log

# Terminal 3: Nginx Access
sudo tail -f /var/log/nginx/django_access.log
```

### Verificar processos
```bash
# Ver processos Gunicorn
ps aux | grep gunicorn

# Ver processos Nginx
ps aux | grep nginx

# Ver portas em uso
sudo netstat -plnt | grep -E ':(80|8000|443)'
```

### Testar configurações
```bash
# Nginx
sudo nginx -t

# Supervisor
sudo supervisorctl status

# Django settings
sudo su - django
cd ~/apps/projeto_do_fim
source venv/bin/activate
python manage.py check
python manage.py check --deploy
```

### Reiniciar tudo
```bash
sudo supervisorctl restart django
sudo systemctl restart nginx
```

---

## 📋 Checklist de Verificação Rápida

Quando algo não funciona, verifique nesta ordem:

1. **Serviços rodando?**
   ```bash
   sudo supervisorctl status django
   sudo systemctl status nginx
   ```

2. **Logs mostram erros?**
   ```bash
   sudo tail -100 /var/log/django/gunicorn.log
   sudo tail -100 /var/log/nginx/django_error.log
   ```

3. **Gunicorn escutando na porta 8000?**
   ```bash
   sudo netstat -plnt | grep 8000
   ```

4. **Nginx pode conectar ao Gunicorn?**
   ```bash
   curl http://127.0.0.1:8000
   ```

5. **Nginx respondendo?**
   ```bash
   curl http://127.0.0.1
   ```

6. **Firewall/NSG permitindo tráfego?**
   ```bash
   sudo ufw status
   # Verificar NSG no Azure Portal
   ```

7. **Banco de dados conectando?**
   ```bash
   psql -h IP_DB -U django_user -d portaldb
   ```

8. **Permissões corretas?**
   ```bash
   ls -la /home/django/apps/projeto_do_fim
   ```

---

## 🆘 Última Tentativa: Reiniciar do Zero

Se nada funcionar, reinicie os serviços do zero:

```bash
# 1. Parar tudo
sudo supervisorctl stop django
sudo systemctl stop nginx

# 2. Limpar processos órfãos
sudo pkill -9 gunicorn
sudo pkill -9 nginx

# 3. Verificar permissões
sudo chown -R django:django /home/django/apps/projeto_do_fim
sudo chown -R django:django /var/log/django

# 4. Recarregar configs
sudo supervisorctl reread
sudo supervisorctl update

# 5. Iniciar novamente
sudo systemctl start nginx
sudo supervisorctl start django

# 6. Verificar status
sudo supervisorctl status
sudo systemctl status nginx
```

Se ainda não funcionar, reveja a seção de configuração no `AZURE_VM_SETUP_COMPLETO.md`.
