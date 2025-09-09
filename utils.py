from typing import List, Dict, Any
from agent_state import ACADEMIC_KEYWORDS

def is_academic_topic(user_query: str) -> bool:
    """Return True if the query smells like 'academic' based on simple keywords."""
    return any(keyword in user_query.lower() for keyword in ACADEMIC_KEYWORDS)

def remove_duplicate_urls(items: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Deduplicate by URL or pdf_url (first seen wins)."""
    seen = set()
    unique = []
    for r in items:
        url = r.get("url") or r.get("pdf_url") or ""
        if url and url not in seen:
            seen.add(url)
            unique.append(r)
    return unique
