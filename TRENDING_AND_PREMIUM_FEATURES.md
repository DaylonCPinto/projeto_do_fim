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

### 3. Artigos Premium (Premium Articles) - SOFT PAYWALL

**Admin Field:** `is_premium` (Conteúdo Exclusivo?)

**Behavior (Soft Paywall System):**
- Premium articles have **red titles** (#E3120B)
- Display a red star ⭐ before the title
- **Premium articles are VISIBLE in all listings** (home, sections, support pages)
- **Non-subscribers can see the article preview but not full content**
- Premium articles follow normal chronological order (don't override trending)

**Content Access Control:**
- **Non-subscribers:** See article in listings → Click to read → See introduction + first 2 content blocks → Paywall message
- **Subscribers:** See article in listings → Click to read → See full article content
- Access control is based on `UserProfile.is_subscriber` field (not groups)

**Setting Up Premium Subscribers:**
1. Go to Django admin (Accounts → User profiles)
2. Edit a user's profile
3. Check "Assinante Ativo?" (is_subscriber)
4. Save the profile
5. That user now has access to all premium content

**Visual Indicators:**
- Red title color in listings (#E3120B)
- Red star ⭐ emoji before title
- "Premium" badge next to title
- On article page: "Premium" badge in title

**Template Integration:**
- All listing templates (home_page.html, section_page.html, support_section_page.html) show premium indicators
- Article detail page (article_page.html) uses `is_subscriber` context variable for paywall logic

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
   └─ All articles in chronological order (INCLUDING premium)
   └─ Premium articles visible to all users in listings
   └─ Content access restricted on detail page for non-subscribers
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

## User Subscription System

### UserProfile.is_subscriber Field
**Purpose:** Controls access to premium article content (NOT visibility in listings)

**Model:** `accounts.models.UserProfile`

**Setup:**
1. Django Admin → Accounts → User profiles
2. Select a user's profile
3. Check "Assinante Ativo?" (is_subscriber field)
4. Save

**Behavior:**
- Created automatically for all users via Django signals
- Default value: `False`
- When `True`: User can read full premium article content
- When `False`: User sees article preview + paywall message

**Migration Note:** This field should already exist from the accounts app setup

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
- [x] **Premium articles VISIBLE in all listings (soft paywall)**
- [x] **Premium content restricted on detail page for non-subscribers**
- [x] **Subscribers see full premium content**
- [x] Main highlight stays fixed at top
- [x] All timestamps show relative time format
- [x] Paragraph spacing works correctly
- [x] Features work on Home, Section, and Support pages
- [x] Comprehensive test suite passing (19 tests)

---

## Troubleshooting

### Trending not working
1. Check that the article is published (`live=True`)
2. Verify `is_trending=True` in admin
3. Check if `trending_until` is in the future (or None for manual trending)

### Premium content showing to non-subscribers
1. Verify the user's `UserProfile.is_subscriber` is set to `True` in Django admin
2. Ensure user is authenticated
3. Check that the article_page.html template is using the correct `is_subscriber` context variable

### Premium articles not appearing in listings
1. Articles SHOULD appear in listings (this is the soft paywall behavior)
2. Check if article is published (`live=True`)
3. Verify article is not being filtered as featured or trending
4. If articles appear in trending section instead of regular section, this is correct (new articles auto-trend)

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
- `accounts/models.py` - UserProfile model with is_subscriber field
- `static/css/custom.css` - Styling for trending and premium articles
- `content/templatetags/navigation_tags.py` - Time display filter
- `content/templates/content/article_page.html` - Article detail with paywall logic
- `content/templates/content/home_page.html` - Home page with premium indicators
- `content/templates/content/section_page.html` - Section page with premium indicators
- `content/templates/content/support_section_page.html` - Support section with premium indicators

### Key Methods
- `ArticlePage.save()` - Auto-sets trending for new articles
- `ArticlePage.is_currently_trending()` - Checks if article should show as trending
- `ArticlePage.get_context()` - Adds is_subscriber flag to context for paywall
- `HomePage.get_context()` - Implements article hierarchy (shows ALL articles including premium)
- `SectionPage.get_context()` - Implements article hierarchy (shows ALL articles including premium)
- `SupportSectionPage.get_context()` - Implements article hierarchy (shows ALL articles including premium)

### Test Files
- `content/test_premium_and_trending.py` - Tests for premium and trending persistence
- `content/test_soft_paywall.py` - Tests for soft paywall functionality

---

## Soft Paywall Implementation Details

### How It Works

1. **Listings Behavior**: 
   - All articles (including premium) appear in listings
   - Premium articles show visual indicators: ⭐ + red title + "Premium" badge
   - No filtering based on user subscription status

2. **Article Detail Behavior**:
   - `ArticlePage.get_context()` sets `is_subscriber` in context
   - Template checks: `{% if page.is_premium %}{% if is_subscriber %}`
   - **Subscribers**: See full content
   - **Non-subscribers**: See introduction + first 2 content blocks + paywall overlay

3. **Subscriber Check Logic**:
   ```python
   is_subscriber = (
       user.is_authenticated and 
       hasattr(user, 'userprofile') and
       user.userprofile.is_subscriber
   )
   ```

4. **Template Usage**:
   - Listings: Check `article.specific.is_premium` for styling
   - Detail page: Check `is_subscriber` context variable for content access

### Benefits of Soft Paywall
- Better SEO (all content indexed)
- Increases premium article discovery
- Clear value proposition for subscriptions
- Users can see what they're missing
