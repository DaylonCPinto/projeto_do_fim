# Quick Start Guide - Trending & Premium Features

## 🚀 5-Minute Setup

### Step 1: Apply Database Changes
```bash
python manage.py migrate content
```

### Step 2: Create Premium Group
```bash
python manage.py shell
```
Then run:
```python
from django.contrib.auth.models import Group
Group.objects.get_or_create(name='assinantes_premium')
exit()
```

### Step 3: Collect Static Files
```bash
python manage.py collectstatic --no-input
```

### Step 4: Restart Server
Development:
```bash
python manage.py runserver
```

Production (example):
```bash
sudo systemctl restart gunicorn
```

---

## 📖 How to Use Each Feature

### 🏆 Create a Fixed Main Highlight
1. Go to Wagtail admin → Pages
2. Edit the article you want as main highlight
3. Scroll to "Configurações do Artigo"
4. Check ✅ **"Artigo de Alto Impacto?"**
5. Click "Publish"
6. Done! Article appears at top of homepage

**To change:** Uncheck the old one, check a new one.

---

### 🔥 Make an Article Trending
**Option A: Automatic (Recommended)**
- Just publish a new article
- It automatically becomes trending for 3 hours
- No action needed!

**Option B: Manual**
1. Edit any article in Wagtail admin
2. Check ✅ **"Em Alta?"**
3. Leave "Em Alta Até" blank (stays trending forever)
   OR set a date/time for auto-expiration
4. Click "Publish"

**To stop trending:** Uncheck "Em Alta?"

---

### ⭐ Create Premium Content
1. Edit article in Wagtail admin
2. Check ✅ **"Conteúdo Exclusivo?"**
3. Click "Publish"
4. Article now only visible to premium subscribers

**Add premium subscribers:**
1. Go to Django admin → Users
2. Edit user
3. Add to group: "assinantes_premium"
4. Save

---

## 👀 What You'll See

### Trending Articles (Em Alta)
- **Title:** Orange color
- **Badge:** Animated 🔥 emoji on image
- **Section:** "🔥 Em Alta"
- **Time:** "Postado há 2 horas"

### Premium Articles
- **Title:** Red color with ⭐ star
- **Badge:** "Premium"
- **Visibility:** Only for subscribers

### Main Highlight
- **Position:** Top of homepage
- **Layout:** Large image + text
- **Badge:** "⭐ Destaque Principal"

---

## ✅ Quick Test

### Test 1: Create New Article (1 minute)
1. Create any new article
2. Publish it
3. Check homepage → Should appear in "🔥 Em Alta" section
4. Title should be orange with fire emoji

### Test 2: Make Premium Article (2 minutes)
1. Edit an article
2. Check "Conteúdo Exclusivo?"
3. Publish
4. Log out → Article should be hidden
5. Log in as premium user → Article appears with red title

### Test 3: Set Main Highlight (1 minute)
1. Edit your best article
2. Check "Artigo de Alto Impacto?"
3. Publish
4. Check homepage → Article at top in large format

---

## 🎨 Visual Reference

**Homepage Layout:**
```
┌────────────────────────────┐
│ ⭐ DESTAQUE PRINCIPAL       │  ← Fixed, manual
│   (Large format)           │
└────────────────────────────┘
┌────────────────────────────┐
│ 🔥 EM ALTA                 │  ← Auto + manual
│ [Orange titles]            │
└────────────────────────────┘
┌────────────────────────────┐
│ ANÁLISES RECENTES          │  ← Regular + Premium
│ [Blue + Red titles]        │
└────────────────────────────┘
```

---

## 🆘 Troubleshooting

### Problem: "Em Alta" not working
**Solution:** Check that:
- Article is published (not draft)
- "Em Alta?" is checked
- If "Em Alta Até" is set, date is in the future

### Problem: Premium articles visible to everyone
**Solution:** Check that:
- Group name is exactly `assinantes_premium` (no spaces)
- User is in the group
- User is logged in

### Problem: New articles not auto-trending
**Solution:**
- This only works for NEW articles
- Existing articles need manual "Em Alta?" checkbox
- Check that article is published, not just saved

### Problem: Styles not showing
**Solution:**
```bash
python manage.py collectstatic --no-input
# Then restart server
```

---

## 📚 Full Documentation

For detailed information, see:
- **TRENDING_AND_PREMIUM_FEATURES.md** - Complete feature guide
- **VISUAL_GUIDE.md** - Visual layouts and test scenarios
- **IMPLEMENTATION_SUMMARY_2025-10-13.md** - Technical details

---

## 🎯 Success Checklist

After setup, verify:
- [ ] Migration applied successfully
- [ ] "assinantes_premium" group created
- [ ] Static files collected
- [ ] Server restarted
- [ ] Can create new trending article
- [ ] Can mark article as premium
- [ ] Can set main highlight
- [ ] Time showing as "Postado há X horas"
- [ ] Styles loading correctly (orange/red titles)

---

## 💡 Pro Tips

1. **Only one main highlight:** If multiple articles are marked "Alto Impacto", only the most recent one shows as highlight.

2. **Trending + Premium:** An article can be both trending AND premium. It will show orange title but only to premium subscribers.

3. **Manual trending:** To keep an article trending indefinitely, check "Em Alta?" but leave "Em Alta Até" blank.

4. **Time display:** All timestamps automatically update as time passes. No need to edit articles.

5. **Mobile friendly:** All features work on mobile devices with responsive design.

---

## 🔄 Updates

**Automatic behaviors:**
- ✅ New articles → auto-trending for 3 hours
- ✅ After 3 hours → automatically move to regular section
- ✅ Time display → automatically updates format

**Manual control:**
- ✅ Main highlight (check/uncheck "Alto Impacto")
- ✅ Trending status (check/uncheck "Em Alta")
- ✅ Premium status (check/uncheck "Conteúdo Exclusivo")

---

## 📞 Need Help?

Check the troubleshooting section above or review:
- TRENDING_AND_PREMIUM_FEATURES.md (detailed guide)
- VISUAL_GUIDE.md (visual examples)

---

**Status:** ✅ Ready to use  
**Setup time:** ~5 minutes  
**Difficulty:** Easy (just follow steps above)

---

## 🎨 Configure Homepage Layout

### NEW: Layout Customization (Admin-Configurable)

You can now customize the homepage layout without touching code!

### How to Change Layout

1. Go to Wagtail admin → Pages
2. Edit the HomePage
3. Scroll to **"Configurações de Layout da Home"**
4. Configure the following options:

#### Available Options:

**📐 Preset de Layout da Home:**
- **Grade de 3 Colunas (Padrão)** - Classic grid with 3 columns
- **Grade de 2 Colunas** - Wider cards with 2 columns
- **Lista com Divisores** - Full-width list with horizontal dividers
- **Destaque no Topo + Grade** - Featured article + grid below
- **Masonry Leve** - Pinterest-style masonry layout

**🖥️ Colunas (Desktop):** Choose 1-4 columns for desktop view
**📱 Colunas (Mobile):** Choose 1-2 columns for mobile view
**↔️ Espaçamento entre Cards:** Small, Medium, Large, or Extra Large
**〰️ Mostrar Divisores?** - Add horizontal lines between articles
**🔥 Mostrar Seção 'Em Alta'?** - Show or hide the trending section

### Example Configurations

#### Configuration 1: Compact Grid (More Content)
- Preset: Grade de 4 Colunas
- Desktop: 4 columns
- Mobile: 2 columns
- Gap: Pequeno (0.5rem)
- Dividers: No
- Trending: Yes

#### Configuration 2: Magazine Style
- Preset: Grade de 2 Colunas
- Desktop: 2 columns
- Mobile: 1 column
- Gap: Grande (1.5rem)
- Dividers: No
- Trending: Yes

#### Configuration 3: News Feed
- Preset: Lista com Divisores
- Desktop: 1 column
- Mobile: 1 column
- Gap: Médio (1rem)
- Dividers: Yes
- Trending: Yes

#### Configuration 4: Pinterest-Like
- Preset: Masonry Leve
- Desktop: 3 columns
- Mobile: 1 column
- Gap: Médio (1rem)
- Dividers: No
- Trending: Yes

### Changes Take Effect Immediately
- No code deployment needed
- Changes appear on next page refresh
- Preview in Wagtail's live preview mode

---

## 🐛 Bug Fixes in This Release

### 1. ✅ Premium Articles No Longer Expire
**Problem:** Premium articles were incorrectly expiring after 3 hours (same as trending).

**Solution:** 
- `is_premium` is now completely independent from trending logic
- Premium status persists until manually removed in admin
- Comprehensive tests ensure this never breaks

**How to Verify:**
1. Mark an article as premium
2. Wait 4+ hours (or use freezegun in tests)
3. Article should still be premium
4. Only appears to users in "assinantes_premium" group

### 2. ✅ Header No Longer Overlaps Content
**Problem:** When no featured article was shown, the fixed header would overlap the "Análises Recentes" title.

**Solution:**
- Dynamic padding calculation based on actual header height
- Automatically adjusts on window resize
- Works on mobile and desktop
- 25% extra spacing for visual comfort

**How to Verify:**
1. Remove featured article (uncheck "Artigo de Alto Impacto?" on all articles)
2. View homepage
3. Section title should be clearly visible below header
4. Test on mobile (DevTools → Toggle device toolbar)

**See Also:** [HEADER_SPACING_TEST_GUIDE.md](HEADER_SPACING_TEST_GUIDE.md) for detailed testing instructions.

---

## 🧪 Testing

### Automated Tests
```bash
# Run all content tests
python manage.py test content

# Run only premium/trending tests
python manage.py test content.test_premium_and_trending
```

### Manual Testing Checklist

✅ **Premium Articles:**
- [ ] Create premium article → verify it's hidden from non-subscribers
- [ ] Login as premium user → verify article is visible
- [ ] Wait 4+ hours → verify article is still premium

✅ **Trending Articles:**
- [ ] Create new article → verify auto-trending for 3 hours
- [ ] After 3 hours → verify it moves to regular section
- [ ] Manually set trending without expiration → verify it stays trending

✅ **Header Spacing:**
- [ ] View homepage without featured article
- [ ] Check that section titles are visible (not overlapped)
- [ ] Test on mobile (< 768px width)
- [ ] Test on desktop (>= 1024px width)

✅ **Layout Configuration:**
- [ ] Change layout preset in admin → verify homepage updates
- [ ] Test different column configurations
- [ ] Enable/disable dividers → verify visual change
- [ ] Hide trending section → verify it disappears
- [ ] Test on mobile and desktop

---

## 📚 Additional Documentation

- **[HEADER_SPACING_TEST_GUIDE.md](HEADER_SPACING_TEST_GUIDE.md)** - Detailed guide for testing header spacing fix
- **[TRENDING_AND_PREMIUM_FEATURES.md](TRENDING_AND_PREMIUM_FEATURES.md)** - Original feature documentation
- **[IMPLEMENTATION_SUMMARY_2025-10-13.md](IMPLEMENTATION_SUMMARY_2025-10-13.md)** - Technical implementation details

---

## 💡 Tips & Best Practices

### Premium Content
- Use premium sparingly for high-value content
- Premium articles show red title + ⭐ star icon
- Consider offering a preview/teaser for non-subscribers

### Trending Articles
- Let new articles auto-trend for 3 hours (best for engagement)
- Use manual trending for evergreen content
- Trending articles show orange title + 🔥 animated emoji

### Layout Configuration
- Start with default "Grade de 3 Colunas" preset
- For content-heavy sites, try 4 columns desktop + 2 mobile
- For magazine-style, try 2 columns with large gap
- List layout works well for news/blog feeds
- Masonry layout is great for varied content lengths

### Performance
- Layout changes are CSS-only (no JavaScript overhead)
- Header padding calculation is lightweight
- All layouts are fully responsive

---

## 🔧 Troubleshooting

### Premium Articles Still Appear to Non-Subscribers
1. Check user is in "assinantes_premium" group
2. Verify `is_premium=True` in article admin
3. Clear browser cache
4. Check for custom template overrides

### Trending Not Working
1. Verify article is published (`live=True`)
2. Check `is_trending=True` in admin
3. If using `trending_until`, ensure date is in future
4. Check template includes trending section

### Layout Not Changing
1. Verify changes were saved in admin
2. Hard refresh browser (Ctrl+F5 or Cmd+Shift+R)
3. Clear browser cache
4. Check CSS file is loaded (DevTools → Network tab)
5. Verify static files collected: `python manage.py collectstatic`

### Header Still Overlaps
1. Hard refresh browser to load new JavaScript
2. Check `header_padding.js` is loaded (DevTools → Sources)
3. Verify no JavaScript errors (DevTools → Console)
4. Test with debug mode: add `?debug` to URL

---

## 🚀 What's Next?

Future enhancements you could add:
1. Custom trending duration per article
2. A/B testing for different layouts
3. Analytics to track which layout performs best
4. Schedule layout changes (seasonal themes)
5. Per-section layout configuration
6. Dark mode support

