import os
import requests
from dotenv import load_dotenv
from langchain.tools import tool
from langgraph.prebuilt import create_react_agent
# from langchain_groq import ChatGroq
# from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_openai import ChatOpenAI
from rag import sync_tasks_to_chroma, search_tasks

load_dotenv()

SPRING_API_URL = os.getenv("SPRING_API_URL")
SPRING_API_TOKEN = os.getenv("SPRING_API_TOKEN")

headers = {
    "Authorization": f"Bearer {SPRING_API_TOKEN}",
    "Content-Type": "application/json"
}

@tool
def create_task(title: str, description: str, priority: str, due_date: str) -> str:
    """Create a new task with title, description, priority (LOW/MEDIUM/HIGH) and due_date (YYYY-MM-DD)"""
    response = requests.post(f"{SPRING_API_URL}/api/tasks", json={
        "title": title,
        "description": description,
        "priority": priority,
        "dueDate": due_date
    }, headers=headers)
    return response.json()

@tool
def get_tasks() -> str:
    """Get all tasks for the current user"""
    response = requests.get(f"{SPRING_API_URL}/api/tasks", headers=headers)
    return response.json()

@tool
def update_task(task_id: int, status: str) -> str:
    """Update the status of a task by id. Status can be TODO, IN_PROGRESS or DONE"""
    # First get the existing task
    get_response = requests.get(f"{SPRING_API_URL}/api/tasks/{task_id}", headers=headers)
    existing_task = get_response.json()
    
    # Send only the required fields
    payload = {
        "title": existing_task["title"],
        "description": existing_task.get("description", ""),
        "status": status,
        "priority": existing_task["priority"],
        "dueDate": existing_task["dueDate"]
    }
    
    response = requests.put(f"{SPRING_API_URL}/api/tasks/{task_id}", json=payload, headers=headers)
    return response.json()

@tool
def delete_task(task_id: int) -> str:
    """Delete a task by id"""
    response = requests.delete(f"{SPRING_API_URL}/api/tasks/{task_id}", headers=headers)
    return {"message": "Task deleted successfully"}

@tool
def semantic_search_tasks(query: str) -> str:
    """Search tasks by meaning/similarity. Use this when user wants to find tasks related to a topic."""
    sync_tasks_to_chroma()  # sync latest tasks first
    results = search_tasks(query)
    
    if not results["ids"][0]:
        return "No similar tasks found"
    
    tasks = []
    for i, doc in enumerate(results["documents"][0]):
        metadata = results["metadatas"][0][i]
        tasks.append(f"Task ID {metadata['id']}: {metadata['title']} - {metadata['status']} - {metadata['priority']}")
    
    return "\n".join(tasks)


# model = ChatGroq(model="llama-3.1-8b-instant")
# model = ChatGoogleGenerativeAI(model="gemini-2.0-flash")
model = ChatOpenAI(model="gpt-4o-mini")
tools = [create_task, get_tasks, update_task, delete_task, semantic_search_tasks]

agent = create_react_agent(model, tools)

if __name__ == "__main__":
    while True:
        user_input = input("\nYou: ")
        if user_input.lower() == "exit":
            break
        response = agent.invoke({"messages": [{"role": "user", "content": user_input}]})
        print(f"\nAI: {response['messages'][-1].content}")