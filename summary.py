# summarize_thesis.py
from ollama import chat
import fitz
import os 
from pathlib import Path

PDF_PATH = r"C:/Users/Evangelia/Documents/ΕΥΑΓΓΕΛΙΑ ΕΓΓΡΑΦΑ/UoCrete/tasks/task 5.1 files/europa/url_try/Unionisation and the twin transition _ good practices in collective action and employee involvement..pdf"
CHUNK_SIZE = 4000   # characters per chunk (~700–800 words)
OVERLAP = 500       # overlap between chunks
MODEL_NAME = "llama3"
OUTPUT_FILE = Path(PDF_PATH).stem + ".txt"

def extract_text_from_pdf(path):
    text = ""
    with fitz.open(path) as doc:
        for page in doc:
            text += page.get_text()
    return text

def chunk_text(text, chunk_size=4000, overlap=500):
    """Split text into overlapping chunks."""
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start += chunk_size - overlap
    return chunks


def summarize_chunk(chunk, index):
    """Ask Llama 3 to summarize a specific chunk."""
    prompt = f"Summarize the following part ({index}) of an academic document. Focus on main ideas, findings, and arguments:\n\n{chunk}"
    response = chat(model=MODEL_NAME, messages=[{'role': 'user', 'content': prompt}])
    return response.message.content.strip()


def combine_summaries(summaries):
    """Combine partial summaries into one coherent summary."""
    joined = "\n\n".join([f"Part {i+1} Summary:\n{summ}" for i, summ in enumerate(summaries)])
    prompt = f"""Combine the following partial summaries into one clear, concise, and cohesive summary of the full document.
Avoid repetition and ensure logical flow of ideas:

{joined}
"""
    response = chat(model=MODEL_NAME, messages=[{'role': 'user', 'content': prompt}])
    return response.message.content.strip()


def summarize_pdf(pdf_path):
    """Main summarization routine."""
    print("📖 Extracting text from PDF...")
    text = extract_text_from_pdf(pdf_path)
    print(f"✅ Extracted {len(text)} characters from document.")

    print("✂️ Splitting text into chunks...")
    chunks = chunk_text(text, CHUNK_SIZE, OVERLAP)
    print(f"✅ Created {len(chunks)} chunks (~{CHUNK_SIZE} chars each).")

    summaries = []
    for i, chunk in enumerate(chunks, start=1):
        print(f"\n🤖 Summarizing chunk {i}/{len(chunks)}...")
        summary = summarize_chunk(chunk, i)
        summaries.append(summary)
        print(f"🧩 Done with chunk {i}.")

    print("\n🧠 Combining all summaries into final overview...")
    final_summary = combine_summaries(summaries)

    # Save results
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(final_summary)

    print(f"\n✅ Final summary saved to: {os.path.abspath(OUTPUT_FILE)}")
    return final_summary


# === RUN ===
if __name__ == "__main__":
    summarize_pdf(PDF_PATH)