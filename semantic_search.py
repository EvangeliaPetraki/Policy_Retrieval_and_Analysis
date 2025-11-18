import chromadb
from sentence_transformers import SentenceTransformer
from ollama import chat
import datetime
import os


print('importing packages ok')

# === CONFIG ===
# CHROMA_PATH = "thesis_db"  # same as before
CHROMA_PATH = "example_policy_file_db"
# CHROMA_PATH = "article_db"
EMBED_MODEL = "all-MiniLM-L6-v2"
MODEL_NAME = "llama3"  # or another local model you installed via Ollama
TOP_K = 5 # number of retrieved chunks per query
OUTPUT_FILE = "qa_results.txt"
SUMMARY_FILE = "Unionisation and the twin transition _ good practices in collective action and employee involvement..txt"

# === STEP 1: Load the DB and model ===
print("📦 Loading Chroma and embedding model...")
chroma_client = chromadb.PersistentClient(path=CHROMA_PATH)
collection = chroma_client.get_collection(name="thesis_chunks")
embedder = SentenceTransformer(EMBED_MODEL)

with open(SUMMARY_FILE, "r", encoding="utf-8") as f:
    article_summary = f.read()


# QUESTIONS = [
#     "What are the main ways the twin transition (digital + green) is transforming work and employment across Europe?",
#     "How do employee representation and social dialogue influence the success of digital and green transitions?",
#     "Which groups of workers—such as women, low-skilled, or older employees—are most vulnerable in this transition, and what protections are proposed?",
#     "Which case studies best illustrate successful employee involvement in technology adoption and why?",
#     "Across all case studies, what patterns or enabling factors make employee-led innovation effective?",
#     "How do EU-level legal and funding instruments (e.g., Works Council Directive, RRF) support or constrain worker participation?",
#     "Do digitalisation and greening create tensions or synergies in workplace transformation, according to the study?",
#     "How effective are current policy measures in balancing competitiveness with social inclusion?",
#     "What overall conclusions does the study reach about the role of social partners in managing the twin transition?",
#     "Which policy recommendations are most actionable and impactful for ensuring a just and inclusive transition?"
# ]



# # print("\n✅ Ready! Ask questions about your article.")
# # print("Press ENTER on an empty line to exit.\n")


# with open(OUTPUT_FILE, "w", encoding="utf-8") as out:
#     out.write(f"Q&A Results — {datetime.datetime.now().isoformat()}\n")
#     out.write(f"Model: {MODEL_NAME} | Embedder: {EMBED_MODEL} | Top-K: {TOP_K}\n")
#     out.write("="*80 + "\n\n")

# for idx, query in enumerate(QUESTIONS, start=1):
#     print(f"🔎 [{idx}/{len(QUESTIONS)}] Retrieving for question:")
#     print(f"    {query}")
#     query_embedding = embedder.encode([query]).tolist()
#     results = collection.query(query_embeddings=query_embedding, n_results=TOP_K)
#     context = "\n\n".join(results["documents"][0])

#     prompt = f"""
#     You are analysing a Study on EU policies regarding the digital and/or green transition (the twin transition).
#     Below is a global summary of the document, followed by specific excerpts retrieved as context.

#     Question:
#     {query}

#     Article Summary:
#     {article_summary}

#     Context:
#     {context}

#     Provide a detailed, well-reasoned answer that connects the specific excerpts to the overall themes of the study.
#     If excerpts conflict with the summary, prioritise the excerpts as primary evidence. Cite specific points briefly.
#     """

#     try:
#         print("🤖 Asking Llama 3...")
#         response = chat(model=MODEL_NAME, messages=[{'role': 'user', 'content': prompt}])
#         answer_text = response.message.content.strip()
#     except Exception as e:
#         answer_text = f"[ERROR calling model]: {e}"

#     # Write Q&A to file incrementally
#     with open(OUTPUT_FILE, "a", encoding="utf-8") as out:
#         out.write(f"Q{idx}. {query}\n\n")
#         out.write("Answer:\n")
#         out.write(answer_text + "\n\n")
#         out.write("-"*80 + "\n\n")

#     print(f"✅ Saved Q{idx} to '{OUTPUT_FILE}'.\n")

# print(f"🎉 All done! See results in: {os.path.abspath(OUTPUT_FILE)}")


while True: 

    # === STEP 2: Ask your question ===
    query = input("\n❓ Enter your question about the article:\n> ")

    if query == "":  # blank line means stop
        print("\n👋 Exiting semantic search. Goodbye!")
        break

    print("🔍 Searching relevant text...")

    # === STEP 3: Embed and retrieve ===
    query_embedding = embedder.encode([query]).tolist()
    results = collection.query(query_embeddings=query_embedding, n_results=TOP_K)

    if not results["documents"][0]:
        print("⚠️ No relevant text found.\n")
        continue
    
    # === STEP 4: Show retrieved chunks ===
    print(f"\n🔍 Found {len(results['documents'][0])} relevant chunks:\n")
    for i, doc in enumerate(results["documents"][0]):
        print(f"--- Chunk {i+1} ---")
        print(doc[:500].replace("\n", " "))
        print("...")

    # === STEP 5: Feed retrieved text to Llama ===
    context = "\n\n".join(results["documents"][0])
    prompt = f"""
    You are analysing a Study having to do with policies of the EU regarding green transition and/or digital transition (twin transition). Below is a global summary of the document, followed by specific excerpts retrieved as context.
    
    Question: {query}

    Article Summary:
    {article_summary}

    Context:
    {context}

    Provide a detailed, well-reasoned answer that connects the specific excerpts to the overall themes of the article.

    Answer:"""

    print("\n🤖 Asking Llama 3...")
    response = chat(model=MODEL_NAME, messages=[{'role': 'user', 'content': prompt}])

    print("\n🧠 Llama 3's answer:\n")
    print(response.message.content)