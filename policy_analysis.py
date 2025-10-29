# import os
# from llama_cpp import Llama
# from PyPDF2 import PdfReader
# from tqdm import tqdm

# print('ok')


# llm = Llama.from_pretrained(
#     repo_id="Qwen/Qwen2-0.5B-Instruct-GGUF",
#     filename="qwen2-0_5b-instruct-q8_0.gguf",  # exact filename
#     n_ctx=4096,
#     verbose=False
# )

# print('ok')

# from ollama import chat
# from ollama import ChatResponse

# file = '"C:/Users/Evangelia/Documents/ΕΥΑΓΓΕΛΙΑ ΕΓΓΡΑΦΑ\UoCrete/tasks/task 5.1 files/europa/policy_files/Meeting skill needs for the green transition _ skills anticipation and VET for a greener future..pdf"'

# response: ChatResponse = chat(model='llama3', messages=[
#   {
#     'role': 'user',
#     'content': 'Why is the sky blue?',
#   },
# ])
# print(response['message']['content'])
# # or access fields directly from the response object
# print(response.message.content)

from ollama import chat
import fitz  # PyMuPDF

pdf_path = r"C:/Users/Evangelia/Documents/ΕΥΑΓΓΕΛΙΑ ΕΓΓΡΑΦΑ\UoCrete/tasks/task 5.1 files/europa/policy_files/Meeting skill needs for the green transition _ skills anticipation and VET for a greener future..pdf"

# Extract text from the PDF
def extract_text_from_pdf(path):
    text = ""
    with fitz.open(path) as doc:
        for page in doc:
            text += page.get_text()
    return text

text = extract_text_from_pdf(pdf_path)


def chunk_text(text, chunk_size=10000, overlap=500):
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end]
        chunks.append(chunk)
        start += chunk_size - overlap
    return chunks


# text = text[:8000] 
# response = chat(
#     model='llama3',
#     messages=[
#         {
#             'role': 'user',
#             'content': f"Summarize the following document:\n\n{text}"
#         }
#     ]
# )


def summarize_large_document(text, filename):
    chunks = chunk_text(text, chunk_size=10000, overlap=500)
    partial_summaries = []

    print(f"Splitting {filename} into {len(chunks)} chunks...")

    for i, chunk in enumerate(chunks):
        prompt = f"Summarize part {i+1} of the document '{filename}'. Focus on key ideas, findings, and themes:\n\n{chunk}"
        response = chat(model='llama3', messages=[{'role': 'user', 'content': prompt}])
        partial_summaries.append(response.message.content)

    # Now merge partial summaries into a final one
    combined_summary = "\n\n".join(partial_summaries)
    merge_prompt = (
        f"Combine the following partial summaries of {filename} into a single concise summary:\n\n{combined_summary}"
    )
    final_response = chat(model='llama3', messages=[{'role': 'user', 'content': merge_prompt}])
    return final_response.message.content

if __name__ == "__main__":
    text = extract_text_from_pdf(pdf_path)
    final_summary = summarize_large_document(text, "Meeting skill needs for the green transition.pdf")
    print("\n🧠 FINAL SUMMARY:\n")
    print(final_summary)