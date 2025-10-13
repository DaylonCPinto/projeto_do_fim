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
