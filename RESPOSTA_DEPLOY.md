# Resposta: Guia Completo de Deploy Azure com 2 VMs

## 📋 Sua Situação

Você tem:
- ✅ 2 VMs Azure com Ubuntu 22.04 já criadas
- ✅ VM Web com IP público (para o site)
- ✅ VM Database sem IP público (para PostgreSQL)
- ❌ Nada instalado ainda
- ❌ Teve problemas com nginx e gunicorn antes

## 🎯 O Que Foi Preparado Para Você

Criei um conjunto completo de **guias e scripts de automação** para resolver exatamente seu problema e evitar configurações manuais futuras.

### 📚 Documentação Nova

1. **[DEPLOY_INDEX.md](DEPLOY_INDEX.md)** ⭐ COMECE POR AQUI
   - Índice completo de toda documentação
   - Ajuda você a encontrar o guia certo
   - FAQ com problemas comuns

2. **[GUIA_RAPIDO_AZURE.md](GUIA_RAPIDO_AZURE.md)** ⭐ SEU GUIA PRINCIPAL
   - Passo a passo objetivo e direto
   - Comandos prontos para copiar e colar
   - Checklist de verificação
   - Tempo estimado: ~55 minutos

3. **[AZURE_VM_SETUP_COMPLETO.md](AZURE_VM_SETUP_COMPLETO.md)** 📖 REFERÊNCIA COMPLETA
   - Explicações detalhadas de cada passo
   - Todas as configurações de rede (VNet, NSG, firewall)
   - Alternativas e opções
   - Seção de troubleshooting integrada

4. **[TROUBLESHOOTING_NGINX_GUNICORN.md](TROUBLESHOOTING_NGINX_GUNICORN.md)** 🔧 RESOLUÇÃO DE PROBLEMAS
   - Soluções específicas para erros 502 Bad Gateway
   - Problemas de conexão com PostgreSQL
   - Static files não carregando
   - Permissões e configurações
   - Comandos de diagnóstico

### 🤖 Scripts de Automação

Todos em [scripts/](scripts/) - **Prontos para usar!**

1. **`configure_azure_nsg.sh`**
   - Onde: Seu computador local (Azure CLI)
   - Configura firewall/NSG automaticamente
   - Abre portas corretas em cada VM

2. **`setup_database.sh`**
   - Onde: VM Database (via SSH)
   - Instala PostgreSQL 14
   - Configura conexões remotas
   - Cria banco e usuário
   - **Evita todos os problemas de configuração manual!**

3. **`setup_web.sh`**
   - Onde: VM Web (via SSH)
   - Instala Python 3.12, Nginx, Supervisor
   - Clona o repositório
   - Configura Gunicorn corretamente
   - Configura Nginx corretamente
   - **Evita problemas com nginx e gunicorn!**

4. **`test_connectivity.sh`**
   - Onde: VM Web (via SSH)
   - Testa conectividade com VM Database
   - Verifica firewall, NSG, PostgreSQL
   - Gera string de conexão para .env

## 🚀 Lista Detalhada de Passos

### FASE 1: Configuração de Rede no Azure (10 min)

#### 1.1 Verificar se VNets estão conectadas

Se suas VMs estão em VNets diferentes, crie VNet Peering:

**Via Azure Portal:**
1. Acesse "Virtual networks"
2. Selecione a VNet da VM Web
3. Vá em "Peerings" → "+ Add"
4. Configure peering para a VNet da VM Database
5. Repita o processo na direção oposta

**Via Azure CLI** (mais rápido):
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

#### 1.2 Configurar NSG (Firewall)

**Opção A: Script Automático** (RECOMENDADO)
```bash
# No seu computador com Azure CLI
cd scripts/
./configure_azure_nsg.sh
```

**Opção B: Azure Portal Manual**

Para VM Web - Permitir da Internet:
- Porta 22 (SSH)
- Porta 80 (HTTP)
- Porta 443 (HTTPS)

Para VM Database - Permitir APENAS da VM Web:
- Porta 5432 (PostgreSQL) vindo do IP privado da VM Web

---

### FASE 2: Configurar VM Database (15 min)

#### 2.1 Conectar à VM Database

Como ela não tem IP público, use SSH Jump da VM Web:

```bash
# Método direto
ssh -J azureuser@IP_PUBLICO_VM_WEB azureuser@IP_PRIVADO_VM_DB

# Ou configure ~/.ssh/config para facilitar (recomendado):
cat >> ~/.ssh/config << EOF
Host azure-web
    HostName IP_PUBLICO_VM_WEB
    User azureuser

Host azure-db
    HostName IP_PRIVADO_VM_DB
    User azureuser
    ProxyJump azure-web
EOF

# Depois conecte simplesmente:
ssh azure-db
```

#### 2.2 Executar Script de Setup

```bash
# Na VM Database, baixar o script
wget https://raw.githubusercontent.com/DaylonCPinto/projeto_do_fim/main/scripts/setup_database.sh

# Tornar executável
chmod +x setup_database.sh

# Executar
sudo ./setup_database.sh
```

O script irá pedir:
- Nome do banco [portaldb]
- Usuário [django_user]
- **Senha** (escolha uma senha forte e ANOTE!)
- Subnet da VM Web (ex: 10.0.1.0/24)

**⚠️ IMPORTANTE**: Ao final, o script mostra as credenciais. ANOTE TUDO!

---

### FASE 3: Configurar VM Web (20 min)

#### 3.1 Conectar à VM Web

```bash
ssh azureuser@IP_PUBLICO_VM_WEB
```

#### 3.2 Executar Script de Setup

```bash
# Baixar o script
wget https://raw.githubusercontent.com/DaylonCPinto/projeto_do_fim/main/scripts/setup_web.sh

# Tornar executável
chmod +x setup_web.sh

# Executar
sudo ./setup_web.sh
```

O script irá:
- Instalar Python 3.12, pip, venv
- Instalar Nginx e Supervisor
- Clonar seu repositório
- Criar ambiente virtual
- Instalar dependências
- Configurar Gunicorn e Nginx corretamente
- Criar template do .env

#### 3.3 Configurar Arquivo .env

```bash
# Mudar para usuário django
sudo su - django

# Navegar até o projeto
cd ~/apps/projeto_do_fim

# Copiar template
cp .env.template .env

# Editar
nano .env
```

Configure assim:
```bash
# Gerar SECRET_KEY nova (rode este comando primeiro):
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"

# Cole a chave gerada:
SECRET_KEY=chave_gerada_acima
DEBUG=False
ALLOWED_HOSTS=SEU_IP_PUBLICO,seu-dominio.com
CSRF_TRUSTED_ORIGINS=https://SEU_IP_PUBLICO,https://seu-dominio.com

# Use as credenciais da VM Database:
DATABASE_URL=postgres://django_user:SENHA_DO_DB@IP_PRIVADO_DB:5432/portaldb

WAGTAILADMIN_BASE_URL=https://SEU_IP_PUBLICO
```

Salve com `Ctrl+O`, `Enter`, `Ctrl+X`

#### 3.4 Preparar Aplicação Django

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

#### 3.5 Iniciar Serviços

```bash
# Voltar para usuário root
exit

# Recarregar supervisor
sudo supervisorctl reread
sudo supervisorctl update

# Iniciar Gunicorn
sudo supervisorctl start django

# Verificar status
sudo supervisorctl status django

# Reiniciar Nginx
sudo systemctl restart nginx
sudo systemctl status nginx
```

---

### FASE 4: Testar e Verificar (5 min)

#### 4.1 Testar Conectividade

```bash
# Na VM Web, baixar script de teste
wget https://raw.githubusercontent.com/DaylonCPinto/projeto_do_fim/main/scripts/test_connectivity.sh
chmod +x test_connectivity.sh
./test_connectivity.sh
```

O script testa:
- Ping entre VMs
- Porta PostgreSQL (5432)
- Conexão com banco de dados
- Gera string de conexão correta

#### 4.2 Verificar Logs

```bash
# Ver logs do Gunicorn
sudo tail -f /var/log/django/gunicorn.log

# Ver logs do Nginx
sudo tail -f /var/log/nginx/django_error.log

# Status dos serviços
sudo supervisorctl status
sudo systemctl status nginx
```

#### 4.3 Testar no Navegador

Abra o navegador e acesse:
- **Site**: `http://SEU_IP_PUBLICO`
- **Admin Django**: `http://SEU_IP_PUBLICO/admin/`
- **Wagtail CMS**: `http://SEU_IP_PUBLICO/cms/`

Se tudo aparecer com CSS/JS funcionando: **✅ SUCESSO!**

---

## 🔧 Problemas Comuns e Soluções

### ❌ Erro 502 Bad Gateway

**Causa**: Gunicorn não está rodando ou não consegue conectar com Nginx.

**Solução**:
```bash
# Verificar status
sudo supervisorctl status django

# Ver logs
sudo tail -100 /var/log/django/gunicorn.log

# Se não estiver rodando, iniciar
sudo supervisorctl start django

# Se continuar com erro, verificar configuração
cat /etc/supervisor/conf.d/django.conf

# Reiniciar tudo
sudo supervisorctl restart django
sudo systemctl restart nginx
```

**Detalhes**: Veja [TROUBLESHOOTING_NGINX_GUNICORN.md - Erro 502](TROUBLESHOOTING_NGINX_GUNICORN.md#🔴-erro-502-bad-gateway)

---

### ❌ Erro de Conexão com Banco de Dados

**Causa**: NSG bloqueado, firewall, ou credenciais erradas.

**Solução**:
```bash
# Testar conexão da VM Web → VM DB
psql -h IP_PRIVADO_DB -U django_user -d portaldb

# Se falhar, verificar:

# 1. NSG da VM DB permite porta 5432?
# Verificar no Azure Portal: Network Security Groups

# 2. Firewall na VM DB permite?
# Na VM DB:
sudo ufw status
sudo ufw allow 5432/tcp

# 3. PostgreSQL está configurado para aceitar conexões remotas?
# Na VM DB:
sudo grep listen_addresses /etc/postgresql/14/main/postgresql.conf
# Deve ser: listen_addresses = '*'

# 4. pg_hba.conf permite a subnet?
sudo cat /etc/postgresql/14/main/pg_hba.conf
# Deve ter linha com sua subnet
```

**Detalhes**: Veja [TROUBLESHOOTING_NGINX_GUNICORN.md - Erro de Conexão](TROUBLESHOOTING_NGINX_GUNICORN.md#🔴-erro-de-conexão-com-banco-de-dados)

---

### ❌ CSS e JavaScript não carregam

**Causa**: Arquivos estáticos não coletados ou permissões erradas.

**Solução**:
```bash
# Coletar static files novamente
sudo su - django
cd ~/apps/projeto_do_fim
source venv/bin/activate
python manage.py collectstatic --noinput

# Corrigir permissões
exit
sudo chown -R django:django /home/django/apps/projeto_do_fim/static_root
sudo chmod -R 755 /home/django/apps/projeto_do_fim/static_root

# Reiniciar Nginx
sudo systemctl restart nginx
```

**Detalhes**: Veja [TROUBLESHOOTING_NGINX_GUNICORN.md - Static Files](TROUBLESHOOTING_NGINX_GUNICORN.md#🔴-static-files-cssjsimagens-não-carregam)

---

## 🔄 Como Fazer Deploy de Atualizações

Quando você fizer mudanças no código:

```bash
# 1. Conectar à VM Web
ssh azureuser@IP_PUBLICO_WEB

# 2. Mudar para usuário django
sudo su - django
cd ~/apps/projeto_do_fim

# 3. Atualizar código
git pull origin main

# 4. Ativar ambiente virtual
source venv/bin/activate

# 5. Atualizar dependências (se mudaram)
pip install -r requirements.txt

# 6. Executar migrações (se houver)
python manage.py migrate

# 7. Coletar static files (se mudaram)
python manage.py collectstatic --noinput

# 8. Voltar para root
exit

# 9. Reiniciar Gunicorn
sudo supervisorctl restart django

# 10. Verificar status
sudo supervisorctl status django
```

---

## 🔒 Adicionar SSL/HTTPS (Opcional)

Se você tem um domínio apontando para sua VM Web:

```bash
# Na VM Web
sudo apt install -y certbot python3-certbot-nginx

# Obter certificado (substitua seu-dominio.com)
sudo certbot --nginx -d seu-dominio.com -d www.seu-dominio.com

# Atualizar .env
sudo su - django
cd ~/apps/projeto_do_fim
nano .env

# Atualizar:
ALLOWED_HOSTS=IP_PUBLICO,seu-dominio.com,www.seu-dominio.com
CSRF_TRUSTED_ORIGINS=https://seu-dominio.com,https://www.seu-dominio.com
WAGTAILADMIN_BASE_URL=https://seu-dominio.com

# Salvar e sair
exit

# Reiniciar aplicação
sudo supervisorctl restart django
```

---

## ✅ Checklist Final de Verificação

Antes de considerar o deploy completo:

### Rede
- [ ] VNets conectadas (se necessário)
- [ ] NSG da VM Web permite 22, 80, 443
- [ ] NSG da VM DB permite 5432 apenas da VM Web
- [ ] Consegue SSH na VM Web
- [ ] Consegue SSH na VM DB via jump

### VM Database
- [ ] PostgreSQL instalado e rodando
- [ ] Banco `portaldb` criado
- [ ] Usuário `django_user` criado
- [ ] VM Web consegue conectar ao PostgreSQL
- [ ] Credenciais anotadas em local seguro

### VM Web
- [ ] Python 3.12 instalado
- [ ] Nginx instalado e rodando
- [ ] Supervisor instalado e rodando
- [ ] Repositório clonado
- [ ] .env configurado corretamente
- [ ] Migrações executadas sem erros
- [ ] Static files coletados
- [ ] Superusuário criado
- [ ] Gunicorn rodando via Supervisor

### Testes
- [ ] Site abre no navegador
- [ ] Admin Django funciona
- [ ] Wagtail CMS funciona
- [ ] CSS e JavaScript carregam
- [ ] Sem erro 502 Bad Gateway
- [ ] Logs sem erros críticos

---

## 📊 Comandos Úteis para o Dia a Dia

### Ver Logs em Tempo Real
```bash
# Gunicorn
sudo tail -f /var/log/django/gunicorn.log

# Nginx
sudo tail -f /var/log/nginx/django_error.log
sudo tail -f /var/log/nginx/django_access.log

# PostgreSQL (na VM DB)
sudo tail -f /var/log/postgresql/postgresql-14-main.log
```

### Gerenciar Serviços
```bash
# Gunicorn
sudo supervisorctl status django
sudo supervisorctl start django
sudo supervisorctl stop django
sudo supervisorctl restart django

# Nginx
sudo systemctl status nginx
sudo systemctl restart nginx
sudo systemctl reload nginx  # Sem downtime
```

### Comandos Django Úteis
```bash
sudo su - django
cd ~/apps/projeto_do_fim
source venv/bin/activate

# Ver configurações
python manage.py check
python manage.py check --deploy

# Criar usuário
python manage.py createsuperuser

# Limpar sessões antigas
python manage.py clearsessions

# Ver informações do banco
python manage.py dbshell
```

---

## 📚 Onde Encontrar Mais Informações

- **[DEPLOY_INDEX.md](DEPLOY_INDEX.md)** - Índice completo da documentação
- **[GUIA_RAPIDO_AZURE.md](GUIA_RAPIDO_AZURE.md)** - Referência rápida
- **[AZURE_VM_SETUP_COMPLETO.md](AZURE_VM_SETUP_COMPLETO.md)** - Guia detalhado
- **[TROUBLESHOOTING_NGINX_GUNICORN.md](TROUBLESHOOTING_NGINX_GUNICORN.md)** - Solução de problemas
- **[scripts/README.md](scripts/README.md)** - Documentação dos scripts

---

## 💡 Resumo - Por Que Isso Evita Problemas?

### Scripts Automatizam:
1. ✅ Instalação correta do PostgreSQL com configurações remotas
2. ✅ Configuração correta do Gunicorn (workers, timeout, bind)
3. ✅ Configuração correta do Nginx (proxy, static files, timeouts)
4. ✅ Permissões corretas de arquivos e diretórios
5. ✅ Supervisor para gerenciar Gunicorn automaticamente
6. ✅ Logs em locais padronizados

### Documentação Cobre:
1. ✅ Todos os cenários de erro comum (502, conexão DB, static files)
2. ✅ Comandos de diagnóstico para cada problema
3. ✅ Soluções passo a passo testadas
4. ✅ Checklist completo de verificação

### Resultado:
- 🚀 Deploy mais rápido (55 min vs várias horas)
- 🛡️ Menos erros (configuração automatizada)
- 🔧 Fácil de debugar (logs padronizados + guia troubleshooting)
- 🔄 Fácil de atualizar (processo documentado)

---

## 🎉 Pronto!

Siga os passos nesta ordem:
1. Ler [GUIA_RAPIDO_AZURE.md](GUIA_RAPIDO_AZURE.md)
2. Executar os scripts nas VMs
3. Se tiver problemas, consultar [TROUBLESHOOTING_NGINX_GUNICORN.md](TROUBLESHOOTING_NGINX_GUNICORN.md)

**Tempo estimado total**: ~55 minutos do início ao fim.

Boa sorte com o deploy! 🚀
