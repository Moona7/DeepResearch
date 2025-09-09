
import asyncio
import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq

from graph_builder import build_graph
from mcp_server import init_mcp  # or: from mcp_use import MCPClient

async def main():
    load_dotenv()
    if not os.getenv("GROQ_API_KEY"):
        raise ValueError("GROQ_API_KEY missing from .env")

    # MCP bootstrap
    config_path = "C:/Users/Muna/Desktop/AgenticAI/DeepResearch/browser_mcp.json"
    client = await init_mcp(config_path)

    # LLM
    llm = ChatGroq(model="openai/gpt-oss-20b")

    # Graph app
    app = build_graph(client, llm)

    print("\n=== Welcome to Deep Research Agent ===")
    print("Type a topic to research. Type 'exit' to quit.")
    print("=========================================\n")

    try:
        while True:
            topic = input("\nYou: ").strip()
            if topic.lower() in ("exit", "quit"):
                print("Goodbye!")
                break
            if not topic:
                continue

            state = {
                "query": topic,
                "subqueries": [],
                "search_results": [],
                "evidence_passages": [],
                "final_report": ""
            }

            result = await app.ainvoke(state)
            print("\n" + result["final_report"] + "\n")

    finally:
        # If your MCP client exposes sessions, close them politely.
        if client and getattr(client, "sessions", None):
            try:
                await client.close_all_sessions()
            except Exception as e:
                print("Warning during MCP cleanup:", e)

if __name__ == "__main__":
    asyncio.run(main())
