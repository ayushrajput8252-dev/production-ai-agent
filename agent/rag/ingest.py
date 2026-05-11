from dotenv import load_dotenv
import os
import pickle
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_pinecone import PineconeVectorStore
from pinecone import Pinecone, ServerlessSpec

load_dotenv()
PDF_FOLDER = "C:/AYUSH/openeyes/production-ai-agent/agent/rag/data"
STORAGE_FOLDER = "storage"
os.makedirs(STORAGE_FOLDER, exist_ok=True)

PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
INDEX_NAME = os.getenv("PINECONE_INDEX", "openeyes-rag")

# Use HuggingFace embeddings that produce 768 dimensions
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-mpnet-base-v2",
    model_kwargs={'device': 'cpu'}
)

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

splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200
)
chunks = splitter.split_documents(documents)

# Save chunks for BM25 retrieval
with open("chunks.pkl", "wb") as f:
    pickle.dump(chunks, f)

print(f"Successfully processed {len(documents)} documents into {len(chunks)} chunks")
print("Chunks saved to storage/chunks.pkl")

# Upload to Pinecone
print("Uploading to Pinecone...")
try:
    PineconeVectorStore.from_documents(
        documents=chunks,
        embedding=embeddings,
        index_name=INDEX_NAME
    )
    print(f"Successfully uploaded {len(chunks)} chunks to Pinecone index: {INDEX_NAME}")
except Exception as e:
    print(f"Error uploading to Pinecone: {e}")
