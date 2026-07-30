from dataclasses import dataclass


@dataclass
class TaxCodeChunk:
    text: str
    citation: str
    section: str
    section_title: str
    subsection: str | None = None
    chapter: str | None = None
    subchapter: str | None = None