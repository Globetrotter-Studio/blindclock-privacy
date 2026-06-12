#!/usr/bin/env python3
"""Build assets/i18n.js (window.BC_STRINGS) from zh-Hant source + the 10-locale workflow output.
English is NOT included — it is the in-HTML default/fallback."""
import json, re, sys

WEB = "/Users/pan/Workspace/Projects/AI Projects/BlindClock/Website"
SRC = WEB + "/_web_source.json"
OUT = "/private/tmp/claude-501/-Users-pan-Workspace-Projects-AI-Projects-BlindClock-Website/5a37b262-204d-4a80-80ae-8a722fc86823/tasks/w8zbx8x5p.output"
ALT = "/private/tmp/claude-501/-Users-pan-Workspace-Projects-AI-Projects-BlindClock/5a37b262-204d-4a80-80ae-8a722fc86823/tasks/w8zbx8x5p.output"
NEW_LOCALES = ["ja", "ko", "de", "fr-FR", "it", "pl", "pt-BR", "es-MX", "tr", "vi"]

def tag_sig(s):
    """signature of structural HTML in a string: counts of tags/links to compare preservation."""
    return (
        len(re.findall(r"<a\b", s)), s.count("</a>"),
        len(re.findall(r"<b\b", s)), s.count("</b>"),
        len(re.findall(r"<i\b", s)), s.count("</i>"),
        len(re.findall(r"<br", s)),
        len(re.findall(r'href="[^"]*"', s)),
    )

def main():
    import os
    out_path = OUT if os.path.exists(OUT) else ALT
    src = json.load(open(SRC))
    res = json.load(open(out_path))["result"]["results"]
    by = {r["locale"]: {t["key"]: t["value"] for t in r["translations"]} for r in res}

    keys = list(src.keys())
    problems = []
    bc = {}
    # zh-Hant straight from the source map
    bc["zh-Hant"] = {k: src[k]["zh-Hant"] for k in keys}

    for loc in NEW_LOCALES:
        if loc not in by:
            problems.append(f"MISSING LOCALE {loc}")
            continue
        tmap = by[loc]
        d = {}
        for k in keys:
            if k not in tmap:
                problems.append(f"[{loc}] missing key {k}")
                continue
            v = tmap[k]
            if tag_sig(src[k]["en"]) != tag_sig(v):
                problems.append(f"[{loc}] HTML mismatch key={k}: en{tag_sig(src[k]['en'])} != tr{tag_sig(v)} :: {v[:80]!r}")
            d[k] = v
        bc[loc] = d

    print(f"=== problems: {len(problems)} ===")
    for p in problems[:60]:
        print("  " + p)
    if problems:
        print("\nABORTING — review HTML/key issues above.")
        return 1

    body = json.dumps(bc, ensure_ascii=False, indent=2, sort_keys=True)
    js = ("/* BlindClock site translations — generated, do not hand-edit lightly.\n"
          "   English is the in-HTML default; this file holds every other language.\n"
          "   Rebuild with Website/_build_i18n.py after changing _web_source.json. */\n"
          "window.BC_STRINGS = " + body + ";\n")
    open(WEB + "/assets/i18n.js", "w").write(js)
    print(f"\n=== WROTE assets/i18n.js ===")
    print(f"  languages: {', '.join(bc.keys())}")
    print(f"  keys per language: {len(keys)}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
