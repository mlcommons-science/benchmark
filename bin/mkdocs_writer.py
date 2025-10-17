"""Utilities for generating MkDocs content from benchmark YAML data.

The module centres around :class:`MkdocsWriter`, which produces:

* ``cards.md`` — card grid with filter controls consumed by ``filters.js``.
* ``{id}.md`` detail pages — rich information for each benchmark.
* ``benchmarks_table.md`` — empty table shell hydrated by ``benchmarks-table.js``.
"""

from __future__ import annotations

import html
import os
import re
import textwrap
from dataclasses import dataclass, field
from typing import Any, Dict, Iterable, List, Sequence, Tuple
from urllib.parse import quote

from pybtex.database import parse_string
from pybtex.plugin import find_plugin

from cloudmesh.common.console import Console
from generate_latex import ALL_COLUMNS, DEFAULT_COLUMNS, write_to_file

__all__ = ["MkdocsWriter"]


# ---------------------------------------------------------------------------
# Template fragments
# ---------------------------------------------------------------------------

INDEX_HEADER_TEMPLATE = textwrap.dedent(
    """
    # Index of Benchmarks

    <div class="filter-bar">
    <input type="search" id="f_q" placeholder="Search (name, focus, metrics…)" />
    <select id="f_domain"><option value="">All domains</option></select>
    <input type="text" id="f_keywords" placeholder="Keywords (comma-separated)" />
    <input type="date" id="f_from" placeholder="From date" />
    <input type="date" id="f_to" placeholder="To date" />
    <input type="number" id="f_minrating" min="0" max="5" step="0.1" placeholder="Min avg rating" />
    <select id="f_sort">
      <option value="date_desc">Sort: Date ↓</option>
      <option value="date_asc">Sort: Date ↑</option>
      <option value="name_asc">Sort: Name A–Z</option>
      <option value="rating_desc">Sort: Rating ↓</option>
    </select>
    <button id="f_reset" type="button">Reset</button>
    </div>

    <div id="cards-root" class="grid cards">
    """
).strip() + "\n"

INDEX_FOOTER_TEMPLATE = "</div>\n{script}"

CARD_TEMPLATE = textwrap.dedent(
    """
    <article class="benchmark-card"
            data-id="{data_id}"
            data-name="{data_name}"
            data-date="{data_date}"
            data-focus="{data_focus}"
            data-domain="{data_domain}"
            data-task-types="{data_task_types}"
            data-metrics="{data_metrics}"
            data-keywords="{data_keywords}"
            data-ratings-avg="{data_ratings_avg}">
        <h3>{title}</h3>
        {subtitle_html}
        {chips_html}
        <p class="muted">Avg rating: {rating_badge}</p>
        <p><a class="md-button md-button--primary" href="{detail_href}">Details</a></p>
    </article>
    """
).strip()

DETAIL_TEMPLATE = textwrap.dedent(
    """
    # {title}

    {back_link}
    {meta_block}{resource_block}{keywords_block}{citations_block}{ratings_block}{extra_block}{average_block}
    {radar_block}
    {edit_block}
    """
).strip() + "\n"

BACK_LINK_TEMPLATE = '<p><a class="md-button back-link" href="{href}">← Back to all benchmarks</a></p>\n'

RADAR_TEMPLATE = textwrap.dedent(
    """
    <h3>Radar plot</h3>

    <div class="radar-wrap">
        <img class="radar-img" alt="{alt}" src="../../../tex/images/{image_name}_radar.png" />
    </div>
    """
).strip() + "\n"

EDIT_LINK_HTML = (
    "\n<p><strong>Edit:</strong> "
    '<a href="https://github.com/mlcommons-science/benchmark/tree/main/source">'
    "edit this entry</a></p>\n"
)

META_FIELDS: List[str] = [
    "date",
    "name",
    "domain",
    "focus",
    "task_types",
    "metrics",
    "models",
    "ml_motif",
]

HTML = str


# ---------------------------------------------------------------------------
# Utilities
# ---------------------------------------------------------------------------

def _esc(value: Any) -> HTML:
    """Escape ``value`` for safe HTML embedding."""
    return html.escape("" if value is None else str(value), quote=True)


def _nonempty(value: Any) -> bool:
    """Return ``True`` if ``value`` contains meaningful data."""
    return value not in (None, "", [])


def _as_list(value: Any) -> List[str]:
    """Coerce scalars into a list of stripped strings."""
    if value is None or value == "":
        return []
    if isinstance(value, list):
        return [str(item).strip() for item in value]
    return [str(value).strip()]


def _flatten_text(value: Any) -> str:
    """Flatten lists or structured strings into single-line text."""
    if value is None:
        return ""
    text = str(value).replace("\n", " ").replace("['", "").replace("']", "")
    text = text.replace("', '", ", ").replace("','", ", ").replace("[]", "")
    text = text.replace("[", " ").replace("]", " ").replace("(", " ").replace(")", " ")
    return text.strip()


def _dotted_get(data: Dict[str, Any], dotted_key: str) -> Any:
    """Retrieve nested values using dot notation."""
    current: Any = data
    for part in dotted_key.split("."):
        if isinstance(current, dict):
            current = current.get(part)
        else:
            return None
    return current


def _col_label(column: str) -> str:
    """Return the human-readable label for ``column``."""
    return str(ALL_COLUMNS[column]["label"])


def _validate_columns(columns: Iterable[str]) -> List[str]:
    """Filter ``columns`` to those defined in ``ALL_COLUMNS``."""
    valid: List[str] = []
    invalid: List[str] = []
    for column in columns:
        if column in ALL_COLUMNS:
            valid.append(column)
        else:
            invalid.append(column)
    if invalid:
        Console.warning(f"Unknown columns skipped: {', '.join(invalid)}")
    return valid


def _bibtex_to_text(entry: str) -> str:
    """Render a BibTeX entry to plain text (best effort)."""
    try:
        if not isinstance(entry, str):
            raise TypeError(f"Expected string for BibTeX entry, got {type(entry).__name__}")
        bib_data = parse_string(entry, bib_format="bibtex")
        style = find_plugin("pybtex.style.formatting", "plain")()
        formatted = next(style.format_entries(bib_data.entries.values()))
        return re.sub(r"<[^>]+>", " ", str(formatted.text)).strip()
    except Exception as exc:  # pragma: no cover - defensive
        return f"Could not parse citation: {exc}"


# ---------------------------------------------------------------------------
# Normalised entry representation
# ---------------------------------------------------------------------------


@dataclass
class BenchmarkEntry:
    """Value object wrapping a single benchmark for rendering."""

    raw: Dict[str, Any]
    id: str = field(init=False)
    name: str = field(init=False)
    date: str = field(init=False)
    domains: List[str] = field(init=False)
    metrics: List[str] = field(init=False)
    task_types: List[str] = field(init=False)
    keywords: List[str] = field(init=False)
    focus: str = field(init=False)

    def __post_init__(self) -> None:
        entry_id = str(self.raw.get("id") or "").strip()
        if not entry_id:
            raise KeyError(
                "Benchmark entry is missing an 'id'. Ensure YamlManager.clean_string ran before generation."
            )
        self.id = entry_id
        self.name = str(self.raw.get("name") or self.id).strip()
        self.date = str(self.raw.get("date") or "").strip()
        self.domains = _as_list(self.raw.get("domain"))
        self.metrics = _as_list(self.raw.get("metrics"))
        self.task_types = _as_list(self.raw.get("task_types"))
        self.keywords = _as_list(self.raw.get("keywords"))
        self.focus = _flatten_text(self.raw.get("focus"))

    # ------------------------------------------------------------------ cards

    def card_html(self, ratings_average: float | None, use_directory_urls: bool) -> HTML:
        """HTML card snippet for the MkDocs index page."""
        rating_value = f"{ratings_average:.2f}" if ratings_average is not None else ""
        badge = self._rating_badge(ratings_average)
        subtitle_parts: List[str] = []
        if self.domains:
            subtitle_parts.append(", ".join(self.domains))
        if self.metrics:
            subtitle_parts.append(", ".join(self.metrics))
        subtitle_html = (
            f'<p class="muted">{_esc(" • ".join(subtitle_parts))}</p>'
            if subtitle_parts
            else "<!-- no subtitle -->"
        )
        chips_html = (
            '<div class="chips">'
            + " ".join(
                f'<a class="chip chip-link" href="#kw={_esc(keyword)}">{_esc(keyword)}</a>'
                for keyword in self.keywords[:5]
            )
            + "</div>"
            if self.keywords
            else "<!-- no keywords -->"
        )
        detail_href = f"../{self.id}/" if use_directory_urls else f"../{self.id}.html"
        return CARD_TEMPLATE.format(
            data_id=_esc(self.id),
            data_name=_esc(self.name),
            data_date=_esc(self.date),
            data_focus=_esc(self.focus),
            data_domain=_esc(", ".join(self.domains)),
            data_task_types=_esc(", ".join(self.task_types)),
            data_metrics=_esc(", ".join(self.metrics)),
            data_keywords=_esc(", ".join(self.keywords)),
            data_ratings_avg=_esc(rating_value),
            title=_esc(self.name),
            subtitle_html=subtitle_html,
            chips_html=chips_html,
            rating_badge=badge,
            detail_href=_esc(detail_href),
        )

    # --------------------------------------------------------------- detail

    def render_detail(
        self,
        columns: Sequence[str],
        *,
        average_ratings: bool,
        use_directory_urls: bool,
    ) -> Tuple[HTML, float | None]:
        """Return the detail page HTML and average rating."""
        ratings_block, ratings_average = self._ratings_block(columns)
        average_block = ""
        if average_ratings and ratings_average is not None:
            average_block = (
                '<div class="avg-rating">'
                "  <strong>Average rating:</strong> "
                + self._rating_badge(ratings_average)
                + "</div>"
            )

        detail_html = DETAIL_TEMPLATE.format(
            title=_esc(self.name),
            back_link=BACK_LINK_TEMPLATE.format(
                href=_esc("../cards/" if use_directory_urls else "../cards.html")
            ),
            meta_block=self._meta_block(),
            resource_block=self._resources_block(),
            keywords_block=self._keywords_block(),
            citations_block=self._citations_block(columns),
            ratings_block=ratings_block,
            extra_block=self._extra_block(columns),
            average_block=average_block,
            radar_block=RADAR_TEMPLATE.format(
                alt=_esc(f"{self.name} radar"), image_name=_esc(self.id)
            ),
            edit_block=EDIT_LINK_HTML,
        )
        return detail_html, ratings_average

    # --------------------------------------------------------------- sections

    def _meta_block(self) -> HTML:
        rows: List[str] = ['<div class="info-block meta-block">\n']
        for key in META_FIELDS:
            if key not in ALL_COLUMNS:
                continue
            value = _dotted_get(self.raw, key)
            if not _nonempty(value):
                continue
            rows.append(
                f'  <p class="meta-row"><span class="meta-label">{_esc(_col_label(key))}</span>'
                f'<span class="meta-sep">:</span> <span class="meta-value">{_esc(self._render_value(value))}</span></p>\n'
            )
        rows.append("</div>\n")
        return "".join(rows)

    def _resources_block(self) -> HTML:
        benchmark_url = self.raw.get("url")
        dataset_links = self._extract_links(self.raw.get("datasets"))
        result_links = self._extract_links(self.raw.get("results"))

        if not (benchmark_url or dataset_links or result_links):
            return ""

        groups: List[str] = []
        if benchmark_url:
            groups.append(
                '<div class="resource-group">'
                '<span class="resource-label">Benchmark:</span> '
                f'<a class="md-chip md-chip--primary" href="{_esc(benchmark_url)}" target="_blank" rel="noopener">Visit</a>'
                "</div>"
            )
        if dataset_links:
            groups.append(
                '<div class="resource-group">'
                '<span class="resource-label">Datasets:</span> '
                + ", ".join(
                    f'<a class="md-chip" href="{_esc(url)}" target="_blank" rel="noopener">{_esc(name)}</a>'
                    for name, url in dataset_links
                )
                + "</div>"
            )
        if result_links:
            groups.append(
                '<div class="resource-group">'
                '<span class="resource-label">Results:</span> '
                + ", ".join(
                    f'<a class="md-chip" href="{_esc(url)}" target="_blank" rel="noopener">{_esc(name)}</a>'
                    for name, url in result_links
                )
                + "</div>"
            )

        return (
            '<div class="info-block resource-block">\n'
            "<h3>Resources</h3>\n"
            + "\n".join(groups)
            + "\n</div>\n"
        )

    def _keywords_block(self) -> HTML:
        if not self.keywords:
            return ""
        chips = " ".join(
            f'<a class="chip chip-link" href="../#kw={quote(keyword)}">{_esc(keyword)}</a>'
            for keyword in self.keywords
        )
        return "<h3>Keywords</h3>\n\n<div class=\"chips\">" + chips + "</div>\n"

    def _citations_block(self, columns: Sequence[str]) -> HTML:
        if "cite" not in columns:
            return ""
        citations = _as_list(self.raw.get("cite"))
        if not citations:
            return ""
        rendered: List[str] = [f"<h3>{_esc(_col_label('cite'))}</h3>\n\n"]
        for bib in citations:
            if not isinstance(bib, str):
                rendered.append(
                    f"- Could not parse citation: Expected BibTeX string, got {html.escape(type(bib).__name__)}\n"
                )
                continue
            rendered.append(f"- {html.escape(_bibtex_to_text(bib))}\n\n")
            rendered.append('<pre><code class="language-bibtex">')
            rendered.append(html.escape(bib.strip()))
            rendered.append("</code></pre>\n")
        return "".join(rendered)

    def _ratings_block(self, columns: Sequence[str]) -> Tuple[HTML, float | None]:
        ratings = self.raw.get("ratings")
        if not isinstance(ratings, dict):
            return "", self._ratings_average(ratings)

        requested = self._requested_rating_aspects(columns)
        ordered_items = self._ordered_ratings(ratings)
        if not ordered_items:
            return "", self._ratings_average(ratings)

        rows: List[str] = []
        total = 0.0
        count = 0
        for category, info in ordered_items:
            rating_value = info.get("rating")
            reason_value = info.get("reason")
            aspects = requested.get(category)

            rating_number: float | None = None
            rating_label = "—"
            if _nonempty(rating_value):
                try:
                    rating_number = float(rating_value)
                    rating_label = f"{rating_number:.2f}"
                    total += rating_number
                    count += 1
                except (ValueError, TypeError):
                    Console.error(f'The rating "{rating_value}" must be a number')

            if not aspects:
                continue

            width_pct = 0
            if rating_number is not None:
                width_pct = max(0, min(100, int(round((rating_number / 5.0) * 100))))

            rows.append(
                '<div class="rating-item">'
                f'  <div class="rating-cat">{_esc(category.replace("_", " ").title())}</div>'
                f'  <div class="rating-badge">{_esc(rating_label)}</div>'
                f'  <div class="rating-bar"><span style="width:{width_pct}%"></span></div>'
                + (
                    f'  <div class="rating-reason">{_esc(reason_value)}</div>'
                    if _nonempty(reason_value) and "reason" in aspects
                    else ""
                )
                + "</div>"
            )

        average = round(total / count, 3) if count else None
        if not rows:
            return "", average

        block = (
            "<h3>Ratings</h3>\n"
            '<div class="ratings-grid">\n'
            '  <div class="ratings-head ratings-cell"><span>Category</span><span>Rating</span></div>\n'
            f'  {"".join(rows)}\n'
            "</div>\n"
        )
        return block, average

    def _extra_block(self, columns: Sequence[str]) -> HTML:
        extras: List[str] = []
        for column in columns:
            if column in META_FIELDS or column in {"keywords", "cite"}:
                continue
            if column.startswith("ratings."):
                continue
            if column not in ALL_COLUMNS:
                continue
            value = _dotted_get(self.raw, column)
            if not _nonempty(value):
                continue
            extras.append(
                f"<p><strong>{_esc(_col_label(column))}</strong>: {_esc(self._render_value(value))}</p>\n"
            )
        return "".join(extras)

    # ------------------------------------------------------------- rating utils

    def _ratings_average(self, ratings: Any) -> float | None:
        if not isinstance(ratings, dict):
            return None
        total = 0.0
        count = 0
        for info in ratings.values():
            if not isinstance(info, dict):
                continue
            rating_value = info.get("rating")
            if _nonempty(rating_value):
                try:
                    total += float(rating_value)
                    count += 1
                except (ValueError, TypeError):
                    Console.error(f'The rating "{rating_value}" must be a number')
        return round(total / count, 3) if count else None

    def _requested_rating_aspects(self, columns: Sequence[str]) -> Dict[str, set]:
        requested: Dict[str, set] = {}
        for column in columns:
            if column.startswith("ratings."):
                _, category, aspect = column.split(".", 2)
                requested.setdefault(category, set()).add(aspect)
        return requested

    def _ordered_ratings(self, ratings: Dict[str, Any]) -> List[Tuple[str, Dict[str, Any]]]:
        preferred = [
            "software",
            "specification",
            "dataset",
            "metrics",
            "reference_solution",
            "documentation",
        ]
        items: Dict[str, Dict[str, Any]] = {}
        for category, payload in ratings.items():
            if isinstance(payload, dict):
                items[str(category)] = {"rating": payload.get("rating"), "reason": payload.get("reason")}
        ordered = [key for key in preferred if key in items] + sorted(
            key for key in items.keys() if key not in preferred
        )
        return [(key, items[key]) for key in ordered]

    def _rating_badge(self, average: float | None, size: str = "sm") -> str:
        if average is None:
            return ""
        color = "ok" if average >= 4 else "meh" if average >= 3 else "bad"
        return f'<span class="badge badge--{color} badge--{size}">{average:.2f}/5</span>'

    # ------------------------------------------------------------- misc utils

    def _render_value(self, value: Any) -> str:
        if isinstance(value, (list, tuple)):
            return ", ".join(map(str, value))
        return _flatten_text(value)

    def _extract_links(self, section: Any) -> List[Tuple[str, str]]:
        if not isinstance(section, dict):
            return []
        links = section.get("links")
        if not isinstance(links, list):
            return []
        result: List[Tuple[str, str]] = []
        for entry in links:
            if not isinstance(entry, dict):
                continue
            url = entry.get("url")
            name = entry.get("name") or entry.get("title") or url
            if url and name:
                result.append((str(name), str(url)))
        return result


# ---------------------------------------------------------------------------
# Public writer API
# ---------------------------------------------------------------------------


class MkdocsWriter:
    """Generate MkDocs artefacts from raw benchmark entries."""

    def __init__(
        self,
        benchmarks: Iterable[Dict[str, Any]] | None,
        *,
        use_directory_urls: bool = True,
    ):
        self.use_directory_urls = use_directory_urls
        self.entries: List[BenchmarkEntry] = []
        if benchmarks:
            for raw in benchmarks:
                try:
                    self.entries.append(BenchmarkEntry(raw))
                except Exception as exc:  # pragma: no cover - defensive
                    raise ValueError(f"Invalid benchmark entry: {exc}") from exc

    # ------------------------------------------------------------------ writers

    def write_individual_entries(
        self,
        output_dir: str = "content/md/benchmarks",
        columns: Iterable[str] = DEFAULT_COLUMNS,
        author_trunc: int | None = None,  # kept for API parity
        average_ratings: bool = True,
        *,
        filters_js_src: str | None = None,
    ) -> None:
        """
        Write ``cards.md`` and one detail page per benchmark.

        ``filters_js_src`` may point to the runtime script if the theme does not
        already include ``assets/js/filters.js``.
        """

        valid_columns = _validate_columns(list(columns))
        os.makedirs(output_dir, exist_ok=True)

        card_lines: List[str] = [INDEX_HEADER_TEMPLATE]

        for entry in self.entries:
            detail_html, ratings_average = entry.render_detail(
                valid_columns,
                average_ratings=average_ratings,
                use_directory_urls=self.use_directory_urls,
            )
            write_to_file(
                content=detail_html,
                filename=os.path.join(output_dir, f"{entry.id}.md"),
            )
            card_lines.append(entry.card_html(ratings_average, self.use_directory_urls))

        card_lines.append(self._index_footer(filters_js_src))
        write_to_file(
            content="".join(card_lines),
            filename=os.path.join(output_dir, "cards.md"),
        )

    def write_table(
        self,
        filename: str = "content/md/benchmarks_table.md",
        columns: Iterable[str] = DEFAULT_COLUMNS,
        average_ratings: bool = True,
    ) -> None:
        """Emit the static table shell consumed by ``benchmarks-table.js``."""
        _validate_columns(list(columns))
        contents = (
            "# Benchmarks Table\n\n"
            '<table id="benchmarksTable" class="display nowrap" style="width:100%"></table>\n'
        )
        write_to_file(content=contents, filename=filename)

    def write_index_md(
        self,
        output_dir: str = "content/md/benchmarks",
        *,
        title: str = "Index of Benchmarks",
        detail_base: str = ".",
        sort_by: str = "name",
    ) -> None:
        """Create a minimal Markdown index linking every detail page."""
        os.makedirs(output_dir, exist_ok=True)
        items: List[Tuple[str, str]] = [(entry.id, entry.name) for entry in self.entries]
        if sort_by in {"name", "id"}:
            idx = 1 if sort_by == "name" else 0
            items.sort(key=lambda item: (item[idx] or "").lower())

        lines: List[str] = [f"# {title}\n", "\n"]
        for entry_id, name in items:
            href = os.path.normpath(f"{detail_base}/{entry_id}").replace("\\", "/") + ".md"
            lines.append(f"- [{name}]({href})\n")

        write_to_file(
            content="".join(lines),
            filename=os.path.join(output_dir, "index.md"),
        )

    # ------------------------------------------------------------------ helpers

    def _index_footer(self, filters_js_src: str | None) -> HTML:
        script = (
            f'\n<script src="{_esc(filters_js_src)}"></script>\n' if filters_js_src else ""
        )
        return INDEX_FOOTER_TEMPLATE.format(script=script)
