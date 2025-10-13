# Comparação Visual das Mudanças

## 1. Espaçamento do Header no Artigo

### Antes
```
┌─────────────────────────────────────┐
│         HEADER FIXO (105px)         │
└─────────────────────────────────────┘
┌─────────────────────────────────────┐  ← Sem padding/margin extra
│ # Título do Artigo (COBERTO!)      │
│ Data de publicação...               │
└─────────────────────────────────────┘
```

### Depois (PC)
```
┌─────────────────────────────────────┐
│         HEADER FIXO (105px)         │
└─────────────────────────────────────┘
│                                     │
│   Espaço extra (~64px)              │  ← padding-top: 3rem + margin-top: 1rem
│                                     │
┌─────────────────────────────────────┐
│ # Título do Artigo (VISÍVEL!)      │
│ Data de publicação...               │
└─────────────────────────────────────┘
```

### Depois (Mobile)
```
┌─────────────────────────────────────┐
│         HEADER FIXO (105px)         │
└─────────────────────────────────────┘
│                                     │
│   Espaço extra (~32px)              │  ← padding-top: 1.5rem + margin-top: 0.5rem
│                                     │
┌─────────────────────────────────────┐
│ # Título do Artigo (VISÍVEL!)      │
│ Data de publicação...               │
└─────────────────────────────────────┘
```

---

## 2. Legendas e Créditos de Imagens

### Antes (Sem legendas/créditos)
```
┌─────────────────────────────────────┐
│                                     │
│         [IMAGEM DE DESTAQUE]        │
│                                     │
└─────────────────────────────────────┘
```

### Depois - Posição "Início" (Padrão)
```
┌─────────────────────────────────────┐
│                                     │
│         [IMAGEM DE DESTAQUE]        │
│                                     │
└─────────────────────────────────────┘
Paisagem do Rio de Janeiro | Créditos: João Silva/Reuters
```

### Depois - Posição "Centro"
```
┌─────────────────────────────────────┐
│                                     │
│         [IMAGEM DE DESTAQUE]        │
│                                     │
└─────────────────────────────────────┘
     Paisagem do Rio de Janeiro | Créditos: João Silva/Reuters
```

### Depois - Posição "Fim"
```
┌─────────────────────────────────────┐
│                                     │
│         [IMAGEM DE DESTAQUE]        │
│                                     │
└─────────────────────────────────────┘
                Paisagem do Rio de Janeiro | Créditos: João Silva/Reuters
```

---

## 3. Admin Panel - Novos Campos

### Seção "Imagem de Destaque" no Wagtail Admin

```
┌──────────────────────────────────────────────────────────────┐
│ Imagem de Destaque (escolha uma opção)                       │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│ ┌────────────────────────────────────────────────────┐     │
│ │ Imagem de Destaque                                 │     │
│ │ [Escolher imagem]                                  │     │
│ └────────────────────────────────────────────────────┘     │
│                                                              │
│ ┌────────────────────────────────────────────────────┐     │
│ │ URL de Imagem Externa                              │     │
│ │ [https://...]                                      │     │
│ └────────────────────────────────────────────────────┘     │
│                                                              │
│ ┌────────────────────────────────────────────────────┐  ← NOVO
│ │ Legenda da Imagem de Destaque                      │     │
│ │ [Descrição da imagem...]                           │     │
│ └────────────────────────────────────────────────────┘     │
│                                                              │
│ ┌────────────────────────────────────────────────────┐  ← NOVO
│ │ Créditos da Imagem de Destaque                     │     │
│ │ [Foto de João Silva/Reuters]                       │     │
│ └────────────────────────────────────────────────────┘     │
│                                                              │
│ ┌────────────────────────────────────────────────────┐  ← NOVO
│ │ Posição da Legenda                                 │     │
│ │ [▼ Início (Esquerda)]                              │     │
│ │    Centro                                          │     │
│ │    Fim (Direita)                                   │     │
│ └────────────────────────────────────────────────────┘     │
│                                                              │
└──────────────────────────────────────────────────────────────┘
```

---

## 4. ImageBlock/GifBlock - Novos Campos

### Ao adicionar ImageBlock no conteúdo do artigo

```
┌──────────────────────────────────────────────────────────────┐
│ Imagem (Upload ou URL)                                       │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│ ┌────────────────────────────────────────────────────┐     │
│ │ Imagem (Upload)                                    │     │
│ │ [Escolher imagem]                                  │     │
│ └────────────────────────────────────────────────────┘     │
│                                                              │
│ ┌────────────────────────────────────────────────────┐     │
│ │ URL da Imagem                                      │     │
│ │ [https://...]                                      │     │
│ └────────────────────────────────────────────────────┘     │
│                                                              │
│ ┌────────────────────────────────────────────────────┐     │
│ │ Legenda                                            │     │
│ │ [Descrição...]                                     │     │
│ └────────────────────────────────────────────────────┘     │
│                                                              │
│ ┌────────────────────────────────────────────────────┐     │
│ │ Crédito                                            │     │
│ │ [Fonte...]                                         │     │
│ └────────────────────────────────────────────────────┘     │
│                                                              │
│ ┌────────────────────────────────────────────────────┐  ← NOVO
│ │ Posição da Legenda                                 │     │
│ │ [▼ Início (Esquerda)]                              │     │
│ └────────────────────────────────────────────────────┘     │
│                                                              │
└──────────────────────────────────────────────────────────────┘
```

---

## 5. Exemplos de Uso Real

### Exemplo 1: Imagem com Legenda e Créditos
```html
<div class="featured-image-container mb-4">
    <img src="https://example.com/image.jpg" alt="Artigo" class="img-fluid rounded">
    
    <div class="featured-image-caption text-start">
        <span>Manifestantes protestam em Brasília na manhã desta terça-feira</span>
        <span class="featured-image-credit">
            | Créditos: Agência Brasil/Reuters
        </span>
    </div>
</div>
```

**Renderizado:**
```
┌─────────────────────────────────────────────────────────────┐
│                                                             │
│              [FOTO DOS MANIFESTANTES]                       │
│                                                             │
└─────────────────────────────────────────────────────────────┘
Manifestantes protestam em Brasília... | Créditos: Agência Brasil/Reuters
```

### Exemplo 2: Imagem Apenas com Créditos
```html
<div class="featured-image-container mb-4">
    <img src="image.jpg" alt="Artigo" class="img-fluid rounded">
    
    <div class="featured-image-caption text-center">
        <span class="featured-image-credit">
            Créditos: João Silva/Reuters
        </span>
    </div>
</div>
```

**Renderizado:**
```
┌─────────────────────────────────────────────────────────────┐
│                                                             │
│                     [FOTO GERAL]                            │
│                                                             │
└─────────────────────────────────────────────────────────────┘
                    Créditos: João Silva/Reuters
```

---

## 6. CSS Classes Aplicadas

### Posições Disponíveis

```css
/* Início (Esquerda) - PADRÃO */
.featured-image-caption.text-start {
    text-align: left;
}

/* Centro */
.featured-image-caption.text-center {
    text-align: center;
}

/* Fim (Direita) */
.featured-image-caption.text-end {
    text-align: right;
}
```

### Estilo da Legenda

```css
.featured-image-caption {
    margin-top: 0.5rem;      /* Espaço entre imagem e legenda */
    font-size: 0.9rem;       /* Um pouco menor que o texto normal */
    color: #666;             /* Cinza médio */
    font-style: italic;      /* Itálico para destaque */
}
```

### Estilo dos Créditos

```css
.featured-image-credit {
    font-size: 0.85rem;      /* Menor que a legenda */
    color: #888;             /* Cinza mais claro */
    font-weight: 500;        /* Um pouco mais pesado */
}
```

---

## 7. Fluxo de Trabalho Recomendado

### Ao Criar um Artigo:

1. **Escolha a imagem de destaque**
   - Upload de arquivo local OU
   - URL de imagem externa

2. **Adicione a legenda** (opcional mas recomendado)
   - Descreva o que a imagem mostra
   - Seja conciso mas informativo

3. **Adicione os créditos** (obrigatório se não for sua imagem)
   - Formato: "Foto de [Nome]/[Agência]"
   - Exemplo: "Foto de Maria Silva/Agência Brasil"

4. **Escolha a posição**
   - **Início:** Para layout profissional (padrão)
   - **Centro:** Para imagens artísticas
   - **Fim:** Raramente usado

5. **Publique o artigo**

---

## 8. Boas Práticas

### ✅ Faça:
- Sempre adicione créditos se a imagem não for sua
- Use legendas descritivas
- Mantenha legendas concisas (máx. 255 caracteres)
- Use posição "Início" como padrão

### ❌ Não Faça:
- Deixar créditos em branco para imagens de terceiros
- Usar legendas muito longas
- Usar HTML nas legendas (texto plano apenas)
- Esquecer de verificar o preview antes de publicar

---

**Resultado Final:** Interface mais profissional, compliance com direitos autorais e melhor experiência para o usuário!
