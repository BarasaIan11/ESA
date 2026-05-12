print("Importing pypdf...")
import pypdf
print("pypdf imported!")
reader = pypdf.PdfReader("knowledge_base/sample_bc.md") # This will fail but let's test import
