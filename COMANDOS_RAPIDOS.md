# ⚡ Comandos Rápidos - Portal de Análise

## 🚨 Solução Rápida: Erro após git pull

```bash
pip install -r requirements.txt
```

---

## 📥 Atualizando o Projeto

```bash
# 1. Baixar código atualizado
git pull origin main

# 2. Instalar/atualizar dependências (IMPORTANTE!)
pip install -r requirements.txt

# 3. Executar migrações
python manage.py migrate

# 4. Coletar arquivos estáticos (produção)
python manage.py collectstatic --noinput

# 5. Reiniciar servidor (produção)
sudo systemctl restart gunicorn nginx
```

---

## 🖥️ Desenvolvimento Local

```bash
# Ativar ambiente virtual
source .venv/bin/activate          # Linux/Mac
.venv\Scripts\activate             # Windows

# Instalar dependências
pip install -r requirements.txt

# Criar migrações
python manage.py makemigrations

# Aplicar migrações
python manage.py migrate

# Criar superusuário
python manage.py createsuperuser

# Iniciar servidor
python manage.py runserver

# Acessar:
# Site: http://localhost:8000/
# Admin: http://localhost:8000/admin/
```

---

## 🌐 Servidor de Produção

```bash
# Conectar ao servidor
ssh azureuser@seu-servidor

# Navegar para o projeto
cd ~/projeto_do_fim

# Ativar ambiente virtual
source .venv/bin/activate

# Atualizar projeto
git pull origin main
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --noinput

# Reiniciar serviços
sudo systemctl restart gunicorn
sudo systemctl restart nginx

# Verificar status
sudo systemctl status gunicorn
sudo systemctl status nginx

# Ver logs
sudo journalctl -u gunicorn -n 50 --no-pager
sudo tail -n 50 /var/log/nginx/error.log
```

---

## 🔍 Diagnóstico

```bash
# Verificar instalação do Python
python --version

# Verificar se bleach está instalado
python -c "import bleach; print('✓ bleach OK')"

# Verificar Django
python manage.py check

# Verificar seções do site
python manage.py check_sections

# Shell interativo do Django
python manage.py shell
```

---

## 🛠️ Comandos de Gestão

```bash
# Criar superusuário
python manage.py createsuperuser

# Limpar sessões antigas
python manage.py clearsessions

# Configurar site inicial
python manage.py setup_site

# Corrigir seção geopolítica
python manage.py fix_geopolitica

# Backup do banco (SQLite local)
cp db.sqlite3 db.sqlite3.backup

# Restaurar banco
cp db.sqlite3.backup db.sqlite3
```

---

## 🐛 Troubleshooting

```bash
# Erro: ModuleNotFoundError
pip install -r requirements.txt

# Erro: migrações pendentes
python manage.py migrate

# Erro: arquivos estáticos não carregam
python manage.py collectstatic --noinput

# Ver todas as dependências instaladas
pip list

# Ver dependências desatualizadas
pip list --outdated

# Reinstalar todas as dependências
pip install -r requirements.txt --force-reinstall
```

---

## 📦 Gestão de Dependências

```bash
# Instalar nova biblioteca
pip install nome-da-biblioteca

# Atualizar requirements.txt
pip freeze > requirements.txt

# Instalar versão específica
pip install biblioteca==1.2.3

# Desinstalar biblioteca
pip uninstall nome-da-biblioteca

# Ver informações de uma biblioteca
pip show nome-da-biblioteca
```

---

## 🔐 Variáveis de Ambiente

```bash
# Copiar exemplo
cp .env.example .env

# Editar variáveis
nano .env
# ou
vim .env

# Gerar nova SECRET_KEY
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

---

## 📊 Banco de Dados

```bash
# Criar migração
python manage.py makemigrations

# Ver SQL das migrações
python manage.py sqlmigrate app_name 0001

# Reverter migração
python manage.py migrate app_name 0001

# Ver migrações aplicadas
python manage.py showmigrations

# Shell do banco
python manage.py dbshell
```

---

## 🧪 Testes

```bash
# Executar todos os testes
python manage.py test

# Testar app específico
python manage.py test accounts

# Testar com verbosidade
python manage.py test --verbosity=2

# Manter banco de teste
python manage.py test --keepdb
```

---

## 🚀 Deploy

```bash
# Checklist completo de deploy
git pull origin main
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --noinput
sudo systemctl restart gunicorn nginx
sudo systemctl status gunicorn
```

---

## 💡 Aliases Úteis

Adicione ao `~/.bashrc` ou `~/.zshrc`:

```bash
# Ativar ambiente
alias venv='source .venv/bin/activate'

# Atualizar projeto
alias update-projeto='git pull && pip install -r requirements.txt && python manage.py migrate && python manage.py collectstatic --noinput'

# Reiniciar servidor
alias restart-server='sudo systemctl restart gunicorn nginx'

# Ver logs
alias logs-gunicorn='sudo journalctl -u gunicorn -f'
alias logs-nginx='sudo tail -f /var/log/nginx/error.log'

# Atalhos Django
alias dm='python manage.py'
alias dmr='python manage.py runserver'
alias dmm='python manage.py makemigrations'
alias dmi='python manage.py migrate'
alias dmc='python manage.py createsuperuser'
```

Depois, use assim:
```bash
venv                    # Ativa ambiente virtual
update-projeto          # Atualiza tudo
dmr                     # Inicia servidor
```

---

## 📚 Documentação

- **README.md** - Visão geral do projeto
- **SETUP_GUIDE.md** - Guia completo de configuração
- **TROUBLESHOOTING.md** - Solução de problemas
- **VALIDATION_CHANGES.md** - Mudanças no sistema de validação
- **FIX_BLEACH_ERROR.md** - Fix do erro do bleach
- **RESUMO_CORRECAO.md** - Resumo em português do problema

---

**💡 Dica:** Mantenha este arquivo aberto em uma aba do navegador para referência rápida!

*Última atualização: Outubro 2025*
