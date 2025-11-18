from ollama import chat
import fitz
import os 
from pathlib import Path

PDF_PATH = r"C:/Users/Evangelia/Documents/ΕΥΑΓΓΕΛΙΑ ΕΓΓΡΑΦΑ/UoCrete/tasks/task 5.1 files/europa/url_try/Unionisation and the twin transition _ good practices in collective action and employee involvement..pdf"
CHUNK_SIZE = 4000   # characters per chunk (~700–800 words)
OVERLAP = 500       # overlap between chunks
MODEL_NAME = "llama3"
OUTPUT_FILE = Path(PDF_PATH).stem + ".txt"
print(OUTPUT_FILE)