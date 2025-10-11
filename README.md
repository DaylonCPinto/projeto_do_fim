# Portal de Análise - Django/Wagtail

Portal de análise de conteúdo com sistema de paywall para conteúdo premium, construído com Django e Wagtail CMS.

## 🚀 Características

- Sistema de autenticação de usuários
- Paywall para conteúdo premium
- CMS Wagtail para gerenciamento de conteúdo
- Sistema de perfis de usuários com assinaturas
- Interface responsiva com Bootstrap 5
- Suporte para PostgreSQL em produção
- Deploy otimizado para Azure

## 🔒 Segurança

Este projeto implementa as melhores práticas de segurança:

- ✅ HTTPS enforcement em produção
- ✅ HSTS (HTTP Strict Transport Security)
- ✅ Cookies seguros (Secure, HttpOnly, SameSite)
- ✅ Proteção CSRF
- ✅ Proteção XSS
- ✅ Proteção SQL Injection (via Django ORM)
- ✅ Proteção Clickjacking (X-Frame-Options)
- ✅ Content Type Nosniff
- ✅ PostgreSQL com SSL obrigatório
- ✅ Validação de senhas fortes
- ✅ Logging de segurança

Veja [SECURITY_CHECKLIST.md](SECURITY_CHECKLIST.md) para mais detalhes.

## 📋 Pré-requisitos

- Python 3.12+
- PostgreSQL 14+ (para produção)
- Conta no Azure (para deploy)

## 🛠️ Instalação Local

1. Clone o repositório:
```bash
git clone https://github.com/DaylonCPinto/projeto_do_fim.git
cd projeto_do_fim
```

2. Crie e ative um ambiente virtual:
```bash
python -m venv venv
source venv/bin/activate  # No Windows: venv\Scripts\activate
```

3. Instale as dependências:
```bash
pip install -r requirements.txt
```

4. Crie um arquivo `.env` baseado no `.env.example`:
```bash
cp .env.example .env
```

5. Gere uma SECRET_KEY:
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

6. Edite o `.env` e configure as variáveis (para desenvolvimento local, você pode usar valores simples):
```
SECRET_KEY=sua-secret-key-gerada-acima
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost
```

7. Execute as migrações:
```bash
python manage.py migrate
```

8. Crie um superusuário:
```bash
python manage.py createsuperuser
```

9. Colete arquivos estáticos:
```bash
python manage.py collectstatic --noinput
```

10. Execute o servidor de desenvolvimento:
```bash
python manage.py runserver
```

Acesse: http://localhost:8000

## 📦 Estrutura do Projeto

```
projeto_do_fim/
├── accounts/          # App de autenticação e perfis de usuários
├── content/           # App de conteúdo com Wagtail
├── core/              # Configurações do projeto
├── static/            # Arquivos estáticos (CSS, JS, imagens)
├── templates/         # Templates HTML
├── .env.example       # Exemplo de variáveis de ambiente
├── requirements.txt   # Dependências Python
├── Procfile          # Configuração para Gunicorn
└── manage.py         # Script de gerenciamento Django
```

## 🌐 Deploy no Azure

### Guias Disponíveis:

**Se você já tem 2 VMs Azure prontas (Web + Database):**
- 📘 **[GUIA_RAPIDO_AZURE.md](GUIA_RAPIDO_AZURE.md)** - Início rápido com comandos objetivos
- 📗 **[AZURE_VM_SETUP_COMPLETO.md](AZURE_VM_SETUP_COMPLETO.md)** - Guia completo e detalhado
- 🔧 **[TROUBLESHOOTING_NGINX_GUNICORN.md](TROUBLESHOOTING_NGINX_GUNICORN.md)** - Resolução de problemas
- 🤖 **[scripts/](scripts/)** - Scripts de automação

**Para criar VMs do zero:**
- 📙 **[AZURE_DEPLOYMENT_VM.md](AZURE_DEPLOYMENT_VM.md)** - Criação de infraestrutura com Azure CLI

**Para usar Azure App Service (PaaS):**
- 📕 **[AZURE_DEPLOYMENT.md](AZURE_DEPLOYMENT.md)** - Deploy em App Service

### Resumo Rápido (VMs já existentes):

```bash
# 1. Configurar NSG (no seu computador)
./scripts/configure_azure_nsg.sh

# 2. Configurar VM Database (via SSH)
ssh -J azureuser@IP_WEB azureuser@IP_DB
sudo ./scripts/setup_database.sh

# 3. Configurar VM Web (via SSH)
ssh azureuser@IP_WEB
sudo ./scripts/setup_web.sh
# Depois: configurar .env, executar migrações, iniciar serviços

# 4. Testar conectividade
./scripts/test_connectivity.sh
```

## 🧪 Testes

```bash
# Executar todos os testes
python manage.py test

# Executar testes de uma app específica
python manage.py test accounts

# Verificar configuração de deploy
python manage.py check --deploy
```

## 📝 Variáveis de Ambiente

Veja `.env.example` para uma lista completa. As principais são:

- `SECRET_KEY`: Chave secreta do Django (obrigatório)
- `DEBUG`: Modo debug (True/False)
- `ALLOWED_HOSTS`: Domínios permitidos
- `DATABASE_URL`: String de conexão do PostgreSQL
- `WAGTAILADMIN_BASE_URL`: URL base do admin do Wagtail
- `CSRF_TRUSTED_ORIGINS`: Origens confiáveis para CSRF

## 🤝 Contribuindo

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📚 Documentação

- [Django Documentation](https://docs.djangoproject.com/)
- [Wagtail Documentation](https://docs.wagtail.org/)
- [Azure App Service](https://docs.microsoft.com/azure/app-service/)
- [PostgreSQL on Azure](https://docs.microsoft.com/azure/postgresql/)

## 🔧 Comandos Úteis

```bash
# Criar migrações
python manage.py makemigrations

# Aplicar migrações
python manage.py migrate

# Criar superusuário
python manage.py createsuperuser

# Coletar arquivos estáticos
python manage.py collectstatic

# Executar shell do Django
python manage.py shell

# Limpar sessões expiradas
python manage.py clearsessions
```

## 📊 Administração

- **Django Admin**: `/django-admin/`
- **Wagtail Admin**: `/admin/`
- **Login**: `/accounts/login/`
- **Registro**: `/accounts/signup/`

## 🐛 Troubleshooting

### Erro de SECRET_KEY
Certifique-se de que a SECRET_KEY está definida no arquivo `.env`.

### Erro de Banco de Dados
Para desenvolvimento local, certifique-se de que não há `DATABASE_URL` no `.env`. O projeto usará SQLite automaticamente.

### Arquivos Estáticos Não Carregam
Execute `python manage.py collectstatic` e verifique se `DEBUG=True` em desenvolvimento.

### Erro 500 em Produção
- Verifique os logs: `az webapp log tail` (Azure)
- Certifique-se de que `DEBUG=False`
- Verifique se todas as variáveis de ambiente estão configuradas
- Execute as migrações: `python manage.py migrate`

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo LICENSE para mais detalhes.

## 👤 Autor

Daylon C. Pinto

## 🙏 Agradecimentos

- Django Software Foundation
- Wagtail CMS Team
- Bootstrap Team
- Todos os contribuidores open source
