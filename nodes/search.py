"""
run searches against arXiv + academic sources via MCP tools,
normalize results, and de-duplicate them.

"""

import json
from typing import List, Dict, Any
from agent_state import ResearchState, MAX_SEARCH_RESULTS
from utils import remove_duplicate_urls, is_academic_topic
from mcp_use import MCPClient  # reuse your existing client wrapper

def _parse_academic_textblock(text: str) -> List[Dict[str, str]]:
    """Turn a block of 'Title:/DOI:/Authors:' lines into dicts."""
    entries: List[Dict[str, str]] = []
    chunks = text.strip().split("\n\n")
    for chunk in chunks:
        lines = chunk.strip().split("\n")
        item: Dict[str, str] = {}
        for line in lines:
            if line.startswith("Title:"):
                item["title"] = line.replace("Title:", "").strip()
            elif line.startswith("DOI:"):
                item["url"] = "https://doi.org/" + line.replace("DOI:", "").strip()
            elif line.startswith("Authors:"):
                item["snippet"] = "Authors: " + line.replace("Authors:", "").strip()
        if item:
            entries.append(item)
    return entries

def _normalize_items(response: Any) -> List[Dict[str, Any]]:
    """
    Make tool responses consistent:
    - {'papers': [...]} → [...]
    - [TextContent(text='{"papers": ...}')] → [...]
    - already a list of dicts → keep it
    """
    raw = getattr(response, "output", None) or getattr(response, "content", None)

    # Special case: single TextContent with JSON payload
    if isinstance(raw, list) and len(raw) == 1 and hasattr(raw[0], "text"):
        try:
            raw = json.loads(raw[0].text)
        except Exception as e:
            print("Failed to parse Arxiv JSON:", e)
            return []

    if isinstance(raw, dict) and "papers" in raw:
        return raw["papers"]

    if isinstance(raw, list) and all(isinstance(x, dict) for x in raw):
        return raw

    return []

async def perform_search(state: ResearchState, mcp_client: MCPClient) -> ResearchState:
    results: List[Dict[str, Any]] = []
    prioritize_arxiv = is_academic_topic(state["query"])

    # Tool sessions
    arxiv = mcp_client.get_session("arxiv-mcp-server")
    academic = mcp_client.get_session("academic-search")

    async def search_arxiv(q: str):
        try:
            print(f"Searching Arxiv: {q}")
            resp = await arxiv.call_tool(
                name="search_papers",
                arguments={"query": q, "max_results": MAX_SEARCH_RESULTS, "date_from": "2023-01-01"}
            )
            items = _normalize_items(resp)
            print(f"{len(items)} normalized results from Arxiv")
            for it in items:
                results.append({
                    "title": it.get("title", ""),
                    "url": it.get("url_abs") or it.get("url", ""),
                    "pdf_url": it.get("url_pdf", ""),
                    "arxiv_id": it.get("arxiv_id", ""),
                    "snippet": it.get("summary", ""),
                    "source_type": "arxiv",
                })
        except Exception as e:
            print(f"Arxiv error: {e}")

    async def search_academic(q: str):
        try:
            print(f"Searching Academic: {q}")
            resp = await academic.call_tool(
                name="search_papers",
                arguments={"query": q, "max_results": MAX_SEARCH_RESULTS}
            )
            if isinstance(resp.content, list):
                block = resp.content[0].text if hasattr(resp.content[0], "text") else str(resp.content[0])
                items = _parse_academic_textblock(block)
            else:
                items = []
            print(f"{len(items)} normalized results from Academic")
            for it in items:
                results.append({
                    "title": it.get("title", ""),
                    "url": it.get("url", ""),
                    "snippet": it.get("snippet", ""),
                    "source_type": "academic",
                })
        except Exception as e:
            print(f"Academic search error: {e}")

    # Run searches for each subquery in a chosen order
    for q in state["subqueries"]:
        if prioritize_arxiv:
            await search_arxiv(q)
            await search_academic(q)
        else:
            await search_academic(q)
            await search_arxiv(q)

    return {**state, "search_results": remove_duplicate_urls(results)}
