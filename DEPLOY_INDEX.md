# 📚 Índice de Documentação de Deploy

Este documento ajuda você a encontrar o guia certo para o seu cenário de deploy.

## 🎯 Qual guia devo usar?

### Cenário 1: Tenho 2 VMs Azure prontas (Web + Database)
**✅ Esta é a sua situação atual!**

Use nesta ordem:
1. 📘 **[GUIA_RAPIDO_AZURE.md](GUIA_RAPIDO_AZURE.md)** ⭐ COMECE AQUI
   - Guia objetivo e direto ao ponto
   - Lista de comandos essenciais
   - Checklist de verificação
   - ~10 páginas

2. 📗 **[AZURE_VM_SETUP_COMPLETO.md](AZURE_VM_SETUP_COMPLETO.md)** ⭐ GUIA COMPLETO
   - Passo a passo detalhado
   - Explicações de cada comando
   - Configurações completas de rede
   - Scripts de automação incluídos
   - ~40 páginas

3. 🤖 **[scripts/](scripts/)**
   - Scripts de automação prontos para usar
   - `configure_azure_nsg.sh` - Configurar firewall/NSG
   - `setup_database.sh` - Instalar e configurar PostgreSQL
   - `setup_web.sh` - Instalar Django, Nginx, Gunicorn
   - `test_connectivity.sh` - Testar conectividade entre VMs

4. 🔧 **[TROUBLESHOOTING_NGINX_GUNICORN.md](TROUBLESHOOTING_NGINX_GUNICORN.md)**
   - Soluções para erros 502 Bad Gateway
   - Problemas de conexão com banco de dados
   - Problemas com static files
   - Guia de diagnóstico completo

---

### Cenário 2: Quero criar VMs do zero no Azure
**Use Azure CLI para criar toda a infraestrutura**

📙 **[AZURE_DEPLOYMENT_VM.md](AZURE_DEPLOYMENT_VM.md)**
- Criação de Resource Groups
- Criação de VNets e Subnets
- Criação de NSGs
- Criação de VMs
- Configuração completa da infraestrutura

---

### Cenário 3: Quero usar Azure App Service (PaaS)
**Opção mais simples, sem gerenciar VMs**

📕 **[AZURE_DEPLOYMENT.md](AZURE_DEPLOYMENT.md)**
- Deploy em App Service
- Configuração de PostgreSQL gerenciado
- Deploy via Git
- Mais fácil, mas menos flexível

---

## 🚀 Início Rápido (para quem já tem VMs)

### Fase 1: Preparação (5 min)
1. Anote os IPs das suas VMs (público da Web, privado da DB)
2. Verifique se consegue SSH na VM Web
3. Baixe os scripts de automação

### Fase 2: Configuração de Rede (10 min)
```bash
# No seu computador local (com Azure CLI)
cd scripts/
./configure_azure_nsg.sh
```

### Fase 3: Setup Database (15 min)
```bash
# Via SSH Jump da VM Web
ssh -J azureuser@IP_WEB azureuser@IP_DB
wget https://raw.githubusercontent.com/DaylonCPinto/projeto_do_fim/main/scripts/setup_database.sh
chmod +x setup_database.sh
sudo ./setup_database.sh
# ANOTE AS CREDENCIAIS!
```

### Fase 4: Setup Web (20 min)
```bash
# Na VM Web
ssh azureuser@IP_WEB
wget https://raw.githubusercontent.com/DaylonCPinto/projeto_do_fim/main/scripts/setup_web.sh
chmod +x setup_web.sh
sudo ./setup_web.sh

# Configurar .env
sudo su - django
cd ~/apps/projeto_do_fim
cp .env.template .env
nano .env  # Edite com credenciais do DB

# Preparar Django
source venv/bin/activate
python manage.py migrate
python manage.py collectstatic --noinput
python manage.py createsuperuser

# Iniciar serviços
exit
sudo supervisorctl start django
sudo systemctl restart nginx
```

### Fase 5: Verificação (5 min)
```bash
# Na VM Web
wget https://raw.githubusercontent.com/DaylonCPinto/projeto_do_fim/main/scripts/test_connectivity.sh
chmod +x test_connectivity.sh
./test_connectivity.sh

# Acessar no navegador
http://SEU_IP_PUBLICO
```

**Tempo Total Estimado: ~55 minutos**

---

## 📖 Documentação por Tópico

### Rede e Conectividade
- **VNet Peering**: [AZURE_VM_SETUP_COMPLETO.md](AZURE_VM_SETUP_COMPLETO.md#passo-1-configuração-de-rede-no-azure-portal) - Seção 1.1
- **NSG Configuration**: [AZURE_VM_SETUP_COMPLETO.md](AZURE_VM_SETUP_COMPLETO.md#12-configurar-nsg-da-vm-web) - Seções 1.2 e 1.3
- **SSH Jump Host**: [AZURE_VM_SETUP_COMPLETO.md](AZURE_VM_SETUP_COMPLETO.md#21-conectar-à-vm-database-via-ssh-jump) - Seção 2.1

### PostgreSQL
- **Instalação**: [scripts/setup_database.sh](scripts/setup_database.sh)
- **Configuração Manual**: [AZURE_VM_SETUP_COMPLETO.md](AZURE_VM_SETUP_COMPLETO.md#23-configuração-manual-do-postgresql-alternativa) - Seção 2.3
- **Troubleshooting**: [TROUBLESHOOTING_NGINX_GUNICORN.md](TROUBLESHOOTING_NGINX_GUNICORN.md#🔴-erro-de-conexão-com-banco-de-dados)

### Nginx
- **Instalação e Configuração**: [scripts/setup_web.sh](scripts/setup_web.sh)
- **Problemas 502**: [TROUBLESHOOTING_NGINX_GUNICORN.md](TROUBLESHOOTING_NGINX_GUNICORN.md#🔴-erro-502-bad-gateway)
- **Static Files**: [TROUBLESHOOTING_NGINX_GUNICORN.md](TROUBLESHOOTING_NGINX_GUNICORN.md#🔴-static-files-cssjsimagens-não-carregam)

### Gunicorn
- **Configuração com Supervisor**: [AZURE_VM_SETUP_COMPLETO.md](AZURE_VM_SETUP_COMPLETO.md#35-iniciar-serviços) - Seção 3.5
- **Problemas de Timeout**: [TROUBLESHOOTING_NGINX_GUNICORN.md](TROUBLESHOOTING_NGINX_GUNICORN.md#🔴-gunicorn-timeout)
- **Não inicia**: [TROUBLESHOOTING_NGINX_GUNICORN.md](TROUBLESHOOTING_NGINX_GUNICORN.md#🔴-erro-502-bad-gateway)

### Segurança
- **SSL com Let's Encrypt**: [AZURE_VM_SETUP_COMPLETO.md](AZURE_VM_SETUP_COMPLETO.md#passo-5-ssl-com-lets-encrypt-opcional) - Passo 5
- **Firewall (ufw)**: [scripts/setup_database.sh](scripts/setup_database.sh) e [scripts/setup_web.sh](scripts/setup_web.sh)
- **Security Checklist**: [SECURITY_CHECKLIST.md](SECURITY_CHECKLIST.md)

### Manutenção
- **Deploy de Atualizações**: [GUIA_RAPIDO_AZURE.md](GUIA_RAPIDO_AZURE.md#🔄-atualizar-código-deploy)
- **Backup**: [AZURE_VM_SETUP_COMPLETO.md](AZURE_VM_SETUP_COMPLETO.md#📦-backup-e-restauração)
- **Logs**: [GUIA_RAPIDO_AZURE.md](GUIA_RAPIDO_AZURE.md#📊-comandos-úteis)

---

## 🔧 Scripts de Automação

Todos os scripts estão em [scripts/](scripts/) com documentação completa.

| Script | Executa Onde | O Que Faz |
|--------|--------------|-----------|
| `configure_azure_nsg.sh` | Seu computador | Configura NSG no Azure |
| `setup_database.sh` | VM Database | Instala PostgreSQL |
| `setup_web.sh` | VM Web | Instala Django+Nginx |
| `test_connectivity.sh` | VM Web | Testa conexão com DB |

---

## ❓ FAQ - Perguntas Frequentes

### Como conecto na VM Database se ela não tem IP público?
Use SSH Jump Host através da VM Web:
```bash
ssh -J azureuser@IP_PUBLICO_WEB azureuser@IP_PRIVADO_DB
```

### Erro 502 Bad Gateway, o que fazer?
1. Verifique se Gunicorn está rodando: `sudo supervisorctl status django`
2. Veja os logs: `sudo tail -f /var/log/django/gunicorn.log`
3. Consulte: [TROUBLESHOOTING_NGINX_GUNICORN.md](TROUBLESHOOTING_NGINX_GUNICORN.md#🔴-erro-502-bad-gateway)

### CSS e JavaScript não carregam, por quê?
1. Execute: `python manage.py collectstatic --noinput`
2. Verifique permissões: `sudo chown -R django:django /home/django/apps/projeto_do_fim/static_root`
3. Consulte: [TROUBLESHOOTING_NGINX_GUNICORN.md](TROUBLESHOOTING_NGINX_GUNICORN.md#🔴-static-files-cssjsimagens-não-carregam)

### Como atualizar o código depois do deploy?
```bash
cd ~/apps/projeto_do_fim
git pull origin main
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --noinput
exit
sudo supervisorctl restart django
```

### Posso usar SSL/HTTPS?
Sim! Se você tem um domínio, veja: [AZURE_VM_SETUP_COMPLETO.md - Passo 5: SSL](AZURE_VM_SETUP_COMPLETO.md#passo-5-ssl-com-lets-encrypt-opcional)

---

## ✅ Checklist Completo

### Antes de começar:
- [ ] Tenho 2 VMs Azure com Ubuntu 22.04
- [ ] VM Web tem IP público
- [ ] VM Database tem apenas IP privado
- [ ] Consigo SSH na VM Web
- [ ] Tenho Azure CLI instalado (para configurar NSG)

### Durante o setup:
- [ ] NSGs configurados (portas abertas)
- [ ] PostgreSQL instalado na VM DB
- [ ] Credenciais do DB anotadas
- [ ] Nginx e Gunicorn instalados na VM Web
- [ ] Arquivo .env configurado
- [ ] Migrações executadas
- [ ] Static files coletados
- [ ] Superusuário criado
- [ ] Serviços iniciados

### Verificação final:
- [ ] Site abre no navegador
- [ ] Admin funciona (/admin/)
- [ ] Wagtail CMS funciona (/cms/)
- [ ] CSS e JS carregam corretamente
- [ ] Sem erros 502 no Nginx
- [ ] Logs sem erros críticos
- [ ] Conexão com banco funciona

---

## 📞 Precisa de Ajuda?

1. **Verifique os logs primeiro**:
   - `/var/log/django/gunicorn.log`
   - `/var/log/nginx/django_error.log`

2. **Execute o teste de conectividade**:
   ```bash
   ./scripts/test_connectivity.sh
   ```

3. **Consulte o troubleshooting**:
   - [TROUBLESHOOTING_NGINX_GUNICORN.md](TROUBLESHOOTING_NGINX_GUNICORN.md)

4. **Revise o guia completo**:
   - [AZURE_VM_SETUP_COMPLETO.md](AZURE_VM_SETUP_COMPLETO.md)

---

## 🎓 Documentação Adicional

- [README.md](README.md) - Visão geral do projeto
- [SECURITY_CHECKLIST.md](SECURITY_CHECKLIST.md) - Checklist de segurança
- [FEATURES_GUIDE.md](FEATURES_GUIDE.md) - Guia de funcionalidades
- [PROJECT_STATUS.md](PROJECT_STATUS.md) - Status do projeto

---

**Última atualização**: Este guia foi criado especificamente para facilitar o deploy em 2 VMs Azure já existentes, minimizando configurações manuais e evitando problemas comuns com Nginx e Gunicorn.
