import requests
import json

BASE_URL = "http://127.0.0.1:8000"

def verify_integration():
    print(f"--- Starting End-to-End Verification ---")
    
    # 1. Get Token
    print("Step 1: Authenticating...")
    auth_resp = requests.post(
        f"{BASE_URL}/auth/token",
        json={"api_key": "secret-key"}
    )
    if auth_resp.status_code != 200:
        print(f"Auth failed: {auth_resp.text}")
        return
    
    token = auth_resp.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    print("  Authenticated successfully.")

    # 2. Ask RAG-specific question
    question = "How do I set up a new Chart of Accounts in Business Central?"
    print(f"\nStep 2: Asking question: '{question}'...")
    
    chat_resp = requests.post(
        f"{BASE_URL}/chat/ask",
        headers=headers,
        json={"question": question}
    )
    
    if chat_resp.status_code != 200:
        print(f"Chat request failed: {chat_resp.text}")
        return

    data = chat_resp.json()
    print("\n--- AI Response ---")
    print(data["answer"])
    
    print("\n--- Sources Cited ---")
    for src in data["sources"]:
        print(f"- {src}")

    if len(data["sources"]) > 0:
        print("\n✅ SUCCESS: RAG integration is working! Sources were retrieved and used.")
    else:
        print("\n❌ FAILED: No sources were cited. Is the vector database empty?")

if __name__ == "__main__":
    verify_integration()
