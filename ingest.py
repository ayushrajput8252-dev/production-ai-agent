from dotenv import load_dotenv
import os
import pickle
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.embeddings import OllamaEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_pinecone import PineconeVectorStore
from pinecone import Pinecone, ServerlessSpec
load_dotenv()

PDF_FOLDER = "C:/AYUSH/openeyes/production-ai-agent/data"
STORAGE_FOLDER = "storage"
os.makedirs(STORAGE_FOLDER, exist_ok=True)


PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
INDEX_NAME = os.getenv("PINECONE_INDEX")

document = []
for file in os.listdir(PDF_FOLDER):
    if file.endswith(".pdf"):

        loader = PyPDFLoader(
            os.path.join(PDF_FOLDER, file)
        )
        docs = loader.load()

        for d in docs:
            d.metadata["source"] = file
        
        document.extend(docs)
# SPLIT DOCUMENTS
splitter = RecursiveCharacterTextSplitter(
    chunk_size = 1000,
    chunk_overlap = 200,
    separators = ["\n\n", "\n", ".", " "]
)

chunks = splitter.split_documents(document)

print(f"Created {len(chunks)} chunks")

with open("storage/chunks.pkl", "wb") as f:
    pickle.dump(chunks, f)

# EMBEDDINGS
embeddings = OllamaEmbeddings(
    model = "mxbai-embed-large"
)

#pinecone
pc = Pinecone(api_key = os.getenv("PINECONE_API_KEY"))

existing_indexes = [
    index["name"]
    for index in pc.list_indexes()
]
if INDEX_NAME not in existing_indexes:

    pc.create_index(
        name=INDEX_NAME,
        dimension=1024,
        metric="cosine",
        spec=ServerlessSpec(
            cloud="aws",
            region="us-east-1"
        )
    )
print("Pinecone index ready")

PineconeVectorStore.from_documents(
    documents=chunks,
    embedding=embeddings,
    index_name=INDEX_NAME
)
print("Documents uploaded to Pinecone")