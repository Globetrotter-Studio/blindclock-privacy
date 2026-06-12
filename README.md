# BlindClock Website

GitHub Pages site for the BlindClock iOS app (repo: `Globetrotter-Studio/blindclock-privacy`).
Three static pages, bilingual (EN / 繁體中文) via a client-side toggle — no build step.

## Pages & App Store Connect URLs

| Page | File | Live URL | Used as |
|---|---|---|---|
| Marketing landing | `index.html` | `https://globetrotter-studio.github.io/blindclock-privacy/` | 行銷 URL (Marketing URL) |
| Support | `support.html` | `https://globetrotter-studio.github.io/blindclock-privacy/support.html` | 支援 URL (Support URL) |
| Privacy Policy | `privacy.html` | `https://globetrotter-studio.github.io/blindclock-privacy/privacy.html` | 隱私權政策 URL (Privacy Policy URL) |

> ⚠️ `index.html` used to BE the privacy policy. After deploying this version,
> update the Privacy Policy URL in App Store Connect to point at `privacy.html`.
> Do **not** rename the GitHub repo — it would break every URL above.

## Language switching (12 languages, since v1.9)

The site is localized in **English, 繁體中文, 日本語, 한국어, Deutsch, Français, Italiano, Polski, Português (BR), Español (LA), Türkçe, Tiếng Việt**.

- **English lives in the HTML** (so the page works with JS off and is indexable). Every other language lives in `assets/i18n.js` as `window.BC_STRINGS[lang][key]`.
- Each translatable element carries a `data-i18n="<key>"` attribute. `assets/lang.js` swaps that element's `innerHTML` to the chosen language (or restores the English default).
- `assets/lang.js` sets `data-lang` on `<html>` and builds the `<select id="lang-select">` dropdown from its `LANGS` list.
- Priority: `?lang=<code>` query param → saved choice (localStorage) → browser language → English.
- **To change/add copy:** edit `_web_source.json` (`key → { en, zh-Hant }`) then rebuild i18n.js, OR edit the value directly in `assets/i18n.js`. To add a *new language*: add it to `LANGS` in `lang.js` and add its block to `BC_STRINGS`.

> The repo keeps the build helpers used in v1.9: `_web_source.json` (key → en + zh-Hant source),
> `_build_i18n.py` (regenerates `assets/i18n.js`), and the one-off `_convert*.py` scripts.

## 🔁 Release checklist — update this site with EVERY app release

When a new version (e.g. 1.11) ships, update:

1. **`index.html`**
   - Version pill in the hero (`Version 1.9 …` → new version). Update the English default in the HTML **and** the `i8` value in `_web_source.json` / each language in `assets/i18n.js`.
   - The “What’s new in X.Y” section (`i27`, `i28a/b`, `i29a/b`, `i30a/b`): replace with the new release notes in every language.
   - Feature grid: add/adjust cards if features were added, removed, or re-tiered (free vs Pro).
2. **`support.html`**
   - Version number in the `.meta` line (`s4`).
   - FAQ entries: add questions for new features; fix any answers invalidated by changes.
   - Minimum OS line / supported-languages line (`s25`) if they changed.
3. **`privacy.html`** — only if data practices changed (new SDK, new data collected, new permission).
   If changed, also bump the “Effective date” (`pv2`) in every language.
4. **Translations:** after editing any English string, update its translation for all 11 other languages (edit `_web_source.json` + `python3 _build_i18n.py`, or edit `assets/i18n.js` directly).
5. Fill in the real App Store URL in `index.html` (`store-badge` link) once the app page is live.
6. Commit and push to `main` — GitHub Pages deploys automatically.

## Local preview

```sh
python3 -m http.server 8000
# open http://localhost:8000
```
