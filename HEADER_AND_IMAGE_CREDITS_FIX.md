# Correção do Header e Créditos de Imagem

**Data:** 2025-10-13  
**Branch:** copilot/fix-header-overlap-and-image-credits

## 📋 Problemas Resolvidos

### 1. Header Cobrindo Títulos de Artigos
**Problema:** O header fixo estava cobrindo o título dos artigos tanto no PC quanto no celular.

**Solução Implementada:**
- **PC (Desktop):** Aumentado o espaçamento superior em ~30%
- **Mobile:** Aumentado o espaçamento superior em ~5%

### 2. Falta de Legendas e Créditos em Imagens de Destaque
**Problema:** Não havia como adicionar legendas e créditos para imagens de destaque, e não era possível escolher a posição da legenda.

**Solução Implementada:**
- Adicionados 3 novos campos no ArticlePage:
  - Legenda da Imagem de Destaque
  - Créditos da Imagem de Destaque
  - Posição da Legenda (Início/Centro/Fim)
- Estendido para ImageBlock e GifBlock (blocos de conteúdo inline)

---

## 🔧 Mudanças Detalhadas

### 1. Espaçamento do Header nos Artigos

**Arquivo:** `static/css/custom.css`

```css
.article-header {
    border-bottom: 1px solid #ddd;
    padding-bottom: 1.5rem;
    margin-bottom: 2rem;
    padding-top: 1.5rem;  /* Espaçamento base para mobile (~5%) */
    margin-top: 0.5rem;
}

/* Desktop - aumenta o espaçamento superior */
@media (min-width: 769px) {
    .article-header {
        padding-top: 3rem;  /* ~30% a mais de espaço no desktop */
        margin-top: 1rem;
    }
}
```

**Resultado:**
- No PC: Título do artigo não é mais coberto pelo header
- No celular: Espaçamento adequado sem ocupar muito espaço

---

### 2. Campos de Legenda e Créditos

**Arquivo:** `content/models.py` - ArticlePage

```python
# Caption and credits for featured image
featured_image_caption = models.CharField(
    max_length=255,
    blank=True,
    verbose_name="Legenda da Imagem de Destaque",
    help_text="Legenda descritiva para a imagem de destaque"
)

featured_image_credit = models.CharField(
    max_length=255,
    blank=True,
    verbose_name="Créditos da Imagem de Destaque",
    help_text="Créditos/fonte da imagem (ex: Foto de João Silva/Reuters)"
)

# Caption position choices
CAPTION_POSITION_CHOICES = [
    ('text-start', 'Início (Esquerda)'),
    ('text-center', 'Centro'),
    ('text-end', 'Fim (Direita)'),
]

featured_image_caption_position = models.CharField(
    max_length=20,
    choices=CAPTION_POSITION_CHOICES,
    default='text-start',
    verbose_name="Posição da Legenda",
    help_text="Escolha onde a legenda e créditos devem aparecer"
)
```

**Admin Panel Atualizado:**
```python
MultiFieldPanel([
    FieldPanel('featured_image'),
    FieldPanel('external_image_url'),
    FieldPanel('featured_image_caption'),        # NOVO
    FieldPanel('featured_image_credit'),         # NOVO
    FieldPanel('featured_image_caption_position'), # NOVO
], heading="Imagem de Destaque (escolha uma opção)"),
```

---

### 3. Template de Exibição

**Arquivo:** `content/templates/content/article_page.html`

```html
<!-- IMAGEM DE DESTAQUE -->
{% if page.featured_image or page.external_image_url %}
<div class="featured-image-container mb-4">
    {% if page.external_image_url %}
        <img src="{{ page.external_image_url }}" alt="{{ page.title }}" class="img-fluid rounded">
    {% elif page.featured_image %}
        {% image page.featured_image original class="img-fluid rounded" %}
    {% endif %}
    
    {% if page.featured_image_caption or page.featured_image_credit %}
    <div class="featured-image-caption {{ page.featured_image_caption_position }}">
        {% if page.featured_image_caption %}
            <span>{{ page.featured_image_caption }}</span>
        {% endif %}
        {% if page.featured_image_credit %}
            <span class="featured-image-credit">
                {% if page.featured_image_caption %} | {% endif %}
                Créditos: {{ page.featured_image_credit }}
            </span>
        {% endif %}
    </div>
    {% endif %}
</div>
{% endif %}
```

---

### 4. Estilos CSS para Legendas

**Arquivo:** `static/css/custom.css`

```css
/* Featured Image Caption & Credits */
.featured-image-container {
    position: relative;
}

.featured-image-caption {
    margin-top: 0.5rem;
    font-size: 0.9rem;
    color: #666;
    font-style: italic;
}

.featured-image-caption.text-start {
    text-align: left;
}

.featured-image-caption.text-center {
    text-align: center;
}

.featured-image-caption.text-end {
    text-align: right;
}

.featured-image-credit {
    font-size: 0.85rem;
    color: #888;
    font-weight: 500;
}
```

---

### 5. Blocos de Conteúdo (ImageBlock e GifBlock)

**ImageBlock** - Adicionado campo `caption_position`:
```python
caption_position = blocks.ChoiceBlock(
    choices=[
        ('text-start', 'Início (Esquerda)'),
        ('text-center', 'Centro'),
        ('text-end', 'Fim (Direita)'),
    ],
    default='text-start',
    required=False,
    label="Posição da Legenda",
)
```

**GifBlock** - Adicionados campos `credit` e `caption_position`:
```python
credit = blocks.CharBlock(
    required=False,
    label="Crédito"
)
caption_position = blocks.ChoiceBlock(
    choices=[
        ('text-start', 'Início (Esquerda)'),
        ('text-center', 'Centro'),
        ('text-end', 'Fim (Direita)'),
    ],
    default='text-start',
    required=False,
    label="Posição da Legenda",
)
```

**Templates atualizados para usar a posição e créditos**

---

## 📊 Migrações Criadas

1. **0016_articlepage_featured_image_caption_and_more.py**
   - Adiciona `featured_image_caption`
   - Adiciona `featured_image_credit`
   - Adiciona `featured_image_caption_position`

2. **0017_alter_articlepage_content_blocks.py**
   - Atualiza ImageBlock com `caption_position`

3. **0018_alter_articlepage_content_blocks.py**
   - Atualiza GifBlock com `credit` e `caption_position`

---

## 🎯 Como Usar no Admin

### Para Imagem de Destaque:

1. Acesse o artigo no Wagtail Admin
2. Vá até a seção "Imagem de Destaque"
3. Preencha os novos campos:
   - **Legenda da Imagem de Destaque:** Descrição da imagem
   - **Créditos da Imagem de Destaque:** Fonte/fotógrafo (ex: "Foto de João Silva/Reuters")
   - **Posição da Legenda:** Escolha onde a legenda deve aparecer
4. Salve o artigo

### Para Imagens Inline (ImageBlock/GifBlock):

1. Ao adicionar um ImageBlock ou GifBlock no conteúdo
2. Preencha os campos:
   - **Legenda:** Descrição da imagem
   - **Crédito:** Fonte da imagem
   - **Posição da Legenda:** Escolha o alinhamento
3. A legenda e créditos aparecerão conforme configurado

---

## ✅ Benefícios

1. **Melhor experiência de leitura:** Títulos não são mais cobertos pelo header
2. **Compliance de direitos autorais:** Créditos podem ser adicionados facilmente
3. **Flexibilidade:** Escolha a posição da legenda conforme o layout desejado
4. **Consistência:** Mesmo sistema em todos os tipos de imagem
5. **Padrão correto:** Créditos aparecem no início (esquerda) por padrão

---

## 🔄 Valores de Referência

### Espaçamento Desktop
- **padding-top:** 3rem (~48px)
- **margin-top:** 1rem (~16px)
- **Total:** ~64px de espaço extra

### Espaçamento Mobile
- **padding-top:** 1.5rem (~24px)
- **margin-top:** 0.5rem (~8px)
- **Total:** ~32px de espaço extra

---

## 📝 Notas Importantes

- **Posição padrão:** Legendas aparecem à esquerda (início) por padrão
- **Créditos obrigatórios:** Use sempre que a imagem não for de sua autoria
- **Formato sugerido:** "Foto de [Nome]/[Agência]" ou "Créditos: [Fonte]"
- **Campos opcionais:** Todos os campos de legenda/créditos são opcionais

---

## 🧪 Testes Realizados

- ✅ Django system check passou sem erros
- ✅ Migrações aplicadas com sucesso
- ✅ Código Python validado
- ✅ Templates renderizam corretamente
- ✅ CSS formatado e válido

---

**Autor:** GitHub Copilot  
**Revisor:** Aguardando review  
**Status:** Pronto para produção
