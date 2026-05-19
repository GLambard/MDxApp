"""Validate and sanitize evidence references from LLM output."""

import re
from typing import List, Optional
from urllib.parse import urlparse

from ..core.ai_client import EvidenceItem

_VALID_URL = re.compile(r"^https?://", re.I)
_BLOCKED_HOSTS = frozenset({"example.com", "localhost", "127.0.0.1"})


def _normalize_pmid(pmid: Optional[str]) -> Optional[str]:
    if not pmid:
        return None
    digits = re.sub(r"\D", "", pmid.strip())
    return digits if 7 <= len(digits) <= 8 else None


def _pubmed_url(pmid: str) -> str:
    return f"https://pubmed.ncbi.nlm.nih.gov/{pmid}/"


def _normalize_pubmed_url(url: str) -> Optional[str]:
    """Map pubmed.ncbi.nlm.nih.gov paths to a canonical article URL."""
    parsed = urlparse(url.strip())
    host = (parsed.netloc or "").lower()
    if "pubmed.ncbi.nlm.nih.gov" not in host and "ncbi.nlm.nih.gov" not in host:
        return url.strip()
    match = re.search(r"/(\d{7,8})/?", parsed.path)
    if match:
        return _pubmed_url(match.group(1))
    return url.strip()


def _is_safe_url(url: str) -> bool:
    parsed = urlparse(url.strip())
    if parsed.scheme not in ("http", "https"):
        return False
    host = (parsed.netloc or "").lower().split(":")[0]
    if not host or host in _BLOCKED_HOSTS:
        return False
    return True


def resolve_evidence_link(item: EvidenceItem) -> Optional[str]:
    """Best link for UI/PDF: sanitized URL or PubMed from PMID."""
    if item.url and _VALID_URL.match(item.url) and _is_safe_url(item.url):
        return item.url
    pmid = _normalize_pmid(item.pmid)
    if pmid:
        return _pubmed_url(pmid)
    return None


def sanitize_evidence_items(items: List[EvidenceItem]) -> List[EvidenceItem]:
    """Drop invalid entries; normalize PubMed links; deduplicate."""
    cleaned: List[EvidenceItem] = []
    seen: set[str] = set()

    for item in items:
        title = (item.title or "").strip()
        if not title:
            continue

        source = (item.source or "Reference").strip()[:200]
        pmid = _normalize_pmid(item.pmid)
        url = item.url.strip() if item.url else None

        if url and _VALID_URL.match(url) and _is_safe_url(url):
            url = _normalize_pubmed_url(url)
        else:
            url = None

        if pmid and not url:
            url = _pubmed_url(pmid)

        # Recover PMID embedded in a bad URL path
        if not pmid and url:
            match = re.search(r"/(\d{7,8})/?", urlparse(url).path)
            if match:
                pmid = match.group(1)

        dedupe_key = url or (f"pmid:{pmid}" if pmid else f"title:{title.lower()}")
        if dedupe_key in seen:
            continue
        seen.add(dedupe_key)

        cleaned.append(
            EvidenceItem(
                title=title[:500],
                source=source,
                url=url,
                pmid=pmid,
            )
        )

    return cleaned[:6]
