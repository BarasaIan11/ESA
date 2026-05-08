"""
Diagnostic script to verify your Gemini API key is working.
Run with: .venv\Scripts\python.exe scratch\test_gemini.py
"""
import os, sys

# Load .env manually
env_path = os.path.join(os.path.dirname(__file__), '..', '.env')
with open(env_path) as f:
    for line in f:
        line = line.strip()
        if line and not line.startswith('#') and '=' in line:
            k, v = line.split('=', 1)
            os.environ.setdefault(k.strip(), v.strip())

api_key = os.environ.get('GEMINI_API_KEY', '')
model   = os.environ.get('GEMINI_MODEL', 'gemini-2.0-flash')

print(f"API Key: {api_key[:10]}...{api_key[-4:] if len(api_key) > 14 else ''}")
print(f"Model:   {model}")
print()

try:
    from google import genai
    client = genai.Client(api_key=api_key)

    # Step 1: List available models (does NOT consume quota)
    print("Step 1: Listing available models for your key...")
    models = list(client.models.list())
    flash_models = [m.name for m in models if 'flash' in m.name.lower() or 'pro' in m.name.lower()]
    print(f"  Found {len(models)} models. Relevant ones:")
    for m in flash_models[:8]:
        print(f"    - {m}")
    print()

    # Step 2: Try a minimal generate call
    print("Step 2: Sending a minimal test message...")
    response = client.models.generate_content(
        model=model,
        contents="Say exactly: WORKING",
    )
    print(f"  SUCCESS! Response: {response.text.strip()}")

except Exception as e:
    print(f"  FAILED: {type(e).__name__}: {e}")
    if '429' in str(e):
        print()
        print("  FIX NEEDED: Your API key has limit=0 on the free tier.")
        print("  This means the Gemini API is NOT properly enabled for your project.")
        print()
        print("  To fix this:")
        print("  1. Go to https://aistudio.google.com/apikey")
        print("  2. Click 'Create API Key'")
        print("  3. In the dialog, select 'Create API key in new project'")
        print("  4. Copy the new key into your .env file as GEMINI_API_KEY=")
