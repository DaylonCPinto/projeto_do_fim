#!/bin/bash
# Script de inicialização para Azure App Service

echo "===== Iniciando aplicação Django/Wagtail ====="

# Executar migrações
echo "Executando migrações do banco de dados..."
python manage.py migrate --noinput

# Coletar arquivos estáticos
echo "Coletando arquivos estáticos..."
python manage.py collectstatic --noinput

echo "===== Inicialização concluída ====="

# Iniciar Gunicorn
echo "Iniciando Gunicorn..."
gunicorn core.wsgi --bind=0.0.0.0:8000 --timeout 600 --workers 4 --log-file -
