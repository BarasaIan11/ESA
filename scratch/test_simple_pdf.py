import os
import pypdf

print("Starting simple test...")
print(f"pypdf version: {pypdf.__version__}")

def load_pdf(file_path):
    print(f"Testing PDF load: {file_path}")
    reader = pypdf.PdfReader(file_path)
    print(f"Pages: {len(reader.pages)}")
    return len(reader.pages)

if __name__ == "__main__":
    load_pdf("knowledge_base/sample_bc.md") # Should fail but print something
