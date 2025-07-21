#!/usr/bin/env python
"""
Get citation from DOI(s), arXiv ID(s), or various sources including IEEE, OpenAlex, CrossRef, Semantic Scholar, DBLP.

Usage:
  getbib.py [--source=<src>] [--indent=<n>] [--format=<fmt>] <identifier>...
  getbib.py (-h | --help)

Arguments:
  <identifier>    One or more DOIs (e.g. 10.1038/nphys1170), arXiv IDs (e.g. 2106.14834), or search strings (for --source search)

Options:
  --source=<src>   Source to search from [default: doi]
                   Options: doi, ieee, openalex, crossref, semanticscholar, dblp
  --indent=<n>     Number of spaces to indent the entire output [default: 0]
  --format=<fmt>   Output format [default: bibtex]
                   Options: bibtex, ris, yaml, json, txt, tx
  -h --help        Show this help message.
"""

from docopt import docopt
import requests
import re
import sys
from bs4 import BeautifulSoup
import bibtexparser
import yaml
import json

def pretty_print_bibtex(bibtex_str, indent_spaces=4):
    try:
        bib_db = bibtexparser.loads(bibtex_str)
        writer = bibtexparser.bwriter.BibTexWriter()
        writer.indent = '    '
        writer.comma_first = False
        writer.align_values = True
        pretty_str = writer.write(bib_db).strip()

        if indent_spaces > 0:
            indent_prefix = ' ' * indent_spaces
            indented_lines = [(indent_prefix + line) if line.strip() else line for line in pretty_str.splitlines()]
            return '\n'.join(indented_lines)
        else:
            return pretty_str
    except Exception:
        if indent_spaces > 0:
            indent_prefix = ' ' * indent_spaces
            indented_lines = [(indent_prefix + line) if line.strip() else line for line in bibtex_str.splitlines()]
            return '\n'.join(indented_lines).strip()
        else:
            return bibtex_str.strip()

def bibtex_to_dict(bibtex_str):
    try:
        bib_db = bibtexparser.loads(bibtex_str)
        return bib_db.entries
    except Exception:
        return []

def dict_to_ris(entries):
    if not entries:
        return ""
    e = entries[0]
    ris_lines = []
    tag_map = {
        'author': 'AU',
        'title': 'TI',
        'journal': 'JO',
        'year': 'PY',
        'volume': 'VL',
        'number': 'IS',
        'pages': 'SP',
        'doi': 'DO',
        'url': 'UR',
        'publisher': 'PB',
        'abstract': 'AB',
    }
    ris_lines.append("TY  - JOUR")
    for k, v in e.items():
        tag = tag_map.get(k.lower())
        if tag and v:
            if tag == 'AU':
                authors = re.split(r'\s+and\s+', v)
                for author in authors:
                    ris_lines.append(f"{tag}  - {author}")
            else:
                ris_lines.append(f"{tag}  - {v}")
    ris_lines.append("ER  - ")
    return '\n'.join(ris_lines)

def dict_to_attributes(entries):
    if not entries:
        return ""
    e = entries[0]
    lines = [f"{k}: {v}" for k, v in e.items()]
    return '\n'.join(lines)

def dict_to_str(entries):
    if not entries:
        return ""
    e = entries[0]

    natbib_order = [
        'author', 'title', 'journal', 'booktitle', 'year',
        'volume', 'number', 'pages', 'doi', 'url', 'publisher', 'editor'
    ]

    values = []
    for attr in natbib_order:
        if attr in e and e[attr].strip():
            val = str(e[attr]).replace('\n', ' ').strip()
            if attr == 'author':
                val = val.rstrip('.') + '.'  # author ends with period
                values.append(val)
            elif attr == 'volume':
                values.append(f"vol. {val}")
            elif attr == 'number':
                values.append(f"no. {val}")
            elif attr == 'pages':
                values.append(f"pages {val}")
            else:
                values.append(val)

    # Add any other keys not in natbib_order
    other_keys = [k for k in e.keys() if k not in natbib_order]
    for k in other_keys:
        if e[k].strip():
            values.append(str(e[k]).replace('\n', ' ').strip())

    # Join author with period, rest separated by commas with space
    if values:
        author_part = values[0]
        rest = values[1:]
        if rest:
            return author_part + " " + ", ".join(rest)
        else:
            return author_part
    return ""



def indent_text(text, indent_spaces):
    if indent_spaces > 0:
        indent_prefix = ' ' * indent_spaces
        indented_lines = [(indent_prefix + line) if line.strip() else line for line in text.splitlines()]
        return '\n'.join(indented_lines)
    else:
        return text

def get_bibtex_from_doi(doi):
    doi = doi.replace("doi:", "")
    url = f"https://doi.org/{doi}"
    headers = {"Accept": "application/x-bibtex"}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.text.strip()
    else:
        raise Exception(f"Failed to fetch BibTeX from DOI ({response.status_code}): {doi}")

def get_bibtex_from_arxiv(arxiv_id_or_url):
    match = re.search(r'(\d{4}\.\d{4,5})(v\d+)?', arxiv_id_or_url)
    if not match:
        raise ValueError(f"Invalid arXiv ID or URL: {arxiv_id_or_url}")
    arxiv_id = match.group(1)
    url = f"https://arxiv.org/bibtex/{arxiv_id}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.text.strip()
    else:
        raise Exception(f"Failed to fetch BibTeX from arXiv ({response.status_code}): {arxiv_id}")

def get_bibtex_from_ieee(query):
    search_url = f"https://ieeexplore.ieee.org/search/searchresult.jsp?newsearch=true&queryText={requests.utils.quote(query)}"
    headers = {"User-Agent": "Mozilla/5.0"}
    search_page = requests.get(search_url, headers=headers)
    if search_page.status_code != 200:
        raise Exception("Failed to fetch search results from IEEE Xplore")
    soup = BeautifulSoup(search_page.text, 'html.parser')
    scripts = soup.find_all("script")
    for script in scripts:
        if 'global.document.metadata' in script.text:
            match = re.search(r'documentId":"(\d+)"', script.text)
            if match:
                doc_id = match.group(1)
                bibtex_url = f"https://ieeexplore.ieee.org/document/{doc_id}/citations?citations-format=citation&download-format=bibtex"
                bib_response = requests.get(bibtex_url, headers=headers)
                if bib_response.status_code == 200:
                    return bib_response.text.strip()
                else:
                    raise Exception("Found document but failed to fetch BibTeX")
    raise Exception("Could not find a valid IEEE document in search results")

def get_bibtex_from_openalex(query):
    url = f"https://api.openalex.org/works?filter=title.search:{requests.utils.quote(query)}"
    r = requests.get(url)
    if r.status_code != 200:
        raise Exception(f"OpenAlex request failed with status {r.status_code}")
    data = r.json()
    results = data.get('results', [])
    if not results:
        raise Exception("No results found on OpenAlex")
    work = results[0]
    doi = work.get('doi')
    if not doi:
        raise Exception("No DOI found in OpenAlex result")
    return get_bibtex_from_doi(doi)

def get_bibtex_from_crossref(query):
    url = f"https://api.crossref.org/works?query.title={requests.utils.quote(query)}"
    r = requests.get(url)
    if r.status_code != 200:
        raise Exception(f"CrossRef request failed with status {r.status_code}")
    data = r.json()
    items = data.get('message', {}).get('items', [])
    if not items:
        raise Exception("No results found on CrossRef")
    doi = items[0].get('DOI')
    if not doi:
        raise Exception("No DOI found in CrossRef result")
    return get_bibtex_from_doi(doi)

def get_bibtex_from_semanticscholar(query):
    url = f"https://api.semanticscholar.org/graph/v1/paper/search?query={requests.utils.quote(query)}&limit=1&fields=title,authors,year,venue,externalIds"
    r = requests.get(url)
    if r.status_code != 200:
        raise Exception(f"Semantic Scholar request failed with status {r.status_code}")
    data = r.json()
    papers = data.get('data', [])
    if not papers:
        raise Exception("No results found on Semantic Scholar")
    paper = papers[0]
    external_ids = paper.get('externalIds', {})
    doi = external_ids.get('DOI')
    if not doi:
        raise Exception("No DOI found in Semantic Scholar result")
    return get_bibtex_from_doi(doi)

def get_bibtex_from_dblp(query):
    url = f"https://dblp.org/search/publ/api?q={requests.utils.quote(query)}&format=json"
    r = requests.get(url)
    if r.status_code != 200:
        raise Exception(f"DBLP request failed with status {r.status_code}")
    data = r.json()
    hits = data.get('result', {}).get('hits', {}).get('hit', [])
    if not hits:
        raise Exception("No results found on DBLP")
    info = hits[0].get('info', {})
    key = info.get('key')
    if not key:
        raise Exception("No key found for DBLP result")
    bib_url = f"https://dblp.org/rec/{key}.bib"
    bib_r = requests.get(bib_url)
    if bib_r.status_code != 200:
        raise Exception("Failed to fetch BibTeX from DBLP")
    return bib_r.text.strip()

def fetch_bibtex(identifier, source='doi'):
    identifier = identifier.strip()
    source = source.lower()
    if source == 'ieee':
        return get_bibtex_from_ieee(identifier)
    elif source == 'openalex':
        return get_bibtex_from_openalex(identifier)
    elif source == 'crossref':
        return get_bibtex_from_crossref(identifier)
    elif source == 'semanticscholar':
        return get_bibtex_from_semanticscholar(identifier)
    elif source == 'dblp':
        return get_bibtex_from_dblp(identifier)
    else:
        # Default tries arXiv if it looks like arxiv ID else DOI
        if "arxiv" in identifier or re.match(r'^\d{4}\.\d{4,5}(v\d+)?$', identifier):
            return get_bibtex_from_arxiv(identifier)
        else:
            return get_bibtex_from_doi(identifier)

def convert_and_print(bibtex_str, fmt='bibtex', indent=4):
    fmt = fmt.lower()
    entries = bibtex_to_dict(bibtex_str)
    if fmt == 'bibtex':
        output = pretty_print_bibtex(bibtex_str, indent_spaces=indent)
    elif fmt == 'ris':
        ris_str = dict_to_ris(entries)
        output = indent_text(ris_str, indent)
    elif fmt == 'yaml':
        yml = yaml.dump(entries, sort_keys=False, allow_unicode=True)
        output = indent_text(yml, indent)
    elif fmt == 'json':
        if indent > 0:
            indent=2
            output = json.dumps(entries, indent=indent, ensure_ascii=False)
        else:
            output = json.dumps(entries, separators=(',', ':'), ensure_ascii=False)
        # No extra indent for JSON since handled above
    elif fmt == 'attributes':
        # Attribute names only
        attr_str = dict_to_attributes(entries)
        output = indent_text(attr_str, indent)
    elif fmt == 'str':
        # Values comma separated single line
        tx_str = dict_to_str(entries)
        output = indent_text(tx_str, indent)
    else:
        raise Exception(f"Unsupported output format: {fmt}")

    print(output + "\n")

def main():
    args = docopt(__doc__)
    identifiers = args['<identifier>']
    source = args['--source']
    indent = int(args['--indent'])
    fmt = args['--format']


    for ident in identifiers:
        try:
            bibtex = fetch_bibtex(ident, source=source)
            convert_and_print(bibtex, fmt=fmt, indent=indent)
        except Exception as e:
            print(f"Error for '{ident}': {e}", file=sys.stderr)

if __name__ == '__main__':
    main()
