# Guia de Configuração - Portal de Análise

## 🚀 Início Rápido

### Passo 1: Configurar Ambiente

```bash
# Clone o repositório (se ainda não fez)
git clone <repository-url>
cd projeto_do_fim

# Instale as dependências
pip install -r requirements.txt

# Configure as variáveis de ambiente
cp .env.example .env
# Edite o arquivo .env com suas configurações
```

### Passo 2: Configurar Banco de Dados

```bash
# Execute as migrações
python manage.py migrate

# Crie um superusuário para acessar o admin
python manage.py createsuperuser
```

### Passo 3: Configurar Estrutura do Site

**NOVO: Comando Automático!**

Agora você pode usar o comando de gerenciamento para criar automaticamente a estrutura do site:

```bash
python manage.py setup_site
```

Este comando irá:
- ✅ Criar a HomePage (Início)
- ✅ Criar todas as páginas de seção (Geopolítica, Economia, Clima, Tecnologia, Escatologia)
- ✅ Configurar o site padrão
- ✅ Configurar as URLs corretas para cada página

**Saída esperada:**
```
Created HomePage: Início
Created SectionPage: Geopolítica (/geopolitica/)
Created SectionPage: Economia (/economia/)
Created SectionPage: Clima (/clima/)
Created SectionPage: Tecnologia (/tecnologia/)
Created SectionPage: Escatologia (/escatologia/)

✅ Site setup complete!
Home page URL: /
Section URLs:
  - Geopolítica: /geopolitica/
  - Economia: /economia/
  - Clima: /clima/
  - Tecnologia: /tecnologia/
  - Escatologia: /escatologia/
```

### Passo 4: Iniciar o Servidor

```bash
python manage.py runserver
```

Acesse:
- **Site público:** http://localhost:8000/
- **Painel admin:** http://localhost:8000/admin/

## 📋 Configuração Manual (Alternativa)

Se preferir criar as páginas manualmente:

### 1. Criar HomePage

1. Acesse `/admin/pages/`
2. Clique em "Root"
3. Clique em "Add child page"
4. Selecione "Home Page"
5. Preencha:
   - **Título:** Início
   - **Slug:** home
6. Clique em "Publish"

### 2. Criar Páginas de Seção

Para cada seção, repita:

1. Acesse `/admin/pages/`
2. Clique na "Home Page" que você criou
3. Clique em "Add child page"
4. Selecione "Página de Seção"
5. Preencha conforme a tabela abaixo:

| Seção | Título | Slug | Section Key |
|-------|--------|------|-------------|
| Geopolítica | Geopolítica | geopolitica | geopolitica |
| Economia | Economia | economia | economia |
| Clima | Clima | clima | clima |
| Tecnologia | Tecnologia | tecnologia | tecnologia |
| Escatologia | Escatologia | escatologia | escatologia |

6. Adicione uma introdução descritiva (opcional)
7. Clique em "Publish"

## 📝 Criando Conteúdo

### Criar um Artigo

1. Acesse `/admin/pages/`
2. Navegue até a seção desejada (ex: Geopolítica)
3. Clique em "Add child page"
4. Selecione "Article Page"
5. Preencha:
   - **Título:** Ex: "Tensões no Oriente Médio"
   - **Introdução:** Resumo breve do artigo
   - **Seção:** Selecione a seção correspondente (ex: Geopolítica)
   - **Imagem de Destaque:** Upload ou URL externa
   - **Conteúdo do Artigo:** Use os blocos do StreamField
6. Clique em "Publish"

### Adicionar Imagens

**Opção 1: Upload Local**
- Use o campo "Imagem de Destaque" para fazer upload

**Opção 2: URL Externa**
- Cole uma URL no campo "URL de Imagem Externa"
- Exemplos:
  - `https://picsum.photos/800/400`
  - `https://source.unsplash.com/800x400/?politics`

### Usar StreamField

No campo "Conteúdo do Artigo", você pode adicionar:

1. **Parágrafo:** Texto com formatação básica
2. **Título/Subtítulo:** Para seções do artigo
3. **Imagem (Upload ou URL):** Imagens com legenda
4. **Vídeo:** Incorporar vídeos do YouTube, Vimeo, etc.
5. **Citação:** Destacar citações importantes
6. **Lista:** Listas de itens
7. **Divisor:** Linha horizontal
8. **HTML Customizado:** Para conteúdo avançado

## 🔧 Estrutura do Site

### Hierarquia de Páginas

```
Root
└── Home Page (Início) - /
    ├── Geopolítica - /geopolitica/
    │   ├── Artigo 1
    │   └── Artigo 2
    ├── Economia - /economia/
    │   ├── Artigo 3
    │   └── Artigo 4
    ├── Clima - /clima/
    ├── Tecnologia - /tecnologia/
    └── Escatologia - /escatologia/
```

### URLs do Site

- **Home:** `/` ou `/home/`
- **Seções:** `/geopolitica/`, `/economia/`, `/clima/`, `/tecnologia/`, `/escatologia/`
- **Artigos:** `/geopolitica/nome-do-artigo/`, `/economia/outro-artigo/`, etc.
- **Admin:** `/admin/`
- **Django Admin:** `/django-admin/`

## 🎨 Customização Visual

### Customizar Cores e Fontes

1. Acesse `/admin/snippets/content/sitecustomization/`
2. Clique em "Add Site Customization"
3. Configure:
   - **Fontes:** Escolha fontes do Google Fonts
   - **Cores:** Use códigos hexadecimais (ex: #E3120B)
   - **Layout:** Ative/desative seção de vídeos, ajuste artigos por página

## 🐛 Solução de Problemas

### Erro 404 nas Seções

**Problema:** Acessar `/geopolitica/` retorna 404

**Solução:**
1. Execute o comando de setup: `python manage.py setup_site`
2. OU crie as páginas de seção manualmente no admin
3. Verifique que o slug está correto (geopolitica, não geopolítica com acento)
4. Certifique-se que a página está publicada (não rascunho)

### Imagens Não Aparecem

**Problema:** Imagens não carregam no site

**Solução:**
1. Para imagens locais:
   ```bash
   python manage.py collectstatic
   ```
2. Para URLs externas:
   - Verifique se a URL é acessível
   - Certifique-se que começa com http:// ou https://

### Site Não Carrega

**Problema:** Erro ao acessar a home page

**Solução:**
1. Verifique se executou as migrações:
   ```bash
   python manage.py migrate
   ```
2. Execute o comando de setup:
   ```bash
   python manage.py setup_site
   ```
3. Verifique se há uma HomePage publicada:
   ```bash
   python manage.py shell
   >>> from content.models import HomePage
   >>> HomePage.objects.all()
   ```

### Artigos Não Aparecem na Seção

**Problema:** Criou artigos mas não aparecem na página da seção

**Solução:**
1. Verifique se o artigo está publicado (não em rascunho)
2. Certifique-se que o campo "Seção" do artigo corresponde à section_key da página de seção
3. Verifique se o artigo é filho (child) da página de seção ou da HomePage

## 📚 Recursos Adicionais

### Documentação

- **FEATURES_GUIDE.md:** Guia completo de funcionalidades
- **IMPLEMENTATION_SUMMARY.md:** Resumo técnico das implementações
- **README.md:** Visão geral do projeto

### Comandos Úteis

```bash
# Criar migração após alterar models
python manage.py makemigrations

# Aplicar migrações
python manage.py migrate

# Criar superusuário
python manage.py createsuperuser

# Coletar arquivos estáticos
python manage.py collectstatic

# Configurar estrutura do site
python manage.py setup_site

# Iniciar servidor de desenvolvimento
python manage.py runserver

# Abrir shell Django
python manage.py shell
```

## 🚢 Deploy em Produção

Para deploy em produção (Azure, AWS, etc.):

1. Configure variáveis de ambiente no `.env`:
   ```
   DEBUG=False
   ALLOWED_HOSTS=seudominio.com
   DATABASE_URL=postgres://...
   SECRET_KEY=sua-chave-secreta-forte
   ```

2. Execute migrações:
   ```bash
   python manage.py migrate
   ```

3. Colete arquivos estáticos:
   ```bash
   python manage.py collectstatic --noinput
   ```

4. Configure o site:
   ```bash
   python manage.py setup_site
   ```

5. Inicie o servidor com Gunicorn:
   ```bash
   gunicorn core.wsgi:application
   ```

---

## ✅ Checklist de Configuração

- [ ] Dependências instaladas (`pip install -r requirements.txt`)
- [ ] Variáveis de ambiente configuradas (`.env`)
- [ ] Migrações executadas (`python manage.py migrate`)
- [ ] Superusuário criado (`python manage.py createsuperuser`)
- [ ] Site configurado (`python manage.py setup_site`)
- [ ] Servidor iniciado (`python manage.py runserver`)
- [ ] HomePage acessível em `/`
- [ ] Seções acessíveis em `/geopolitica/`, `/economia/`, etc.
- [ ] Admin acessível em `/admin/`

---

**Desenvolvido com ❤️ para o Portal de Análise**
