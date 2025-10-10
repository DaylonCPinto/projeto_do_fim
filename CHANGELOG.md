# Changelog - Portal de Análise

Todas as mudanças notáveis neste projeto serão documentadas neste arquivo.

---

## [1.1.0] - 2025-10-10

### 🎉 Novas Funcionalidades

#### Sistema de Tags/Tópicos
- ✨ Adicionado sistema completo de tags usando django-taggit
- ✨ Criado modelo `ArticlePageTag` para tags de artigos
- ✨ Campo `tags` adicionado ao modelo `ArticlePage`
- ✨ Interface no Wagtail Admin para adicionar/gerenciar tags
- ✨ Gerenciamento de tags no Django Admin (`/django-admin/taggit/tag/`)

#### Campo CPF no Cadastro
- ✨ Adicionado campo `cpf` ao modelo `UserProfile`
- ✨ Campo CPF obrigatório no formulário de cadastro
- ✨ Validação de formato de CPF (11 dígitos)
- ✨ Validação de unicidade (CPF não pode ser duplicado)
- ✨ Validação contra sequências repetidas (111.111.111-11)
- ✨ Campo CPF exibido no Django Admin
- ✨ Busca por CPF habilitada no admin

### 🌍 Localização

#### Português do Brasil
- 🌐 `LANGUAGE_CODE` alterado para `'pt-br'`
- 🌐 Labels de formulários traduzidos para português
- 🌐 Mensagens de erro em português
- 🌐 Interface admin em português (onde disponível)

#### Fuso Horário de Brasília
- 🕐 `TIME_ZONE` alterado para `'America/Sao_Paulo'` (GMT-3)
- 🕐 Todas as datas exibidas no horário de Brasília
- 🕐 Formato de data brasileiro (DD/MM/YYYY HH:MM)

### 📚 Documentação

#### Novos Documentos
- 📄 `MIGRATION_GUIDE.md` - Guia completo de migração SQLite → PostgreSQL
- 📄 `FEATURES_GUIDE.md` - Documentação de todas as funcionalidades
- 📄 `PROJECT_STATUS.md` - Avaliação completa do projeto (75-80%)
- 📄 `QUICK_REFERENCE.md` - Referência rápida de comandos
- 📄 `RESPOSTAS_COMPLETAS.md` - Respostas detalhadas às perguntas
- 📄 `CHANGELOG.md` - Este arquivo

#### Scripts
- 🔧 `migrate_to_postgres.sh` - Script automático de migração de dados

#### Atualizações
- 📝 `AZURE_DEPLOYMENT.md` - Adicionada seção sobre migração de dados
- 📝 `.gitignore` - Adicionados padrões para backups (*.sqlite3.backup.*, backup_data.json)

### 🔄 Migrações

#### Accounts
- 🗄️ `0003_userprofile_cpf.py` - Adiciona campo CPF ao UserProfile

#### Content
- 🗄️ `0005_articlepagetag_articlepage_tags.py` - Adiciona sistema de tags

### 🛠️ Melhorias Técnicas

#### Models
- Adicionados imports para tags (`modelcluster.contrib.taggit`, `taggit.models`)
- Validação robusta de CPF no formulário
- Help texts descritivos

#### Forms
- Labels em português
- Validação aprimorada
- Placeholders informativos

#### Admin
- Campo CPF adicionado ao UserProfileInline
- Campo CPF adicionado ao UserProfileAdmin
- Busca por CPF habilitada

---

## [1.0.0] - Data Anterior

### ✅ Funcionalidades Base

#### Sistema de Autenticação
- Sistema de login/logout
- Registro de usuários
- Reset de senha
- Proteção CSRF

#### Sistema de Assinatura Premium
- Campo `is_subscriber` em UserProfile
- Controle de acesso a conteúdo premium
- Ações em massa no admin para ativar/desativar premium
- Badges visuais de status

#### CMS (Wagtail)
- HomePage para listagem de artigos
- ArticlePage com editor rico
- Upload de imagens
- Imagem de destaque
- Campo `is_premium` para conteúdo exclusivo
- Data de publicação
- Introdução/preview

#### Infraestrutura
- Suporte SQLite (desenvolvimento)
- Suporte PostgreSQL (produção)
- Configuração para Azure App Service
- Whitenoise para arquivos estáticos
- Gunicorn como servidor WSGI
- Logging configurado
- Variáveis de ambiente via python-decouple

#### Segurança
- SECRET_KEY via variável de ambiente
- DEBUG=False em produção
- SSL Redirect em produção
- HSTS configurado
- Session cookies seguros
- CSRF cookies seguros
- X-Frame-Options: DENY

#### Documentação
- README.md
- QUICK_START.md
- AZURE_DEPLOYMENT.md
- SECURITY_CHECKLIST.md
- AUDIT_COMPLETE.md

---

## 📊 Estatísticas da Versão 1.1.0

### Arquivos Modificados: 7
- `core/settings.py`
- `accounts/models.py`
- `accounts/forms.py`
- `accounts/admin.py`
- `content/models.py`
- `AZURE_DEPLOYMENT.md`
- `.gitignore`

### Arquivos Criados: 9
- `accounts/migrations/0003_userprofile_cpf.py`
- `content/migrations/0005_articlepagetag_articlepage_tags.py`
- `MIGRATION_GUIDE.md`
- `FEATURES_GUIDE.md`
- `PROJECT_STATUS.md`
- `QUICK_REFERENCE.md`
- `RESPOSTAS_COMPLETAS.md`
- `CHANGELOG.md`
- `migrate_to_postgres.sh`

### Linhas de Código: +1,500
- Python: +200 linhas
- Documentação: +1,300 linhas

### Completude: 75-80% ✅

---

## 🎯 Roadmap Futuro

### Versão 1.2.0 (Planejado)
- [ ] Melhorias no frontend
- [ ] Páginas públicas de tags
- [ ] Sistema de busca
- [ ] SEO básico
- [ ] Testes unitários

### Versão 2.0.0 (Planejado)
- [ ] Sistema de pagamento
- [ ] Dashboard do usuário
- [ ] Email marketing
- [ ] Analytics
- [ ] API REST

### Versão 3.0.0 (Futuro)
- [ ] Comentários
- [ ] Newsletter
- [ ] App mobile
- [ ] Programa de afiliados

---

## 🔗 Links Úteis

- **Repositório:** [GitHub](https://github.com/DaylonCPinto/projeto_do_fim)
- **Documentação:** Veja os arquivos .md no repositório
- **Issues:** [GitHub Issues](https://github.com/DaylonCPinto/projeto_do_fim/issues)

---

## 📝 Notas de Migração

### De 1.0.0 para 1.1.0

1. **Executar migrações:**
   ```bash
   python manage.py migrate accounts 0003
   python manage.py migrate content 0005
   ```

2. **Atualizar .env (opcional):**
   - Não há novas variáveis de ambiente necessárias

3. **Verificar:**
   ```bash
   python manage.py check
   ```

4. **Testar:**
   - Acesse `/accounts/signup/` e verifique campo CPF
   - Acesse `/admin/` e adicione tags a um artigo
   - Acesse `/django-admin/accounts/userprofile/` e veja CPF

---

## 👥 Contribuidores

- **Daylon C. Pinto** - Desenvolvedor Principal

---

## 📄 Licença

Este projeto está sob a licença MIT.

---

**Última atualização:** 2025-10-10
