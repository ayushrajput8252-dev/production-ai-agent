import os
import pickle
from dotenv import load_dotenv
from langchain_community.retrievers import BM25Retriever

load_dotenv()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
chunks_path = os.path.join(
    BASE_DIR,
    "storage",
    "chunks.pkl"
)

try:
    with open(chunks_path, "rb") as f:
        chunks = pickle.load(f)
    bm25_retriever = BM25Retriever.from_documents(chunks)
    bm25_retriever.k = 8
except FileNotFoundError:
    print(f"Warning: {chunks_path} not found. Please run ingest.py first.")
    bm25_retriever = None
    chunks = []

# Use BM25 retriever only
print("Using BM25 retriever for document retrieval")
hybrid_retriever = bm25_retriever
# =========================
# OPTIONAL RERANKER
# =========================

reranker = None

# if ENABLE_RERANKER:
#     try:
#         reranker = CrossEncoder(
#             "BAAI/bge-reranker-base"
#         )
#     except Exception as exc:
#         print(f"Reranker unavailable: {exc}")

# =========================
# RETRIEVE DOCS
# =========================

def retrieve_docs(query):
    if not hybrid_retriever:
        return []
    
    docs = hybrid_retriever.invoke(query)
    
    unique_docs = []
    seen = set()
    
    for doc in docs:
        if doc.page_content not in seen:
            seen.add(doc.page_content)
            unique_docs.append(doc)
    
    return unique_docs[:4]