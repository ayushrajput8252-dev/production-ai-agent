from dotenv import load_dotenv
import os
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_pinecone import PineconeVectorStore
from pinecone import Pinecone, ServerlessSpec
load_dotenv()

PDF_FOLDER = "C:/AYUSH/openeyes/production-ai-agent/data"

PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
INDEX_NAME = os.getenv("PINECONE_INDEX")

document = []
for file in os.listdir(PDF_FOLDER):
    if file.endswith(".pdf"):

        loader = PyPDFLoader(
            os.path.join(PDF_FOLDER, file)
        )