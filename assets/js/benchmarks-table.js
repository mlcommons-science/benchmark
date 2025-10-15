(function () {
  'use strict';

  const TABLE_ID = 'benchmarksTable';
  const DEFAULT_WIDTH = '240px';
  const DEFAULT_LINES = 2;
  const EXPORT_FILENAME = 'science-ai-benchmarks';

  // -------- helpers (unchanged) --------
  const esc = s => String(s ?? '').replace(/[&<>"']/g, m => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[m]));
  const asList = v => Array.isArray(v) ? v.map(String) : (v == null ? [] : [String(v)]);
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

  function downloadJson(data, filename) {
    try {
      const payload = JSON.stringify(data, null, 2);
      const blob = new Blob([payload], { type: 'application/json' });
      const url = URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.href = url;
      link.download = `${filename}.json`;
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
      URL.revokeObjectURL(url);
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
    'Date',
    'Domain',
    'Focus',
    'Summary',
    'Task Types',
    'AI Capability',
    'Metrics',
    'Models',
    'Average Ratings'
  ]);
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

  // ----- columns definition (unchanged) -----
  const C = [
    col({
      title: 'Name', width: '300px', className: 'dt-nowrap',
      data: r => r.name || r.id,
      render: (v, type, r) => {
        if (type !== 'display') return v;
        const id = r.id ? encodeURIComponent(String(r.id)) : '';
        const detailPath = id ? `../benchmarks/${encodeURIComponent(String(id))}/` : '';
        const goto = detailPath ? `<a class="name-link" href="${detailPath}" title="Open details">↗</a>` : '';
        return `${clampSpan(v, { oneLine: true })} ${goto}`;
      }
    }),
    col({ title: 'Date',        width: '130px', className: 'dt-nowrap', oneLine: true, data: r => r.date }),
    col({ title: 'Version',     width: '90px',  className: 'dt-nowrap', oneLine: true, data: r => r.version }),
    col({ title: 'Updated',     width: '110px', className: 'dt-nowrap', oneLine: true, data: r => r.last_updated }),
    col({ title: 'Valid',       width: '70px',  className: 'dt-center dt-nowrap', oneLine: true, data: r => r.valid, render: v => yesNo(v) }),
    col({ title: 'Valid Date',  width: '110px', className: 'dt-nowrap', oneLine: true, data: r => r.valid_date }),
    col({ title: 'Expired',     width: '100px', className: 'dt-center dt-nowrap', oneLine: true, data: r => r.expired, render: v => yesNo(v) }),
    col({ title: 'Domain',      width: '160px', oneLine: true, data: r => r.domain }),
    col({ title: 'Focus',       width: '280px', lines: 2,      data: r => r.focus }),
    col({ title: 'Summary',     width: '320px', lines: 3,      data: r => r.summary }),
    col({ title: 'Task Types',   width: '180px', lines: 2, data: r => asList(r.task_types) }),
    col({ title: 'AI Capability',width:'200px', lines: 2, data: r => asList(r.ai_capability_measured) }),
    col({ title: 'Metrics',      width: '150px', lines: 2, data: r => asList(r.metrics) }),
    col({ title: 'Models',       width: '200px', lines: 2, data: r => asList(r.models) }),
    col({ title: 'ML Task',      width: '180px', lines: 2, data: r => asList(r.ml_task) }),
    col({ title: 'ML Motif',     width: '180px', lines: 2, data: r => asList(r.ml_motif) }),
    col({ title: 'Keywords',     width: '200px', lines: 2, data: r => asList(r.keywords) }),
    col({ title: 'Type',         width: '120px', oneLine: true, data: r => r.type }),
    col({ title: 'Solutions',   width: '120px', oneLine: true, data: r => r.solutions }),
    col({ title: 'Notes',       width: '200px', lines: 2,      data: r => r.notes }),
    col({ title: 'URL',         width: '220px', oneLine: true, data: r => r.url, render: v => (v ? link(v, v) : '') }),
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
    col({ title: 'Average Ratings', width:'60px', className:'dt-right dt-nowrap', oneLine:true, verticalHeader: true,
      data: r => r.ratings, render: (v, type) => {
        const n = avgRatings(v);
        if (type !== 'display') return n;
        return Number.isFinite(n) ? n.toFixed(1) : '';
      }
    }),
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

  const DEFAULT_HIDDEN_INDEXES = C
    .map((cfg, idx) => (PRIMARY_COLUMN_TITLES.has(cfg.title) ? null : idx))
    .filter(idx => idx != null);

  // -------- idempotent initializer --------
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
      dom: 'Bfrtip',
      buttons: [
        { extend: 'copyHtml5', text: 'Copy', exportOptions: mkExportOptions() },
        { extend: 'csvHtml5', text: 'CSV', exportOptions: mkExportOptions(), filename: EXPORT_FILENAME },
        {
          text: 'JSON',
          action: function (_, dtInstance) {
            const data = dtInstance
              .rows({ search: 'applied', order: 'applied', page: 'all' })
              .data()
              .toArray();
            const rows = data.map(row => {
              if (row && typeof row === 'object') {
                try { return JSON.parse(JSON.stringify(row)); }
                catch (_) { return row; }
              }
              return row;
            });
            downloadJson(rows, EXPORT_FILENAME);
          }
        },
        { extend: 'print', text: 'Print', exportOptions: mkExportOptions(), title: exportTitle },
        { extend: 'colvis', text: 'Columns' }
      ],
      pageLength: 25,
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
        api.columns().every(function (colIdx) {
          const cfg = C[colIdx];
          const w = cfg?.width;
          if (w) {
            $(this.nodes()).css({ 'width': w, 'min-width': w, 'max-width': w });
          }
        });
        api.columns.adjust();
        try { api.fixedColumns().relayout(); } catch (_) {}
      },
      drawCallback: function () {
        const api = this.api();
        api.columns().every(function (colIdx) {
          const cfg = C[colIdx];
          const w = cfg?.width;
          if (w) {
            $(this.nodes()).css({ 'width': w, 'min-width': w, 'max-width': w });
          }
        });
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
      if (el.scrollHeight > el.clientHeight + 1) el.classList.add('is-truncated');
      else el.classList.remove('is-truncated');
    });
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
