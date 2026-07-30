from __future__ import annotations

import json
import xml.etree.ElementTree as ET
from pathlib import Path


INPUT_PATH = Path("data/raw/usc26.xml")
OUTPUT_PATH = Path("data/processed/usc26.jsonl")


def get_namespace(root: ET.Element) -> str:
    """
    Extract the namespace URI from a namespaced XML tag.

    Example:
        {http://xml.house.gov/schemas/uslm/1.0}uslm
    """
    if root.tag.startswith("{"):
        return root.tag.split("}", 1)[0][1:]

    return ""


def clean_text(element: ET.Element | None) -> str:
    """
    Convert an XML element and its children into normalized text.
    """
    if element is None:
        return ""

    return " ".join(
        text.strip()
        for text in element.itertext()
        if text and text.strip()
    )


def parse_sections(xml_path: Path):
    tree = ET.parse(xml_path)
    root = tree.getroot()

    namespace = get_namespace(root)

    if namespace:
        ns = {"uslm": namespace}
        section_path = ".//uslm:section"
        num_path = "uslm:num"
        heading_path = "uslm:heading"
    else:
        ns = {}
        section_path = ".//section"
        num_path = "num"
        heading_path = "heading"

    sections = root.findall(section_path, ns)

    print(f"Namespace: {namespace or '(none)'}")
    print(f"Sections found: {len(sections)}")

    for section in sections:
        num = section.find(num_path, ns)
        heading = section.find(heading_path, ns)

        if num is None:
            continue

        raw_number = clean_text(num)

        section_number = (
            raw_number
            .replace("§", "")
            .strip()
        )

        text = clean_text(section)

        if not text:
            continue

        yield {
            "title": 26,
            "section": section_number,
            "heading": clean_text(heading) or None,
            "citation": f"26 U.S.C. § {section_number}",
            "text": text,
        }


def main():
    if not INPUT_PATH.exists():
        raise FileNotFoundError(
            f"Could not find {INPUT_PATH}. "
            "Put the Title 26 XML file there first."
        )

    OUTPUT_PATH.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    count = 0

    with OUTPUT_PATH.open(
        "w",
        encoding="utf-8",
    ) as output_file:

        for record in parse_sections(INPUT_PATH):
            output_file.write(
                json.dumps(
                    record,
                    ensure_ascii=False,
                )
                + "\n"
            )

            count += 1

    print()
    print(
        f"Wrote {count} records to "
        f"{OUTPUT_PATH}"
    )


if __name__ == "__main__":
    main()