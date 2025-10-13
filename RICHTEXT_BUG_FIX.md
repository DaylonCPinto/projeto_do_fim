# Fix: Richtext Rendering Bug in Article Listings

## Problema Identificado

Nas páginas inicial, de seção e de seção de apoio, os artigos que não eram destaques estavam mostrando código interno do editor de texto Wagtail na introdução:

```
<p data-block-key="n68if">Grupo ficou mais de dois anos na Faixa de Gaza; acordo também prevê entrega …
```

Esse código `data-block-key="n68if"` é um resquício interno do Draft.js (editor usado pelo Wagtail) e não deveria aparecer para o público.

## Causa Raiz

O campo `introduction` no modelo `ArticlePage` é definido como `RichTextField`:

```python
introduction = RichTextField(
    max_length=500, 
    verbose_name="Introdução",
    features=['bold', 'italic', 'link'],
    help_text="Introdução do artigo (até 500 caracteres) com formatação básica"
)
```

Quando o Wagtail armazena conteúdo em um `RichTextField`, ele inclui metadados internos (como `data-block-key`) que são usados pelo editor para reconstruir o conteúdo na interface de administração.

O problema ocorreu porque os templates estavam exibindo esse conteúdo diretamente, sem passar pelo filtro `|richtext` do Wagtail, que converte o formato interno em HTML limpo.

## Solução Implementada

Adicionamos a cadeia de filtros `|richtext|striptags` antes do `|truncatewords:15` em três templates:

### 1. `content/templates/content/home_page.html` (linha 117)

**ANTES:**
```django
{{ article.specific.introduction|truncatewords:15 }}
```

**DEPOIS:**
```django
{{ article.specific.introduction|richtext|striptags|truncatewords:15 }}
```

### 2. `content/templates/content/section_page.html` (linha 90)

**ANTES:**
```django
{{ article.introduction|truncatewords:15 }}
```

**DEPOIS:**
```django
{{ article.introduction|richtext|striptags|truncatewords:15 }}
```

### 3. `content/templates/content/support_section_page.html` (linha 93)

**ANTES:**
```django
{{ article.introduction|truncatewords:15 }}
```

**DEPOIS:**
```django
{{ article.introduction|richtext|striptags|truncatewords:15 }}
```

## Como os Filtros Funcionam

A cadeia de filtros funciona da seguinte forma:

1. **`|richtext`** - Converte o formato interno do Wagtail (com `data-block-key` e outros metadados) em HTML limpo e renderizável
2. **`|striptags`** - Remove todas as tags HTML, deixando apenas o texto puro
3. **`|truncatewords:15`** - Limita o texto a 15 palavras

## Comparação Antes x Depois

### Antes (com o bug):
```
&lt;p data-block-key="n68if"&gt;Grupo ficou mais de dois anos na Faixa de …
```

### Depois (corrigido):
```
Grupo ficou mais de dois anos na Faixa de Gaza; acordo também prevê …
```

## Teste de Validação

Para validar a correção, executamos um teste demonstrando o comportamento:

```python
# Conteúdo com metadados internos do editor
raw_richtext = '<p data-block-key="n68if">Grupo ficou mais de dois anos na Faixa de Gaza...</p>'

# SEM |richtext filter (BUG)
{{ content|truncatewords:10 }}
# Resultado: &lt;p data-block-key=&quot;n68if&quot;&gt;Grupo ficou mais de dois anos...

# COM |richtext|striptags filter (CORREÇÃO)
{{ content|richtext|striptags|truncatewords:10 }}
# Resultado: Grupo ficou mais de dois anos na Faixa de Gaza...
```

## Prevenção

Para evitar problemas similares no futuro, sempre que exibir um campo `RichTextField` do Wagtail em templates:

1. **Para exibir HTML formatado:**
   ```django
   {{ page.field|richtext }}
   ```

2. **Para exibir como texto puro (sem HTML):**
   ```django
   {{ page.field|richtext|striptags }}
   ```

3. **Para prévia com truncamento:**
   ```django
   {{ page.field|richtext|striptags|truncatewords:N }}
   ```

## Referências

- [Wagtail RichTextField Documentation](https://docs.wagtail.org/en/stable/topics/writing_templates.html#rich-text-fields)
- [Django Template Filters](https://docs.djangoproject.com/en/stable/ref/templates/builtins/#built-in-filter-reference)

## Arquivos Modificados

- `content/templates/content/home_page.html`
- `content/templates/content/section_page.html`
- `content/templates/content/support_section_page.html`

## Impacto

✅ Corrige a exibição de introduções de artigos em todas as páginas de listagem  
✅ Remove o código interno do editor que estava aparecendo para os usuários  
✅ Melhora a experiência do usuário ao navegar pelo site  
✅ Sem impacto negativo - apenas melhoria visual  
✅ Mudanças mínimas e cirúrgicas em apenas 3 linhas de código
