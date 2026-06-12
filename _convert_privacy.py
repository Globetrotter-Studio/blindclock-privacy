#!/usr/bin/env python3
"""Convert privacy.html's two parallel language blocks into one data-i18n block."""
import re, json

WEB = "/Users/pan/Workspace/Projects/AI Projects/BlindClock/Website"
path = WEB + "/privacy.html"
html = open(path).read()

ZH_COMMENT = "<!-- ===================== 繁體中文"
region_start = html.index('<div class="lang-en">')
region_end = html.index("</main>")
en_div = html[region_start:html.index(ZH_COMMENT)]            # lang-en wrapper (full)
zh_div = html[html.index(ZH_COMMENT):region_end]              # lang-zh wrapper (full)

LEAF = re.compile(r"<(h1|h2|p|li)(\b[^>]*)>(.*?)</\1>", re.DOTALL)

en_leaves = LEAF.findall(en_div)   # list of (tag, attrs, inner)
zh_leaves = LEAF.findall(zh_div)

assert len(en_leaves) == len(zh_leaves), f"leaf mismatch en={len(en_leaves)} zh={len(zh_leaves)}"

# build map + inject data-i18n into the en block sequentially
m = json.load(open(WEB + "/_web_source.json"))
counter = [0]
def inject(mat):
    counter[0] += 1
    key = f"pv{counter[0]}"
    tag, attrs, inner = mat.group(1), mat.group(2), mat.group(3)
    en_inner = inner.strip()
    zh_inner = zh_leaves[counter[0]-1][2].strip()
    m[key] = {"en": en_inner, "zh-Hant": zh_inner}
    return f'<{tag}{attrs} data-i18n="{key}">{inner}</{tag}>'

new_en = LEAF.sub(inject, en_div)
new_en = new_en.replace('<div class="lang-en">', '<div class="policy">', 1)

html = html[:region_start] + new_en + "\n" + html[region_end:]
open(path, "w").write(html)
json.dump(m, open(WEB + "/_web_source.json", "w"), ensure_ascii=False, indent=2)

print(f"privacy body: converted {counter[0]} leaf elements")
print(f"source map total keys: {len(m)}")
print("sample pairs:")
for k in ["pv1", "pv2", "pv3"]:
    print(f"  {k} EN: {m[k]['en'][:70]}")
    print(f"  {k} ZH: {m[k]['zh-Hant'][:50]}")
print("remaining lang-en/zh in privacy.html:", open(path).read().count('class="lang-en"'), open(path).read().count('class="lang-zh"'))
