# Task AI Service

Python AI agent that provides natural language interface for the Task Management API.

## Tech Stack

- Python 3.13
- LangChain + LangGraph
- OpenAI GPT-4o-mini
- ChromaDB (Semantic Search / RAG)

## Features

- Natural language task management
- Semantic search over tasks using RAG
- Connects to Spring Boot Task Management API

## Example Commands

"Create a task called Review project proposal with HIGH priority due 2026-06-15"
"Show me all my tasks"
"Mark task 5 as IN_PROGRESS"
"Find tasks related to client work"
"Delete task 4"

## How It Works

User prompt → LangChain Agent → decides which tool to call → hits Spring Boot API → returns natural response

For semantic search, ChromaDB stores task embeddings and retrieves similar tasks based on meaning, not just keywords.

## Setup

1. Clone the repo
2. Create `.env` file:


OPENAI_API_KEY=your-key
SPRING_API_URL=http://localhost:8081
SPRING_API_TOKEN=your-jwt-token

3. Install dependencies: `uv sync`
4. Run: `uv run python main.py`

## Related

- [task-management-api](https://github.com/edwinmjose98/task-management-api) — Spring Boot backend

