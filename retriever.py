import os
import pickle
from dotenv import load_dotenv
from langchain_community.embeddings import OllamaEmbeddings
from langchain_pinecone import PineconeVectorStore
from langchain_community.retrievers import BM25Retriever
from langchain.retrievers import EnsembleRetriever
from sentence_transformers import CrossEncoder
from pinecone import Pinecone

load_dotenv()
with open("storage/chunks.pkl", "rb") as f:
    chunks = pickle.load(f)

PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
INDEX_NAME = os.getenv("PINECONE_INDEX")

embeddings = OllamaEmbeddings(
    model = "mxbai-embed-large"
)
# PINECONE VECTOR STORE
vectorstore = PineconeVectorStore(
    index_name = INDEX_NAME,
    embedding = embeddings
)
# VECTOR RETRIEVER
vector_retriever = vectorstore.as_retriever(
    search_kwargs={"k": 8}
)

#BM25 
bm25_retriever = BM25Retriever.from_documents(
    chunks
)
bm25_retriever.k = 8

#hybrid retriiver 
hybrid_retriever = EnsembleRetriever(
    retrievers = [vector_retriever, bm25_retriever],
    weights = [0.5, 0.5]
)

#reranker-----------------
reranker = CrossEncoder(
    model_name = "BAAI/bge-reranker-base"
)

def retrieve_docs(query):
    docs = hybrid_retriever.invoke(query)

    pairs = []
    for doc in docs:
        pairs.append(
            (query, doc.page_content)
        )
    #get score
    scores = reranker.predict(pairs)
    #combine docs
    scored_docs = []

    for doc, score in zip(docs, scores):

        scored_docs.append({
            "doc": doc,
            "score": score
        })

    # SORT HIGH SCORE FIRST
    scored_docs = sorted(
        scored_docs,
        key=lambda x: x["score"],
        reverse=True
    )

    # TOP 4 DOCS
    final_docs = []

    for item in scored_docs[:4]:
        final_docs.append(item["doc"])

    return final_docs
