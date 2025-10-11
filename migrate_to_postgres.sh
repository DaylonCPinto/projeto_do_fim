#!/bin/bash
# migrate_to_postgres.sh
# Script para migrar dados do SQLite para PostgreSQL

set -e  # Parar em caso de erro

echo "=== Migração SQLite → PostgreSQL ==="
echo ""

# Verificar se estamos no diretório correto
if [ ! -f "manage.py" ]; then
    echo "❌ ERRO: execute este script no diretório raiz do projeto"
    exit 1
fi

# Verificar se o ambiente virtual está ativado
if [ -z "$VIRTUAL_ENV" ]; then
    echo "⚠️  AVISO: Ambiente virtual não detectado"
    echo "Por favor, ative o ambiente virtual primeiro:"
    echo "  source venv/bin/activate"
    exit 1
fi

# 1. Backup SQLite
echo "1. Fazendo backup do SQLite..."
if [ -f "db.sqlite3" ]; then
    BACKUP_FILE="db.sqlite3.backup.$(date +%Y%m%d_%H%M%S)"
    cp db.sqlite3 "$BACKUP_FILE"
    echo "✓ Backup do SQLite criado: $BACKUP_FILE"
    
    # Criar dump JSON
    python manage.py dumpdata --natural-foreign --natural-primary \
        --exclude=contenttypes --exclude=auth.permission \
        --exclude=sessions --exclude=admin.logentry \
        --indent=2 > backup_data.json
    
    echo "✓ Dump de dados criado: backup_data.json"
else
    echo "⚠️  AVISO: db.sqlite3 não encontrado, pulando backup"
fi
echo ""

# 2. Verificar DATABASE_URL
echo "2. Verificando configuração do PostgreSQL..."
if grep -q "DATABASE_URL" .env 2>/dev/null; then
    echo "✓ DATABASE_URL encontrado no .env"
else
    echo "❌ ERRO: DATABASE_URL não está configurado no .env"
    echo ""
    echo "Adicione no arquivo .env:"
    echo "DATABASE_URL=postgres://usuario@servidor:senha@servidor.postgres.database.azure.com:5432/banco?sslmode=require"
    exit 1
fi
echo ""

# 3. Executar migrações
echo "3. Executando migrações no PostgreSQL..."
python manage.py migrate --noinput
echo "✓ Migrações concluídas"
echo ""

# 4. Carregar dados (se houver backup)
if [ -f "backup_data.json" ]; then
    echo "4. Carregando dados no PostgreSQL..."
    python manage.py loaddata backup_data.json
    echo "✓ Dados carregados com sucesso"
    echo ""
else
    echo "4. Nenhum backup de dados encontrado, pulando..."
    echo ""
fi

# 5. Coletar estáticos
echo "5. Coletando arquivos estáticos..."
python manage.py collectstatic --noinput
echo "✓ Arquivos estáticos coletados"
echo ""

echo "=== Migração Concluída com Sucesso! ==="
echo ""
echo "Próximos passos:"
echo "1. Verifique os dados: python manage.py shell"
echo "2. Acesse o admin Django e teste"
echo "3. Crie um superusuário se necessário: python manage.py createsuperuser"
echo ""
echo "Arquivos criados:"
if [ -f "$BACKUP_FILE" ]; then
    echo "  - $BACKUP_FILE"
fi
if [ -f "backup_data.json" ]; then
    echo "  - backup_data.json"
fi
