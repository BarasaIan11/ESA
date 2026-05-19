import os
import sys
import httpx

# Ensure we can run it against the running uvicorn server on localhost:8000
BASE_URL = "http://localhost:8000"

def test_flow():
    print("--- Starting End-to-End ESA Functionality Test ---")
    
    # 1. Exchange API key for JWT Token
    print("\n1. Requesting Authentication JWT from /auth/token...")
    try:
        response = httpx.post(f"{BASE_URL}/auth/token", json={"api_key": "test_dev_key"})
        response.raise_for_status()
        token_data = response.json()
        token = token_data.get("access_token")
        print(f"   [SUCCESS] Received Token: {token[:30]}...")
    except Exception as e:
        print(f"   [FAILED] Could not authenticate: {e}")
        return

    # 2. Query Chat Ask endpoint with RAG context
    headers = {"Authorization": f"Bearer {token}"}
    question = "How do I set up the IC Chart of Accounts in Business Central?"
    print(f"\n2. Querying RAG Endpoint /chat/ask with: '{question}'...")
    
    payload = {
        "question": question,
        "session_id": "test-session-123"
    }
    
    try:
        response = httpx.post(f"{BASE_URL}/chat/ask", json=payload, headers=headers, timeout=90.0)
        response.raise_for_status()
        chat_data = response.json()
        answer = chat_data.get("answer")
        sources = chat_data.get("sources")
        
        print("\n   [SUCCESS] Received Response:")
        print("-" * 60)
        print(answer)
        print("-" * 60)
        print("   Sources retrieved from Pinecone:")
        for src in sources:
            print(f"   - {src}")
        print("-" * 60)
    except Exception as e:
        print(f"   [FAILED] Chat query failed: {e}")

if __name__ == "__main__":
    test_flow()
