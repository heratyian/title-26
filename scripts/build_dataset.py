from __future__ import annotations

import json
import xml.etree.ElementTree as ET
from pathlib import Path


INPUT_PATH = Path("data/raw/usc26.xml")
OUTPUT_PATH = Path("data/processed/usc26.jsonl")


def clean_text(element: ET.Element | None) -> str:
    """Return normalized text from an XML element and its descendants."""
    if element is None:
        return ""

    return " ".join(
        text.strip()
        for text in element.itertext()
        if text and text.strip()
    )


def parse_sections(xml_path: Path):
    """Yield normalized records for every section in a Title 26 USLM XML file."""
    sections = ET.parse(xml_path).getroot().findall(".//{*}section")
    print(f"Sections found: {len(sections)}")

    for section in sections:
        num = section.find("{*}num")
        if num is None:
            continue

        section_number = clean_text(num).replace("§", "").strip()
        text = clean_text(section)
        if not text:
            continue

        yield {
            "title": 26,
            "section": section_number,
            "heading": clean_text(section.find("{*}heading")) or None,
            "citation": f"26 U.S.C. § {section_number}",
            "text": text,
        }


def main():
    """Build the JSONL dataset from the configured Title 26 XML file."""
    if not INPUT_PATH.exists():
        raise FileNotFoundError(
            f"Could not find {INPUT_PATH}. Put the Title 26 XML file there first."
        )

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with OUTPUT_PATH.open("w", encoding="utf-8") as output_file:
        count = 0
        for record in parse_sections(INPUT_PATH):
            output_file.write(json.dumps(record, ensure_ascii=False) + "\n")
            count += 1

    print(f"Wrote {count} records to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
