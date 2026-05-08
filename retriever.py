import os
import pickle

from dotenv import load_dotenv

from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_pinecone import PineconeVectorStore

from langchain_community.retrievers import BM25Retriever
from langchain_classic.retrievers import EnsembleRetriever

# from sentence_transformers import CrossEncoder

load_dotenv()

# =========================
# LOAD CHUNKS
# =========================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

chunks_path = os.path.join(
    BASE_DIR,
    "storage",
    "chunks.pkl"
)

with open(chunks_path, "rb") as f:
    chunks = pickle.load(f)

# =========================
# CONFIG
# =========================

PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
INDEX_NAME = os.getenv("PINECONE_INDEX")

EMBEDDING_MODEL = "models/gemini-embedding-001"

ENABLE_RERANKER = (
    os.getenv("ENABLE_RERANKER", "false").lower() == "true"
)

if not PINECONE_API_KEY:
    raise ValueError("Missing PINECONE_API_KEY")

if not GOOGLE_API_KEY:
    raise ValueError("Missing GOOGLE_API_KEY")

if not INDEX_NAME:
    raise ValueError("Missing PINECONE_INDEX")

# =========================
# EMBEDDINGS
# =========================

embeddings = GoogleGenerativeAIEmbeddings(
    model=EMBEDDING_MODEL,
    google_api_key=GOOGLE_API_KEY
)

# =========================
# VECTOR STORE
# =========================

vectorstore = PineconeVectorStore(
    index_name=INDEX_NAME,
    embedding=embeddings
)

vector_retriever = vectorstore.as_retriever(
    search_kwargs={"k": 8}
)

# =========================
# BM25
# =========================

bm25_retriever = BM25Retriever.from_documents(chunks)

bm25_retriever.k = 8

# =========================
# HYBRID SEARCH
# =========================

hybrid_retriever = EnsembleRetriever(
    retrievers=[
        vector_retriever,
        bm25_retriever
    ],
    weights=[0.5, 0.5]
)

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

    docs = hybrid_retriever.invoke(query)

    unique_docs = []

    seen = set()

    for doc in docs:

        if doc.page_content not in seen:

            seen.add(doc.page_content)

            unique_docs.append(doc)

    # OPTIONAL RERANKING
    if reranker and unique_docs:

        pairs = [
            (query, doc.page_content)
            for doc in unique_docs
        ]

        scores = reranker.predict(pairs)

        scored_docs = list(zip(unique_docs, scores))

        scored_docs.sort(
            key=lambda x: x[1],
            reverse=True
        )

        return [
            doc
            for doc, score in scored_docs[:4]
        ]

    return unique_docs[:4]