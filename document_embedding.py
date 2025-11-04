import fitz  # PyMuPDF
from sentence_transformers import SentenceTransformer
import chromadb
import os

# === CONFIGURATION ===
PDF_PATH = r"C:/Users/Evangelia/Documents/Studies/medical engineering/TERM 2/Thesis/final docs/βιβλ/Evangelia Petraki Thesis.pdf"
CHROMA_PATH = "thesis_db"
EMBED_MODEL = "all-MiniLM-L6-v2"  # small, local, free
CHUNK_SIZE = 1000  # characters per chunk
OVERLAP = 200      # to avoid cutting sentences

# === FUNCTIONS ===
def extract_text_from_pdf(pdf_path):
    text = ""
    with fitz.open(pdf_path) as doc:
        for page in doc:
            text += page.get_text("text")
    return text

def chunk_text(text, chunk_size=1000, overlap=200):
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end]
        chunks.append(chunk)
        start += chunk_size - overlap
    return chunks

def embed_thesis():
    print("📖 Extracting text...")
    text = extract_text_from_pdf(PDF_PATH)
    chunks = chunk_text(text, CHUNK_SIZE, OVERLAP)
    print(f"Split thesis into {len(chunks)} chunks")

    print("🧠 Loading embedding model...")
    model = SentenceTransformer(EMBED_MODEL)

    print("💾 Creating Chroma collection...")
    chroma_client = chromadb.PersistentClient(path=CHROMA_PATH)
    collection = chroma_client.get_or_create_collection(name="thesis_chunks")

    print("🔢 Computing embeddings...")
    embeddings = model.encode(chunks, show_progress_bar=True).tolist()
    collection.add(ids=[f"chunk_{i}" for i in range(len(chunks))], documents=chunks, embeddings=embeddings)
    print("✅ Thesis embedded and stored successfully!")

if __name__ == "__main__":
    embed_thesis()
