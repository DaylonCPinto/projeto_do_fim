# Guia de Funcionalidades do Portal de Análise

Este documento descreve todas as funcionalidades implementadas no projeto e como utilizá-las.

## 📋 Índice

1. [Sistema de Usuários e Perfis](#sistema-de-usuários-e-perfis)
2. [Sistema de Assinatura Premium](#sistema-de-assinatura-premium)
3. [Sistema de Tags/Tópicos](#sistema-de-tagstópicos)
4. [Gerenciamento de Conteúdo](#gerenciamento-de-conteúdo)
5. [Rotas e URLs](#rotas-e-urls)

---

## Sistema de Usuários e Perfis

### Cadastro de Usuários

O formulário de cadastro inclui os seguintes campos:
- **Nome de usuário**: Identificador único do usuário
- **E-mail**: Obrigatório e validado para unicidade
- **CPF**: Obrigatório, validado e único no sistema (formato: XXX.XXX.XXX-XX)
- **Senha**: Com confirmação e validações de segurança

**Rota de Cadastro:**
```
/accounts/signup/
```

**Como usar:**
1. Acesse `/accounts/signup/` no navegador
2. Preencha todos os campos obrigatórios
3. O CPF será validado automaticamente
4. Após o registro, o usuário é automaticamente autenticado

### Perfil de Usuário

Cada usuário tem um perfil (`UserProfile`) criado automaticamente com:
- CPF
- Status de assinante (gratuito/premium)
- Data de assinatura (quando aplicável)

---

## Sistema de Assinatura Premium

### Como Funciona

O sistema permite que administradores concedam acesso premium aos usuários, permitindo que vejam conteúdo exclusivo.

### Gerenciar Usuários Premium - Django Admin

**Acesso:** `/django-admin/`

#### Método 1: Através da Lista de Usuários

1. Acesse `/django-admin/auth/user/`
2. Selecione os usuários desejados marcando as caixas de seleção
3. No menu "Ação", escolha:
   - **"✓ Ativar assinatura premium"** - para ativar
   - **"✗ Desativar assinatura premium"** - para desativar
4. Clique em "Ir"

#### Método 2: Através dos Perfis de Usuário

1. Acesse `/django-admin/accounts/userprofile/`
2. Visualize todos os perfis com status de assinatura
3. Selecione os perfis desejados
4. Use as ações em massa (igual ao Método 1)

#### Método 3: Editando Individualmente

1. Acesse `/django-admin/auth/user/`
2. Clique no usuário desejado
3. Na seção "Perfil do Assinante", marque/desmarque "Assinante Ativo?"
4. Salve as alterações

### Visualização de Status

O admin exibe visualmente o status dos usuários:
- **★ PREMIUM** - Badge vermelho para assinantes ativos
- **☆ GRATUITO** - Badge cinza para usuários gratuitos
- **✓ Assinante Premium** - Ícone verde na lista de usuários
- **✗ Gratuito** - Ícone cinza na lista de usuários

### Conteúdo Premium

Artigos marcados como "Conteúdo Exclusivo" só são acessíveis para:
- Usuários com `is_subscriber=True`
- Administradores (staff)

---

## Sistema de Tags/Tópicos

### O que são Tags?

Tags (ou tópicos) permitem categorizar os artigos para melhor organização e navegação.

### Como Adicionar Tags aos Artigos

**Via Wagtail Admin:**

1. Acesse `/admin/` (Wagtail Admin)
2. Navegue até "Pages" → "Home" → Seus artigos
3. Edite um artigo
4. No campo "Tags", digite o nome da tag e pressione Enter
5. Você pode adicionar múltiplas tags
6. Salve o artigo

**Exemplos de tags:**
- Economia
- Política
- Tecnologia
- Esportes
- Internacional

### Gerenciar Tags Existentes

**Via Django Admin:**

1. Acesse `/django-admin/`
2. Navegue até "Taggit" → "Tags"
3. Aqui você pode:
   - Ver todas as tags utilizadas
   - Editar nomes de tags
   - Excluir tags não utilizadas
   - Ver quantos artigos usam cada tag

### Filtrar Artigos por Tag

As tags podem ser usadas para:
- Filtrar artigos no admin
- Criar páginas de categoria (implementação futura)
- Melhorar SEO e navegação

**Programaticamente:**
```python
from content.models import ArticlePage

# Buscar artigos com tag específica
artigos = ArticlePage.objects.live().filter(tags__name="Economia")

# Buscar todas as tags de um artigo
artigo = ArticlePage.objects.first()
tags = artigo.tags.all()
```

---

## Gerenciamento de Conteúdo

### Criar Novo Artigo

1. Acesse `/admin/` (Wagtail Admin)
2. Navegue até "Pages"
3. Clique em "Home"
4. Clique em "Add child page"
5. Escolha "Article Page"
6. Preencha os campos:
   - **Title**: Título do artigo
   - **Data de Publicação**: Quando o artigo foi/será publicado
   - **Introdução**: Breve resumo (máx. 250 caracteres)
   - **Conteúdo Exclusivo**: Marque se for apenas para premium
   - **Imagem de Destaque**: Upload da imagem principal
   - **Corpo do Artigo**: Conteúdo completo (editor rico)
   - **Tags**: Categorias do artigo
7. Clique em "Publish"

### Editar Artigos Existentes

1. Acesse `/admin/pages/`
2. Navegue até o artigo desejado
3. Clique em "Edit"
4. Faça as alterações
5. Clique em "Save draft" (rascunho) ou "Publish" (publicar)

### Imagens de Destaque

As imagens são gerenciadas pelo Wagtail:
- Acesse `/admin/images/` para ver todas as imagens
- Upload automático ao adicionar em um artigo
- Redimensionamento automático

---

## Rotas e URLs

### URLs Públicas

| Rota | Descrição |
|------|-----------|
| `/` | Página inicial com listagem de artigos |
| `/accounts/signup/` | Cadastro de novos usuários |
| `/accounts/login/` | Login de usuários |
| `/accounts/logout/` | Logout (POST) |
| `/[slug-do-artigo]/` | Página individual do artigo |

### URLs Administrativas

| Rota | Descrição |
|------|-----------|
| `/admin/` | Wagtail Admin (gerenciar conteúdo) |
| `/django-admin/` | Django Admin (gerenciar usuários/sistema) |
| `/django-admin/auth/user/` | Lista de usuários |
| `/django-admin/accounts/userprofile/` | Lista de perfis |
| `/admin/pages/` | Gerenciar páginas (Wagtail) |
| `/admin/images/` | Gerenciar imagens (Wagtail) |

### URLs de Recuperação de Senha

| Rota | Descrição |
|------|-----------|
| `/accounts/password_reset/` | Solicitar reset de senha |
| `/accounts/password_reset/done/` | Confirmação de email enviado |
| `/accounts/reset/<uidb64>/<token>/` | Link do email para resetar |
| `/accounts/reset/done/` | Senha alterada com sucesso |

---

## Configurações Importantes

### Localização

O projeto está configurado para:
- **Idioma**: Português do Brasil (pt-br)
- **Fuso Horário**: America/Sao_Paulo (GMT-3, Horário de Brasília)

Todas as datas e horários exibidos respeitam essas configurações.

### Sessões

- Duração: 2 semanas
- Cookie HTTPOnly: Sim (segurança)
- Cookie SameSite: Lax

---

## Fluxo de Trabalho Recomendado

### Para Administradores

1. **Gerenciar Usuários Premium:**
   - Use `/django-admin/auth/user/` para ações em massa
   - Ou `/django-admin/accounts/userprofile/` para visão detalhada

2. **Criar Conteúdo:**
   - Use `/admin/` (Wagtail) para criar/editar artigos
   - Sempre adicione tags relevantes
   - Marque "Conteúdo Exclusivo" para artigos premium

3. **Organização:**
   - Revise as tags periodicamente
   - Mantenha consistência nos nomes das tags
   - Use imagens de alta qualidade

### Para Desenvolvedores

1. **Acessar dados via código:**
```python
from django.contrib.auth.models import User
from accounts.models import UserProfile
from content.models import ArticlePage

# Verificar se usuário é premium
user = User.objects.get(username='exemplo')
is_premium = user.userprofile.is_subscriber

# Buscar artigos premium
premium_articles = ArticlePage.objects.live().filter(is_premium=True)

# Buscar artigos por tag
tagged_articles = ArticlePage.objects.live().filter(tags__name="Economia")
```

2. **Template tags úteis:**
```django
{% load wagtailcore_tags %}
{% load navigation_tags %}

{# Verificar se usuário é premium #}
{% if request.user.userprofile.is_subscriber %}
    {# Conteúdo exclusivo #}
{% endif %}

{# Listar tags de um artigo #}
{% for tag in page.tags.all %}
    {{ tag.name }}
{% endfor %}
```

---

## Próximos Passos e Melhorias Sugeridas

### Funcionalidades a Implementar

1. **Sistema de Pagamento:**
   - Integração com gateway de pagamento
   - Renovação automática de assinaturas
   - Histórico de pagamentos

2. **Páginas de Tag:**
   - Criar páginas que listam artigos por tag
   - URL: `/topico/[nome-da-tag]/`

3. **Busca Avançada:**
   - Busca por título, conteúdo, tags
   - Filtros múltiplos

4. **Dashboard do Usuário:**
   - Página de perfil do usuário
   - Histórico de leitura
   - Gerenciar assinatura

5. **Newsletter:**
   - Cadastro de emails
   - Envio automático de novos artigos

6. **Comentários:**
   - Sistema de comentários nos artigos
   - Moderação de comentários

7. **Analytics:**
   - Artigos mais lidos
   - Estatísticas de acesso
   - Dashboard para administradores

---

## Perguntas Frequentes

### Como ativar um usuário premium?

Use o Django Admin (`/django-admin/auth/user/`), selecione o usuário e use a ação "Ativar assinatura premium".

### Onde gerencio as tags?

Via Wagtail Admin (`/admin/`) ao editar artigos, ou via Django Admin (`/django-admin/taggit/tag/`) para gerenciamento completo.

### Como adiciono CPF a usuários existentes?

Via Django Admin (`/django-admin/accounts/userprofile/`), edite cada perfil e adicione o CPF.

### Posso ter artigos sem tags?

Sim, tags são opcionais. Mas é recomendado usar tags para melhor organização.

### Como removo o acesso premium de um usuário?

Use o Django Admin, selecione o usuário e use a ação "Desativar assinatura premium".

---

## Suporte

Para mais informações, consulte:
- **README.md** - Visão geral do projeto
- **MIGRATION_GUIDE.md** - Migração de dados
- **AZURE_DEPLOYMENT.md** - Deploy em produção
- **SECURITY_CHECKLIST.md** - Checklist de segurança

---

**Última atualização:** 2025-10-10
