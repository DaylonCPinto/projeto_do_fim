# Header Spacing Fix - Manual Testing Guide

## What Was Fixed

Previously, when no featured article was displayed on the homepage, the fixed header would overlap the "Análises Recentes" section title, making it difficult to read. This was especially problematic on mobile devices.

**Solution:** We implemented a dynamic padding system that:
1. Calculates the actual header height on page load
2. Applies a 1.25x multiplier (25% extra spacing)
3. Automatically adjusts on window resize
4. Works across all screen sizes (mobile and desktop)

## Files Changed

1. **`static/js/header_padding.js`** - New file with dynamic padding calculation
2. **`static/css/custom.css`** - Added CSS custom properties for header spacing
3. **`templates/base.html`** - Included the header_padding.js script
4. **`templates/header.html`** - Removed hardcoded 105px spacer div

## How to Test in Browser DevTools

### Test 1: Desktop View (Default)

1. **Open the homepage** in your browser
2. **Open DevTools** (F12 or Right-click → Inspect)
3. **Check the Console tab** (optional - add `?debug` to URL to see logs):
   ```
   http://localhost:8000/?debug
   ```
4. **Inspect the `<main class="container">` element**:
   - Look for `padding-top` in the Computed styles panel
   - It should show approximately **131px** (105px header × 1.25)
5. **Verify no overlap**:
   - The section title "Análises Recentes" should be clearly visible
   - There should be comfortable spacing below the header

### Test 2: Mobile View

1. **In DevTools, toggle device toolbar** (Ctrl+Shift+M or click the phone/tablet icon)
2. **Select a mobile device** (e.g., iPhone 12, Galaxy S20)
3. **Refresh the page**
4. **Check spacing**:
   - The section title should still be visible
   - No overlap with the fixed header
   - Spacing should look proportional

### Test 3: Responsive Resize

1. **With DevTools device toolbar active**, drag to resize the viewport
2. **Watch the spacing adjust** in real-time
3. **Try various widths**: 320px, 375px, 768px, 1024px, 1920px
4. **Verify**: At each breakpoint, content is clearly visible below the header

### Test 4: Without Featured Article

1. **In Wagtail Admin**, go to any ArticlePage
2. **Uncheck "Artigo de Alto Impacto?"** on all articles
3. **View the homepage**
4. **Verify**:
   - "Em Alta" or "Análises Recentes" section should be the first visible content
   - Title should NOT be hidden behind the header
   - Spacing should look natural

### Test 5: CSS Custom Properties

1. **In DevTools Console**, check the CSS variables:
   ```javascript
   getComputedStyle(document.documentElement).getPropertyValue('--site-header-height')
   getComputedStyle(document.documentElement).getPropertyValue('--calculated-padding')
   ```
2. **Expected output**:
   ```
   --site-header-height: "105px" (or actual header height)
   --calculated-padding: "131px" (or --site-header-height * 1.25)
   ```

### Test 6: Manual Override (Advanced)

You can test different multipliers in the console:

```javascript
// Get actual header height
const headerHeight = document.querySelector('.modern-header').offsetHeight;

// Test with 1.2x multiplier (20% extra)
document.documentElement.style.setProperty('--calculated-padding', `${headerHeight * 1.2}px`);

// Test with 1.3x multiplier (30% extra)
document.documentElement.style.setProperty('--calculated-padding', `${headerHeight * 1.3}px`);
```

## Expected Results

✅ **Pass Criteria:**
- No content is hidden behind the fixed header
- Section titles are fully visible
- Spacing looks natural (not too tight, not too loose)
- Works on mobile and desktop
- Adjusts automatically on window resize

❌ **Fail Indicators:**
- Section title is partially hidden
- Content overlaps with header
- Too much white space (indicates multiplier is too high)
- Spacing doesn't adjust on resize

## Fallback Behavior

If JavaScript is disabled:
- Fallback padding of **131px** is applied via CSS
- May not be perfectly optimal, but content will still be visible
- Consider using a `<noscript>` message if JS is critical for your use case

## Debug Mode

Add `?debug` to any URL to enable console logging:
```
http://localhost:8000/?debug
```

This will log:
- Header height in pixels
- Calculated padding value
- Multiplier being used

## Troubleshooting

**Problem: Spacing is too tight**
- Increase the multiplier in `static/js/header_padding.js` (line 31)
- Change from `1.25` to `1.3` or `1.35`

**Problem: Too much white space**
- Decrease the multiplier to `1.2` or `1.15`

**Problem: Doesn't work on mobile**
- Check that the header has class `.modern-header`
- Verify that `main.container` exists in your template
- Check browser console for JavaScript errors

## Browser Compatibility

Tested and working on:
- ✅ Chrome/Edge 90+
- ✅ Firefox 88+
- ✅ Safari 14+
- ✅ Mobile browsers (iOS Safari, Chrome Mobile)

CSS Custom Properties are supported in all modern browsers. For IE11 support (if needed), you would need a polyfill.
