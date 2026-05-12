import os
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_core.documents import Document
import pypdf

# Configuration
DATA_PATH = "knowledge_base"
DB_PATH = "vector_db"
EMBEDDING_MODEL = "all-MiniLM-L6-v2"

def load_pdf(file_path):
    """Custom PDF loader using pypdf directly."""
    docs = []
    try:
        reader = pypdf.PdfReader(file_path)
        for i, page in enumerate(reader.pages):
            text = page.extract_text()
            if text.strip():
                docs.append(Document(
                    page_content=text,
                    metadata={"source": file_path, "page": i + 1}
                ))
    except Exception as e:
        print(f"  !! Error reading PDF {file_path}: {e}")
    return docs

def load_text(file_path):
    """Custom text loader."""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
            return [Document(page_content=content, metadata={"source": file_path})]
    except Exception as e:
        print(f"  !! Error reading text {file_path}: {e}")
    return []

def ingest():
    print(f"--- Starting Ingestion from '{DATA_PATH}' ---", flush=True)
    
    if not os.path.exists(DB_PATH):
        os.makedirs(DB_PATH)

    print(f"Initializing embeddings model '{EMBEDDING_MODEL}'...", flush=True)
    embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)
    
    print("Connecting to vector store...", flush=True)
    vector_db = Chroma(persist_directory=DB_PATH, embedding_function=embeddings)

    processed_log = os.path.join(DB_PATH, "processed_files.txt")
    already_processed = set()
    if os.path.exists(processed_log):
        with open(processed_log, "r") as f:
            already_processed = set(line.strip() for line in f)

    blacklist = ["bc_getting_started.pdf", "bc_service_management.pdf"]

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=150,
        separators=["\n\n", "\n", " ", ""]
    )

    processed_count = 0
    print("Scanning knowledge base...", flush=True)
    for root, _, files in os.walk(DATA_PATH):
        for file in files:
            if file in already_processed or file in blacklist:
                continue
                
            ext = os.path.splitext(file)[1].lower()
            file_path = os.path.join(root, file)
            
            if ext == ".pdf":
                print(f"\nProcessing PDF: {file} ...", flush=True)
                file_docs = load_pdf(file_path)
            elif ext in [".md", ".txt"]:
                print(f"\nProcessing Text: {file} ...", flush=True)
                file_docs = load_text(file_path)
            else:
                continue

            if file_docs:
                file_chunks = text_splitter.split_documents(file_docs)
                print(f"  -> Adding {len(file_chunks)} chunks in batches of 500...", flush=True)
                
                batch_size = 500
                for i in range(0, len(file_chunks), batch_size):
                    batch = file_chunks[i : i + batch_size]
                    vector_db.add_documents(batch)
                    print(f"     Processed {i + len(batch)}/{len(file_chunks)}...", flush=True)
                
                with open(processed_log, "a") as f:
                    f.write(f"{file}\n")
                processed_count += 1
                print(f"  -> DONE.", flush=True)

    if processed_count == 0:
        print("\nNo new documents were processed.", flush=True)
    else:
        print(f"\n--- Ingestion Complete! New files processed: {processed_count}. ---", flush=True)

if __name__ == "__main__":
    ingest()
