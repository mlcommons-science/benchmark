# ---------------------------------------------------------------------------
# MkDocs writer that:
# - Generates a filterable/sortable index page with pre-rendered cards.
# - Generates one HTML-rich detail page per entry.
# - No global table here (temporarily removed).
# - Emits data-* attributes for DOM-only filters/sorting.
# ---------------------------------------------------------------------------

from __future__ import annotations

import html
import os
import re
import sys
import textwrap
from typing import Any, Dict, List, Tuple
from urllib.parse import quote

from pybtex.database import parse_string
from pybtex.plugin import find_plugin

from cloudmesh.common.console import Console
from generate_latex import ALL_COLUMNS, DEFAULT_COLUMNS, write_to_file


# ----------------------------- configuration ---------------------------------

# Hardcoded subset shown first on the detail page (skip missing values)
_HARDCODED_DETAIL_FIELDS: List[str] = [
    "date",
    "name",
    "domain",
    "focus",
    "task_types",
    "metrics",
    "models",
    "ml_motif",
]


# ------------------------------- utilities -----------------------------------


def _nonempty(v: Any) -> bool:
    """Return True if v is a meaningful value for rendering/filtering."""
    return not (v is None or v == "" or v == [])


def _listify(v: Any) -> List[str]:
    """Coerce a value into a list of strings (used for domain/metrics/... on cards and meta)."""
    if v is None or v == "":
        return []
    return v if isinstance(v, list) else [v]


def _extract_links(section: Any) -> List[Tuple[str, str]]:
    """Return [(name, url), ...] from a nested section.links list of dicts."""
    items: List[Tuple[str, str]] = []
    if not isinstance(section, dict):
        return items
    links = section.get("links")
    if not isinstance(links, list):
        return items
    for link in links:
        if not isinstance(link, dict):
            continue
        url = link.get("url")
        name = link.get("name") or link.get("title") or url
        if not url or not name:
            continue
        items.append((str(name), str(url)))
    return items


def _raw_get(entry: Dict[str, Any], key: str) -> Any:
    """Retrieve a nested value from the raw YAML entry using dot-separated keys."""
    current: Any = entry
    for part in key.split("."):
        if isinstance(current, dict):
            current = current.get(part)
        else:
            return None
    return current


def _val_to_str(val: Any) -> str:
    """
    Legacy-style flattening used for detail page values:
      - remove brackets/quotes/parentheses,
      - keep commas between items,
      - collapse newlines.
    """
    if val is None:
        return ""
    s = str(val).replace("\n", " ").replace("['", "").replace("']", "")
    s = s.replace("', '", ", ").replace("','", ", ").replace("[]", "")
    s = s.replace("[", " ").replace("]", " ").replace("(", " ").replace(")", " ")
    return s.strip()


def _esc(v: Any) -> str:
    """Escape text for safe HTML embedding."""
    return html.escape("" if v is None else str(v), quote=True)


def _col_label(col: str) -> str:
    """Return the human label for a valid column."""
    return str(ALL_COLUMNS[col]["label"])


def _validate_columns(columns: List[str]) -> List[str]:
    """
    Validate `columns` against ALL_COLUMNS.
    Returns a filtered list; logs a warning for unknown columns (does not hard-fail).
    """
    valid, invalid = [], []
    for c in columns:
        if c in ALL_COLUMNS:
            valid.append(c)
        else:
            invalid.append(c)
    if invalid:
        Console.warning(f"Unknown columns skipped: {', '.join(invalid)}")
    return valid


def _bibtex_to_text(entry: str) -> str:
    """
    Render a BibTeX entry to plain text.
    Returns a readable error string if parsing fails (never raises).
    """
    try:
        if not isinstance(entry, str):
            raise TypeError(
                f"Expected string for BibTeX entry, got {type(entry).__name__}"
            )
        bib_data = parse_string(entry, bib_format="bibtex")
        style = find_plugin("pybtex.style.formatting", "plain")()
        formatted = next(style.format_entries(bib_data.entries.values()))
        return re.sub(r"<[^>]+>", " ", str(formatted.text)).strip()
    except Exception as e:
        return f"Could not parse citation: {e}"


def _collect_ratings(
    entry: Dict[str, Any],
) -> Tuple[List[Tuple[str, Dict[str, Any]]], float, int]:
    """
    Collect ratings.*.{rating,reason} grouped by category.
    Returns:
      - ordered list of (category, {rating, reason})
      - sum of numeric ratings present
      - count of numeric ratings present
    Order: preferred categories first, then alphabetical.
    """
    groups: Dict[str, Dict[str, Any]] = {}
    pat = re.compile(r"^ratings\.([^.]+)\.(rating|reason)$")

    for k, v in entry.items():
        m = pat.match(k)
        if not m:
            continue
        cat, kind = m.group(1), m.group(2)
        groups.setdefault(cat, {})[kind] = v

    preferred = [
        "software",
        "specification",
        "dataset",
        "metrics",
        "reference_solution",
        "documentation",
    ]
    ordered_keys = [k for k in preferred if k in groups] + sorted(
        [k for k in groups.keys() if k not in preferred]
    )

    items: List[Tuple[str, Dict[str, Any]]] = [(k, groups[k]) for k in ordered_keys]

    s = 0.0
    c = 0
    for _, d in items:
        r = d.get("rating")
        try:
            if _nonempty(r):
                s += float(r)
                c += 1
        except (ValueError, TypeError):
            Console.error(f'The rating "{r}" must be a number')

    return items, s, c


def _requested_rating_aspects(columns: List[str]) -> Dict[str, set]:
    """
    From `columns`, extract which rating aspects are requested per category.
    Example return: {"software": {"rating","reason"}, "documentation":{"reason"}}
    """
    req: Dict[str, set] = {}
    for col in columns:
        if not col.startswith("ratings."):
            continue
        parts = col.split(".")
        if len(parts) >= 3:
            _, cat, aspect = parts[0], parts[1], parts[2]
            req.setdefault(cat, set()).add(aspect)
    return req


# ------------------------------- main writer ---------------------------------


class MkdocsWriter:
    """
    Writes:
      - index.md with filter controls and pre-rendered cards (data-* attributes),
      - one HTML-rich detail page per entry ({id}.md).
    """

    def __init__(
        self,
        entries: List[Dict[str, Any]],
        raw_entries: List[Dict[str, Any]] | None = None,
        *,
        use_directory_urls: bool = True,
    ):
        self.entries = entries
        self.raw_entries = raw_entries
        self.use_directory_urls = use_directory_urls
        self._raw_by_id: Dict[str, Dict[str, Any]] = {}
        self._raw_by_name: Dict[str, Dict[str, Any]] = {}
        if isinstance(raw_entries, list):
            self._collect_raw_entries(raw_entries)

    # ----------------------- md table utilities ------------------------------

    def _collect_raw_entries(self, data: List[Any]) -> None:
        for item in data:
            if isinstance(item, dict):
                self._register_raw_entry(item)
                for value in item.values():
                    if isinstance(value, list):
                        self._collect_raw_entries(value)
                    elif isinstance(value, dict):
                        self._collect_raw_entries([value])
            elif isinstance(item, list):
                self._collect_raw_entries(item)

    def _register_raw_entry(self, entry: Dict[str, Any]) -> None:
        id_val = entry.get("id")
        name_val = entry.get("name")
        if _nonempty(id_val):
            self._raw_by_id[str(id_val).strip()] = entry
            if _nonempty(name_val):
                self._raw_by_name[str(name_val).strip()] = entry
        elif _nonempty(name_val) and any(
            key in entry for key in ("domain", "metrics", "task_types", "ml_motif")
        ):
            self._raw_by_name[str(name_val).strip()] = entry

    def _get_raw_entry(self, entry: Dict[str, Any]) -> Dict[str, Any] | None:
        id_val = entry.get("id")
        if _nonempty(id_val):
            raw = self._raw_by_id.get(str(id_val).strip())
            if raw:
                return raw
        name_val = entry.get("name")
        if _nonempty(name_val):
            return self._raw_by_name.get(str(name_val).strip())
        return None

    def _escape_md(self, text) -> str:
        if not isinstance(text, str):
            text = str(text)
        return text.replace("|", "\\|").replace("\n", " ")

    def _colunm_label(self, col):
        if col not in ALL_COLUMNS:
            Console.error(f"Column '{col}' is not a valid column name.")
            sys.exit(1)
        content = ALL_COLUMNS[col]["label"]
        return content

    def _colunm_width(self, col):
        if col not in ALL_COLUMNS:
            Console.error(f"Column '{col}' is not a valid column name.")
            sys.exit(1)
        content = float(ALL_COLUMNS[col]["width"])
        return content

    def _column_width_str(self, col):
        if col not in ALL_COLUMNS:
            Console.error(f"Column '{col}' is not a valid column name.")
            sys.exit(1)
        content = "-" * int(self._colunm_width(col) * 10.0)
        return content

    # ----------------------- index page composition --------------------------

    def _detail_href(self, id_: str) -> str:
        """Build the runtime URL for a detail page (MkDocs routing)."""
        if self.use_directory_urls:
            return f"../{id_}/"
        return f"../{id_}.html"

    def _index_header_html(self) -> str:
        """Controls + container for cards; your DOM script wires the behavior."""
        return (
            "# Index of Benchmarks\n\n"
            '<div class="filter-bar">\n'
            '<input type="search" id="f_q" placeholder="Search (name, focus, metrics…)" />\n'
            '<select id="f_domain"><option value="">All domains</option></select>\n'
            '<input type="text" id="f_keywords" placeholder="Keywords (comma-separated)" />\n'
            '<input type="date" id="f_from" placeholder="From date" />\n'
            '<input type="date" id="f_to" placeholder="To date" />\n'
            '<input type="number" id="f_minrating" min="0" max="5" step="0.1" placeholder="Min avg rating" />\n'
            '<select id="f_sort">\n'
            '  <option value="date_desc">Sort: Date ↓</option>\n'
            '  <option value="date_asc">Sort: Date ↑</option>\n'
            '  <option value="name_asc">Sort: Name A–Z</option>\n'
            '  <option value="rating_desc">Sort: Rating ↓</option>\n'
            "</select>\n"
            '<button id="f_reset" type="button">Reset</button>\n'
            "</div>\n\n"
            '<div id="cards-root" class="grid cards">\n'
        )

    def _index_footer_html(self, filters_js_src: str | None) -> str:
        """
        Close the cards container and (optionally) include your filters.js.
        If you manage JS via theme, pass filters_js_src=None.
        """
        script = (
            f'\n<script src="{_esc(filters_js_src)}"></script>\n'
            if filters_js_src
            else ""
        )
        return "</div>\n" + script

    def _rating_badge(self, avg, size="sm"):
        if avg is None:
            return ""
        color = "ok" if avg >= 4 else "meh" if avg >= 3 else "bad"
        return f'<span class="badge badge--{color} badge--{size}">{avg:.2f}/5</span>'

    def _index_card_html(
        self,
        entry: Dict[str, Any],
        raw_entry: Dict[str, Any] | None,
        ratings_avg: float | None,
    ) -> str:
        """
        Generate one card with the data-* attributes needed for DOM filtering/sorting.
        Only uses fields relevant to filtering/sorting; adding new YAML columns won’t break the UI.
        """
        if raw_entry is None:
            raise KeyError("Raw entry is required for card rendering.")

        if not raw_entry.get("id"):
            raise KeyError("Raw entry missing required 'id' field.")

        id_ = str(raw_entry.get("id"))
        name = str(raw_entry.get("name", id_))
        date = str(raw_entry.get("date", ""))

        domain_list = _listify(raw_entry.get("domain"))
        metrics_list = _listify(raw_entry.get("metrics"))
        task_types_list = _listify(raw_entry.get("task_types"))
        keywords_list = _listify(raw_entry.get("keywords"))
        focus_val = raw_entry.get("focus")
        focus_str = _val_to_str(focus_val)

        # subtitle under the title (optional)
        subs: List[str] = []
        if domain_list:
            subs.append(", ".join(str(d) for d in domain_list))
        if metrics_list:
            subs.append(", ".join(str(m) for m in metrics_list))
        subtitle = " • ".join(subs)

        # keyword chips (first few)
        chips = ""
        if keywords_list:
            chips = (
                '<div class="chips">'
                + " ".join(
                    f'<a class="chip chip-link" href="#kw={_esc(k)}">{_esc(k)}</a>'
                    for k in keywords_list[:5]
                )
                + "</div>\n"
            )

        rating_val = None
        try:
            rating_val = None if ratings_avg is None else float(ratings_avg)
        except (TypeError, ValueError):
            rating_val = None

        rating_str = f"{rating_val:.2f}" if rating_val is not None else ""
        badge_html = self._rating_badge(rating_val)  # DO NOT _esc()

        detail_href = _esc(self._detail_href(id_))

        # data-* attributes used by filters.js
        return f"""
            <article class="benchmark-card"
                    data-id="{_esc(id_)}"
                    data-name="{_esc(name)}"
                    data-date="{_esc(date)}"
                    data-focus="{_esc(focus_str)}"
                    data-domain="{_esc(', '.join(map(str, domain_list)))}"
                    data-task-types="{_esc(', '.join(map(str, task_types_list)))}"
                    data-metrics="{_esc(', '.join(map(str, metrics_list)))}"
                    data-keywords="{_esc(', '.join(map(str, keywords_list)))}"
                    data-ratings-avg="{_esc(rating_str)}">
                <h3>{_esc(name)}</h3>
                {f'<p class="muted">{_esc(subtitle)}</p>' if subtitle else ''}
                {chips}
                <p class="muted">Avg rating: {badge_html}</p>
                <p><a class="md-button md-button--primary" href="{detail_href}">Details</a></p>
            </article>
            """.strip()

    # ---------------------- detail page composition --------------------------

    def _meta_block_html(self, raw_entry: Dict[str, Any]) -> str:
        """HTML meta block showing the hardcoded subset first (skip missing)."""
        rows = ['<div class="info-block meta-block">\n']
        for key in _HARDCODED_DETAIL_FIELDS:
            if key not in ALL_COLUMNS:
                continue
            val = _raw_get(raw_entry, key)
            if not _nonempty(val):
                continue
            label = _esc(_col_label(key))
            value = _esc(
                ", ".join(map(str, _listify(val)))
                if isinstance(val, (list, tuple))
                else _val_to_str(val)
            )
            rows.append(
                f'  <p class="meta-row"><span class="meta-label">{label}</span>'
                f'<span class="meta-sep">:</span> <span class="meta-value">{value}</span></p>\n'
            )
        rows.append("</div>\n")
        return "".join(rows)

    def _resource_links_html(self, raw_entry: Dict[str, Any]) -> str:
        """Render benchmark url, dataset links, and result links as a resource block."""
        benchmark_url = raw_entry.get("url")
        dataset_links = _extract_links(raw_entry.get("datasets"))
        result_links = _extract_links(raw_entry.get("results"))

        if not (benchmark_url or dataset_links or result_links):
            return ""

        parts: List[str] = ['<div class="info-block resource-block">\n', "<h3>Resources</h3>\n"]
        groups: List[str] = []

        if benchmark_url:
            groups.append(
                '<div class="resource-group">'
                '<span class="resource-label">Benchmark:</span> '
                f'<a class="md-chip md-chip--primary" href="{_esc(benchmark_url)}" '
                'target="_blank" rel="noopener">Visit</a>'
                "</div>"
            )

        if dataset_links:
            dataset_links_html = ", ".join(
                f'<a class="md-chip" href="{_esc(url)}" target="_blank" rel="noopener">{_esc(name)}</a>'
                for name, url in dataset_links
            )
            groups.append(
                '<div class="resource-group">'
                '<span class="resource-label">Datasets:</span> '
                f"{dataset_links_html}"
                "</div>"
            )

        if result_links:
            result_links_html = ", ".join(
                f'<a class="md-chip" href="{_esc(url)}" target="_blank" rel="noopener">{_esc(name)}</a>'
                for name, url in result_links
            )
            groups.append(
                '<div class="resource-group">'
                '<span class="resource-label">Results:</span> '
                f"{result_links_html}"
                "</div>"
            )

        if groups:
            parts.append("\n".join(groups) + "\n")

        parts.append("</div>\n")
        return "".join(parts)

    def _keywords_html(self, raw_entry: Dict[str, Any], link_base: str) -> str:
        """Clickable keyword chips linking back to index with prefilled hash."""
        kws = _listify(raw_entry.get("keywords"))
        if not kws:
            return ""
        out = ['<h3>Keywords</h3>\n\n<div class="chips">']
        for kw in kws:
            safe = _esc(str(kw).strip().replace('"', "").replace("'", ""))
            safe_href = (
                f"{link_base}kw={quote(kw.strip())}"  # e.g. ./#kw=long%20context
            )
            out.append(f'<a class="chip chip-link" href="{safe_href}">{safe}</a> ')
        out.append("</div>\n")
        return "".join(out)

    def _citations_html(self, raw_entry: Dict[str, Any], columns: List[str]) -> str:
        """Citations rendered only if 'cite' is included in `columns`."""
        if "cite" not in columns:
            return ""
        citations = _listify(raw_entry.get("cite"))
        if not citations:
            return ""
        out: List[str] = [f"<h3>{_esc(_col_label('cite'))}</h3>\n\n"]
        for bib in citations:
            if not isinstance(bib, str):
                out.append(
                    f"- Could not parse citation: Expected BibTeX string, got {html.escape(type(bib).__name__)}\n"
                )
                continue
            out.append(f"- {html.escape(_bibtex_to_text(bib))}\n\n")
            out.append('<pre><code class="language-bibtex">')
            out.append(html.escape(bib.strip()))
            out.append("</code></pre>\n")
        return "".join(out)

    def _ratings_html(
        self, entry: Dict[str, Any], columns: List[str]
    ) -> Tuple[str, float | None]:
        """
        Render ratings as a compact, comparable grid (badge + bar + reason).
        Shows only aspects requested in `columns`. Average = sum/count of present numeric ratings.
        """
        requested = _requested_rating_aspects(
            columns
        )  # {"software":{"rating","reason"}, ...}
        items, s, c = _collect_ratings(entry)
        if not items:
            return "", None

        # If nothing requested, show nothing but still return the average
        if not any(requested.get(cat) for cat, _ in items):
            return "", (round(s / c, 3) if c else None)

        rows: List[str] = []
        for cat, d in items:
            aspects = requested.get(cat)
            if not aspects:
                continue

            # rating number
            r_val = d.get("rating")
            r_num: float | None = None
            r_str = "—"
            if _nonempty(r_val):
                try:
                    r_num = float(r_val)
                    r_str = f"{r_num:.2f}"
                except (ValueError, TypeError):
                    pass

            # reason
            reason = d.get("reason") if "reason" in aspects else None

            # progress bar width (0–100) against a 0–5 scale
            width_pct = 0
            if r_num is not None:
                width_pct = max(0, min(100, int(round((r_num / 5.0) * 100))))

            rows.append(
                '<div class="rating-item">'
                f'  <div class="rating-cat">{_esc(cat.replace("_", " ").title())}</div>'
                f'  <div class="rating-badge">{_esc(r_str)}</div>'
                f'  <div class="rating-bar"><span style="width:{width_pct}%"></span></div>'
                + (
                    f'  <div class="rating-reason">{_esc(reason)}</div>'
                    if _nonempty(reason)
                    else ""
                )
                + "</div>"
            )

        if not rows:
            return "", (round(s / c, 3) if c else None)

        block = (
            "<h3>Ratings</h3>\n"
            '<div class="ratings-grid">\n'
            '  <div class="ratings-head ratings-cell"><span>Category</span><span>Rating</span></div>\n'
            f'  {"".join(rows)}\n'
            "</div>\n"
        )
        avg = round(s / c, 3) if c else None
        return block, avg

    def _extra_fields_html(self, raw_entry: Dict[str, Any], columns: List[str]) -> str:
        """
        Append any additional fields from `columns` that are NOT:
          - in the hardcoded subset,
          - a ratings.* key,
          - 'cite'.
        """
        out: List[str] = []
        for col in columns:
            if (
                col in _HARDCODED_DETAIL_FIELDS
                or col == "keywords"
                or col == "cite"
                or col.startswith("ratings.")
            ):
                continue
            if col not in ALL_COLUMNS:
                continue
            val = _raw_get(raw_entry, col)
            if not _nonempty(val):
                continue
            out.append(
                f"<p><strong>{_esc(_col_label(col))}</strong>: {_esc(_val_to_str(val))}</p>\n"
            )
        return "".join(out)

    def _detail_page_html(
        self,
        entry: Dict[str, Any],
        raw_entry: Dict[str, Any] | None,
        columns: List[str],
        average_ratings: bool,
    ) -> str:
        """Compose one detail page as Markdown+HTML mix (works well in MkDocs)."""
        if raw_entry is None:
            raise KeyError("Raw entry is required for detail rendering.")
        if not raw_entry.get("id"):
            raise KeyError("Raw entry missing required 'id' field.")

        id_ = str(raw_entry.get("id"))
        name = str(raw_entry.get("name", id_))
        parts: List[str] = []

        # Title
        parts.append(f"# {_esc(name)}\n")

        back_href = "../cards/" if self.use_directory_urls else "../cards.html"
        parts.append(
            f"\n<p><a class=\"md-button back-link\" href=\"{_esc(back_href)}\">"
            "← Back to all benchmarks</a></p>\n"
        )

        # Meta subset
        parts.append(self._meta_block_html(raw_entry))
        parts.append(self._resource_links_html(raw_entry))

        # Keywords
        parts.append(self._keywords_html(raw_entry, link_base="../#"))

        # Citations (if requested)
        parts.append(self._citations_html(raw_entry, columns))

        # Ratings (grid)
        ratings_html, ratings_avg = self._ratings_html(entry, columns)
        parts.append(ratings_html)

        # Extra fields before image
        parts.append(self._extra_fields_html(raw_entry, columns))

        # Average line (sum/count across present numeric ratings)
        if average_ratings and ratings_avg is not None:
            parts.append(
                '<div class="avg-rating">'
                "  <strong>Average rating:</strong> "
                + self._rating_badge(ratings_avg)
                + "</div>"
            )

        # Radar image (correct relative path from content/md/benchmarks/{id}.md)
        parts.append("<h3>Radar plot</h3>\n\n")
        parts.append(
            f'<div class="radar-wrap"><img class="radar-img" alt="{_esc(name)} radar" '
            f'src="../../../tex/images/{_esc(id_)}_radar.png" /></div>\n'
        )

        # Edit link
        parts.append(
            "\n<p><strong>Edit:</strong> "
            '<a href="https://github.com/mlcommons-science/benchmark/tree/main/source">'
            "edit this entry</a></p>\n"
        )

        return "".join(parts)

    # ------------------------------- public API ------------------------------

    def write_individual_entries(
        self,
        output_dir: str = "content/md/benchmarks",
        columns: List[str] = DEFAULT_COLUMNS,
        author_trunc: int | None = None,  # API parity (unused)
        average_ratings: bool = True,
        *,
        filters_js_src: (
            str | None
        ) = None,  # optionally inject <script src="..."></script> into index.md
    ) -> None:
        """
        Write:
          - index.md with filter controls + pre-rendered cards (data-* attributes),
          - {id}.md detail pages.
        """
        valid_columns = _validate_columns(list(columns))
        os.makedirs(output_dir, exist_ok=True)

        # Build index
        index_lines: List[str] = [self._index_header_html()]

        for i, entry in enumerate(self.entries):
            # Compute ratings average over present numeric ratings (JS-compatible behavior)
            _, s, c = _collect_ratings(entry)
            ratings_avg = round(s / c, 3) if c else None

            raw_entry = self._get_raw_entry(entry)
            if raw_entry is None:
                raise KeyError(
                    f"Raw entry not found for benchmark "
                    f"{entry.get('id') or entry.get('name') or f'index {i}'}"
                )
            if not raw_entry.get("id"):
                raise KeyError(
                    f"Raw entry missing required 'id' for "
                    f"{entry.get('name') or f'index {i}'}"
                )

            # Detail page
            id_ = str(raw_entry.get("id"))
            filename = os.path.join(output_dir, f"{id_}.md")
            page_html = self._detail_page_html(
                entry, raw_entry, valid_columns, average_ratings
            )
            write_to_file(content=page_html, filename=filename)

            # Index card
            index_lines.append(self._index_card_html(entry, raw_entry, ratings_avg))

        index_lines.append(self._index_footer_html(filters_js_src))
        index_filename = os.path.join(output_dir, "cards.md")
        write_to_file(content="".join(index_lines), filename=index_filename)

    def write_table_new(
        self,
        filename="content/md/benchmarks_table.md",
        columns=DEFAULT_COLUMNS,
        average_ratings: bool = True,
    ) -> None:
        
        contents = (
            "# Benchmarks Table\n\n"
            "<table id=\"benchmarksTable\" class=\"display nowrap\" style=\"width:100%\"></table>\n"
        )

        write_to_file(content=contents, filename=filename)

    def write_index_md(
        self,
        output_dir: str = "content/md/benchmarks",
        *,
        title: str = "Index of Benchmarks",
        detail_base: str = ".",  # where detail pages live relative to this index
        sort_by: str = "name",  # "name" | "id" | None
    ) -> None:
        """
        Writes ONLY an index file listing all benchmarks as links to their detail pages.
        """
        os.makedirs(output_dir, exist_ok=True)
        index_filename = os.path.join(output_dir, "index.md")

        # Prepare items (id, name)
        items = []
        for i, entry in enumerate(self.entries):
            raw_entry = self._get_raw_entry(entry)
            if raw_entry is None or not raw_entry.get("id"):
                raise KeyError(
                    f"Raw entry missing for benchmark "
                    f"{entry.get('name') or entry.get('id') or f'index {i}'}"
                )
            id_ = str(raw_entry.get("id")).strip()
            name = str(raw_entry.get("name", id_)).strip()
            items.append((id_, name))

        # Optional stable sort (case-insensitive)
        if sort_by in {"name", "id"}:
            idx = 1 if sort_by == "name" else 0
            items.sort(key=lambda t: (t[idx] or "").lower())

        # Build content
        lines = []
        lines.append(f"# {title}\n")
        lines.append("\n")

        for id_, name in items:
            href = os.path.normpath(f"{detail_base}/{id_}").replace("\\", "/") + ".md"
            lines.append(f"- [{name}]({href})\n")

        write_to_file(content="".join(lines), filename=index_filename)
