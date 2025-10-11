# Scripts de Automação - Deploy Azure

Esta pasta contém scripts de automação para facilitar o deploy da aplicação Django/Wagtail em VMs Azure.

## 📜 Scripts Disponíveis

### 1. `configure_azure_nsg.sh`
**Onde executar**: No seu computador local (com Azure CLI instalado)

**O que faz**:
- Configura Network Security Groups (NSG) automaticamente
- Abre portas 22, 80, 443 na VM Web
- Abre porta 5432 na VM Database (apenas para VM Web)

**Como usar**:
```bash
./configure_azure_nsg.sh
```

Você precisará fornecer:
- Resource Group e nome do NSG da VM Web
- Nome da VM Web
- Resource Group e nome do NSG da VM Database

---

### 2. `setup_database.sh`
**Onde executar**: Na VM Database (via SSH)

**O que faz**:
- Instala PostgreSQL 14
- Configura para aceitar conexões remotas
- Cria banco de dados e usuário
- Configura firewall (ufw)
- Gera string de conexão

**Como usar**:
```bash
# 1. Conectar à VM Database via jump
ssh -J azureuser@IP_PUBLICO_WEB azureuser@IP_PRIVADO_DB

# 2. Baixar o script
wget https://raw.githubusercontent.com/DaylonCPinto/projeto_do_fim/main/scripts/setup_database.sh

# 3. Executar
chmod +x setup_database.sh
sudo ./setup_database.sh
```

**Importante**: Anote as credenciais mostradas ao final!

---

### 3. `setup_web.sh`
**Onde executar**: Na VM Web (via SSH)

**O que faz**:
- Instala Python 3.12, Nginx, Supervisor
- Clona o repositório
- Cria ambiente virtual
- Instala dependências
- Configura Gunicorn e Nginx
- Cria template do arquivo .env

**Como usar**:
```bash
# 1. Conectar à VM Web
ssh azureuser@IP_PUBLICO_WEB

# 2. Baixar o script
wget https://raw.githubusercontent.com/DaylonCPinto/projeto_do_fim/main/scripts/setup_web.sh

# 3. Executar
chmod +x setup_web.sh
sudo ./setup_web.sh
```

**Após o script**:
1. Configure o arquivo `.env`
2. Execute migrações
3. Colete static files
4. Inicie os serviços

---

### 4. `test_connectivity.sh`
**Onde executar**: Na VM Web (via SSH)

**O que faz**:
- Testa conectividade com a VM Database
- Verifica ping, porta, PostgreSQL
- Gera string de conexão para o .env
- Fornece sugestões de correção se houver problemas

**Como usar**:
```bash
# Na VM Web
wget https://raw.githubusercontent.com/DaylonCPinto/projeto_do_fim/main/scripts/test_connectivity.sh
chmod +x test_connectivity.sh
./test_connectivity.sh
```

---

## 🔄 Ordem de Execução Recomendada

### Fase 1: Configuração de Rede
```bash
# No seu computador local
./configure_azure_nsg.sh
```

### Fase 2: Configuração da VM Database
```bash
# Na VM Database (via SSH jump)
ssh -J azureuser@IP_WEB azureuser@IP_DB
sudo ./setup_database.sh
# ANOTE AS CREDENCIAIS!
```

### Fase 3: Configuração da VM Web
```bash
# Na VM Web
ssh azureuser@IP_WEB
sudo ./setup_web.sh

# Depois do script, configure .env
sudo su - django
cd ~/apps/projeto_do_fim
cp .env.template .env
nano .env
# Edite com as credenciais do banco

# Execute setup Django
source venv/bin/activate
python manage.py migrate
python manage.py collectstatic --noinput
python manage.py createsuperuser

# Volte para root e inicie serviços
exit
sudo supervisorctl start django
sudo systemctl restart nginx
```

### Fase 4: Testar Conectividade
```bash
# Na VM Web
./test_connectivity.sh
```

---

## 🛡️ Segurança

- Todos os scripts pedem confirmação antes de executar ações críticas
- Senhas não são armazenadas em arquivos de log
- Credenciais são salvas apenas em arquivos protegidos (chmod 600)
- Scripts verificam pré-requisitos antes de executar

---

## 🔧 Troubleshooting

Se algum script falhar:

1. **Verifique os logs**:
   - Para `setup_database.sh`: `/var/log/postgresql/`
   - Para `setup_web.sh`: `/var/log/django/`, `/var/log/nginx/`

2. **Verifique permissões**:
   ```bash
   ls -la script.sh  # Deve ser -rwxr-xr-x
   chmod +x script.sh  # Se necessário
   ```

3. **Verifique se está executando como root** (quando necessário):
   ```bash
   sudo ./script.sh
   ```

4. **Consulte o guia completo**:
   - `AZURE_VM_SETUP_COMPLETO.md` - Instruções detalhadas
   - `TROUBLESHOOTING_NGINX_GUNICORN.md` - Problemas específicos

---

## 📝 Notas

- Scripts foram testados em Ubuntu 22.04
- Azure CLI versão 2.x ou superior necessário para `configure_azure_nsg.sh`
- Conexão com internet necessária para baixar pacotes
- Scripts são idempotentes (podem ser executados múltiplas vezes)

---

## 🆘 Suporte

Para mais informações, consulte:
- **Guia Rápido**: `GUIA_RAPIDO_AZURE.md`
- **Guia Completo**: `AZURE_VM_SETUP_COMPLETO.md`
- **Troubleshooting**: `TROUBLESHOOTING_NGINX_GUNICORN.md`
