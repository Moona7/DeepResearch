
from langchain_groq import ChatGroq
from agent_state import ResearchState

async def generate_subqueries(state: ResearchState, llm: ChatGroq) -> ResearchState:
    topic = state["query"].strip()

    prompt = f"""
You are a research assistant. 
Rewrite the following topic into exactly 3 focused search queries. 

Rules:
- Output only the 3 queries, nothing else. 
- Put each query on its own line.
- Do not explain your reasoning.

Topic: {topic}
"""
    resp = await llm.ainvoke(prompt)

    # Clean bullet chars and blank lines
    lines = [ln.strip("-• ").strip() for ln in resp.content.splitlines() if ln.strip()]

    return {**state, "subqueries": lines[:3]}
