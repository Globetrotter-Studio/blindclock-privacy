/* BlindClock site — path-based language switcher (v1.10+).
   Each language is a pre-rendered static folder. English is at the site root;
   every other language lives under /<slug>/ :
       (en) /   zh /zh   ja /jp   ko /ko   de /de   fr /fr   it /it
       pl /pl   pt-BR /pt   es-MX /es   tr /tr   vi /vi
   This script ONLY builds the <select> and navigates — content is already baked
   into each page (see _build_pages.py). No runtime text swapping.
   Keep LANGS in sync with _build_pages.py. */
(function () {
  /* [code, slug, label]  — slug "" = English at root. */
  var LANGS = [
    ["en", "", "English"],
    ["zh-Hant", "zh", "繁體中文"],
    ["ja", "jp", "日本語"],
    ["ko", "ko", "한국어"],
    ["de", "de", "Deutsch"],
    ["fr-FR", "fr", "Français"],
    ["it", "it", "Italiano"],
    ["pl", "pl", "Polski"],
    ["pt-BR", "pt", "Português (BR)"],
    ["es-MX", "es", "Español (LA)"],
    ["tr", "tr", "Türkçe"],
    ["vi", "vi", "Tiếng Việt"]
  ];

  var SLUG_TO_CODE = {};
  for (var i = 0; i < LANGS.length; i++) if (LANGS[i][1]) SLUG_TO_CODE[LANGS[i][1]] = LANGS[i][0];

  /* Split the current path into { base, slug, file }. Works both at the custom-
     domain root (/jp/privacy.html) and under a project subpath on github.io
     (/blindclock/jp/privacy.html). */
  function parse() {
    var path = location.pathname;
    var lastSlash = path.lastIndexOf("/");
    var tail = path.slice(lastSlash + 1);
    var file = /\.html?$/i.test(tail) ? tail : "";
    var dir = file ? path.slice(0, lastSlash + 1) : path;          // always ends with "/"
    var segs = dir.replace(/\/+$/, "").split("/");                  // ["", "blindclock", "jp"]
    var last = segs[segs.length - 1];
    var slug = "", base = dir;
    if (SLUG_TO_CODE[last]) {
      slug = last;
      base = segs.slice(0, -1).join("/") + "/";
    }
    if (base === "") base = "/";
    return { base: base, slug: slug, file: file };
  }

  function currentCode() {
    var p = parse();
    return p.slug ? SLUG_TO_CODE[p.slug] : "en";
  }

  function targetUrl(toSlug) {
    var p = parse();
    var file = (p.file === "" || p.file === "index.html") ? "" : p.file;  // clean dir URLs
    return p.base + (toSlug ? toSlug + "/" : "") + file;
  }

  document.addEventListener("DOMContentLoaded", function () {
    var sel = document.getElementById("lang-select");
    if (!sel) return;
    var cur = currentCode();
    for (var i = 0; i < LANGS.length; i++) {
      var o = document.createElement("option");
      o.value = LANGS[i][1];                  // slug ("" for English)
      o.textContent = LANGS[i][2];
      if (LANGS[i][0] === cur) o.selected = true;
      sel.appendChild(o);
    }
    sel.addEventListener("change", function () {
      location.href = targetUrl(this.value);
    });
  });
})();
