/* static.js
   ------------------------------------------------------------------------
   Lightweight DOM-only filtering/sorting + state persistence for MkDocs.
   Works with MkDocs Material (instant navigation) and the MkDocs writer
   that emits index cards with data-* attributes and detail pages with a
   ".back-link" anchor.

   Features
   - Text search, domain filter, keywords, date range, min rating, sort.
   - Builds from existing DOM; no JSON fetch.
   - Persists state in URL hash AND sessionStorage.
   - Updates each "Details" link to carry current filters (via hash).
   - Detail page "Back to results" always returns to parent index with
     saved filters (no weird history jumps).
   - Idempotent init; safe with Material's document$.subscribe.
   ---------------------------------------------------------------------- */

(function () {
  const STORAGE_KEY = "bench_filters_v1";
  const collator = new Intl.Collator(undefined, { sensitivity: "base", numeric: true });

  // ---------------- helpers ----------------
  function splitTokens(s) {
    return (s || "").split(/[;,]/).map(t => t.trim()).filter(Boolean);
  }
  function norm(s) {
    return (s ?? "").toString().toLowerCase();
  }
  function parseDate(s) {
    if (!s) return null;
    const d = new Date(s);
    return isNaN(d) ? null : d;
  }
  function cmpNumAsc(x, y) {
    const ax = Number.isFinite(x), ay = Number.isFinite(y);
    if (ax && ay) return x - y;
    if (ax && !ay) return -1;
    if (!ax && ay) return 1;
    return 0;
  }
  function readParams() {
    const H = new URLSearchParams((location.hash || "").slice(1));
    const Q = new URLSearchParams((location.search || "").slice(1));
    return {
      kw: H.get("kw") || Q.get("kw") || "",
      domain: H.get("domain") || Q.get("domain") || "",
      q: H.get("q") || Q.get("q") || "",
      from: H.get("from") || Q.get("from") || "",
      to: H.get("to") || Q.get("to") || "",
      minrating: H.get("minrating") || Q.get("minrating") || "",
      sort: H.get("sort") || Q.get("sort") || "",
    };
  }
  function toHashFromState(s) {
    const p = new URLSearchParams();
    if (s.kw) p.set("kw", s.kw);
    if (s.domain) p.set("domain", s.domain);
    if (s.q) p.set("q", s.q);
    if (s.from) p.set("from", s.from);
    if (s.to) p.set("to", s.to);
    if (s.minrating) p.set("minrating", s.minrating);
    if (s.sort && s.sort !== "date_desc") p.set("sort", s.sort);
    const str = p.toString();
    return str ? "#" + str : "";
  }
  function loadSaved() {
    try { return JSON.parse(sessionStorage.getItem(STORAGE_KEY) || "{}"); }
    catch { return {}; }
  }
  function saveState(s) {
    try { sessionStorage.setItem(STORAGE_KEY, JSON.stringify(s)); }
    catch { /* ignore private mode errors */ }
  }

  // ---------------- index page ----------------
  function initIndex() {
    const root = document.getElementById("cards-root");
    if (!root || root.dataset.filtersBound === "1") return;
    root.dataset.filtersBound = "1";

    const els = {
      root,
      q: document.getElementById("f_q"),
      domain: document.getElementById("f_domain"),
      keywords: document.getElementById("f_keywords"),
      from: document.getElementById("f_from"),
      to: document.getElementById("f_to"),
      minrating: document.getElementById("f_minrating"),
      sort: document.getElementById("f_sort"),
      reset: document.getElementById("f_reset"),
    };

    // Build items from DOM
    const cards = Array.from(root.querySelectorAll(".benchmark-card"));
    const items = cards.map((el, index) => {
      const ds = el.dataset;
      const domains   = splitTokens(ds.domain);
      const metrics   = splitTokens(ds.metrics);
      const taskTypes = splitTokens(ds.taskTypes);
      const keywords  = splitTokens(ds.keywords);
      const d = parseDate(ds.date);
      const dateTs = d ? d.getTime() : NaN;
      const r = ds.ratingsAvg === "" ? NaN : Number(ds.ratingsAvg);
      return {
        el, index,
        id: ds.id || "",
        name: ds.name || "",
        nameKey: (ds.name || "").toString(),
        date: ds.date || "",
        dateTs,
        rating: Number.isFinite(r) ? r : -Infinity,
        domains, metrics, taskTypes, keywords,
        hay: [ds.name, ds.focus, ...metrics, ...taskTypes, ...domains, ...keywords]
              .join(" • ").toLowerCase()
      };
    });

    // Populate domain dropdown (clear previous except first)
    if (els.domain) {
      while (els.domain.options.length > 1) els.domain.remove(1);
      const domainSet = new Set();
      for (const it of items) it.domains.forEach(d => domainSet.add(d));
      [...domainSet].sort(collator.compare).forEach(d => {
        const o = document.createElement("option");
        o.value = o.textContent = d;
        els.domain.appendChild(o);
      });
    }

    // Restore state from URL hash/search or session
    const urlState = readParams();
    const saved = loadSaved();
    const state = Object.assign(
      { q:"", domain:"", kw:"", from:"", to:"", minrating:"", sort:"date_desc" },
      saved,
      urlState   // URL wins when provided
    );

    // Prefill controls
    if (els.q)        els.q.value = state.q || "";
    if (els.domain)   els.domain.value = state.domain || "";
    if (els.keywords) els.keywords.value = state.kw || "";
    if (els.from)     els.from.value = state.from || "";
    if (els.to)       els.to.value = state.to || "";
    if (els.minrating)els.minrating.value = state.minrating || "";
    if (els.sort)     els.sort.value = state.sort || "date_desc";

    function matches(it) {
      const q = norm(els.q && els.q.value);
      const dom = els.domain && els.domain.value;
      const kws = (els.keywords && els.keywords.value || "")
        .split(",").map(x => x.trim()).filter(Boolean).map(norm);
      const dfrom = parseDate(els.from && els.from.value);
      const dto   = parseDate(els.to && els.to.value);
      const minr  = els.minrating && els.minrating.value ? parseFloat(els.minrating.value) : null;

      if (q && !it.hay.includes(q)) return false;
      if (dom && !it.domains.includes(dom)) return false;
      if (kws.length) {
        const set = new Set(it.keywords.map(norm));
        if (!kws.some(k => set.has(k))) return false;
      }
      if (dfrom || dto) {
        if (!it.date) return false;
        const d = parseDate(it.date);
        if (!d) return false;
        if (dfrom && d < dfrom) return false;
        if (dto && d > dto) return false;
      }
      if (minr != null) {
        if (!Number.isFinite(it.rating) || it.rating < minr) return false;
      }
      return true;
    }

    const comparators = {
      "date_desc":   (a,b) => cmpNumAsc(b.dateTs, a.dateTs) || a.index - b.index,
      "date_asc":    (a,b) => cmpNumAsc(a.dateTs, b.dateTs) || a.index - b.index,
      "name_asc":    (a,b) => collator.compare(a.nameKey, b.nameKey) || a.index - b.index,
      "rating_desc": (a,b) => cmpNumAsc(b.rating, a.rating) || a.index - b.index,
    };

    function currentState() {
      return {
        q:        (els.q && els.q.value) || "",
        domain:   (els.domain && els.domain.value) || "",
        kw:       (els.keywords && els.keywords.value) || "",
        from:     (els.from && els.from.value) || "",
        to:       (els.to && els.to.value) || "",
        minrating:(els.minrating && els.minrating.value) || "",
        sort:     (els.sort && els.sort.value) || "date_desc",
      };
    }

    function apply() {
      // filter
      for (const it of items) it.el.classList.toggle("is-hidden", !matches(it));

      // sort visible
      const mode = (els.sort && comparators[els.sort.value]) ? els.sort.value : "date_desc";
      const cmp = comparators[mode];
      const visible = items.filter(it => !it.el.classList.contains("is-hidden")).sort(cmp);
      const hidden  = items.filter(it => it.el.classList.contains("is-hidden"));

      const frag = document.createDocumentFragment();
      for (const it of visible) frag.appendChild(it.el);
      for (const it of hidden)  frag.appendChild(it.el);
      root.appendChild(frag);

      // persist state -> hash + sessionStorage
      const s = currentState();
      const hash = toHashFromState(s);
      if (hash !== location.hash) history.replaceState(null, "", hash || location.pathname);
      saveState(s);

      // propagate current filters to each "Details" link
      root.querySelectorAll(".benchmark-card a.md-button").forEach(a => {
        try {
          const u = new URL(a.getAttribute("href"), location.href);
          u.hash = (hash || "").replace(/^#/, "");
          a.setAttribute("href", u.pathname + (u.hash ? "#" + u.hash : ""));
        } catch {
          const base = a.getAttribute("href").replace(/#.*$/, "");
          a.setAttribute("href", base + (hash || ""));
        }
      });
    }

    // bind controls
    const hook = (el, events = ["input","change"]) => el && events.forEach(e => el.addEventListener(e, apply));
    hook(els.q); hook(els.domain); hook(els.keywords); hook(els.from); hook(els.to); hook(els.minrating); hook(els.sort);
    if (els.reset) {
      els.reset.addEventListener("click", () => {
        if (els.q) els.q.value = "";
        if (els.domain) els.domain.value = "";
        if (els.keywords) els.keywords.value = "";
        if (els.from) els.from.value = "";
        if (els.to) els.to.value = "";
        if (els.minrating) els.minrating.value = "";
        if (els.sort) els.sort.value = "date_desc";
        apply();
      });
    }

    // apply once immediately (honors URL/session state)
    apply();

    // If just the hash changes (e.g., you paste a URL), re-apply
    window.addEventListener("hashchange", () => {
      const params = readParams();
      if (els.q)        els.q.value = params.q || "";
      if (els.domain)   els.domain.value = params.domain || "";
      if (els.keywords) els.keywords.value = params.kw || "";
      if (els.from)     els.from.value = params.from || "";
      if (els.to)       els.to.value = params.to || "";
      if (els.minrating)els.minrating.value = params.minrating || "";
      if (els.sort)     els.sort.value = params.sort || "date_desc";
      apply();
    });

    // chip → add keyword + apply
    root.addEventListener("click", (e) => {
      const t = e.target;
      if (t && t.classList.contains("chip-link")) {
        e.preventDefault();
        const kw = t.textContent.trim();
        if (!els.keywords) return;
        const cur = (els.keywords.value || "").split(",").map(s=>s.trim()).filter(Boolean);
        if (!cur.includes(kw)) cur.push(kw);
        els.keywords.value = cur.join(", ");
        apply();
      }
    });
  }

  // ---------------- detail page ----------------
  function computeIndexHrefWithSavedFilters() {
    const url = new URL(location.href);
    // Strip current page segment (…/<id>/) or file (…/<id>.html)
    if (url.pathname.endsWith("/")) {
      url.pathname = url.pathname.replace(/[^/]+\/$/, "");
    } else {
      url.pathname = url.pathname.replace(/[^/]+\.html$/, "");
    }
    url.search = "";
    const saved = loadSaved();
    url.hash = toHashFromState(saved).slice(1); // store without '#'
    return url.href;
  }

  function initDetail() {
    const back = document.querySelector(".back-link");
    if (!back || back.dataset.bound === "1") return;
    back.dataset.bound = "1";

    // Set href immediately so middle-click / long-press works
    back.setAttribute("href", computeIndexHrefWithSavedFilters());

    // Click handler: always go to computed parent index with saved filters
    back.addEventListener("click", (e) => {
      if (e.metaKey || e.ctrlKey || e.shiftKey || e.altKey) return; // allow new tab
      e.preventDefault();
      location.href = computeIndexHrefWithSavedFilters();
    });
  }

  // ---------------- boot (Material instant navigation) ----------------
  function boot() {
    initIndex();   // runs only if #cards-root exists
    initDetail();  // runs only if .back-link exists
  }

  if (document.readyState !== "loading") boot();
  else window.addEventListener("DOMContentLoaded", boot);

  if (window.document$) {
    document$.subscribe(() => {
      boot();
    });
  }
})();
