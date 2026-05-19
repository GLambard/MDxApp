"""Validate and sanitize evidence references from LLM output."""

import re
from typing import List
from urllib.parse import urlparse

from ..core.ai_client import EvidenceItem

_VALID_URL = re.compile(r"^https?://", re.I)


def sanitize_evidence_items(items: List[EvidenceItem]) -> List[EvidenceItem]:
    """Drop invalid URLs; normalize PubMed links."""
    cleaned: List[EvidenceItem] = []
    for item in items:
        url = item.url
        if url and not _VALID_URL.match(url.strip()):
            url = None
        elif url:
            parsed = urlparse(url.strip())
            if not parsed.netloc:
                url = None
        pmid = item.pmid.strip() if item.pmid else None
        if pmid and pmid.isdigit() and not url:
            url = f"https://pubmed.ncbi.nlm.nih.gov/{pmid}/"
        cleaned.append(
            EvidenceItem(
                title=item.title[:500],
                source=item.source[:200],
                url=url,
                pmid=pmid if pmid and pmid.isdigit() else None,
            )
        )
    return cleaned
