import os
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document
import pypdf

# Configuration
DATA_PATH = "knowledge_base"
DB_PATH = "vector_db"
EMBEDDING_MODEL = "all-MiniLM-L6-v2"

def load_pdf(file_path):
    docs = []
    try:
        reader = pypdf.PdfReader(file_path)
        for i, page in enumerate(reader.pages):
            text = page.extract_text()
            if text and text.strip():
                docs.append(Document(
                    page_content=text,
                    metadata={"source": file_path, "page": i + 1}
                ))
    except Exception as e:
        print(f"  !! Error reading PDF {file_path}: {e}")
    return docs

def load_text(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
            return [Document(page_content=content, metadata={"source": file_path})]
    except Exception as e:
        print(f"  !! Error reading text {file_path}: {e}")
    return []

def ingest():
    print(f"--- Starting Ingestion (FAISS) from '{DATA_PATH}' ---", flush=True)
    
    if not os.path.exists(DB_PATH):
        os.makedirs(DB_PATH)

    print(f"Initializing embeddings model '{EMBEDDING_MODEL}'...", flush=True)
    embeddings = HuggingFaceEmbeddings(
        model_name=EMBEDDING_MODEL,
        model_kwargs={'device': 'cpu'}
    )
    
    all_chunks = []
    blacklist = ["bc_getting_started.pdf", "bc_service_management.pdf"]
    extensions = [".pdf", ".md", ".txt"]
    
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=150,
        separators=["\n\n", "\n", " ", ""]
    )

    print("Scanning knowledge base...", flush=True)
    for root, _, files in os.walk(DATA_PATH):
        for file in files:
            if file in blacklist:
                continue
                
            ext = os.path.splitext(file)[1].lower()
            file_path = os.path.join(root, file)
            
            if ext == ".pdf":
                print(f"Processing PDF: {file} ...", flush=True)
                file_docs = load_pdf(file_path)
            elif ext in [".md", ".txt"]:
                print(f"Processing Text: {file} ...", flush=True)
                file_docs = load_text(file_path)
            else:
                continue

            if file_docs:
                chunks = text_splitter.split_documents(file_docs)
                all_chunks.extend(chunks)
                print(f"  -> Found {len(chunks)} chunks.", flush=True)

    if not all_chunks:
        print("\nNo documents were processed.", flush=True)
        return

    print(f"\nCreating FAISS index from {len(all_chunks)} total chunks...", flush=True)
    vector_db = FAISS.from_documents(all_chunks, embeddings)
    
    print(f"Saving FAISS index to '{DB_PATH}'...", flush=True)
    vector_db.save_local(DB_PATH)
    
    print(f"\n--- Ingestion Complete! ---", flush=True)

if __name__ == "__main__":
    ingest()
