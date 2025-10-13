# Trending and Premium Article Features - Documentation

## Overview
This document describes the new features implemented for article management, including trending articles, premium content, and display hierarchy.

## Features Implemented

### 1. Destaque Principal Fixo (Fixed Main Highlight)

**Admin Field:** `is_featured_highlight` (Artigo de Alto Impacto?)

**Behavior:**
- When enabled, the article becomes the main highlight on the homepage
- Remains fixed at the top regardless of new publications
- Only one article should be marked as highlight at a time (first one takes precedence)
- Must be manually unmarked in admin to be replaced

**Usage:**
1. Edit an article in Wagtail admin
2. Check "Artigo de Alto Impacto?" in the article settings
3. Publish the article
4. The article will appear as the main highlight on the homepage

---

### 2. Notícias "Em Alta" (Trending News)

**Admin Fields:** 
- `is_trending` (Em Alta?)
- `trending_until` (Em Alta Até)

**Automatic Behavior:**
- **New articles are automatically marked as "Em Alta" for 3 hours** after publication
- During this period:
  - Title appears in **orange color** (#FF8C00)
  - Animated 🔥 emoji appears on the article image
  - Article appears in the "Em Alta" section before regular articles

**Manual Control:**
- You can manually mark/unmark articles as "Em Alta" in the admin
- Manually marked articles remain "Em Alta" until you unmark them
- The `trending_until` field controls automatic expiration

**Visual Indicators:**
- Orange title color
- Animated fire emoji 🔥 on article image
- Appears in dedicated "🔥 Em Alta" section

**Display Order:**
- Trending articles appear immediately after the main highlight
- Sorted by publication date (most recent first)

---

### 3. Artigos Premium (Premium Articles)

**Admin Field:** `is_premium` (Conteúdo Exclusivo?)

**Behavior:**
- Premium articles have **red titles** (#E3120B)
- Display a red star ⭐ before the title
- **Only visible to users in the "assinantes_premium" group**
- Non-subscribers will not see premium articles in any listing
- Premium articles follow normal chronological order (don't override trending)

**Setting Up Premium Subscribers:**
1. Go to Django admin (Settings → Groups)
2. Create a group named "assinantes_premium"
3. Add users to this group to grant premium access

**Visual Indicators:**
- Red title color
- Red star ⭐ emoji before title
- "Premium" badge next to title

---

### 4. Display Hierarchy

Articles are displayed in the following order on the homepage:

```
1. DESTAQUE PRINCIPAL (Fixed Highlight)
   └─ Article marked with is_featured_highlight=True
   
2. EM ALTA (Trending)
   └─ Articles with is_trending=True and valid trending_until
   └─ Sorted by publication_date (newest first)
   
3. ARTIGOS REGULARES E PREMIUM (Regular & Premium)
   └─ All other articles in chronological order
   └─ Premium articles hidden from non-subscribers
   └─ Sorted by publication_date (newest first)
```

---

### 5. Time Display Format

**Feature:** All article listings now show relative time instead of absolute dates

**Format Examples:**
- "Postado há 2 horas"
- "Postado há 1 dia"
- "Postado há 5 dias"
- "Postado há 2 meses"

**Implementation:** Uses the `timesince_brasilia` template filter with Brasília timezone (America/Sao_Paulo)

---

### 6. Paragraph Spacing Fix

**Issue Resolved:** Pressing Enter in the article editor now properly creates paragraph spacing

**CSS Implementation:**
```css
.rich-text p,
.richtext p,
[data-block-key] p {
    margin-bottom: 1.5rem;
}
```

This ensures proper spacing between paragraphs in article content.

---

## CSS Classes Added

### Trending Articles
```css
.trending-title a { color: #FF8C00 !important; }
.trending-fire-badge { /* Animated fire emoji */ }
@keyframes flicker { /* Fire animation */ }
```

### Premium Articles
```css
.premium-article-title a { color: #E3120B !important; }
.premium-star { color: #E3120B; }
```

---

## Database Fields

### ArticlePage Model

| Field | Type | Description |
|-------|------|-------------|
| `is_featured_highlight` | BooleanField | Marks article as main highlight (fixed) |
| `is_trending` | BooleanField | Marks article as trending |
| `trending_until` | DateTimeField | Automatic expiration for trending status |
| `is_premium` | BooleanField | Marks article as premium content |

---

## Migration

**File:** `content/migrations/0020_articlepage_is_trending_articlepage_trending_until.py`

Adds the `is_trending` and `trending_until` fields to the ArticlePage model.

---

## Admin Configuration

All fields are accessible in the Wagtail admin under "Configurações do Artigo" (Article Settings):
- Data de Publicação
- Seção
- Conteúdo Exclusivo? (Premium)
- Artigo de Alto Impacto? (Main Highlight)
- Em Alta? (Trending)
- Em Alta Até (Trending Until)

---

## User Groups Required

### assinantes_premium
**Purpose:** Grants access to premium articles

**Setup:**
1. Django Admin → Groups → Add Group
2. Name: `assinantes_premium`
3. Add users to this group for premium access

---

## Template Updates

### Updated Templates:
1. `content/templates/content/home_page.html`
2. `content/templates/content/section_page.html`
3. `content/templates/content/support_section_page.html`

All templates now include:
- Trending articles section with fire emoji
- Premium article styling
- Relative time display
- Proper article hierarchy

---

## Testing Checklist

- [x] New articles automatically become trending for 3 hours
- [x] Trending articles display with orange titles and fire emoji
- [x] Premium articles display with red titles and star
- [x] Premium articles hidden from non-subscribers
- [x] Main highlight stays fixed at top
- [x] All timestamps show relative time format
- [x] Paragraph spacing works correctly
- [x] Features work on Home, Section, and Support pages

---

## Troubleshooting

### Trending not working
1. Check that the article is published (`live=True`)
2. Verify `is_trending=True` in admin
3. Check if `trending_until` is in the future (or None for manual trending)

### Premium articles visible to all users
1. Verify the user group is named exactly "assinantes_premium"
2. Check that the user is added to the group
3. Ensure user is authenticated

### Article not appearing in listings
1. Check if article is published
2. Verify it's not filtered by premium settings
3. Check if trending expiration has passed

---

## Future Enhancements (Optional)

1. **Admin action** to bulk set/unset trending status
2. **Scheduled task** to clean up expired trending articles
3. **Analytics** to track trending article performance
4. **Email notifications** for premium subscribers on new content
5. **Custom trending duration** per article (instead of fixed 3 hours)

---

## Code References

### Main Implementation Files
- `content/models.py` - ArticlePage model with new fields and methods
- `static/css/custom.css` - Styling for trending and premium articles
- `content/templatetags/navigation_tags.py` - Time display filter

### Key Methods
- `ArticlePage.save()` - Auto-sets trending for new articles
- `ArticlePage.is_currently_trending()` - Checks if article should show as trending
- `HomePage.get_context()` - Implements article hierarchy
- `SectionPage.get_context()` - Implements article hierarchy
- `SupportSectionPage.get_context()` - Implements article hierarchy
