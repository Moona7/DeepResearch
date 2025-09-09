

from langgraph.graph import StateGraph, END
from langchain_groq import ChatGroq
from mcp_use import MCPClient

from agent_state import ResearchState
from nodes.plan import generate_subqueries
from nodes.search import perform_search
from nodes.extract import extract_content
from nodes.rank import rank_passages
from nodes.write import write_final_report

def build_graph(client: MCPClient, llm: ChatGroq):
    graph = StateGraph(ResearchState)

    async def plan_node(state: ResearchState) -> ResearchState:
        return await generate_subqueries(state, llm)

    async def search_node(state: ResearchState) -> ResearchState:
        return await perform_search(state, client)

    async def extract_node(state: ResearchState) -> ResearchState:
        return await extract_content(state, client)

    async def rank_node(state: ResearchState) -> ResearchState:
        return await rank_passages(state, llm)

    async def write_node(state: ResearchState) -> ResearchState:
        return await write_final_report(state, llm)

    graph.add_node("plan", plan_node)
    graph.add_node("search", search_node)
    graph.add_node("extract", extract_node)
    graph.add_node("rank", rank_node)
    graph.add_node("write", write_node)

    graph.set_entry_point("plan")
    graph.add_edge("plan", "search")
    graph.add_edge("search", "extract")
    graph.add_edge("extract", "rank")
    graph.add_edge("rank", "write")
    graph.add_edge("write", END)

    return graph.compile()
