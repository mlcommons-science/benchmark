(function () {
  'use strict';

  const TABLE_ID = 'benchmarksTable';
  const DEFAULT_WIDTH = '240px';
  const DEFAULT_LINES = 2;
  const EXPORT_FILENAME = 'science-ai-benchmarks';
  const PAGE_LENGTH_ALL = -1;
  const PAGE_LENGTH_MENU = [
    [PAGE_LENGTH_ALL, 25, 50, 100],
    ['All rows', '25 rows', '50 rows', '100 rows']
  ];

  // Helpers
  const esc = s => String(s ?? '').replace(/[&<>"']/g, m => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[m]));
  const asList = v => Array.isArray(v) ? v.map(String) : (v == null ? [] : [String(v)]);
  const dedupeStrings = values => {
    const seen = new Set();
    const out = [];
    if (!Array.isArray(values)) return out;
    for (const value of values) {
      if (value == null) continue;
      const str = String(value).trim();
      if (!str) continue;
      const key = str.toLowerCase();
      if (seen.has(key)) continue;
      seen.add(key);
      out.push(str);
    }
    return out;
  };
  const link = (href, text) => href ? `<a href="${esc(href)}" target="_blank" rel="noopener">${esc(text ?? href)}</a>` : '';
  const yesNo = v => {
    if (v === true || v === false) return v ? '✓' : '—';
    const str = String(v ?? '').toLowerCase().trim();
    if (str === 'yes' || str === 'true') return '✓';
    if (str === 'no' || str === 'false') return '—';
    return v ?? '';
  };

  const EXPORT_DELIMITER = '; ';
  function toExportString(value) {
    if (value == null) return '';
    if (Array.isArray(value)) {
      return value.map(toExportString).filter(Boolean).join(EXPORT_DELIMITER);
    }
    if (value instanceof Date) {
      return value.toISOString();
    }
    if (typeof value === 'object') {
      if (value.name != null) return toExportString(value.name);
      if (value.title != null) return toExportString(value.title);
      if (value.text != null) return toExportString(value.text);
      if (value.url != null) return toExportString(value.url);
      return Object.values(value)
        .map(toExportString)
        .filter(Boolean)
        .join(EXPORT_DELIMITER);
    }
    const str = String(value);
    return str.replace(/<[^>]*>/g, ' ').replace(/[\s\u00A0\u200B]+/g, ' ').trim();
  }

  function triggerDownload(href, { filename = '', revoke = false } = {}) {
    const link = document.createElement('a');
    link.href = href;
    link.rel = 'noopener';
    if (filename) link.download = filename;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    if (revoke) URL.revokeObjectURL(href);
  }

  function downloadJson(data, filename) {
    try {
      const payload = JSON.stringify(data, null, 2);
      const blob = new Blob([payload], { type: 'application/json' });
      const url = URL.createObjectURL(blob);
      triggerDownload(url, { filename: `${filename}.json`, revoke: true });
    } catch (err) {
      console.error('JSON export failed:', err);
    }
  }

  function clampSpan(value, { lines = DEFAULT_LINES, oneLine = false, isHtml = false } = {}) {
    if (value == null) return '';
    const text = Array.isArray(value) ? value.join(', ') : String(value);
    const cls = `cell-clamp${oneLine ? ' one-line' : ''}`;
    if (isHtml) {
      return `<span class="${cls} js-expandable" style="--lines:${lines}" title="${esc(text.replace(/<[^>]*>/g, ''))}">${text}</span>`;
    }
    return `<span class="${cls} js-expandable" style="--lines:${lines}" title="${esc(text)}">${esc(text)}</span>`;
  }

  function col({ title, data, width, className = '', lines, oneLine, render, verticalHeader = false }) {
    return {
      title,
      data,
      width: width || DEFAULT_WIDTH,
      className: className,
      verticalHeader,
      render: render || ((v, type) => {
        if (type === 'display') return clampSpan(v, { lines, oneLine });
        if (type === 'export') return toExportString(v);
        return v;
      })
    };
  }

  const RATING_CATS = ['software','specification','dataset','metrics','reference_solution','documentation'];
  const PRIMARY_COLUMN_TITLES = new Set([
    'Name',
    'Avg Rating',
    'Date',
    'Domain',
    'Focus',
    'AI / ML Motif',
    'Models',
    'Summary',
    'Task Types',
    'AI Capability',
    'Metrics',
    'ML Task',
    'Keywords',
    'Type',
    'Solutions',
    'Notes'
  ]);
  const COLUMN_VISIBILITY_PRIORITY = [
    'Name',
    'Avg Rating',
    'Date',
    'Domain',
    'Focus',
    'AI / ML Motif',
    'Models',
    'Summary',
    'Task Types',
    'AI Capability',
    'Metrics',
    'ML Task',
    'Keywords',
    'Type',
    'Solutions',
    'Notes',
    'Version',
    'Updated',
    'Valid',
    'Valid Date',
    'Expired',
    'DOI',
    'Licensing'
  ];
  const avgRatings = ratings => {
    if (!ratings || typeof ratings !== 'object') return '';
    let sum = 0, c = 0;
    for (const k of RATING_CATS) {
      const v = ratings[k]?.rating;
      const n = (typeof v === 'number') ? v : parseFloat(v);
      if (Number.isFinite(n)) { sum += n; c++; }
    }
    return c ? sum / c : '';
  };

  // Column definition
  const C = [
    col({
      title: 'Name', width: '350px', className: 'dt-nowrap',
      data: r => r.name || r.id,
      render: (v, type, r) => {
        if (type === 'export') {
          return r.url ? `${v} (${r.url})` : v;
        }
        if (type !== 'display') return v;
        const id = r.id ? encodeURIComponent(String(r.id)) : '';
        const detailPath = id ? `../benchmarks/${encodeURIComponent(String(id))}/` : '';
        const badges = [];
        if (detailPath) {
          badges.push(`<a class="name-link name-badge name-badge--detail" href="${detailPath}" title="Open details page">Details</a>`);
        }
        if (r.url) {
          badges.push(`<a class="name-link name-badge name-badge--source" href="${esc(r.url)}" title="Open original benchmark URL" target="_blank" rel="noopener">Source</a>`);
        }
        const titleText = esc(String(v ?? ''));
        const title = `<strong class="name-text">${titleText}</strong>`;
        const actions = badges.length ? `<div class="name-badges">${badges.join('')}</div>` : '';
        return `${title}${actions}`;
      }
    }),
    col({
      title: 'Avg Rating', width: '130px', className: 'dt-head-left dt-body-center dt-nowrap average-rating-col', oneLine: true,
      data: r => r.ratings,
      render: (v, type) => {
        const n = avgRatings(v);
        if (!Number.isFinite(n)) return '';
        if (type === 'display') {
          return `<span class="avg-rating-value">${n.toFixed(1)}</span>`;
        }
        return n;
      }
    }),
    col({ title: 'Date',        width: '130px', className: 'dt-head-left dt-nowrap', oneLine: true, data: r => r.date }),
    col({ title: 'Domain',      width: '160px', oneLine: true, data: r => r.domain }),
    col({ title: 'Focus',       width: '280px', lines: 2,      data: r => r.focus }),
    col({
      title: 'AI / ML Motif', width: '220px', lines: 2,
      data: r => dedupeStrings([
        ...asList(r.ai_capability_measured),
        ...asList(r.ml_motif)
      ])
    }),
    col({ title: 'Models',       width: '200px', lines: 2, data: r => asList(r.models) }),
    col({ title: 'Summary',     width: '320px', lines: 3,      data: r => r.summary }),
    col({ title: 'Task Types',   width: '180px', lines: 2, data: r => asList(r.task_types) }),
    col({ title: 'AI Capability',width:'200px', lines: 2, data: r => asList(r.ai_capability_measured) }),
    col({ title: 'Metrics',      width: '150px', lines: 2, data: r => asList(r.metrics) }),
    col({ title: 'ML Task',      width: '180px', lines: 2, data: r => asList(r.ml_task) }),
    col({ title: 'Keywords',     width: '200px', lines: 2, data: r => asList(r.keywords) }),
    col({ title: 'Type',         width: '120px', oneLine: true, data: r => r.type }),
    col({ title: 'Solutions',   width: '120px', oneLine: true, data: r => r.solutions }),
    col({ title: 'Notes',       width: '200px', lines: 2,      data: r => r.notes }),
    col({ title: 'Version',     width: '90px',  className: 'dt-nowrap', oneLine: true, data: r => r.version }),
    col({ title: 'Updated',     width: '110px', className: 'dt-nowrap', oneLine: true, data: r => r.last_updated }),
    col({ title: 'Valid',       width: '70px',  className: 'dt-center dt-nowrap', oneLine: true, data: r => r.valid, render: v => yesNo(v) }),
    col({ title: 'Valid Date',  width: '110px', className: 'dt-nowrap', oneLine: true, data: r => r.valid_date }),
    col({ title: 'Expired',     width: '100px', className: 'dt-center dt-nowrap', oneLine: true, data: r => r.expired, render: v => yesNo(v) }),
    col({ title: 'DOI',         width: '200px', oneLine: true, data: r => r.doi,
      render: v => v ? link(`https://doi.org/${String(v).replace(/^https?:\/\/(dx\.)?doi\.org\//,'')}`, v) : '' }),
    col({ title: 'Licensing',   width: '150px', oneLine: true, data: r => r.licensing }),
    col({ title: 'Contact Name',  width:'160px', oneLine: true, data: r => r.contact?.name }),
    col({ title: 'Contact Email', width:'200px', oneLine: true, data: r => r.contact?.email,
      render: v => v ? `<a href="mailto:${esc(String(v).replace(/\s*\(at\)\s*/, '@'))}">${esc(v)}</a>` : '' }),
    col({ title: 'Datasets Links', width:'280px', lines:2, data: r => r.datasets?.links,
      render: (arr, type) => {
        if (type !== 'display') return Array.isArray(arr) ? arr.map(o => o?.name || '').join(', ') : '';
        if (!Array.isArray(arr)) return '';
        const links = arr.map(o => {
          if (!o) return '';
          if (o.url) return link(o.url, o.name || o.url);
          if (o.name) return esc(o.name);
          return '';
        }).filter(s => s);
        return clampSpan(links.join(', '), { lines: 2, isHtml: true });
      }
    }),
    col({ title: 'Results Links',  width:'280px', lines:2, data: r => r.results?.links,
      render: (arr, type) => {
        if (type !== 'display') return Array.isArray(arr) ? arr.map(o => o?.name || '').join(', ') : '';
        if (!Array.isArray(arr)) return '';
        const links = arr.map(o => {
          if (!o) return '';
          if (o.url) return link(o.url, o.name || o.url);
          if (o.name) return esc(o.name);
          return '';
        }).filter(s => s);
        return clampSpan(links.join(', '), { lines: 2, isHtml: true });
      }
    }),
    col({ title: 'FAIR Reproducible', width:'60px', className:'dt-center dt-nowrap', oneLine:true, verticalHeader: true, data: r => r.fair?.reproducible, render: v => yesNo(v) }),
    col({ title: 'FAIR Ready',        width:'60px', className:'dt-center dt-nowrap', oneLine:true, verticalHeader: true, data: r => r.fair?.benchmark_ready, render: v => yesNo(v) }),
    ...RATING_CATS.map(cat => col({
      title: `Rating ${cat.replace(/_/g,' ').replace(/\b\w/g,c=>c.toUpperCase())}`,
      width: '60px', className:'dt-right dt-nowrap', oneLine: true, verticalHeader: true,
      data: r => r.ratings?.[cat]?.rating,
      render: (v, type) => {
        if (type !== 'display') return v;
        const n = (typeof v === 'number') ? v : parseFloat(v);
        return Number.isFinite(n) ? n.toFixed(1) : '';
      }
    })),
    ...RATING_CATS.map(cat => col({
      title: `Reason ${cat.replace(/_/g,' ').replace(/\b\w/g,c=>c.toUpperCase())}`,
      width: '320px', lines: 3,
      data: r => r.ratings?.[cat]?.reason
    })),
    col({ title: 'Cite', width:'360px', lines:3, data: r => asList(r.cite) }),
  ];

  const COLUMN_INDEX_BY_TITLE = new Map(C.map((cfg, idx) => [cfg.title, idx]));
  const DEFAULT_HIDDEN_INDEXES = C
    .map((cfg, idx) => (PRIMARY_COLUMN_TITLES.has(cfg.title) ? null : idx))
    .filter(idx => idx != null);
  const COLVIS_PRIORITY_INDEXES = (() => {
    const seen = new Set();
    const ordered = [];
    for (const title of COLUMN_VISIBILITY_PRIORITY) {
      const idx = COLUMN_INDEX_BY_TITLE.get(title);
      if (idx == null || seen.has(idx)) continue;
      seen.add(idx);
      ordered.push(idx);
    }
    for (let idx = 0; idx < C.length; idx++) {
      if (seen.has(idx)) continue;
      seen.add(idx);
      ordered.push(idx);
    }
    return ordered;
  })();

  // Initialise / re-initialise DataTable
  function initBenchmarks() {
    const el = document.getElementById(TABLE_ID);
    if (!el) return; // not on this page

    // Build DATA_URL *now* (baseURI may differ after SPA nav)
    const DATA_URL = new URL('../benchmarks.json', document.baseURI).toString();

    // If DataTable already exists, tear down cleanly
    if ($.fn.dataTable.isDataTable(el)) {
      $(el).DataTable().clear().destroy();
      $(el).empty(); // remove headers generated by DT
    }

    const exportTitle = document.title || 'Science AI Benchmarks';
    const mkExportOptions = () => ({
      columns: ':visible',
      orthogonal: 'export',
      modifier: {
        page: 'current',
        search: 'applied',
        order: 'applied'
      },
      format: {
        body: (data, row, column, node) => {
          const fallback = node ? node.textContent || node.innerText || '' : '';
          const value = data ?? fallback;
          return toExportString(value);
        }
      }
    });

    const dt = $(el).DataTable({
      ajax: { url: DATA_URL, dataSrc: '' },
      columns: C,
      columnDefs: DEFAULT_HIDDEN_INDEXES.length ? [{ targets: DEFAULT_HIDDEN_INDEXES, visible: false }] : [],
      autoWidth: false,
      scrollX: true,
      scrollCollapse: true,
      deferRender: true,
      fixedColumns: { left: 1 },
      dom: "<'benchmarks-toolbar'<'benchmarks-toolbar__left'Bl><'benchmarks-toolbar__right'f>>rtip",
      buttons: [
        { extend: 'copyHtml5', text: 'Copy', exportOptions: mkExportOptions() },
        { extend: 'csvHtml5', text: 'CSV', exportOptions: mkExportOptions(), filename: EXPORT_FILENAME },
        makeJsonButton(mkExportOptions),
        makeLatexButton(),
        makeColVisButton()
      ],
      pageLength: PAGE_LENGTH_ALL,
      lengthMenu: PAGE_LENGTH_MENU,
      order: (() => { 
        const i = C.findIndex(c => c.title === 'Date'); 
        return i >= 0 ? [[i, 'desc']] : []; 
      })(),
      headerCallback: function () {
        const api = this.api();
        api.columns().every(function (colIdx) {
          const cfg = C[colIdx];
          if (!cfg) return;
          const header = this.header();
          if (!header) return;
          const w = cfg.width;
          if (w) {
            header.style.width = w;
            header.style.minWidth = w;
            header.style.maxWidth = w;
          }
          const dataTitle = header.getAttribute('data-original-title');
          if (!dataTitle) {
            const text = header.textContent || header.innerText || '';
            header.setAttribute('data-original-title', text);
          }
          if (cfg.verticalHeader) {
            if (!header.classList.contains('has-vertical-text')) {
              const text = header.getAttribute('data-original-title') || header.textContent || header.innerText || '';
              header.innerHTML = `<div class="vertical-text">${esc(text)}</div>`;
              header.classList.add('has-vertical-text');
            }
          } else if (header.classList.contains('has-vertical-text')) {
            const original = header.getAttribute('data-original-title') || '';
            header.textContent = original;
            header.classList.remove('has-vertical-text');
          }
        });
      },
      initComplete: function () {
        const api = this.api();
        applyColumnWidths(api);
        api.columns.adjust();
        try { api.fixedColumns().relayout(); } catch (_) {}
      },
      drawCallback: function () {
        const api = this.api();
        applyColumnWidths(api);
        try { api.fixedColumns().relayout(); } catch (_) {}
        detectTruncatedCells();
      }
    });

    // Delegated handlers must be rebound after SPA nav because table DOM is new
    $(el).off('click.js-expand js-copy'); // prevent duplicate bindings
    $(el).on('click.js-expand', '.js-expandable', function (e) {
      e.stopPropagation();
      if (this.classList.contains('js-copyable')) return;
      this.classList.toggle('expanded');
      this.setAttribute('aria-expanded', this.classList.contains('expanded') ? 'true' : 'false');
    });
    $(el).on('click.js-copy', '.js-copyable', function (e) {
      e.stopPropagation();
      e.preventDefault();
      const text = this.getAttribute('data-cite-text') || this.textContent || this.innerText;
      if (navigator.clipboard && navigator.clipboard.writeText) {
        navigator.clipboard.writeText(text).then(() => showCopyFeedback(this))
          .catch(err => { console.error('Clipboard API failed:', err); fallbackCopy(text, this); });
      } else {
        fallbackCopy(text, this);
      }
    });

    setTimeout(detectTruncatedCells, 100);
  }

  // -------- utilities used by init --------
  function detectTruncatedCells() {
    const expandables = document.querySelectorAll('.js-expandable');
    expandables.forEach(el => {
      const isOneLine = el.classList.contains('one-line');
      let truncated = false;
      if (isOneLine) {
        const scrollW = Math.ceil(el.scrollWidth);
        const clientW = Math.ceil(el.clientWidth);
        truncated = scrollW > clientW;
      } else {
        const scrollH = Math.ceil(el.scrollHeight);
        const clientH = Math.ceil(el.clientHeight);
        truncated = scrollH > clientH;
      }
      if (truncated) {
        el.classList.add('is-truncated');
        el.setAttribute('data-truncated', 'true');
      } else {
        el.classList.remove('is-truncated');
        el.removeAttribute('data-truncated');
      }
    });
  }
  function applyColumnWidths(api) {
    api.columns().every(function (colIdx) {
      const width = C[colIdx]?.width;
      if (!width) return;
      $(this.nodes()).css({ width, 'min-width': width, 'max-width': width });
    });
  }
  function makeJsonButton(exportOptionsFactory) {
    return {
      text: 'JSON',
      action: function (_, dtInstance) {
        const exportOptions = exportOptionsFactory();
        const visibleColumns = dtInstance
          .columns(exportOptions.columns)
          .indexes()
          .toArray();
        const data = dtInstance
          .rows({ search: 'applied', order: 'applied', page: 'current' })
          .data()
          .toArray();
        const rows = data.map(row => pickVisibleFields(row, visibleColumns));
        downloadJson(rows, EXPORT_FILENAME);
      }
    };
  }
  function makeLatexButton() {
    return {
      text: 'LaTeX',
      action: function () {
        const href = new URL('../../downloads/benchmarks-latex.zip', document.baseURI).toString();
        try {
          triggerDownload(href);
        } catch (err) {
          console.error('Download trigger failed:', err);
          window.location.href = href;
        }
      }
    };
  }
  function makeColVisButton() {
    return {
      extend: 'colvis',
      text: 'Columns',
      columns: COLVIS_PRIORITY_INDEXES,
      columnText: function (dtInstance, idx) {
        const cfg = C[idx];
        if (cfg?.title) return cfg.title;
        const header = dtInstance.column(idx).header();
        return header ? header.textContent.trim() : `Column ${idx + 1}`;
      }
    };
  }
  function pickVisibleFields(row, visibleIndexes) {
    if (!row || typeof row !== 'object') return row;
    if (Array.isArray(row)) {
      return visibleIndexes.map(idx => row[idx]);
    }
    const out = {};
    visibleIndexes.forEach(idx => {
      const col = C[idx];
      if (!col) return;
      const key = col.title || col.data;
      if (key == null) return;
      let value = typeof col.data === 'function' ? col.data(row) : row[col.data];
      if (col.render && typeof col.render === 'function') {
        value = col.render(value, 'export', row);
      }
      out[key] = value;
    });
    return out;
  }
  function fallbackCopy(text, element) {
    const textarea = document.createElement('textarea');
    textarea.value = text;
    textarea.style.position = 'fixed';
    textarea.style.opacity = '0';
    document.body.appendChild(textarea);
    textarea.select();
    try { document.execCommand('copy'); showCopyFeedback(element); }
    catch (err) { console.error('Copy failed:', err); }
    document.body.removeChild(textarea);
  }
  function showCopyFeedback(element) {
    const originalBg = element.style.backgroundColor;
    const originalContent = element.getAttribute('data-original-title') || element.title;
    element.style.backgroundColor = '#4CAF50';
    element.style.transition = 'background-color 0.3s';
    element.title = 'Copied!';
    setTimeout(() => {
      element.style.backgroundColor = originalBg;
      element.title = originalContent;
    }, 1000);
  }

  // -------- run on first load + every SPA navigation --------
  window.addEventListener('DOMContentLoaded', initBenchmarks);
  if (window.document$) {
    document$.subscribe(() => {
      // Delay to ensure the new page’s HTML is in place
      requestAnimationFrame(initBenchmarks);
    });
  }
})();
