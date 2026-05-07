# AI RAG Bot

A Retrieval-Augmented Generation (RAG) chatbot built with LangChain, Pinecone, and Google Gemini.

## Features

- **Hybrid Retrieval**: Combines vector search and BM25 for better document retrieval
- **Reranking**: Uses cross-encoder reranking for improved relevance
- **Multiple Document Support**: Processes PDF documents from the data folder
- **Pinecone Integration**: Scalable vector database for embeddings
- **Google Gemini**: Advanced language model for responses

## Prerequisites

1. **Python 3.8+**
2. **Ollama** (for local embeddings)
   - Install from https://ollama.ai
   - Run: `ollama pull mxbai-embed-large`
3. **API Keys**:
   - Google Gemini API Key
   - Pinecone API Key

## Setup

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Set Up Environment Variables**:
   ```bash
   cp .env.example .env
   # Edit .env with your API keys
   ```

3. **Run Ollama**:
   ```bash
   ollama serve
   ```

4. **Process Documents**:
   ```bash
   python ingest.py
   ```

5. **Start Chatbot**:
   ```bash
   python rag_agent.py
   ```

## Usage

- Ask questions about your documents
- Type "exit" to quit
- The bot will answer based on the provided PDF documents

## File Structure

```
├── data/                  # PDF documents
├── storage/              # Processed chunks (auto-created)
├── ingest.py             # Document processing
├── retriever.py          # Retrieval logic
├── rag_agent.py          # Main chatbot
├── requirements.txt       # Dependencies
└── .env.example         # Environment template
```

## Troubleshooting

1. **Ollama Connection Error**: Ensure Ollama is running and the embedding model is pulled
2. **Pinecone Connection**: Verify API key and index name
3. **Missing Chunks**: Run `ingest.py` first to process documents
4. **API Key Issues**: Check environment variables in `.env`

## Architecture

- **Ingestion**: PDFs → Chunks → Embeddings → Pinecone
- **Retrieval**: Hybrid (Vector + BM25) → Reranking → Top Documents
- **Generation**: Retrieved Docs + Gemini → Response
