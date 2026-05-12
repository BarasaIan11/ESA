import os

DATA_PATH = "knowledge_base"

def test_discovery():
    print(f"Checking {DATA_PATH}...")
    if not os.path.exists(DATA_PATH):
        print("ERROR: DATA_PATH does not exist")
        return
        
    for root, _, files in os.walk(DATA_PATH):
        print(f"Found {len(files)} files in {root}")
        for file in files:
            print(f" - {file}")

if __name__ == "__main__":
    test_discovery()
