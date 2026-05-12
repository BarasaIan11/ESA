print("Importing os...")
import os
print("Importing langchain_community...")
from langchain_community.document_loaders import PyPDFLoader, TextLoader
print("Importing langchain_text_splitters...")
from langchain_text_splitters import RecursiveCharacterTextSplitter
print("Importing langchain_huggingface...")
from langchain_huggingface import HuggingFaceEmbeddings
print("Importing langchain_chroma...")
from langchain_chroma import Chroma
print("All imports successful!")
