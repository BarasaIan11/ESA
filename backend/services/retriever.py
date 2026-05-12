import os
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma

# Configuration
DB_PATH = "vector_db"
EMBEDDING_MODEL = "all-MiniLM-L6-v2"

# Global instance for shared use
_retriever = None

def get_retriever():
    """
    Lazy initialization of the ChromaDB retriever.
    """
    global _retriever
    if _retriever is None:
        print(f"Initializing retriever from '{DB_PATH}'...")
        embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)
        
        if not os.path.exists(DB_PATH) or not os.listdir(DB_PATH):
            print("WARNING: Vector database is empty or missing!")
            return None
            
        vector_db = Chroma(
            persist_directory=DB_PATH,
            embedding_function=embeddings
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
        print(f"Searching knowledge base for: '{query}'...")
        docs = retriever.invoke(query)
        # Extract page content from the document objects
        return [doc.page_content for doc in docs]
    except Exception as e:
        print(f"Error querying knowledge base: {e}")
        return []

if __name__ == "__main__":
    # Quick test
    results = query_knowledge_base("How do I set up the Chart of Accounts?")
    print(f"\nFound {len(results)} relevant snippets:")
    for i, res in enumerate(results):
        print(f"\n--- Result {i+1} ---\n{res[:200]}...")
