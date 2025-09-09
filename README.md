# Deep Research Agent

A modular, multi-step research agent powered by [LangGraph](https://github.com/langchain-ai/langgraph), [Groq LLMs](https://groq.com/), and [MCP Tools](https://github.com/modelcontextprotocol/servers?tab=readme-ov-file).  
It breaks down complex queries, pulls from academic sources like Arxiv and Semantic Scholar, and returns structured, citation-rich research reports.


## What it does

This agent automates deep academic research:

1. **Breaks down** user topic into focused sub-queries.
2. **Searches** academic tools (Arxiv + Academic Search).
3. **Extracts** and **ranks** relevant content.
4. **Writes** a clean research report with citations (title and url).

---

## Project Structure

deepresearch/
│
├── .venv/ # Virtual environment
├── pycache/ # Python cache files
├── arxiv_storage/ # Stores downloaded Arxiv PDFs
│
├── main.py # CLI entry point
├── graph_builder.py # Builds LangGraph state machine
├── agent_state.py # Shared state types
├── utils.py # Reusable helper functions
│
├── nodes/ # Agent steps (LangGraph nodes)
│ ├── plan.py # Subquery generation
│ ├── search.py # Arxiv + Academic Search
│ ├── extract.py # Content extraction
│ ├── rank.py # Passage filtering
│ └── write.py # Report generation
│
├── .env.example # Template for environment variables
├── .gitignore # Files to ignore in version control
├── browser_mcp.json # MCP config file (update with your path)
├── .env # Your actual API key (not committed)
├── requirements.txt # Python dependencies


## Setup Instructions

### 1. Clone the repo

git clone https://github.com/moona7/deepresearch.git
cd deepresearch
### 2. Create your .env file
Add a .env file and copy your needed API keys:

for example:
GROQ_API_KEY="123jdndhd875"

### 3. Install dependencies
Make sure you're using Python 3.10+.

pip install -r requirements.txt

### 4. Set up MCP tools
Install and run the following separately:

arxiv-mcp-server- https://github.com/blazickjp/arxiv-mcp-server

academic-search- https://github.com/afrise/academic-search-mcp-server

playwright- https://github.com/executeautomation/mcp-playwright

Ensure your browser_mcp.json file is updated and pointed to the correct local ports.

## Run the Agent

python main.py
You'll be prompted to enter a research topic.
The agent will output a structured report with inline citations and source links.

- Example Output

=== Welcome to Deep Research Agent ===
Type a topic to research. Type 'exit' to quit.

You: effects of microplastics on human health
Searching Arxiv: ...
Searching Semantic Scholar: ...
Extracting content...
Ranking passages...
Writing report...

[Generated research report appears here]

## TODO

 Add PDF export of final report


## License
MIT — free for personal and academic use.

## Credits
LangGraph

LangChain

Groq

MCP Tools
