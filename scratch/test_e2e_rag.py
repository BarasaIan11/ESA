import requests
import json

BASE_URL = "http://127.0.0.1:8000"

def test_chat():
    print("Step 1: Getting Auth Token...")
    auth_resp = requests.post(
        f"{BASE_URL}/auth/token",
        data={"username": "testuser", "password": "testpassword"}
    )
    if auth_resp.status_code != 200:
        print(f"Auth Failed: {auth_resp.text}")
        return
    
    token = auth_resp.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    
    print("\nStep 2: Sending Chat Request (RAG enabled)...")
    chat_resp = requests.post(
        f"{BASE_URL}/chat/ask",
        headers=headers,
        json={"question": "How do I set up the Chart of Accounts in Business Central?"}
    )
    
    if chat_resp.status_code == 200:
        result = chat_resp.json()
        print("\n--- AI RESPONSE ---")
        print(result["answer"])
        print("\n--- SOURCES ---")
        for s in result["sources"]:
            print(f"- {s}")
    else:
        print(f"Chat Failed: {chat_resp.status_code}")
        print(chat_resp.text)

if __name__ == "__main__":
    test_chat()
