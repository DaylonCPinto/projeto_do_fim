# Guia de Deploy no Azure com PostgreSQL

Este documento descreve como fazer o deploy desta aplicação Django/Wagtail no Azure App Service com PostgreSQL.

## Pré-requisitos

1. Conta no Azure
2. Azure CLI instalado (`az`)
3. Repositório Git configurado

## Passo 1: Criar PostgreSQL Database no Azure

```bash
# Login no Azure
az login

# Criar Resource Group
az group create --name meu-projeto-rg --location eastus

# Criar servidor PostgreSQL
az postgres flexible-server create \
  --resource-group meu-projeto-rg \
  --name meu-projeto-db-server \
  --location eastus \
  --admin-user adminuser \
  --admin-password 'SenhaSegura123!' \
  --sku-name Standard_B1ms \
  --tier Burstable \
  --version 14

# Criar banco de dados
az postgres flexible-server db create \
  --resource-group meu-projeto-rg \
  --server-name meu-projeto-db-server \
  --database-name projeto_db

# Permitir conexões do Azure
az postgres flexible-server firewall-rule create \
  --resource-group meu-projeto-rg \
  --name meu-projeto-db-server \
  --rule-name AllowAzureServices \
  --start-ip-address 0.0.0.0 \
  --end-ip-address 0.0.0.0
```

## Passo 2: Criar Web App no Azure

```bash
# Criar App Service Plan
az appservice plan create \
  --name meu-projeto-plan \
  --resource-group meu-projeto-rg \
  --sku B1 \
  --is-linux

# Criar Web App
az webapp create \
  --resource-group meu-projeto-rg \
  --plan meu-projeto-plan \
  --name meu-projeto-webapp \
  --runtime "PYTHON:3.12"
```

## Passo 3: Configurar Variáveis de Ambiente

```bash
# Gerar uma SECRET_KEY segura
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"

# Configurar variáveis de ambiente no Azure
az webapp config appsettings set \
  --resource-group meu-projeto-rg \
  --name meu-projeto-webapp \
  --settings \
    SECRET_KEY='sua-secret-key-gerada' \
    DEBUG='False' \
    ALLOWED_HOSTS='meu-projeto-webapp.azurewebsites.net' \
    CSRF_TRUSTED_ORIGINS='https://meu-projeto-webapp.azurewebsites.net' \
    DATABASE_URL='postgres://adminuser:SenhaSegura123!@meu-projeto-db-server.postgres.database.azure.com:5432/projeto_db?sslmode=require' \
    WAGTAILADMIN_BASE_URL='https://meu-projeto-webapp.azurewebsites.net'
```

## Passo 4: Configurar Deploy do Git

```bash
# Configurar deployment do repositório Git
az webapp deployment source config \
  --resource-group meu-projeto-rg \
  --name meu-projeto-webapp \
  --repo-url https://github.com/seu-usuario/seu-repo \
  --branch main \
  --manual-integration

# OU usar deployment local do Git
az webapp deployment source config-local-git \
  --resource-group meu-projeto-rg \
  --name meu-projeto-webapp

# Adicionar remote do Azure ao Git
git remote add azure https://meu-projeto-webapp.scm.azurewebsites.net/meu-projeto-webapp.git

# Push para o Azure
git push azure main
```

## Passo 5: Executar Migrações

Após o deploy, você precisa executar as migrações do Django:

```bash
# Conectar via SSH ao container
az webapp ssh --resource-group meu-projeto-rg --name meu-projeto-webapp

# Dentro do container, executar:
python manage.py migrate
python manage.py collectstatic --noinput
python manage.py createsuperuser
```

### Migração de Dados do SQLite Local

Se você já tem dados no SQLite local e quer migrá-los para o PostgreSQL:

1. **Localmente, faça backup dos dados:**
   ```bash
   python manage.py dumpdata --natural-foreign --natural-primary \
       --exclude=contenttypes --exclude=auth.permission \
       --exclude=sessions --exclude=admin.logentry \
       --indent=2 > backup_data.json
   ```

2. **Faça commit e push do arquivo:**
   ```bash
   git add backup_data.json
   git commit -m "Add data backup for migration"
   git push
   ```

3. **No Azure (via SSH), carregue os dados:**
   ```bash
   python manage.py loaddata backup_data.json
   ```

4. **Remova o arquivo do repositório após migração:**
   ```bash
   git rm backup_data.json
   git commit -m "Remove data backup"
   git push
   ```

**Consulte `MIGRATION_GUIDE.md` para instruções detalhadas.**

## Passo 6: Configurar Arquivos Estáticos (Opcional - para Azure Storage)

Para usar Azure Blob Storage para arquivos estáticos e mídia:

1. Criar conta de storage:
```bash
az storage account create \
  --name meuprojeto storage \
  --resource-group meu-projeto-rg \
  --location eastus \
  --sku Standard_LRS

# Criar container para mídia
az storage container create \
  --name media \
  --account-name meuprojeto storage \
  --public-access blob
```

2. Adicionar variáveis de ambiente:
```bash
az webapp config appsettings set \
  --resource-group meu-projeto-rg \
  --name meu-projeto-webapp \
  --settings \
    AZURE_ACCOUNT_NAME='meuprojeto storage' \
    AZURE_ACCOUNT_KEY='sua-chave-de-acesso' \
    AZURE_CONTAINER='media'
```

## Verificar Logs

```bash
# Ver logs em tempo real
az webapp log tail --resource-group meu-projeto-rg --name meu-projeto-webapp

# Baixar logs
az webapp log download --resource-group meu-projeto-rg --name meu-projeto-webapp
```

## Comandos de Manutenção Úteis

```bash
# Reiniciar aplicação
az webapp restart --resource-group meu-projeto-rg --name meu-projeto-webapp

# Ver configurações da aplicação
az webapp config appsettings list --resource-group meu-projeto-rg --name meu-projeto-webapp

# Atualizar uma configuração específica
az webapp config appsettings set \
  --resource-group meu-projeto-rg \
  --name meu-projeto-webapp \
  --settings DEBUG='False'
```

## Configuração de SSL Personalizado (Opcional)

Se você quiser usar um domínio personalizado:

```bash
# Adicionar domínio personalizado
az webapp config hostname add \
  --resource-group meu-projeto-rg \
  --webapp-name meu-projeto-webapp \
  --hostname www.seudominio.com

# Ativar SSL/TLS gerenciado
az webapp config ssl create \
  --resource-group meu-projeto-rg \
  --name meu-projeto-webapp \
  --hostname www.seudominio.com
```

## Troubleshooting

### Erro de conexão com o banco de dados
- Verifique se as regras de firewall do PostgreSQL permitem conexões do Azure
- Verifique se a string DATABASE_URL está correta
- Certifique-se de que `sslmode=require` está na connection string

### Erro 500 - Internal Server Error
- Verifique os logs: `az webapp log tail`
- Certifique-se de que DEBUG=False e SECRET_KEY está configurada
- Verifique se as migrações foram executadas

### Arquivos estáticos não carregam
- Execute `python manage.py collectstatic --noinput`
- Verifique se STATIC_ROOT está configurado corretamente
- Whitenoise já está configurado no projeto para servir arquivos estáticos

## Segurança

✅ Este projeto já inclui as seguintes configurações de segurança:
- SECURE_SSL_REDIRECT em produção
- SECURE_HSTS_SECONDS configurado
- SESSION_COOKIE_SECURE em produção
- CSRF_COOKIE_SECURE em produção
- X_FRAME_OPTIONS = 'DENY'
- SECURE_CONTENT_TYPE_NOSNIFF
- Logging configurado para auditoria
- Whitenoise para arquivos estáticos comprimidos

## Backup do Banco de Dados

```bash
# Criar backup
az postgres flexible-server backup create \
  --resource-group meu-projeto-rg \
  --name meu-projeto-db-server

# Listar backups
az postgres flexible-server backup list \
  --resource-group meu-projeto-rg \
  --name meu-projeto-db-server
```

## Monitoramento

Habilite Application Insights para monitoramento:

```bash
az monitor app-insights component create \
  --app meu-projeto-insights \
  --location eastus \
  --resource-group meu-projeto-rg \
  --application-type web

# Conectar ao Web App
az webapp config appsettings set \
  --resource-group meu-projeto-rg \
  --name meu-projeto-webapp \
  --settings APPINSIGHTS_INSTRUMENTATIONKEY='sua-chave-do-insights'
```

## Recursos Adicionais

- [Azure App Service Documentation](https://docs.microsoft.com/azure/app-service/)
- [Azure PostgreSQL Documentation](https://docs.microsoft.com/azure/postgresql/)
- [Django Deployment Checklist](https://docs.djangoproject.com/en/stable/howto/deployment/checklist/)
