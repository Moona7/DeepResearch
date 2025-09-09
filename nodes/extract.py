"""
pull readable content / metadata for each search hit.
"""

from typing import List, Dict, Any, Optional
from agent_state import ResearchState, EvidenceItem, MAX_PAGES_TO_EXTRACT
from mcp_use import MCPClient

async def extract_content(state: ResearchState, mcp_client: MCPClient) -> ResearchState:
    extracted: List[EvidenceItem] = []

    arxiv = mcp_client.get_session("arxiv-mcp-server")
    academic = mcp_client.get_session("academic-search")
    playwright = mcp_client.get_session("playwright")

    async def _extract_one(result: Dict[str, Any]) -> Optional[EvidenceItem]:
        url = result.get("url") or result.get("pdf_url")
        if not url:
            return None

        src = result.get("source_type")

        if src == "arxiv" and result.get("arxiv_id"):
            try:
                await arxiv.call_tool("download_paper", {"paper_id": result["arxiv_id"]})
                resp = await arxiv.call_tool("read_paper", {"paper_id": result["arxiv_id"]})
                text = getattr(resp, "output", "") or getattr(resp, "content", "")
                return EvidenceItem(
                    url=url,
                    title=result.get("title", ""),
                    snippet=result.get("snippet", ""),
                    content=text,
                    source_type="arxiv",
                    arxiv_id=result.get("arxiv_id", ""),
                    pdf_url=result.get("pdf_url", "")
                )
            except Exception as e:
                print(f"Arxiv extraction failed for {url}: {e}")

        elif src == "academic" and result.get("url"):
            try:
                resp = await academic.call_tool("fetch_paper_details", {"paper_id": result.get("url")})
                text = getattr(resp, "output", "") or getattr(resp, "content", "")
                return EvidenceItem(
                    url=url,
                    title=result.get("title", ""),
                    snippet=result.get("snippet", ""),
                    content=text,
                    source_type="academic"
                )
            except Exception as e:
                print(f"Academic extraction failed for {url}: {e}")

        else:
            # Last-ditch: navigate (no scraping here—just showing intent).
            try:
                await playwright.call_tool("browser_navigate", {"url": url})
            except Exception as e:
                print(f"Playwright fallback failed for {url}: {e}")

        return None

    for r in state["search_results"][:MAX_PAGES_TO_EXTRACT]:
        item = await _extract_one(r)
        if item:
            extracted.append(item)

    return {**state, "evidence_passages": extracted}
