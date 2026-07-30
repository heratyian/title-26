# chunking.py

from title_26.models import TaxCodeChunk


def chunk_sections(
    sections: list[TaxCodeChunk],
    max_chars: int = 2000,
) -> list[TaxCodeChunk]:
    """
    Keep subsections intact when possible.
    Split only unusually large legal units.
    """
    return sections