#!/usr/bin/env python3
"""Convert paired lang-en/lang-zh spans into data-i18n elements; collect en+zh map.
Handles index.html & support.html fully, and privacy.html's inline nav/footer pairs
(the privacy BODY two-div block is converted separately by hand)."""
import re, json, os

WEB = "/Users/pan/Workspace/Projects/AI Projects/BlindClock/Website"
PAGES = [("index.html", "i"), ("support.html", "s"), ("privacy.html", "p")]

PAIR = re.compile(
    r'<span class="lang-en">(.*?)</span>\s*<span class="lang-zh">(.*?)</span>',
    re.DOTALL)
SWITCH = re.compile(r'<div class="lang-switch"[\s\S]*?</div>')

source = {}  # key -> {en, zh}

for fname, prefix in PAGES:
    path = os.path.join(WEB, fname)
    html = open(path).read()
    counter = [0]

    def repl(m):
        counter[0] += 1
        key = f"{prefix}{counter[0]}"
        en = m.group(1).strip()
        zh = m.group(2).strip()
        source[key] = {"en": en, "zh-Hant": zh}
        return f'<span data-i18n="{key}">{en}</span>'

    html = PAIR.sub(repl, html)
    # swap 2-button switcher for a dropdown
    html = SWITCH.sub('<select id="lang-select" class="lang-select" aria-label="Language"></select>', html)
    # load i18n.js (defines BC_STRINGS) before lang.js
    html = html.replace(
        '<script src="assets/lang.js"></script>',
        '<script src="assets/i18n.js"></script>\n  <script src="assets/lang.js"></script>')
    open(path, "w").write(html)
    print(f"{fname}: converted {counter[0]} inline pairs")

json.dump(source, open(os.path.join(WEB, "_web_source.json"), "w"), ensure_ascii=False, indent=2)
print(f"\nTOTAL keys collected: {len(source)} -> _web_source.json")
print("remaining lang-en occurrences (should be privacy body block only):")
for fname, _ in PAGES:
    n = open(os.path.join(WEB, fname)).read().count('class="lang-en"')
    print(f"  {fname}: {n}")
