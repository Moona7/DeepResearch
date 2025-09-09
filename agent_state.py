from typing import TypedDict, List, Dict, Any

# What a single extracted evidence item looks like.
class EvidenceItem(TypedDict, total=False):
    url: str
    title: str
    snippet: str
    content: str
    source_type: str
    arxiv_id: str
    pdf_url: str

# The state object that flows through the graph from node to node.
class ResearchState(TypedDict):
    query: str                    # User's original topic
    subqueries: List[str]         # 3 focused queries derived by the LLM
    search_results: List[Dict[str, Any]]  # Raw hits from search tools
    evidence_passages: List[EvidenceItem] # Parsed/cleaned readable evidence
    final_report: str             # The final write-up

# Tunables for the whole app.
MAX_SEARCH_RESULTS = 8
MAX_PAGES_TO_EXTRACT = 10
MINIMUM_TEXT_LENGTH = 500

# Heuristic keywords (kept to preserve behavior).
ACADEMIC_KEYWORDS = (
    "study", "paper", "preprint", "arxiv",
    "survey", "method", "dataset", "benchmark", "research"
)
