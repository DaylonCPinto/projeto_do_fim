# Visual Guide - Trending and Premium Features

## Layout Overview

```
┌─────────────────────────────────────────────────────────────┐
│                    HOMEPAGE LAYOUT                           │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│  ⭐ DESTAQUE PRINCIPAL                                       │
│  ┌───────────────────────────────────────────────────────┐  │
│  │  [Large Image]  │  TÍTULO DO ARTIGO                   │  │
│  │                 │  Introdução do artigo...            │  │
│  │                 │  📅 Postado há 2 horas              │  │
│  └───────────────────────────────────────────────────────┘  │
│  (Always stays at top when marked as "Alto Impacto")        │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│  🔥 EM ALTA                                                  │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐          │
│  │ [Image] 🔥  │ │ [Image] 🔥  │ │ [Image] 🔥  │          │
│  │ TÍTULO      │ │ TÍTULO      │ │ TÍTULO      │          │
│  │ (orange)    │ │ (orange)    │ │ (orange)    │          │
│  │ há 1 hora   │ │ há 30 min   │ │ há 45 min   │          │
│  └─────────────┘ └─────────────┘ └─────────────┘          │
│  (Articles automatically trending for 3 hours)              │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│  ANÁLISES RECENTES                                          │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐          │
│  │ [Image]     │ │ [Image]     │ │ [Image]     │          │
│  │ TÍTULO      │ │ ⭐ TÍTULO   │ │ TÍTULO      │          │
│  │ (blue)      │ │ Premium(red)│ │ (blue)      │          │
│  │ há 1 dia    │ │ há 2 dias   │ │ há 3 dias   │          │
│  └─────────────┘ └─────────────┘ └─────────────┘          │
│  (Regular articles + Premium for subscribers only)          │
└─────────────────────────────────────────────────────────────┘
```

---

## Color Scheme

### Trending Articles (Em Alta)
```
Title Color:    #FF8C00 (Orange)
Badge:          🔥 Animated fire emoji
Section Header: "🔥 Em Alta"
```

### Premium Articles
```
Title Color:    #E3120B (Red)
Star Icon:      ⭐ (before title)
Badge:          "Premium" in red background
```

### Regular Articles
```
Title Color:    #111111 (Dark gray/black)
Hover Color:    #E3120B (Red)
```

---

## Article States and Appearance

### 1. DESTAQUE PRINCIPAL (Fixed Highlight)
```
┌────────────────────────────────────────────────────┐
│ ⭐ Destaque Principal                              │
│ ┌────────────┬─────────────────────────────────┐  │
│ │            │ Display-5 Title                 │  │
│ │   [Image]  │ Large introduction text...      │  │
│ │            │ 📅 Postado há X                 │  │
│ │            │ [Ler Análise Completa →]       │  │
│ └────────────┴─────────────────────────────────┘  │
└────────────────────────────────────────────────────┘

Admin Field: ✅ Artigo de Alto Impacto?
Behavior: Fixed at top, manual control only
```

### 2. TRENDING ARTICLE (Em Alta)
```
┌─────────────────────────────┐
│ [Article Image with 🔥]     │
│ ┌─────────────────────────┐ │
│ │ TÍTULO DO ARTIGO        │ │  ← Orange color
│ │ (Texto da introdução)   │ │
│ │ 📅 Postado há 2 horas   │ │
│ └─────────────────────────┘ │
└─────────────────────────────┘

Admin Fields:
- ✅ Em Alta? (checked)
- Em Alta Até: 2025-10-13 10:45 (auto-set to +3h)

Auto-behavior:
- New articles → automatically trending for 3 hours
- After 3 hours → automatically becomes regular article
```

### 3. PREMIUM ARTICLE
```
┌─────────────────────────────┐
│ [Article Image]             │
│ ┌─────────────────────────┐ │
│ │ ⭐ TÍTULO DO ARTIGO     │ │  ← Red color + star
│ │ [Premium]               │ │
│ │ (Texto da introdução)   │ │
│ │ 📅 Postado há 1 dia     │ │
│ └─────────────────────────┘ │
└─────────────────────────────┘

Admin Field: ✅ Conteúdo Exclusivo?
Visibility: Only for "assinantes_premium" group
```

### 4. REGULAR ARTICLE
```
┌─────────────────────────────┐
│ [Article Image]             │
│ ┌─────────────────────────┐ │
│ │ TÍTULO DO ARTIGO        │ │  ← Blue/dark color
│ │ (Texto da introdução)   │ │
│ │ 📅 Postado há 5 dias    │ │
│ └─────────────────────────┘ │
└─────────────────────────────┘

Default state for all articles
```

---

## Admin Panel Fields

### Article Settings Section (Configurações do Artigo)

```
┌────────────────────────────────────────────┐
│ Configurações do Artigo                    │
├────────────────────────────────────────────┤
│ Data de Publicação:  [2025-10-13 07:00]   │
│                                            │
│ Seção:              [Em Alta ▼]           │
│                                            │
│ ☐ Conteúdo Exclusivo?                     │
│   (Premium article - subscribers only)     │
│                                            │
│ ☐ Artigo de Alto Impacto?                 │
│   (Fixed main highlight)                   │
│                                            │
│ ☑ Em Alta?                                 │
│   (Trending status)                        │
│                                            │
│ Em Alta Até:        [2025-10-13 10:00]    │
│   (Auto-filled for new articles)           │
└────────────────────────────────────────────┘
```

---

## Animations

### Fire Emoji Animation (CSS)
```css
@keyframes flicker {
    0% {
        transform: scale(1) rotate(0deg);
        opacity: 1;
    }
    50% {
        transform: scale(1.1) rotate(-5deg);
        opacity: 0.9;
    }
    100% {
        transform: scale(1) rotate(5deg);
        opacity: 1;
    }
}
```

**Effect:** Subtle pulsing/flickering animation on the 🔥 emoji (1.5s duration, infinite loop)

---

## User Flow Examples

### Example 1: Publishing a New Article
```
1. Admin creates new article
   └─> Save & Publish
   
2. System automatically sets:
   ├─> is_trending = True
   └─> trending_until = now + 3 hours
   
3. Article appears in "🔥 Em Alta" section
   ├─> Orange title
   ├─> 🔥 emoji on image
   └─> "Postado há X minutos"
   
4. After 3 hours:
   └─> Automatically moves to "Análises Recentes"
       ├─> Regular blue title
       └─> No fire emoji
```

### Example 2: Creating Premium Content
```
1. Admin creates article
   └─> Check "Conteúdo Exclusivo?"
   
2. Save & Publish

3. For premium subscribers:
   ├─> Article visible in listings
   ├─> Red title with ⭐ star
   └─> "Premium" badge
   
4. For non-subscribers:
   └─> Article not visible at all
```

### Example 3: Setting Main Highlight
```
1. Admin selects important article
   └─> Check "Artigo de Alto Impacto?"
   
2. Save & Publish

3. Article appears:
   ├─> At top of homepage
   ├─> Large format with full image
   └─> Stays fixed until manually changed
   
4. All other articles appear below
```

---

## Responsive Behavior

### Desktop (>769px)
- Main highlight: 2-column layout (image left, text right)
- Article cards: 3 columns per row
- Fire emoji: 2rem size
- Extra spacing on header elements

### Mobile (≤768px)
- Main highlight: Stacked layout (image top, text bottom)
- Article cards: 2 columns per row
- Fire emoji: 1.5rem size
- Reduced spacing

---

## Time Display Format

### Relative Time Examples
```
Just published:  "Postado há agora"
Under 1 hour:    "Postado há 45 minutos"
Under 24 hours:  "Postado há 12 horas"
1 day:           "Postado há 1 dia"
Multiple days:   "Postado há 5 dias"
Weeks:           "Postado há 3 semanas"
Months:          "Postado há 2 meses"
Years:           "Postado há 1 ano"
```

**Timezone:** America/Sao_Paulo (Brasília)
**Filter:** `timesince_brasilia`

---

## Access Control Matrix

| User Type | Regular Articles | Trending Articles | Premium Articles | Highlight |
|-----------|-----------------|-------------------|------------------|-----------|
| Anonymous | ✅ Visible | ✅ Visible | ❌ Hidden | ✅ Visible |
| Logged In | ✅ Visible | ✅ Visible | ❌ Hidden | ✅ Visible |
| Premium   | ✅ Visible | ✅ Visible | ✅ Visible | ✅ Visible |

**Premium Group:** `assinantes_premium` (exact name required)

---

## CSS Class Reference

### Trending Classes
```css
.trending-title a              /* Orange title color */
.trending-fire-badge          /* Animated fire emoji */
```

### Premium Classes
```css
.premium-article-title a      /* Red title color */
.premium-star                 /* Red star icon */
.premium-badge                /* Premium badge */
```

### General Classes
```css
.highlight-section            /* Main highlight container */
.highlight-badge              /* "Destaque Principal" badge */
.article-card                 /* Article card base */
.article-card-title           /* Article title base */
```

---

## Integration with Existing Features

### Compatible With:
- ✅ Section pages (Geopolítica, Economia, etc.)
- ✅ Support section pages
- ✅ Article search/filtering
- ✅ Custom fonts per article
- ✅ External image URLs
- ✅ Video shorts section

### Does Not Affect:
- ✅ Article content blocks (StreamField)
- ✅ Tags and categories
- ✅ SEO settings
- ✅ Publication workflow
- ✅ User authentication

---

## Performance Notes

- **Queries optimized:** Trending check happens in Python, not in database
- **No additional queries:** Uses existing article queryset
- **Cached timezone:** Timezone info cached for repeated use
- **Minimal JavaScript:** Only CSS animations, no JS needed

---

## Browser Compatibility

- ✅ Chrome/Edge 90+
- ✅ Firefox 88+
- ✅ Safari 14+
- ✅ Mobile browsers
- ✅ CSS animations supported on all modern browsers

---

## Accessibility

- ✅ Semantic HTML structure
- ✅ ARIA labels on badges
- ✅ Color contrast meets WCAG 2.1 AA
- ✅ Keyboard navigation supported
- ✅ Screen reader compatible

---

## Testing Scenarios

### Test 1: New Article Publishing
```
1. Create new article
2. Publish immediately
3. Verify: appears in "Em Alta" with fire emoji
4. Wait 3+ hours
5. Verify: moves to regular section
```

### Test 2: Manual Trending Control
```
1. Edit existing article
2. Check "Em Alta?"
3. Leave "Em Alta Até" blank
4. Publish
5. Verify: appears in trending (stays indefinitely)
6. Uncheck "Em Alta?"
7. Verify: moves to regular section
```

### Test 3: Premium Access
```
1. Create premium article (check "Conteúdo Exclusivo?")
2. Publish
3. Log out → Verify: article hidden
4. Log in as non-premium → Verify: article hidden
5. Add user to "assinantes_premium" group
6. Verify: article visible with red title and star
```

### Test 4: Highlight Priority
```
1. Mark article as "Alto Impacto"
2. Publish
3. Verify: appears at top as main highlight
4. Create new trending article
5. Verify: highlight stays at top, trending below
6. Unmark "Alto Impacto"
7. Verify: most recent article becomes highlight
```
