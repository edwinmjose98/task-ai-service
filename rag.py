import chromadb
import requests
import os
from dotenv import load_dotenv

load_dotenv()

SPRING_API_URL = os.getenv("SPRING_API_URL")
SPRING_API_TOKEN = os.getenv("SPRING_API_TOKEN")

headers = {
    "Authorization": f"Bearer {SPRING_API_TOKEN}",
    "Content-Type": "application/json"
}

# Initialize ChromaDB
chroma_client = chromadb.Client()
collection = chroma_client.get_or_create_collection(name="tasks")

def sync_tasks_to_chroma():
    """Fetch all tasks from Spring Boot and store in ChromaDB"""
    response = requests.get(f"{SPRING_API_URL}/api/tasks", headers=headers)
    tasks = response.json()
    
    for task in tasks:
        collection.upsert(
            ids=[str(task["id"])],
            documents=[f"{task['title']} {task.get('description', '')}"],
            metadatas=[{
                "id": task["id"],
                "title": task["title"],
                "status": task["status"],
                "priority": task["priority"]
            }]
        )
    print(f"Synced {len(tasks)} tasks to ChromaDB")

def search_tasks(query: str, n_results: int = 3):
    """Search tasks by semantic similarity"""
    results = collection.query(
        query_texts=[query],
        n_results=n_results
    )
    return results

if __name__ == "__main__":
    sync_tasks_to_chroma()
    results = search_tasks("client report")
    print(results)