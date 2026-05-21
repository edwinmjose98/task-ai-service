# eval.py
from rag import sync_tasks_to_chroma, search_tasks

test_cases = [
    {
        "query": "urgent bug fix",
        "expected_keywords": ["bug", "authentication", "jwt"]
    },
    {
        "query": "meeting preparation agenda",
        "expected_keywords": ["meeting", "agenda", "standup"]
    },
    {
        "query": "quarterly financial report",
        "expected_keywords": ["quarterly", "financials", "q2"]
    },
    {
        "query": "API documentation update",
        "expected_keywords": ["api", "documentation", "fastapi"]
    },
    {
        "query": "deployment staging environment",
        "expected_keywords": ["staging", "deploy", "environment"]
    }
]

def evaluate():
    sync_tasks_to_chroma()
    
    passed = 0
    for test in test_cases:
        results = search_tasks(test["query"])
        
        if not results["ids"][0]:
            print(f"FAIL — '{test['query']}': no results returned")
            continue
        
        # Check if any returned result contains expected keywords
        top_result = results["documents"][0][0].lower()
        matched = any(kw.lower() in top_result for kw in test["expected_keywords"])
        
        if matched:
            print(f"PASS — '{test['query']}'")
            passed += 1
        else:
            print(f"FAIL — '{test['query']}': got '{top_result[:80]}'")
    
    accuracy = passed / len(test_cases) * 100
    print(f"\nAccuracy: {passed}/{len(test_cases)} = {accuracy:.0f}%")

if __name__ == "__main__":
    evaluate()