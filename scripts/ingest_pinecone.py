import os
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.documents import Document
from pinecone import Pinecone as PineconeClient
import pypdf
import sys

# Ensure backend can be imported to load settings
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from backend.config import settings

# Configuration
DATA_PATH = "knowledge_base"
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
    print(f"--- Starting Ingestion to Pinecone from '{DATA_PATH}' ---", flush=True)
    
    if not settings.pinecone_api_key:
        print("ERROR: PINECONE_API_KEY is not set in your .env file.")
        return

    print(f"Initializing embeddings model '{EMBEDDING_MODEL}'...", flush=True)
    embeddings = HuggingFaceEmbeddings(
        model_name=EMBEDDING_MODEL,
        model_kwargs={'device': 'cpu'}
    )
    
    all_chunks = []
    blacklist = ["bc_getting_started.pdf", "bc_service_management.pdf"]
    
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=150,
        separators=["\n\n", "\n", " ", ""]
    )

    print("Scanning knowledge base...", flush=True)
    if not os.path.exists(DATA_PATH):
        print(f"Directory {DATA_PATH} not found.")
        return
        
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

    print(f"\nPushing {len(all_chunks)} chunks to Pinecone index '{settings.pinecone_index_name}'...", flush=True)
    
    # Initialize Pinecone client
    pc = PineconeClient(api_key=settings.pinecone_api_key)
    index = pc.Index(settings.pinecone_index_name)
    
    # Embed and upload in batches of 100
    batch_size = 100
    total_batches = len(all_chunks) // batch_size + (1 if len(all_chunks) % batch_size != 0 else 0)
    
    print("Beginning upload loop...", flush=True)
    for i in range(0, len(all_chunks), batch_size):
        # 1. Resume check: Check if the first chunk of this batch is already in Pinecone
        try:
            fetch_response = index.fetch(ids=[f"chunk_{i}"])
            if fetch_response and fetch_response.get("vectors") and f"chunk_{i}" in fetch_response.get("vectors"):
                print(f"  Batch {i//batch_size + 1}/{total_batches} already exists. Skipping...", flush=True)
                continue
        except Exception as e:
            print(f"  (Resume check failed: {e}. Upserting anyway...)")
            
        batch_chunks = all_chunks[i:i + batch_size]
        
        # Generate embeddings
        texts = [chunk.page_content for chunk in batch_chunks]
        embeddings_list = embeddings.embed_documents(texts)
        
        vectors_to_upsert = []
        for j, (chunk, embedding) in enumerate(zip(batch_chunks, embeddings_list)):
            idx = i + j
            vectors_to_upsert.append({
                "id": f"chunk_{idx}",
                "values": embedding,
                "metadata": {
                    "text": chunk.page_content,
                    "source": chunk.metadata.get("source", ""),
                    "page": chunk.metadata.get("page", 0)
                }
            })
            
        print(f"  Upserting batch {i//batch_size + 1}/{total_batches} ({len(vectors_to_upsert)} vectors)...", flush=True)
        index.upsert(vectors=vectors_to_upsert)
        
        # Memory optimization: release CPU RAM
        import gc
        gc.collect()
        
    print(f"\n--- Ingestion Complete! ---", flush=True)

if __name__ == "__main__":
    ingest()
