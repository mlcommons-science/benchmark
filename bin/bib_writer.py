import os
import re 

class BibtexWriter:
    def __init__(self, entries: list[dict]):
        self.entries = entries

    def _extract_cite_label(self, bib_entry: str) -> str:
        match = re.match(r"@\w+\{([^,]+),", bib_entry.strip())
        return match.group(1) if match else "<unknown>"

    def write(self, output_dir: str, filename: str = "benchmarks.bib") -> None:
        os.makedirs(output_dir, exist_ok=True)
        bib_entries = []
        found_labels = set()
        found_entries = set()
        found_names = set()

        for record in self.entries:
            record_cite_entries = record.get("cite", [])
            name = record.get("name", "UNKNOWN")

            if isinstance(record_cite_entries, str):
                record_cite_entries = [record_cite_entries]
            elif not isinstance(record_cite_entries, list):
                continue

            for cite_entry in record_cite_entries:
                if not isinstance(cite_entry, str) or not cite_entry.strip().startswith("@"):
                    continue

                label = self._extract_cite_label(cite_entry.lower())

                if label in found_labels:
                    print(f"{_RED}ERROR: Duplicate citation label \"{label}\" found in entry \"{name}\".{_DEFAULT_COLOR}")
                elif cite_entry in found_entries and name in found_names:
                    continue
                else:
                    found_labels.add(label)
                    found_entries.add(cite_entry)
                    found_names.add(name)
                    bib_entries.append(cite_entry.strip())

        bib_path = os.path.join(output_dir, filename)
        with open(bib_path, "w", encoding="utf-8") as f:
            f.write("\n\n".join(bib_entries))
