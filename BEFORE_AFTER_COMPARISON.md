# Comparação: Antes e Depois das Mudanças

## 1. Sidebar "Seções de Apoio"

### ANTES (Hardcoded)
```html
<ul class="dropdown-menu dropdown-menu-end" aria-labelledby="sectionsDropdown">
    <li><a class="dropdown-item" href="/geopolitica/"><i class="bi bi-globe"></i> Geopolítica</a></li>
    <li><a class="dropdown-item" href="/economia/"><i class="bi bi-graph-up"></i> Economia</a></li>
    <li><a class="dropdown-item" href="/clima/"><i class="bi bi-cloud-rain"></i> Clima</a></li>
    <li><a class="dropdown-item" href="/tecnologia/"><i class="bi bi-cpu"></i> Tecnologia</a></li>
</ul>
```

**Problemas:**
- Exibia as 4 seções principais, não as seções de apoio
- Não mostrava páginas do tipo `SupportSectionPage`
- Links hardcoded que não refletiam conteúdo dinâmico

### DEPOIS (Dinâmico)
```html
<ul class="dropdown-menu dropdown-menu-end" aria-labelledby="sectionsDropdown">
    {% get_support_sections as support_sections %}
    {% for section in support_sections %}
        <li><a class="dropdown-item" href="{% pageurl section %}"><i class="bi bi-book"></i> {{ section.title }}</a></li>
    {% empty %}
        <li><span class="dropdown-item text-muted">Nenhuma seção de apoio disponível</span></li>
    {% endfor %}
</ul>
```

**Vantagens:**
- Exibe apenas páginas do tipo `SupportSectionPage`
- Atualiza automaticamente quando novas seções são criadas
- Mostra mensagem quando não há seções disponíveis
- Usa ícone de livro (bi-book) apropriado para seções de apoio

---

## 2. URLs das Seções de Apoio

### ANTES
```
URL gerada: /q/ ou slug incorreto
Exemplo: meudominio.com/q/
```

**Problemas:**
- Slug não era gerado corretamente
- Sem prefixo que identifique como seção de apoio
- URL não descritiva

### DEPOIS
```python
def get_url_parts(self, request=None):
    """Override to add /subsecao/ prefix to support section URLs"""
    url_parts = super().get_url_parts(request=request)
    
    if url_parts is None:
        return None
        
    site_id, root_url, page_path = url_parts
    
    # Add /subsecao/ prefix before the page slug
    if page_path and not page_path.startswith('/subsecao/'):
        page_path = f'/subsecao{page_path}'
    
    return (site_id, root_url, page_path)
```

```
URL gerada: /subsecao/escatologia/
Exemplo: meudominio.com/subsecao/escatologia/
```

**Vantagens:**
- URL descritiva e semântica
- Prefixo `/subsecao/` identifica claramente o tipo de conteúdo
- Slug baseado no título da página
- SEO-friendly

---

## 3. Opções de Tamanho de Fonte

### ANTES
```python
SIZE_CHOICES = [
    ('2rem', 'Pequeno (2rem)'),
    ('2.5rem', 'Médio (2.5rem)'),
    ('3rem', 'Grande (3rem)'),
    ('3.5rem', 'Extra Grande (3.5rem)'),
    ('4rem', 'Muito Grande (4rem)'),
]
```

**Problemas:**
- Menor tamanho era 2rem (ainda muito grande)
- Nomenclatura inconsistente
- Poucas opções para textos menores

### DEPOIS
```python
SIZE_CHOICES = [
    ('1rem', 'Muito Pequeno (1rem)'),
    ('1.5rem', 'Pequeno (1.5rem)'),
    ('2rem', 'Médio (2rem)'),
    ('2.5rem', 'Grande (2.5rem)'),
    ('3rem', 'Muito Grande (3rem)'),
    ('3.5rem', 'Extra Grande (3.5rem)'),
    ('4rem', 'Enorme (4rem)'),
]
```

**Vantagens:**
- Opções menores (1rem, 1.5rem) para textos mais discretos
- Nomenclatura clara e progressiva
- Mais flexibilidade para customização
- Aplicado tanto em `SectionPage` quanto em `SupportSectionPage`

---

## 4. Template Tag para Navegação

### ANTES
Não existia - seções eram hardcoded no template

### DEPOIS
```python
@register.simple_tag()
def get_support_sections():
    """Get all published support section pages for navigation"""
    SupportSectionPage = apps.get_model('content', 'SupportSectionPage')
    return SupportSectionPage.objects.live().order_by('title')
```

**Vantagens:**
- Reutilizável em qualquer template
- Filtra apenas páginas publicadas (`.live()`)
- Ordenação alfabética por título
- Fácil de manter e estender

---

## Fluxo de Uso: Criando uma Seção de Apoio

### 1. No Admin Wagtail
```
/admin/pages/ → Home → Add child page → Seção de Apoio
```

### 2. Preencher Formulário
- **Título**: Escatologia
- **Introdução**: (opcional) Texto sobre a seção
- **Fonte do Título**: Roboto (ou outra)
- **Tamanho do Título**: Médio (2rem) - AGORA COM OPÇÃO DE 1rem ou 1.5rem
- **Fonte do Subtítulo**: Merriweather
- **Tamanho do Subtítulo**: Pequeno (1.5rem) - AGORA REALMENTE PEQUENO

### 3. Publicar

### 4. Resultado
- ✅ Aparece automaticamente no dropdown "Seções de apoio"
- ✅ URL: `meudominio.com/subsecao/escatologia/`
- ✅ Tamanhos menores disponíveis para customização

---

## Impacto das Mudanças

### Performance
- ✅ Query otimizada (usa `.live()` filter do Wagtail)
- ✅ Cache automático do Wagtail para páginas

### Manutenção
- ✅ Código mais limpo e manutenível
- ✅ Sem hardcoding de links
- ✅ Fácil adicionar/remover seções

### UX (Experiência do Usuário)
- ✅ Sidebar reflete conteúdo real do site
- ✅ URLs semânticas e descritivas
- ✅ Mais opções de customização visual

### SEO
- ✅ URLs descritivas melhoram indexação
- ✅ Estrutura clara de navegação
