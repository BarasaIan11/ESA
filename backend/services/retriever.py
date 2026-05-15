import os
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

# Configuration
DB_PATH = "vector_db"
EMBEDDING_MODEL = "all-MiniLM-L6-v2"

# Global instance for shared use
_retriever = None

def get_retriever():
    """
    Lazy initialization of the FAISS retriever.
    """
    global _retriever
    if _retriever is None:
        print(f"Initializing FAISS retriever from '{DB_PATH}'...")
        embeddings = HuggingFaceEmbeddings(
            model_name=EMBEDDING_MODEL,
            model_kwargs={'device': 'cpu'}
        )
        
        # FAISS uses index.faiss and index.pkl
        faiss_file = os.path.join(DB_PATH, "index.faiss")
        if not os.path.exists(faiss_file):
            print("WARNING: FAISS index file is missing!")
            return None
            
        vector_db = FAISS.load_local(
            DB_PATH, 
            embeddings,
            allow_dangerous_deserialization=True # Required for loading local pkl files
        )
        # Search for top 3 relevant chunks
        _retriever = vector_db.as_retriever(search_kwargs={"k": 3})
        
    return _retriever

def query_knowledge_base(query: str) -> list[str]:
    """
    Search the vector database for relevant documentation chunks.
    """
    retriever = get_retriever()
    if not retriever:
        return []
        
    try:
        print(f"Searching FAISS knowledge base for: '{query}'...")
        docs = retriever.invoke(query)
        return [doc.page_content for doc in docs]
    except Exception as e:
        print(f"Error querying knowledge base: {e}")
        return []

if __name__ == "__main__":
    results = query_knowledge_base("How do I set up the Chart of Accounts?")
    print(f"\nFound {len(results)} relevant snippets:")
    for i, res in enumerate(results):
        print(f"\n--- Result {i+1} ---\n{res[:200]}...")
