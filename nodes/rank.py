"""
show preview of evidence passages to the LLM, ask it to pick the 6–8 best.
"""

from langchain_groq import ChatGroq
from agent_state import ResearchState

async def rank_passages(state: ResearchState, llm: ChatGroq) -> ResearchState:
    if not state["evidence_passages"]:
        return state

    # Build a numbered list the LLM can scan quickly.
    items = []
    for i, ev in enumerate(state["evidence_passages"], 1):
        snippet = ev.get("content", "")[:700]
        items.append(f"[{i}] {ev.get('title') or ev.get('url')} :: {snippet}")

    prompt = f"""Select the 6-8 most relevant items to the query. Return ONLY a list of indices like: 1,3,4,7
Query: {state['query']}

Items:
{chr(10).join(items)}"""

    resp = await llm.ainvoke(prompt)
    indices = [int(n) for n in resp.content if n.isdigit()]

    chosen = [state["evidence_passages"][i - 1] for i in indices if 1 <= i <= len(state["evidence_passages"])]
    return {**state, "evidence_passages": chosen or state["evidence_passages"][:8]}
