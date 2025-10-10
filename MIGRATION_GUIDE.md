# Guia de Migração de Dados - SQLite para PostgreSQL

Este guia explica como migrar seus dados do SQLite local para o PostgreSQL no Azure sem perder nenhuma informação.

## Pré-requisitos

- Banco de dados SQLite local com dados (`db.sqlite3`)
- PostgreSQL configurado no Azure (seguindo o `AZURE_DEPLOYMENT.md`)
- Ambiente virtual Python ativado
- Todas as dependências instaladas

## Passo 1: Backup dos Dados do SQLite

```bash
# Navegue até o diretório do projeto
cd /caminho/para/projeto_do_fim

# Ative o ambiente virtual
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows

# Faça o dump de todos os dados do SQLite
python manage.py dumpdata --natural-foreign --natural-primary \
    --exclude=contenttypes --exclude=auth.permission \
    --exclude=sessions --exclude=admin.logentry \
    --indent=2 > backup_data.json

# Faça também um backup do arquivo SQLite
cp db.sqlite3 db.sqlite3.backup
```

**Importante:** O arquivo `backup_data.json` contém todos os seus dados. Guarde-o em local seguro!

## Passo 2: Configurar PostgreSQL no .env

Crie ou edite o arquivo `.env` com as configurações do PostgreSQL:

```env
SECRET_KEY=sua-secret-key-segura
DEBUG=False
ALLOWED_HOSTS=seu-dominio.azurewebsites.net,localhost,127.0.0.1

# PostgreSQL do Azure
DATABASE_URL=postgres://usuario@servidor:senha@servidor.postgres.database.azure.com:5432/nome_do_banco?sslmode=require

CSRF_TRUSTED_ORIGINS=https://seu-dominio.azurewebsites.net,http://localhost:8000
WAGTAILADMIN_BASE_URL=https://seu-dominio.azurewebsites.net
```

## Passo 3: Executar Migrações no PostgreSQL

```bash
# Com o DATABASE_URL configurado, execute as migrações
python manage.py migrate

# Isso criará todas as tabelas no PostgreSQL
```

## Passo 4: Carregar os Dados no PostgreSQL

```bash
# Carregue o backup JSON no PostgreSQL
python manage.py loaddata backup_data.json

# Se houver erros, você pode tentar carregar por partes:
# python manage.py loaddata --app accounts backup_data.json
# python manage.py loaddata --app content backup_data.json
```

## Passo 5: Verificar os Dados

```bash
# Verifique se os dados foram importados corretamente
python manage.py shell

# No shell do Django:
>>> from django.contrib.auth.models import User
>>> from content.models import ArticlePage
>>> print(f"Usuários: {User.objects.count()}")
>>> print(f"Artigos: {ArticlePage.objects.count()}")
>>> exit()
```

## Passo 6: Criar Superusuário (se necessário)

Se você não tinha um superusuário no SQLite ou se ele não foi migrado:

```bash
python manage.py createsuperuser
```

## Passo 7: Coletar Arquivos Estáticos

```bash
python manage.py collectstatic --noinput
```

## Solução de Problemas

### Erro: "Could not load contenttypes"
Se você encontrar erros relacionados a `contenttypes`, tente:

```bash
# Primeiro, execute apenas as migrações
python manage.py migrate --run-syncdb

# Depois, carregue os dados
python manage.py loaddata backup_data.json
```

### Erro: "Duplicate key value"
Se houver conflitos de chaves primárias:

```bash
# Limpe o banco PostgreSQL e tente novamente
python manage.py flush --noinput
python manage.py migrate
python manage.py loaddata backup_data.json
```

### Arquivos de Mídia (Imagens, etc.)
Os arquivos de mídia (uploads) não são incluídos no dump JSON. Você precisa copiar manualmente:

```bash
# Copie a pasta media para o servidor ou Azure Storage
# Se estiver usando Azure, considere usar Azure Blob Storage para arquivos de mídia
```

## Migração para Produção no Azure

Se você estiver migrando diretamente para o Azure:

1. **Faça o dump local:**
   ```bash
   python manage.py dumpdata --natural-foreign --natural-primary \
       --exclude=contenttypes --exclude=auth.permission \
       --exclude=sessions --exclude=admin.logentry \
       --indent=2 > backup_data.json
   ```

2. **Faça o commit do arquivo:**
   ```bash
   git add backup_data.json
   git commit -m "Add data backup for migration"
   git push
   ```

3. **No Azure (via SSH ou Azure Portal):**
   ```bash
   cd /home/site/wwwroot
   python manage.py migrate
   python manage.py loaddata backup_data.json
   python manage.py collectstatic --noinput
   python manage.py createsuperuser
   ```

4. **Remova o arquivo de backup do repositório:**
   ```bash
   git rm backup_data.json
   git commit -m "Remove data backup file"
   git push
   ```

## Script Automático de Migração

Para facilitar, você pode usar este script:

```bash
#!/bin/bash
# migrate_to_postgres.sh

echo "=== Migração SQLite → PostgreSQL ==="
echo ""

# 1. Backup SQLite
echo "1. Fazendo backup do SQLite..."
cp db.sqlite3 db.sqlite3.backup.$(date +%Y%m%d_%H%M%S)
python manage.py dumpdata --natural-foreign --natural-primary \
    --exclude=contenttypes --exclude=auth.permission \
    --exclude=sessions --exclude=admin.logentry \
    --indent=2 > backup_data.json

echo "✓ Backup criado: backup_data.json"
echo ""

# 2. Verificar DATABASE_URL
if [ -z "$DATABASE_URL" ]; then
    echo "❌ ERRO: DATABASE_URL não está configurado no .env"
    exit 1
fi

echo "2. DATABASE_URL detectado"
echo ""

# 3. Executar migrações
echo "3. Executando migrações no PostgreSQL..."
python manage.py migrate

echo "✓ Migrações concluídas"
echo ""

# 4. Carregar dados
echo "4. Carregando dados no PostgreSQL..."
python manage.py loaddata backup_data.json

echo "✓ Dados carregados com sucesso"
echo ""

# 5. Coletar estáticos
echo "5. Coletando arquivos estáticos..."
python manage.py collectstatic --noinput

echo ""
echo "=== Migração Concluída! ==="
echo ""
echo "Próximos passos:"
echo "1. Verifique os dados no admin Django"
echo "2. Teste a aplicação"
echo "3. Crie um superusuário se necessário: python manage.py createsuperuser"
```

Salve como `migrate_to_postgres.sh`, dê permissão de execução e execute:

```bash
chmod +x migrate_to_postgres.sh
./migrate_to_postgres.sh
```

## Notas Importantes

1. **Sempre faça backup** antes de qualquer migração
2. **Teste em ambiente de desenvolvimento** antes de migrar em produção
3. **Arquivos de mídia** precisam ser migrados separadamente
4. **Variáveis de ambiente** devem estar corretamente configuradas
5. **Senhas de usuários** são migradas junto com os dados (hash)
6. **Sessions antigas** não são migradas (usuários precisarão fazer login novamente)

## Referências

- [Django dumpdata Documentation](https://docs.djangoproject.com/en/5.2/ref/django-admin/#dumpdata)
- [Django loaddata Documentation](https://docs.djangoproject.com/en/5.2/ref/django-admin/#loaddata)
- [PostgreSQL on Azure](https://docs.microsoft.com/azure/postgresql/)
