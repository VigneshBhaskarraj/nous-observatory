# Nous Observatory — Design Audit

Run a full visual + accessibility audit across all HTML pages in this project, using the exact standards established during the project's design history. Report every finding with file, line number, and a fix. Then implement all fixes, commit, and push.

## Pages to audit

- `index.html`
- `event.html`
- `model-advisor.html`
- `model-tree.html`

---

## Audit checklist

### 1. Navigation consistency
Every page must have **identical nav link order and icons** in the `.g-hdr`:
```
Overview | 🔍 Search | ⚗️ Models | 📡 Live Intel | ⬡ Model Tree | 🤖 Advisor
```
- All links must be present on every page
- Active page link must have class `on`
- No Power Map link (de-listed — page kept on disk)
- `index.html` uses `<button>` elements for Overview/Search/Models (internal tab switching); all other pages use `<a href="index.html#...">` for Search and Models

### 2. Global header (`g-hdr`) structure
Every page must have this exact structure:
```html
<div class="g-hdr">
  <a href="index.html" class="g-brand">
    <span style="font-size:20px;line-height:1">🔭</span>
    <div>
      <div class="g-brand-name">Nous Observatory</div>
      <div class="g-brand-tag">AI Intelligence Graph</div>
    </div>
  </a>
  <nav class="g-nav">...</nav>
  <div class="g-actions">...</div>
</div>
```
- `.g-brand-tag` color must be `#8b949e` (not `#475569` — too dark on the `#0f172a` header)
- `.g-hdr` must be `position:sticky; top:0; z-index:300`
- Theme toggle button must be present in `.g-actions`

### 3. Page identity strip
Every page must have a `.pg-id` or `.pg-id-dark` strip immediately after `.g-hdr`:
- Light-default pages (index, advisor, event): use `.pg-id` (white bg)
- Dark-default pages (model-tree): use `.pg-id pg-id-dark`
- `.pg-id` must have a `[data-theme="dark"]` override:
  ```css
  [data-theme="dark"] .pg-id { background:#0d1117; border-color:#30363d; }
  [data-theme="dark"] .pg-id-title { color:#c9d1d9; }
  [data-theme="dark"] .pg-id-desc { color:#8b949e; }
  ```

### 4. Dark mode — CSS variable overrides
The dark mode block `[data-theme="dark"]` must override these variables:
- `--bg:#0d1117`
- `--card:#161b22`
- `--border:#30363d`
- `--text:#c9d1d9`
- `--muted:#8b949e`
- `--accent:#818cf8` (NOT `#4f46e5` — only 2.6:1 contrast on dark bg, fails WCAG AA)
- `--accent-bg:rgba(129,140,248,.15)`

For `event.html` specifically, also override:
- `--indigo:#a5b4fc` (the `#4f46e5` default is near-invisible on dark backgrounds)
- `--google-blue:#60a5fa`

### 5. Dark mode — hardcoded color audit
Search every CSS rule for hardcoded hex/rgb colors that are NOT wrapped in a `[data-theme="dark"]` override. Flag any that would fail on a dark background. Common offenders:

| Hardcoded value | Problem | Dark mode replacement |
|---|---|---|
| `color: #475569` | ~3:1 contrast on dark card | `color:#8b949e` |
| `color: #334155` | Very dark, invisible on dark bg | `color:#8b949e` |
| `color: #1d4ed8` | Dark blue, ~2:1 on dark bg | `color:#93c5fd` |
| `color: #1e40af` | Very dark blue | `color:#93c5fd` |
| `color: #374151` | Near-black | `color:#8b949e` |
| `background: #fff` / `#ffffff` | White on dark bg | Add dark override |
| `background: #f8fafc` / `#f1f5f9` | Light gray on dark bg | Add dark override |
| `background: #dbeafe` with `color:#1d4ed8` | Light badge | Translucent dark equivalent |

### 6. Dark mode — sticky/fixed elements
Any element with `position:sticky` or `position:fixed` that has a hardcoded light background must have a `[data-theme="dark"]` override. Especially:
- Sticky table `thead th` in model matrices — must not show white on dark
- Sticky `td:first-child` columns — same
- `.subnav` / `.event-selector-bar` in event.html

### 7. Accessibility — keyboard navigation
All interactive non-`<button>` / non-`<a>` elements that have `onclick` must have:
- `role="button"`
- `tabindex="0"`
- `onkeydown="if(event.key==='Enter'||event.key===' '){event.preventDefault();/* same handler */}"`

### 8. Accessibility — canvas elements
- Decorative canvas (particle effects, backgrounds): `aria-hidden="true"`
- Functional canvas (charts, graphs, interactive): `role="img"` + `aria-label="...description..."`

### 9. Meta description
Every page must have:
```html
<meta name="description" content="...">
```

### 10. Sticky offset layering (event.html)
The three sticky bars must stack correctly:
- `.g-hdr`: `top:0`, height `52px` desktop / `~88px` mobile (wraps)
- `.event-selector-bar`: `top:52px` desktop / `top:88px` mobile
- `.subnav`: `top:105px` desktop / `top:141px` mobile (52+53 / 88+53)

---

## Audit output format

For each finding, output:

```
[SEVERITY] file.html:line — Rule violated
  Current:  <the offending code>
  Expected: <what it should be>
```

Severity levels: `CRITICAL` (broken in dark mode / nav missing) · `HIGH` (contrast failure) · `MEDIUM` (accessibility) · `LOW` (consistency/polish)

After the report, implement **all** findings, commit with message `Design audit fixes: <summary>`, and push to `main`.
