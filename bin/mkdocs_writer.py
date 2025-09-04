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

    # ----------------------- md table utilities ------------------------------
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
        return f"{id_}/" if self.use_directory_urls else f"{id_}.html"

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

    def _index_card_html(self, entry: Dict[str, Any], ratings_avg: float | None) -> str:
        """
        Generate one card with the data-* attributes needed for DOM filtering/sorting.
        Only uses fields relevant to filtering/sorting; adding new YAML columns won’t break the UI.
        """
        id_ = entry.get("id", "")
        name = entry.get("name", id_)
        date = entry.get("date", "")

        domain_list = _listify(entry.get("domain"))
        metrics_list = _listify(entry.get("metrics"))
        task_types_list = _listify(entry.get("task_types"))
        keywords_list = _listify(entry.get("keywords"))

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

        # data-* attributes used by filters.js
        return f"""
            <article class="benchmark-card"
                    data-id="{_esc(id_)}"
                    data-name="{_esc(name)}"
                    data-date="{_esc(date)}"
                    data-focus="{_esc(entry.get('focus', ''))}"
                    data-domain="{_esc(', '.join(map(str, domain_list)))}"
                    data-task-types="{_esc(', '.join(map(str, task_types_list)))}"
                    data-metrics="{_esc(', '.join(map(str, metrics_list)))}"
                    data-keywords="{_esc(', '.join(map(str, keywords_list)))}"
                    data-ratings-avg="{_esc(rating_str)}">
                <h3>{_esc(name)}</h3>
                {f'<p class="muted">{_esc(subtitle)}</p>' if subtitle else ''}
                {chips}
                <p class="muted">Avg rating: {badge_html}</p>
                <p><a class="md-button md-button--primary" href="{_esc(self._detail_href(id_))}">Details</a></p>
            </article>
            """.strip()

    # ---------------------- detail page composition --------------------------

    def _meta_block_html(self, entry: Dict[str, Any]) -> str:
        """HTML meta block showing the hardcoded subset first (skip missing)."""
        rows = ['<div class="info-block meta-block">\n']
        for key in _HARDCODED_DETAIL_FIELDS:
            if key not in ALL_COLUMNS:
                continue
            val = entry.get(key)
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

    def _keywords_html(self, entry: Dict[str, Any], link_base: str) -> str:
        """Clickable keyword chips linking back to index with prefilled hash."""
        kws = _listify(entry.get("keywords"))
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

    def _citations_html(self, entry: Dict[str, Any], columns: List[str]) -> str:
        """Citations rendered only if 'cite' is included in `columns`."""
        if "cite" not in columns:
            return ""
        citations = _listify(entry.get("cite"))
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

    def _extra_fields_html(self, entry: Dict[str, Any], columns: List[str]) -> str:
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
            val = entry.get(col)
            if not _nonempty(val):
                continue
            out.append(
                f"<p><strong>{_esc(_col_label(col))}</strong>: {_esc(_val_to_str(val))}</p>\n"
            )
        return "".join(out)

    def _detail_page_html(
        self, entry: Dict[str, Any], columns: List[str], average_ratings: bool
    ) -> str:
        """Compose one detail page as Markdown+HTML mix (works well in MkDocs)."""
        name = entry.get("name", entry.get("id", ""))
        id_ = entry.get("id", "")
        parts: List[str] = []

        # Title
        parts.append(f"# {_esc(name)}\n")

        # Back link
        parts.append(
            '\n<p><a class="md-button back-link" href="../">← Back to all benchmarks</a></p>\n'
        )

        # Meta subset
        parts.append(self._meta_block_html(entry))

        # Keywords
        parts.append(self._keywords_html(entry, link_base="../#"))

        # Citations (if requested)
        parts.append(self._citations_html(entry, columns))

        # Ratings (grid)
        ratings_html, ratings_avg = self._ratings_html(entry, columns)
        parts.append(ratings_html)

        # Extra fields before image
        parts.append(self._extra_fields_html(entry, columns))

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

            # Detail page
            id_ = entry.get("id", f"entry-{i}")
            filename = os.path.join(output_dir, f"{id_}.md")
            page_html = self._detail_page_html(entry, valid_columns, average_ratings)
            write_to_file(content=page_html, filename=filename)

            # Index card
            index_lines.append(self._index_card_html(entry, ratings_avg))

        index_lines.append(self._index_footer_html(filters_js_src))
        index_filename = os.path.join(output_dir, "cards.md")
        write_to_file(content="".join(index_lines), filename=index_filename)

    def write_table_new(
        self,
        filename="content/md/benchmarks_table.md",
        columns=DEFAULT_COLUMNS,
        average_ratings: bool = True,
    ) -> None:
        # ... (existing code)

        # New section for HTML table generation
        html_table = f'<table id="benchmarksTable" class="display">\n'

        # Generate the table header (<thead>)
        html_table += "<thead>\n<tr>"
        for col in columns:
            html_table += f"<th>{self._colunm_label(col)}</th>"
        if average_ratings:
            html_table += "<th>Average Ratings</th>"
        html_table += "</tr>\n</thead>\n"

        # Generate the table body (<tbody>)
        html_table += "<tbody>\n"
        for entry in self.entries:
            html_table += "<tr>"
            ratings_average = 0

            for col in columns:
                val = entry.get(col, "")

                # Simplified logic for creating HTML cells
                cell_content = ""
                if col == "name":
                    title = self._escape_md(str(val))
                    id_ = str(entry.get("id", "")).strip()
                    if id_:
                        target_md = f"benchmarks/{quote(id_)}.md"
                        cell_content = f"<a href='{target_md}'>{title}</a>"
                    else:
                        cell_content = title
                elif col == "cite":
                    # Handle citations and footnotes in a more robust way
                    # (You might need a separate function for this)
                    citation_refs = []
                    # ... (citation logic)
                    cell_content = ", ".join(citation_refs)
                elif isinstance(val, list):
                    cell_content = ", ".join(map(self._escape_md, val))
                else:
                    if col.endswith("rating"):
                        try:
                            ratings_average += float(val)
                        except ValueError:
                            Console.error(f'Rating entry "{val}" must be a number')
                    cell_content = self._escape_md(str(val))

                html_table += f"<td>{cell_content}</td>"

            # Add average rating column
            if average_ratings:
                avg_rating = round(ratings_average / 6, 3) if 6 > 0 else 0
                html_table += f"<td>{avg_rating}</td>"

            html_table += "</tr>\n"

        html_table += "</tbody>\n</table>\n"

        # Construct the final content with the HTML table
        contents = html_table  # + footnote_contents + table_script

        write_to_file(content=contents, filename=filename)

    def write_table(
        self,
        filename="content/md/benchmarks_table.md",
        columns=DEFAULT_COLUMNS,
        average_ratings: bool = True,
    ) -> None:
        """
        Write:
          - index.md with a plain md table of all entries
        """
        headline = "# Benchmarks (Table)\n\n"
        table_start = '<div class="page-data-table">\n'
        table_end = textwrap.dedent(
            """
            </div>
            """
        )

        table_script = textwrap.dedent(
            """

            <script>
            $(document).ready(function() {
            if ($('.page-data-table table').length) {
                $('.page-data-table table').DataTable({
                scrollX: true,
                fixedColumns: {
                    left: 2
                },
                ordering: true
                });
            }
            });
            </script>
            """
        )

        col_labels = []
        col_widths = []

        for col in columns:
            col_labels.append(self._colunm_label(col))
            col_widths.append(self._column_width_str(col))

        section = f'<div id="bench-table-page"></div>\n\n{headline}'
        header = " | " + " | ".join(col_labels) + " | "
        if average_ratings:
            header += " Average Ratings "
        header += "\n"

        divider = ""
        for e in col_widths:
            divider += "| " + str(e) + " "
        if average_ratings:
            divider += " | -------- "
        divider += "|\n"

        # Create the contents string
        current_contents = ""
        footnotes = []

        # Write each entry to the table
        for entry in self.entries:
            row = ""
            ratings_average = 0

            # Write each cell to the table
            for col in columns:
                val = entry.get(col, "")

                if col == "name":
                    title = self._escape_md(str(val))
                    id_ = str(entry.get("id", "")).strip()
                    if id_:
                        # Link to the source .md; MkDocs will rewrite to the correct output URL
                        # regardless of use_directory_urls.
                        target_md = f"benchmarks/{quote(id_)}.md"
                        row += f"[{title}]({target_md})"
                    else:
                        row += title
                # handle citations
                elif col == "cite":
                    citations = val if isinstance(val, list) else [val]
                    citation_refs = []
                    for c in citations:
                        citation_text = _bibtex_to_text(c)
                        if citation_text.startswith("Could not parse citation:"):
                            footnotes.append(None)
                        else:
                            footnotes.append(self._escape_md(citation_text))
                            citation_refs.append(f"[^{len(footnotes)}]")
                    row += ", ".join(citation_refs)

                elif isinstance(val, list):
                    row += ", ".join(map(self._escape_md, val))

                else:
                    if col.endswith("rating"):
                        try:
                            ratings_average += float(val)
                        except ValueError:
                            Console.error(f'Rating entry "{val}" must be a number')

                    row += self._escape_md(str(val))

                row += " | "

            # Calculate and add average
            ratings_average /= 6
            if average_ratings:
                row += str(round(ratings_average, 3)) + " |"

            current_contents += row + "\n"
        current_contents = current_contents.strip()
        current_contents += "\n\n"
        footnote_contents = ""
        for i, citation in enumerate(footnotes):
            footnote_contents += f"[^{i + 1}]: {citation}\n" if citation else ""

        contents = section + header + divider + current_contents + footnote_contents

        # contents = (
        #     section
        #     + table_start
        #     + header
        #     + divider
        #     + current_contents
        #     + table_end
        #     + footnote_contents
        #     + table_script
        # )

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
            id_ = str(entry.get("id", f"entry-{i}")).strip()
            name = str(entry.get("name", id_)).strip()
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
