try:
    from genai import Client
    print("SUCCESS: from genai import Client works")
except ImportError:
    try:
        from google import genai
        print("SUCCESS: from google import genai works")
    except ImportError as e:
        print(f"FAILED: {e}")
