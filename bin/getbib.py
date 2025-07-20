#!/usr/bin/env python
"""
Get citation from DOI(s), arXiv ID(s), or various sources including IEEE, OpenAlex, CrossRef, Semantic Scholar, DBLP.

Usage:
  getbib.py [--source=<src>] [--indent=<n>] [--format=<fmt>] [--count=<n>] <identifier>...
  getbib.py (-h | --help)

Arguments:
  <identifier>    One or more DOIs (e.g. 10.1007/978-3-031-23220-6\\_4), arXiv IDs (e.g. 2310.17013), 
                  or search strings (for --source search)

Options:
  --source=<src>   Source to search from [default: doi]
                   Options: doi, ieee, openalex, crossref, semanticscholar, dblp
  --indent=<n>     Number of spaces to indent the entire output [default: 0]
  --format=<fmt>   Output format [default: bibtex]
                   Options: bibtex, ris, yaml, json, txt, tx
  --count=<n>      Number of results to return (for sources that support it) [default: 1]
  -h --help        Show this help message.

Note:
    - The ieee is not working well for multiple results, it will return the first result.

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
        return [response.text.strip()] # Return as a list for consistency
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
        return [response.text.strip()] # Return as a list for consistency
    else:
        raise Exception(f"Failed to fetch BibTeX from arXiv ({response.status_code}): {arxiv_id}")

def get_bibtex_from_ieee(query):
    # IEEE Xplore search is tricky for getting multiple results easily via simple URL changes.
    # For now, we'll stick to the first result as the existing implementation does.
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
                    return [bib_response.text.strip()] # Return as a list
                else:
                    raise Exception("Found document but failed to fetch BibTeX")
    raise Exception("Could not find a valid IEEE document in search results")

def get_bibtex_from_openalex(query, count=1):
    url = f"https://api.openalex.org/works?filter=title.search:{requests.utils.quote(query)}&per_page={count}"
    r = requests.get(url)
    if r.status_code != 200:
        raise Exception(f"OpenAlex request failed with status {r.status_code}")
    data = r.json()
    results = data.get('results', [])
    if not results:
        raise Exception("No results found on OpenAlex")

    bibtex_list = []
    for work in results:
        doi = work.get('doi')
        if doi:
            try:
                # OpenAlex provides a BibTeX link directly, which is more reliable
                # than fetching via DOI.
                bibtex_url = work.get('bibtex')
                if bibtex_url:
                    bib_response = requests.get(bibtex_url)
                    if bib_response.status_code == 200:
                        bibtex_list.append(bib_response.text.strip())
                    else:
                        print(f"Warning: Failed to fetch BibTeX from OpenAlex URL for DOI {doi} ({bib_response.status_code})", file=sys.stderr)
                else:
                    # Fallback to DOI if no direct bibtex link (less ideal)
                    bibtex_list.extend(get_bibtex_from_doi(doi))
            except Exception as e:
                print(f"Warning: Error fetching BibTeX for DOI {doi} from OpenAlex: {e}", file=sys.stderr)
    if not bibtex_list:
        raise Exception("No valid BibTeX entries found in OpenAlex results")
    return bibtex_list

def get_bibtex_from_crossref(query, count=1):
    url = f"https://api.crossref.org/works?query.title={requests.utils.quote(query)}&rows={count}"
    r = requests.get(url)
    if r.status_code != 200:
        raise Exception(f"CrossRef request failed with status {r.status_code}")
    data = r.json()
    items = data.get('message', {}).get('items', [])
    if not items:
        raise Exception("No results found on CrossRef")
    
    bibtex_list = []
    for item in items:
        doi = item.get('DOI')
        if doi:
            try:
                # CrossRef has a direct BibTeX content negotiation option
                bib_response = requests.get(f"https://doi.org/{doi}", headers={"Accept": "application/x-bibtex"})
                if bib_response.status_code == 200:
                    bibtex_list.append(bib_response.text.strip())
                else:
                    print(f"Warning: Failed to fetch BibTeX from CrossRef DOI {doi} ({bib_response.status_code})", file=sys.stderr)
            except Exception as e:
                print(f"Warning: Error fetching BibTeX for DOI {doi} from CrossRef: {e}", file=sys.stderr)
    if not bibtex_list:
        raise Exception("No valid BibTeX entries found in CrossRef results")
    return bibtex_list


def get_bibtex_from_semanticscholar(query, count=1):
    # Semantic Scholar API currently doesn't directly return BibTeX.
    # It provides external IDs including DOI. We will fetch DOI and then get BibTeX.
    # The limit parameter works for count.
    url = f"https://api.semanticscholar.org/graph/v1/paper/search?query={requests.utils.quote(query)}&limit={count}&fields=title,authors,year,venue,externalIds"
    r = requests.get(url)
    if r.status_code != 200:
        raise Exception(f"Semantic Scholar request failed with status {r.status_code}")
    data = r.json()
    papers = data.get('data', [])
    if not papers:
        raise Exception("No results found on Semantic Scholar")
    
    bibtex_list = []
    for paper in papers:
        external_ids = paper.get('externalIds', {})
        doi = external_ids.get('DOI')
        if doi:
            try:
                bibtex_list.extend(get_bibtex_from_doi(doi))
            except Exception as e:
                print(f"Warning: Error fetching BibTeX for DOI {doi} from Semantic Scholar: {e}", file=sys.stderr)
    if not bibtex_list:
        raise Exception("No valid BibTeX entries found in Semantic Scholar results")
    return bibtex_list

def get_bibtex_from_dblp(query, count=1):
    url = f"https://dblp.org/search/publ/api?q={requests.utils.quote(query)}&format=json&h={count}" # Use 'h' for hit count
    r = requests.get(url)
    if r.status_code != 200:
        raise Exception(f"DBLP request failed with status {r.status_code}")
    data = r.json()
    hits = data.get('result', {}).get('hits', {}).get('hit', [])
    if not hits:
        raise Exception("No results found on DBLP")
    
    bibtex_list = []
    for hit in hits:
        info = hit.get('info', {})
        key = info.get('key')
        if key:
            try:
                bib_url = f"https://dblp.org/rec/{key}.bib"
                bib_r = requests.get(bib_url)
                if bib_r.status_code == 200:
                    bibtex_list.append(bib_r.text.strip())
                else:
                    print(f"Warning: Failed to fetch BibTeX from DBLP for key {key} ({bib_r.status_code})", file=sys.stderr)
            except Exception as e:
                print(f"Warning: Error fetching BibTeX for DBLP key {key}: {e}", file=sys.stderr)
    
    if not bibtex_list:
        raise Exception("No valid BibTeX entries found in DBLP results")
    return bibtex_list


def fetch_bibtex(identifier, source='doi', count=1):
    identifier = identifier.strip()
    source = source.lower()
    if source == 'ieee':
        # IEEE does not directly support 'count' in a straightforward way through its search.
        # It's better to implement specific parsing for multiple results if needed.
        # For now, it will return a single result in a list.
        return get_bibtex_from_ieee(identifier)
    elif source == 'openalex':
        return get_bibtex_from_openalex(identifier, count=count)
    elif source == 'crossref':
        return get_bibtex_from_crossref(identifier, count=count)
    elif source == 'semanticscholar':
        return get_bibtex_from_semanticscholar(identifier, count=count)
    elif source == 'dblp':
        return get_bibtex_from_dblp(identifier, count=count)
    else:
        # Default tries arXiv if it looks like arxiv ID else DOI.
        # These typically return a single result.
        if "arxiv" in identifier or re.match(r'^\d{4}\.\d{4,5}(v\d+)?$', identifier):
            return get_bibtex_from_arxiv(identifier)
        else:
            return get_bibtex_from_doi(identifier)

def convert_and_print(bibtex_str, fmt='bibtex', indent=4):
    fmt = fmt.lower()
    entries = bibtex_to_dict(bibtex_str) # bibtex_str should be a single bibtex entry here

    if not entries:
        raise Exception("No valid BibTeX entry to convert.")

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
            # JSON format can handle its own indentation
            output = json.dumps(entries, indent=indent, ensure_ascii=False)
        else:
            output = json.dumps(entries, separators=(',', ':'), ensure_ascii=False)
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

    print(output)

def main():
    args = docopt(__doc__)
    identifiers = args['<identifier>']
    source = args['--source']
    indent = int(args['--indent'])
    fmt = args['--format']
    count = int(args['--count'])

    for ident in identifiers:
        try:
            # fetch_bibtex now returns a list of BibTeX strings
            bibtex_results = fetch_bibtex(ident, source=source, count=count)
            for i, bibtex_entry in enumerate(bibtex_results):
                if len(bibtex_results) > 1:
                    print(f"# Result {i+1} for '{ident}'\n")
                convert_and_print(bibtex_entry, fmt=fmt, indent=indent)
                if len(bibtex_results) > 1 and i < len(bibtex_results) - 1:
                    print() # Add a newline between multiple results
            print() # Add a newline after processing all results for an identifier
        except Exception as e:
            print(f"Error for '{ident}': {e}", file=sys.stderr)

if __name__ == '__main__':
    main()