# Quick Reference - Header e Créditos de Imagem

## 🎯 O que foi corrigido?

### Problema 1: Header cobrindo título
**Solução:** Adicionado espaçamento extra no topo dos artigos
- PC: +30% espaço
- Mobile: +5% espaço

### Problema 2: Falta de legendas e créditos em imagens
**Solução:** Adicionados 3 novos campos:
- Legenda (caption)
- Créditos (credit)  
- Posição (start/center/end)

---

## 📝 Como usar no Admin

### Imagem de Destaque

1. Vá até o artigo no Wagtail Admin
2. Seção "Imagem de Destaque"
3. Preencha:
   ```
   Imagem de Destaque: [escolher arquivo]
   Legenda: "Descrição da imagem..."
   Créditos: "Foto de João Silva/Reuters"
   Posição: "Início (Esquerda)" [padrão]
   ```

### Imagem Inline (ImageBlock/GifBlock)

1. Adicione um bloco de Imagem ou GIF
2. Preencha:
   ```
   Imagem/URL: [escolher]
   Legenda: "Descrição..."
   Crédito: "Fonte..."
   Posição: "Início" [padrão]
   ```

---

## 🎨 Posições Disponíveis

```
Início (Esquerda)  → Legenda... | Créditos: Fonte
Centro             →      Legenda... | Créditos: Fonte
Fim (Direita)      →                    Legenda... | Créditos: Fonte
```

**Recomendado:** Use "Início" para aspecto profissional

---

## ⚠️ Importante

- ✅ Sempre adicione créditos se a imagem não é sua
- ✅ Legendas são opcionais mas recomendadas
- ✅ Formato de créditos: "Foto de [Nome]/[Agência]"
- ❌ Não use HTML nas legendas (apenas texto)

---

## 🔧 Arquivos Modificados

```
content/models.py                          # Campos novos
content/templates/content/article_page.html # Display
content/templates/content/blocks/*.html     # Templates
static/css/custom.css                       # Estilos
```

---

## 📊 Migrações

3 migrações criadas e aplicadas:
- `0016_articlepage_featured_image_caption_and_more.py`
- `0017_alter_articlepage_content_blocks.py`
- `0018_alter_articlepage_content_blocks.py`

Para aplicar em produção:
```bash
python manage.py migrate
```

---

## 📚 Documentação Completa

- `HEADER_AND_IMAGE_CREDITS_FIX.md` - Guia técnico detalhado
- `VISUAL_COMPARISON.md` - Comparações visuais antes/depois
- `QUICK_REFERENCE.md` - Este arquivo (referência rápida)

---

**Status:** ✅ Pronto para produção  
**Backward Compatible:** Sim  
**Breaking Changes:** Não
