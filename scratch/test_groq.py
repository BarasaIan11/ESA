"""
Diagnostic script to verify your Groq API key is working.
Run with: .venv\Scripts\python.exe scratch\test_groq.py
"""
import os, sys
import asyncio

# Load .env manually
env_path = os.path.join(os.path.dirname(__file__), '..', '.env')
if os.path.exists(env_path):
    with open(env_path) as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                k, v = line.split('=', 1)
                os.environ.setdefault(k.strip(), v.strip())

api_key = os.environ.get('GROQ_API_KEY', '')
model   = os.environ.get('GROQ_MODEL', 'llama-3.3-70b-versatile')

async def main():
    print(f"Groq API Key: {api_key[:10]}...{api_key[-4:] if len(api_key) > 14 else ''}")
    print(f"Groq Model:   {model}")
    print()

    if not api_key or "PASTE_YOUR_GROQ_KEY" in api_key:
        print("ERROR: Please paste your Groq API key into the .env file first.")
        return

    try:
        from openai import AsyncOpenAI
        client = AsyncOpenAI(
            api_key=api_key,
            base_url="https://api.groq.com/openai/v1"
        )

        print("Sending test message to Groq...")
        response = await client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": "Say 'GROQ IS WORKING'"}],
            max_tokens=20
        )
        print(f"SUCCESS! Response: {response.choices[0].message.content.strip()}")

    except Exception as e:
        print(f"FAILED: {type(e).__name__}: {e}")

if __name__ == "__main__":
    asyncio.run(main())
