# Custom YouTube AI Agent with MCP 🤖📺

An autonomous AI agent built using Python, OpenAI, and the **Model Context Protocol (MCP)**. This project demonstrates how to build a **Custom MCP Server** from scratch that interacts with YouTube transcripts and custom prompt instructions.

## Architecture 🏛️
- **MCP Server (`youtube_mcp_server.py`):** A custom local server using `FastMCP` that provides tools to fetch YouTube transcripts and specific task instructions.
- **MCP Client/Agent (`agent.py`):** An OpenAI-powered agent that connects to the local server via Standard I/O (`MCPServerStdio`) to execute tasks dynamically.

## Features ✨
- Custom tool creation using `@mcp.tool()`.
- Automated extraction of YouTube video transcripts and timestamps.
- Modular prompt instructions for specific tasks (e.g., generating video chapters).

## Setup & Installation 🛠️

1. Clone the repository:
   ```bash
   git clone [https://github.com/YourUsername/YouTube-MCP-Agent.git](https://github.com/YourUsername/YouTube-MCP-Agent.git)
   cd YouTube-MCP-Agent