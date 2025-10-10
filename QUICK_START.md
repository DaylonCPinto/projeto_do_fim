# 🚀 Quick Start Guide

Este guia de início rápido ajudará você a ter o projeto rodando localmente em minutos.

## ⚡ Desenvolvimento Local (5 minutos)

### 1. Clone e Instale

```bash
# Clone o repositório
git clone https://github.com/DaylonCPinto/projeto_do_fim.git
cd projeto_do_fim

# Crie ambiente virtual
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Instale dependências
pip install -r requirements.txt
```

### 2. Configure o Ambiente

```bash
# Crie arquivo .env
cp .env.example .env

# Gere uma SECRET_KEY segura
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"

# Cole a SECRET_KEY gerada no arquivo .env
# Mantenha DEBUG=True para desenvolvimento local
```

Seu `.env` deve ficar assim para desenvolvimento:
```env
SECRET_KEY=sua-secret-key-gerada-acima
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost
```

### 3. Configure o Banco de Dados

```bash
# Execute as migrações
python manage.py migrate

# Crie um superusuário
python manage.py createsuperuser
# Username: admin
# Email: admin@example.com
# Password: (escolha uma senha forte)
```

### 4. Execute o Servidor

```bash
# Inicie o servidor de desenvolvimento
python manage.py runserver
```

✅ Acesse: http://localhost:8000

### 5. Explore o Admin

- **Django Admin**: http://localhost:8000/django-admin/
- **Wagtail Admin**: http://localhost:8000/admin/

Use o superusuário criado no passo 3.

## 🏗️ Criar Conteúdo de Exemplo

### No Wagtail Admin:

1. Acesse http://localhost:8000/admin/
2. Vá em "Pages" → "Home"
3. Clique em "Add child page" → "Article Page"
4. Preencha:
   - Title: "Primeiro Artigo"
   - Publication date: hoje
   - Introduction: "Introdução do artigo"
   - Body: "Conteúdo completo do artigo"
   - Is premium?: Marque se quiser testar o paywall
5. Clique em "Publish"

### Teste o Paywall:

1. Crie um artigo premium
2. Visite o site sem estar logado - verá apenas a introdução
3. Faça login - ainda verá apenas a introdução (não é assinante)
4. No Django Admin, edite seu usuário:
   - Vá em "User profiles"
   - Marque "Assinante Ativo?"
   - Salve
5. Recarregue o artigo - agora verá o conteúdo completo!

## 🎨 Comandos Úteis

```bash
# Criar novas migrações
python manage.py makemigrations

# Aplicar migrações
python manage.py migrate

# Coletar arquivos estáticos (necessário se mudar CSS/JS)
python manage.py collectstatic

# Acessar shell do Django
python manage.py shell

# Verificar problemas
python manage.py check

# Verificar configuração para deploy
python manage.py check --deploy

# Limpar sessões expiradas
python manage.py clearsessions
```

## 🔧 Troubleshooting Comum

### Erro: "No module named 'django'"
```bash
# Certifique-se de ativar o ambiente virtual
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

### Erro: "SECRET_KEY not found"
```bash
# Crie o arquivo .env baseado no .env.example
cp .env.example .env
# Edite o .env e adicione a SECRET_KEY
```

### Erro: "Table doesn't exist"
```bash
# Execute as migrações
python manage.py migrate
```

### Página sem estilo (CSS não carrega)
```bash
# Com DEBUG=True, não é necessário collectstatic
# Mas se quiser, execute:
python manage.py collectstatic --noinput
```

### Porta 8000 já em uso
```bash
# Use outra porta
python manage.py runserver 8001
```

## 🌐 Deploy Rápido no Azure

Para deploy em produção, siga o guia completo em **AZURE_DEPLOYMENT.md**.

### Resumo ultra-rápido:

```bash
# 1. Login no Azure
az login

# 2. Criar PostgreSQL
az postgres flexible-server create \
  --resource-group meu-rg \
  --name meu-db \
  --location eastus \
  --admin-user admin \
  --admin-password 'SenhaForte123!'

# 3. Criar Web App
az webapp create \
  --resource-group meu-rg \
  --plan meu-plan \
  --name meu-webapp \
  --runtime "PYTHON:3.12"

# 4. Configurar variáveis
az webapp config appsettings set \
  --resource-group meu-rg \
  --name meu-webapp \
  --settings \
    SECRET_KEY='nova-secret-key-gerada' \
    DEBUG='False' \
    DATABASE_URL='postgres://...'

# 5. Deploy
git push azure main

# 6. Executar migrações no Azure
az webapp ssh --resource-group meu-rg --name meu-webapp
python manage.py migrate
python manage.py createsuperuser
```

## 📚 Próximos Passos

Depois de ter o projeto rodando:

1. 📖 Leia o **README.md** para entender a arquitetura
2. 🔒 Revise **SECURITY_CHECKLIST.md** antes do deploy
3. ☁️ Siga **AZURE_DEPLOYMENT.md** para deploy em produção
4. ✅ Confira **AUDIT_COMPLETE.md** para ver todas as melhorias de segurança

## 💡 Dicas

- Use `DEBUG=True` apenas em desenvolvimento
- Sempre crie um `.env` e nunca o versione no Git
- Mantenha suas dependências atualizadas: `pip list --outdated`
- Faça backup regular do banco de dados em produção
- Monitore os logs de segurança

## 🆘 Precisa de Ajuda?

- **Documentação Django**: https://docs.djangoproject.com/
- **Documentação Wagtail**: https://docs.wagtail.org/
- **Issues do Projeto**: [GitHub Issues](https://github.com/DaylonCPinto/projeto_do_fim/issues)

---

**Tempo estimado de setup:** 5-10 minutos  
**Dificuldade:** Iniciante  
**Última atualização:** 2025-10-10
