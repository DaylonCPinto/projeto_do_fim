# Checklist de Segurança - Django/Wagtail

## ✅ Configurações Implementadas

### Segurança de Produção
- [x] `DEBUG = False` em produção
- [x] `SECRET_KEY` configurada via variável de ambiente
- [x] `ALLOWED_HOSTS` configurado adequadamente
- [x] `CSRF_TRUSTED_ORIGINS` configurado para domínios do Azure
- [x] `SECURE_SSL_REDIRECT = True` em produção (força HTTPS)
- [x] `SECURE_PROXY_SSL_HEADER` configurado para Azure
- [x] `SESSION_COOKIE_SECURE = True` em produção
- [x] `CSRF_COOKIE_SECURE = True` em produção
- [x] `SECURE_HSTS_SECONDS = 31536000` (HTTP Strict Transport Security)
- [x] `SECURE_HSTS_INCLUDE_SUBDOMAINS = True`
- [x] `SECURE_HSTS_PRELOAD = True`
- [x] `SECURE_CONTENT_TYPE_NOSNIFF = True`
- [x] `SECURE_BROWSER_XSS_FILTER = True`
- [x] `X_FRAME_OPTIONS = 'DENY'` (proteção contra clickjacking)

### Banco de Dados
- [x] PostgreSQL configurado com SSL (`sslmode=require`)
- [x] Connection pooling habilitado (`conn_max_age=600`)
- [x] Health checks de conexão habilitados
- [x] SQLite apenas em desenvolvimento
- [x] Sem uso de raw SQL (prevenção de SQL injection)

### Sessões e Cookies
- [x] `SESSION_COOKIE_HTTPONLY = True` (padrão do Django)
- [x] `SESSION_COOKIE_SAMESITE = 'Lax'`
- [x] `SESSION_COOKIE_AGE = 1209600` (2 semanas)

### Autenticação
- [x] Password validators habilitados:
  - UserAttributeSimilarityValidator
  - MinimumLengthValidator
  - CommonPasswordValidator
  - NumericPasswordValidator
- [x] UserProfile criado automaticamente para novos usuários

### Arquivos Estáticos e Mídia
- [x] Whitenoise configurado para servir arquivos estáticos
- [x] `STATICFILES_STORAGE` usando CompressedManifestStaticFilesStorage
- [x] Separação entre STATIC e MEDIA

### Logging
- [x] Logging configurado para console e arquivo
- [x] Logs de segurança habilitados
- [x] Formato verboso para debug em produção

### Dependências
- [x] Todas as dependências com versões fixadas
- [x] psycopg2-binary incluído para PostgreSQL
- [x] Gunicorn para servidor WSGI em produção
- [x] Whitenoise para arquivos estáticos

## 📋 Checklist para Deploy

### Antes do Deploy
- [ ] Gerar nova `SECRET_KEY` forte e aleatória
- [ ] Configurar todas as variáveis de ambiente no Azure
- [ ] Revisar `.env.example` e garantir que todas as variáveis estão definidas
- [ ] Executar `python manage.py check --deploy`
- [ ] Testar localmente com `DEBUG=False`

### Durante o Deploy
- [ ] Criar banco de dados PostgreSQL no Azure
- [ ] Configurar firewall rules do PostgreSQL
- [ ] Criar App Service no Azure
- [ ] Configurar deployment do Git
- [ ] Push do código para o Azure

### Após o Deploy
- [ ] Executar migrações: `python manage.py migrate`
- [ ] Coletar arquivos estáticos: `python manage.py collectstatic`
- [ ] Criar superusuário: `python manage.py createsuperuser`
- [ ] Testar login no admin: `/admin/`
- [ ] Verificar logs: `az webapp log tail`
- [ ] Testar site em HTTPS
- [ ] Verificar SSL com [SSL Labs](https://www.ssllabs.com/ssltest/)

## 🔒 Práticas de Segurança Adicionais Recomendadas

### Para Implementação Futura
- [ ] Configurar rate limiting (django-ratelimit)
- [ ] Adicionar 2FA para usuários admin
- [ ] Implementar Content Security Policy (CSP)
- [ ] Configurar backup automático do banco de dados
- [ ] Implementar monitoramento com Application Insights
- [ ] Adicionar testes de segurança automatizados
- [ ] Configurar alertas de segurança
- [ ] Implementar rotação de secrets
- [ ] Adicionar CAPTCHA em formulários públicos
- [ ] Configurar WAF (Web Application Firewall)

### Manutenção Regular
- [ ] Atualizar dependências regularmente
- [ ] Revisar logs de segurança semanalmente
- [ ] Testar backups mensalmente
- [ ] Auditar permissões de usuários
- [ ] Revisar e atualizar políticas de senha
- [ ] Verificar tentativas de login falhas

## 🚨 Vulnerabilidades Verificadas e Corrigidas

### ✅ Resolvido
1. **SECRET_KEY exposta**: Movida para variável de ambiente
2. **DEBUG=True em produção**: Configurado para False via .env
3. **ALLOWED_HOSTS genérico**: Configurado via variável de ambiente
4. **Sem HTTPS enforcement**: Adicionado SECURE_SSL_REDIRECT
5. **Cookies inseguros**: Session e CSRF cookies seguros em produção
6. **Sem HSTS**: Configurado HSTS com 1 ano
7. **PostgreSQL sem SSL**: Configurado sslmode=require
8. **WAGTAILADMIN_BASE_URL hardcoded**: Movido para variável de ambiente
9. **Sem logging**: Configuração completa de logging adicionada
10. **Arquivo .env versionado**: Adicionado ao .gitignore

### ❌ Não Encontrado
- SQL Injection: Uso correto do ORM Django
- XSS: Templates usando auto-escaping do Django
- CSRF: Proteção CSRF habilitada e configurada
- Command Injection: Sem uso de subprocess ou shell commands com input do usuário
- Path Traversal: Sem manipulação direta de caminhos de arquivo

## 🧪 Testes de Segurança

### Comandos para Testar
```bash
# Verificar configuração de deploy
python manage.py check --deploy

# Verificar migrações
python manage.py migrate --check

# Testar coleta de estáticos
python manage.py collectstatic --dry-run --noinput

# Verificar se há dependências desatualizadas
pip list --outdated
```

### Ferramentas Recomendadas
- [Safety](https://pyup.io/safety/): Verificar vulnerabilidades em dependências
- [Bandit](https://bandit.readthedocs.io/): Scanner de segurança para Python
- [OWASP ZAP](https://www.zaproxy.org/): Teste de penetração
- [SSL Labs](https://www.ssllabs.com/ssltest/): Testar configuração SSL

## 📚 Recursos

- [Django Security](https://docs.djangoproject.com/en/stable/topics/security/)
- [Django Deployment Checklist](https://docs.djangoproject.com/en/stable/howto/deployment/checklist/)
- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [Wagtail Security](https://docs.wagtail.org/en/stable/advanced_topics/security.html)

## 📞 Contato em Caso de Incidente

Em caso de descoberta de vulnerabilidade de segurança:
1. NÃO divulgue publicamente
2. Entre em contato com a equipe de desenvolvimento imediatamente
3. Documente todos os detalhes da vulnerabilidade
4. Aguarde confirmação e correção antes de divulgar
