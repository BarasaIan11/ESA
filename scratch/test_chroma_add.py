from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_core.documents import Document
import os

DB_PATH = "vector_db_test"
print("Initializing test vector store...")
embeddings = HuggingFaceEmbeddings(
    model_name="all-MiniLM-L6-v2",
    model_kwargs={'device': 'cpu'}
)
vector_db = Chroma(persist_directory=DB_PATH, embedding_function=embeddings)

print("Adding test documents...")
docs = [Document(page_content=f"Test chunk {i}", metadata={"id": i}) for i in range(10)]

try:
    vector_db.add_documents(docs)
    print("SUCCESS: Documents added!")
except Exception as e:
    print(f"FAILED: {e}")
