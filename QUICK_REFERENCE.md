# Referência Rápida - Portal de Análise

Guia de consulta rápida para as principais tarefas administrativas.

---

## 🔐 Acessos Administrativos

| Acesso | URL | Função |
|--------|-----|--------|
| **Wagtail Admin** | `/admin/` | Gerenciar conteúdo (artigos, páginas) |
| **Django Admin** | `/django-admin/` | Gerenciar usuários e sistema |

---

## 👥 Gerenciar Usuários Premium

### Método Rápido (Ações em Massa)

1. Acesse: `/django-admin/auth/user/`
2. ☑️ Selecione os usuários
3. Escolha a ação:
   - `✓ Ativar assinatura premium`
   - `✗ Desativar assinatura premium`
4. Clique em **Ir**

### Ver Todos os Perfis

- URL: `/django-admin/accounts/userprofile/`
- Visualize CPF, email, status de assinatura
- Use filtros e busca

---

## 📝 Gerenciar Artigos

### Criar Novo Artigo

1. Acesse: `/admin/pages/`
2. Clique em **Home**
3. Clique em **+ Adicionar filho**
4. Escolha **Article Page**
5. Preencha:
   - **Título**
   - **Data de Publicação**
   - **Introdução** (resumo)
   - **Conteúdo Exclusivo?** (se for premium)
   - **Imagem de Destaque**
   - **Corpo do Artigo**
   - **Tags** (ex: Economia, Política)
6. Clique em **Publish**

### Editar Artigo Existente

1. Acesse: `/admin/pages/`
2. Encontre o artigo
3. Clique em **Edit**
4. Faça alterações
5. **Save draft** ou **Publish**

---

## 🏷️ Gerenciar Tags

### Adicionar Tags a Artigos

- No editor do artigo (Wagtail)
- Campo "Tags" - digite e pressione Enter
- Exemplos: `Economia`, `Política`, `Tecnologia`

### Ver Todas as Tags

- URL: `/django-admin/taggit/tag/`
- Ver, editar ou excluir tags

---

## 🗄️ Migração de Dados

### SQLite → PostgreSQL

```bash
# 1. Fazer backup
python manage.py dumpdata --natural-foreign --natural-primary \
    --exclude=contenttypes --exclude=auth.permission \
    --exclude=sessions --exclude=admin.logentry \
    --indent=2 > backup_data.json

# 2. Configurar DATABASE_URL no .env
DATABASE_URL=postgres://usuario@servidor:senha@servidor.postgres.database.azure.com:5432/banco?sslmode=require

# 3. Executar migrações
python manage.py migrate

# 4. Carregar dados
python manage.py loaddata backup_data.json

# 5. Coletar estáticos
python manage.py collectstatic --noinput
```

**Ou use o script:**
```bash
./migrate_to_postgres.sh
```

---

## 🚀 Deploy no Azure

### Configuração Rápida

```bash
# Variáveis necessárias no Azure
SECRET_KEY=sua-secret-key-aqui
DEBUG=False
ALLOWED_HOSTS=seudominio.azurewebsites.net
DATABASE_URL=postgres://...
CSRF_TRUSTED_ORIGINS=https://seudominio.azurewebsites.net
WAGTAILADMIN_BASE_URL=https://seudominio.azurewebsites.net
```

### Após Deploy

```bash
# SSH no container
az webapp ssh --resource-group meu-rg --name meu-app

# Executar
python manage.py migrate
python manage.py collectstatic --noinput
python manage.py createsuperuser
```

---

## 🔧 Comandos Úteis

### Desenvolvimento

```bash
# Iniciar servidor
python manage.py runserver

# Criar superusuário
python manage.py createsuperuser

# Fazer migrações
python manage.py makemigrations
python manage.py migrate

# Coletar estáticos
python manage.py collectstatic

# Shell Django
python manage.py shell
```

### Verificações

```bash
# Verificar problemas
python manage.py check

# Verificar deploy
python manage.py check --deploy

# Ver migrações pendentes
python manage.py showmigrations
```

---

## 📊 Checklist de Tarefas Comuns

### ✅ Novo Usuário Premium

- [ ] Acesse `/django-admin/auth/user/`
- [ ] Selecione o usuário
- [ ] Ação: "Ativar assinatura premium"
- [ ] Confirme o status no perfil

### ✅ Publicar Artigo

- [ ] Acesse `/admin/pages/`
- [ ] Crie ou edite artigo
- [ ] Adicione imagem de destaque
- [ ] Adicione tags relevantes
- [ ] Marque "Conteúdo Exclusivo" se premium
- [ ] Clique em "Publish"

### ✅ Preparar para Deploy

- [ ] Teste localmente
- [ ] Configure variáveis no Azure
- [ ] Faça push do código
- [ ] Execute migrações no Azure
- [ ] Colete estáticos
- [ ] Crie superusuário
- [ ] Teste em produção

### ✅ Migrar Dados

- [ ] Backup do SQLite (`dumpdata`)
- [ ] Configure PostgreSQL
- [ ] Execute migrações
- [ ] Carregue backup (`loaddata`)
- [ ] Verifique dados
- [ ] Teste aplicação

---

## 🆘 Problemas Comuns

### Erro: "SECRET_KEY"
```bash
# Gere uma nova
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
# Adicione ao .env
```

### Erro: "Database connection"
```bash
# Verifique DATABASE_URL no .env
# Teste conexão:
python manage.py dbshell
```

### Erro: "Static files not found"
```bash
python manage.py collectstatic --noinput
```

### Erro: "Migration conflicts"
```bash
python manage.py makemigrations --merge
```

---

## 📚 Documentação Completa

| Documento | Conteúdo |
|-----------|----------|
| **README.md** | Visão geral e instalação |
| **QUICK_START.md** | Início rápido (5 min) |
| **FEATURES_GUIDE.md** | Todas as funcionalidades |
| **MIGRATION_GUIDE.md** | Migração de dados |
| **AZURE_DEPLOYMENT.md** | Deploy no Azure |
| **PROJECT_STATUS.md** | Status e avaliação |
| **SECURITY_CHECKLIST.md** | Checklist de segurança |

---

## 💡 Dicas

1. **Sempre faça backup** antes de mudanças grandes
2. **Teste localmente** antes de deploy
3. **Use tags consistentes** para melhor organização
4. **Monitore logs** em produção
5. **Mantenha SECRET_KEY segura** e nunca compartilhe

---

## 📞 URLs Importantes

### Produção
- Site: `https://seudominio.azurewebsites.net`
- Admin Wagtail: `https://seudominio.azurewebsites.net/admin/`
- Admin Django: `https://seudominio.azurewebsites.net/django-admin/`

### Desenvolvimento
- Site: `http://localhost:8000`
- Admin Wagtail: `http://localhost:8000/admin/`
- Admin Django: `http://localhost:8000/django-admin/`

---

**Atualizado em:** 2025-10-10
