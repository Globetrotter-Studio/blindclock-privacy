/* BlindClock site — multi-language switcher (v1.9+).
   English lives in the HTML (SEO + no-JS fallback). All other languages live in
   assets/i18n.js as window.BC_STRINGS[lang][key]; this engine swaps innerHTML by
   the element's data-i18n key. Build-free — just edit i18n.js to add/adjust copy.

   To add a language: add it to LANGS below and add its block to BC_STRINGS in i18n.js. */
(function () {
  var STORAGE_KEY = "bc-lang";
  var DEFAULT = "en";

  /* code -> label shown in the dropdown. Order = dropdown order. */
  var LANGS = [
    ["en", "English"],
    ["zh-Hant", "繁體中文"],
    ["ja", "日本語"],
    ["ko", "한국어"],
    ["de", "Deutsch"],
    ["fr-FR", "Français"],
    ["it", "Italiano"],
    ["pl", "Polski"],
    ["pt-BR", "Português (BR)"],
    ["es-MX", "Español (LA)"],
    ["tr", "Türkçe"],
    ["vi", "Tiếng Việt"]
  ];

  var strings = window.BC_STRINGS || {};

  function isSupported(code) {
    for (var i = 0; i < LANGS.length; i++) if (LANGS[i][0] === code) return true;
    return false;
  }

  function normalize(value) {
    if (!value) return null;
    value = String(value);
    if (isSupported(value)) return value;
    var low = value.toLowerCase();
    if (low.indexOf("zh") === 0) return "zh-Hant";
    if (low.indexOf("pt") === 0) return "pt-BR";
    if (low.indexOf("es") === 0) return "es-MX";
    if (low.indexOf("fr") === 0) return "fr-FR";
    if (low.indexOf("ja") === 0) return "ja";
    if (low.indexOf("ko") === 0) return "ko";
    if (low.indexOf("de") === 0) return "de";
    if (low.indexOf("it") === 0) return "it";
    if (low.indexOf("pl") === 0) return "pl";
    if (low.indexOf("tr") === 0) return "tr";
    if (low.indexOf("vi") === 0) return "vi";
    if (low.indexOf("en") === 0) return "en";
    return null;
  }

  function detect() {
    var fromQuery = normalize(new URLSearchParams(window.location.search).get("lang"));
    if (fromQuery) return fromQuery;
    var saved = null;
    try { saved = normalize(localStorage.getItem(STORAGE_KEY)); } catch (e) {}
    if (saved) return saved;
    var langs = navigator.languages || [navigator.language];
    for (var i = 0; i < langs.length; i++) {
      var lang = normalize(langs[i]);
      if (lang) return lang;
    }
    return DEFAULT;
  }

  /* cache the English (in-HTML) innerHTML once, so we can restore it and so it is
     the fallback for any key a translation happens to miss. */
  var cached = false;
  var nodes = [];
  function cacheDefaults() {
    if (cached) return;
    var found = document.querySelectorAll("[data-i18n]");
    for (var i = 0; i < found.length; i++) {
      nodes.push([found[i], found[i].getAttribute("data-i18n"), found[i].innerHTML]);
    }
    cached = true;
  }

  function apply(lang) {
    cacheDefaults();
    document.documentElement.setAttribute("data-lang", lang);
    document.documentElement.setAttribute("lang", lang);
    var dict = strings[lang] || {};
    for (var i = 0; i < nodes.length; i++) {
      var el = nodes[i][0], key = nodes[i][1], en = nodes[i][2];
      var translated = (lang === DEFAULT) ? en : (dict[key] != null ? dict[key] : en);
      el.innerHTML = translated;
    }
    var sel = document.getElementById("lang-select");
    if (sel) sel.value = lang;
  }

  window.bcSetLang = function (lang) {
    lang = normalize(lang) || DEFAULT;
    try { localStorage.setItem(STORAGE_KEY, lang); } catch (e) {}
    apply(lang);
  };

  document.addEventListener("DOMContentLoaded", function () {
    var sel = document.getElementById("lang-select");
    if (sel) {
      for (var i = 0; i < LANGS.length; i++) {
        var o = document.createElement("option");
        o.value = LANGS[i][0];
        o.textContent = LANGS[i][1];
        sel.appendChild(o);
      }
      sel.addEventListener("change", function () { window.bcSetLang(this.value); });
    }
    apply(detect());
  });
})();
