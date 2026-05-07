from dotenv import load_dotenv
import os
import pickle

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_pinecone import PineconeVectorStore

from pinecone import Pinecone, ServerlessSpec

load_dotenv()

# =========================
# CONFIG
# =========================

PDF_FOLDER = "data"
STORAGE_FOLDER = "storage"

os.makedirs(STORAGE_FOLDER, exist_ok=True)

PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
INDEX_NAME = os.getenv("PINECONE_INDEX")
EMBEDDING_MODEL = "models/gemini-embedding-001"
EMBEDDING_DIMENSION = 3072

if not PINECONE_API_KEY or not GOOGLE_API_KEY or not INDEX_NAME:
    raise ValueError(
        "Missing env vars. Set GOOGLE_API_KEY, PINECONE_API_KEY, and PINECONE_INDEX in .env."
    )

# =========================
# LOAD PDFS
# =========================

documents = []

for file in os.listdir(PDF_FOLDER):

    if file.endswith(".pdf"):

        loader = PyPDFLoader(
            os.path.join(PDF_FOLDER, file)
        )

        docs = loader.load()

        for d in docs:
            d.metadata["source"] = file

        documents.extend(docs)

print(f"Loaded {len(documents)} pages")

# =========================
# SPLIT DOCUMENTS
# =========================

splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200
)

chunks = splitter.split_documents(documents)

print(f"Created {len(chunks)} chunks")

# SAVE CHUNKS
with open("storage/chunks.pkl", "wb") as f:
    pickle.dump(chunks, f)

# =========================
# GEMINI EMBEDDINGS
# =========================

embeddings = GoogleGenerativeAIEmbeddings(
    model=EMBEDDING_MODEL,
    google_api_key=GOOGLE_API_KEY
)

# =========================
# PINECONE
# =========================

pc = Pinecone(api_key=PINECONE_API_KEY)

existing_indexes = pc.list_indexes().names()

if INDEX_NAME not in existing_indexes:

    pc.create_index(
        name=INDEX_NAME,
        dimension=EMBEDDING_DIMENSION,
        metric="cosine",
        spec=ServerlessSpec(
            cloud="aws",
            region="us-east-1"
        )
    )
else:
    index_info = pc.describe_index(INDEX_NAME)
    if index_info.dimension != EMBEDDING_DIMENSION:
        print(
            f"Index '{INDEX_NAME}' has dimension {index_info.dimension}; "
            f"recreating with {EMBEDDING_DIMENSION}."
        )
        pc.delete_index(INDEX_NAME)
        pc.create_index(
            name=INDEX_NAME,
            dimension=EMBEDDING_DIMENSION,
            metric="cosine",
            spec=ServerlessSpec(
                cloud="aws",
                region="us-east-1"
            )
        )

print("Pinecone index ready")

# =========================
# STORE EMBEDDINGS
# =========================

PineconeVectorStore.from_documents(
    documents=chunks,
    embedding=embeddings,
    index_name=INDEX_NAME
)

print("Documents uploaded to Pinecone")