import os
from ollama import chat
import fitz  # PyMuPDF

# === CONFIGURATION ===
PDF_DIR = r"C:/Users/Evangelia/Documents/ΕΥΑΓΓΕΛΙΑ ΕΓΓΡΑΦΑ/UoCrete/tasks/task 5.1 files/europa/ollama_test"
MODEL = "llama3"
OUTPUT_FILE = os.path.join(PDF_DIR, "policy_analysis_results.txt")

# === FUNCTIONS ===
def extract_text_from_pdf(path):
    """Extract all text from a PDF file."""
    text = ""
    with fitz.open(path) as doc:
        for page in doc:
            text += page.get_text()
    return text


def chunk_text(text, chunk_size=10000, overlap=500):
    """Split text into overlapping chunks for large documents."""
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end]
        chunks.append(chunk)
        start += chunk_size - overlap
    return chunks


def analyze_policies_in_document(text, filename):
    """Ask the model to identify implemented policies or steps."""
    chunks = chunk_text(text, chunk_size=10000, overlap=500)
    partial_findings = []

    print(f"\n📄 Processing '{filename}' with {len(chunks)} chunks...")

    # Step 1: Extract relevant info from each chunk
    for i, chunk in enumerate(chunks):
        prompt = (
            f"From this section of the policy document '{filename}', "
            f"list the specific policies, actions, or implementation steps described. "
            f"Provide a clear, numbered list.\n\n{chunk}"
        )
        response = chat(model=MODEL, messages=[{"role": "user", "content": prompt}])
        partial_findings.append(response.message.content)
        print(f"   ✅ Finished chunk {i+1}/{len(chunks)}")

    # Step 2: Merge partial findings into a unified list
    combined = "\n\n".join(partial_findings)
    merge_prompt = (
        f"Combine and refine the following extracted points from '{filename}' into a clear, "
        f"deduplicated list of proposed policies and steps:\n\n{combined}"
    )
    merged_response = chat(model=MODEL, messages=[{"role": "user", "content": merge_prompt}])
    return merged_response.message.content

def synthesize_overall_policies(all_file_policies):
    """Combine all policies and evaluate them across documents."""
    # Build a combined text of all policies and their sources
    combined_text = "\n\n".join([
        f"Document: {filename}\nPolicies:\n{policies}"
        for filename, policies in all_file_policies.items()
    ])

    # Ask the model to merge and evaluate
    prompt = (
        "Here are extracted lists of policies from several EU policy documents. "
        "Your task is to:\n"
        "1. Create a unified, deduplicated list of all distinct policies.\n"
        "2. For each policy, list the document(s) it appears in.\n"
        "3. Evaluate each policy briefly in terms of:\n"
        "   - Effectiveness (High, Medium, Low, or Unknown)\n"
        "   - Impact (Economic, Social, Environmental, or Multiple)\n"
        "   - Social inclusion (Who benefits or is excluded?)\n"
        "Format your answer as a table or bullet list with clear structure.\n\n"
        f"{combined_text}"
    )

    response = chat(model=MODEL, messages=[{"role": "user", "content": prompt}])
    return response.message.content

# === MAIN ===
if __name__ == "__main__":
    all_policies = {}

    # results = []

    pdf_files = [f for f in os.listdir(PDF_DIR) if f.lower().endswith(".pdf")]
    if not pdf_files:
        print("⚠️ No PDF files found in directory:", PDF_DIR)
        exit()

    print(f"Found {len(pdf_files)} PDF files. Starting analysis...\n")

    for pdf_file in pdf_files:
        pdf_path = os.path.join(PDF_DIR, pdf_file)
        text = extract_text_from_pdf(pdf_path)
        policies = analyze_policies_in_document(text, pdf_file)
        all_policies[pdf_file] = policies

        # results.append(f"\n=== {pdf_file} ===\n{policies}\n")

        print("\n🧩 Synthesizing overall policy evaluation across all files...")
        evaluation = synthesize_overall_policies(all_policies)

    # Save everything to a text file
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write("=== INDIVIDUAL POLICY SUMMARIES ===\n\n")
        for file, summary in all_policies.items():
            f.write(f"\n--- {file} ---\n{summary}\n")

        f.write("\n\n=== CROSS-DOCUMENT POLICY EVALUATION ===\n\n")
        f.write(evaluation)

    print(f"\n✅ Done! Results saved to:\n{OUTPUT_FILE}")
