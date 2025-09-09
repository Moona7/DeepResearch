"""
write a structured report using ONLY the provided context text.
"""

from langchain_groq import ChatGroq
from agent_state import ResearchState

async def write_final_report(state: ResearchState, llm: ChatGroq) -> ResearchState:
    if not state["evidence_passages"]:
        return {**state, "final_report": "I couldn't retrieve enough reliable text. Try refining the topic."}

    blocks = []
    for i, ev in enumerate(state["evidence_passages"], 1):
        source = ev.get("arxiv_id") or ev.get("url")
        title = ev.get("title") or "(untitled)"
        preview = ev.get("content", "")[:1600]
        blocks.append(f"[{i}] {title} — {source}\n{preview}")

    context = "\n\n".join(blocks)

    prompt = f"""You are an excellent research writer. Using ONLY the CONTEXT, write a clear, well-structured report on the TOPIC.
- Start with a 5-7 sentence summary.
- Then well detailed and thought out sections: Background, Key Findings, Evidence & Citations, Limitations, Practical Implications.
- Use inline numeric citations like [1], [2].
- End with a Sources section listing [n] Title — URL.

TOPIC: {state['query']}

CONTEXT:
{context}
"""
    resp = await llm.ainvoke(prompt)
    return {**state, "final_report": resp.content}
