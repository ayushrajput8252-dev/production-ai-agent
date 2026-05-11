# OpenEyes AI Agent - Complete Documentation

## Table of Contents
1. [Project Overview](#project-overview)
2. [Project Structure](#project-structure)
3. [Setup & Installation](#setup--installation)
4. [Environment Configuration](#environment-configuration)
5. [Running the Project](#running-the-project)
6. [API Documentation](#api-documentation)
7. [Agent Architecture](#agent-architecture)
8. [Frontend Integration](#frontend-integration)
9. [Troubleshooting](#troubleshooting)

## Project Overview

OpenEyes is a full-stack AI agent application combining:
- **Frontend**: Next.js React application with beautiful UI
- **Backend**: FastAPI server with two main agents:
  - **RAG Agent**: Retrieval-Augmented Generation for knowledge-based Q&A
      ```python
      ----ai-chat-overlay.tsx----
      const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8003"
      ```
  - **Tool Agent**: Multi-purpose agent with specialized sub-agents

### Key Features
- Intelligent query routing
- Email-based workflow automation
- Job matching and career assistance
- Customer feedback classification
- Task assignment system
- Real-time chat interface

## Project Structure

```
production-ai-agent/
├── agent/                           # Backend Python code
│   ├── __init__.py                 # Package init
│   ├── api.py                      # FastAPI app & endpoints
│   ├── tool/                       # Tool Agent
│   │   ├── __init__.py
│   │   ├── agent.py               # LangGraph implementation
│   │   ├── main.py                # CLI entry point
│   │   ├── utils.py               # Helper functions
│   │   ├── mail.py                # Email utilities
│   │   ├── data/                  # Data files
│   │   │   ├── employee.json
│   │   │   └── carerrs.json
│   │   └── sub_agent/             # Specialized agents
│   │       ├── __init__.py
│   │       ├── supervisor.py      # Router agent
│   │       ├── query.py           # Query handler
│   │       ├── feedback.py        # Feedback classifier
│   │       ├── career.py          # Career matcher
│   │       └── task.py            # Task assigner
│   └── rag/                        # RAG Agent
│       ├── __init__.py
│       ├── rag_agent.py           # RAG implementation
│       ├── retriever.py           # Document retrieval
│       └── ingest.py              # Data ingestion
├── app/                            # Frontend (Next.js)
│   ├── page.tsx                   # Main page
│   └── layout.tsx                 # Root layout
├── components/                     # React components
│   ├── chat/                      # Chat components
│   │   ├── ai-chat-overlay.tsx    # Main chat UI
│   │   └── floating-assistant-button.tsx
│   ├── landing/                   # Landing page sections
│   ├── ui/                        # Reusable UI components
│   └── theme-provider.tsx
├── memory.py                       # SQLite chat memory
├── package.json                    # Frontend dependencies
├── requirements.txt                # Python dependencies
├── tsconfig.json                   # TypeScript config
├── next.config.mjs                # Next.js config
└── .env.example                    # Environment template
```

## Setup & Installation

### Prerequisites
- Python 3.8+
- Node.js 16+
- npm or pnpm
- SQLite3 (usually included)

### Step 1: Clone & Install Python Dependencies

```bash
cd c:\AYUSH\openeyes\production-ai-agent

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install Python packages
pip install -r requirements.txt
```

### Step 2: Install Node Dependencies

```bash
# Using npm
npm install

# OR using pnpm (faster)
pnpm install
```

### Step 3: Setup Environment Variables

Create a `.env` file in the project root:

```bash
cp .env.example .env
```

Edit `.env` with your API keys:

```env
# Google Generative AI API Key
GOOGLE_API_KEY=your_google_api_key_here
GEMINI_CHAT_MODEL=models/gemini-2.0-flash

# GROQ API Configuration
GROQ_API_KEY=your_groq_api_key_here
GROQ_MODEL=llama-3.3-70b-versatile

# Pinecone Configuration
PINECONE_API_KEY=your_pinecone_api_key_here
PINECONE_INDEX=your_pinecone_index_name

# Email Configuration
EMAIL_USER=your_email@gmail.com
EMAIL_PASS=your_app_password_here
MAIL_MODE=smtp

# Optional: enable cross-encoder reranking
ENABLE_RERANKER=false
```

## Environment Configuration

### Required API Keys

#### 1. **GROQ API** (LLM Provider)
- Get key from: https://console.groq.com/
- Free tier: 30 requests/minute
- Used for: Supervisor routing, feedback analysis, query classification

#### 2. **Google Generative AI** (Embeddings)
- Get key from: https://ai.google.dev/
- Used for: Document embeddings in RAG system

#### 3. **Pinecone** (Vector Database)
- Get key from: https://www.pinecone.io/
- Used for: Storing and retrieving document embeddings

#### 4. **Email Configuration**
- **For Gmail**:
  1. Enable 2-factor authentication
  2. Create an app password
  3. Use app password in `EMAIL_PASS`
- **MAIL_MODE**:
  - `smtp`: Send real emails
  - `local`: Queue emails locally (for testing)

## Running the Project

### Option 1: Run Backend & Frontend Separately (Development)

**Terminal 1 - Start FastAPI Server:**
```bash
# Activate virtual environment
venv\Scripts\activate

# Run FastAPI server
python -m uvicorn agent.api:app --reload --host 0.0.0.0 --port 8000
```

Server will be available at: `http://localhost:8000`

**Terminal 2 - Start Next.js Frontend:**
```bash
# Make sure you're in the project root
npm run dev
# OR with pnpm
pnpm dev
```

Frontend will be available at: `http://localhost:3000`

### Option 2: Run Tool Agent CLI

For testing the Tool Agent directly:

```bash
python -m agent.tool.main
```

This opens an interactive prompt to test queries.

### Testing the API

Use Postman or curl to test:

```bash
# Test RAG Agent
curl -X POST http://localhost:8000/api/rag-agent \
  -H "Content-Type: application/json" \
  -d '{"query": "What is your company about?"}'

# Test Tool Agent
curl -X POST http://localhost:8000/api/tool-agent \
  -H "Content-Type: application/json" \
  -d '{"query": "I have feedback about the service"}'

# Check health
curl http://localhost:8000/health

# Get available agents
curl http://localhost:8000/api/agents
```

## API Documentation

### Base URL
- **Development**: `http://localhost:8000`
- **Production**: Update `NEXT_PUBLIC_API_URL` in frontend

### Endpoints

#### 1. Health Check
```
GET /health
```
**Response:**
```json
{
  "status": "healthy",
  "message": "OpenEyes AI Agent API is running"
}
```

#### 2. Tool Agent
```
POST /api/tool-agent
```

**Request:**
```json
{
  "query": "I have feedback about your service",
  "session_id": "user_123",
  "context": null
}
```

**Response:**
```json
{
  "success": true,
  "result": "Good feedback mail sent",
  "agent": "tool-agent",
  "error": null
}
```

**Query Types:**
- **Feedback**: "feedback", "complaint", "review"
- **Career**: "career", "resume", "job"
- **Task**: "task", "assign"
- **Query**: General questions

#### 3. RAG Agent
```
POST /api/rag-agent
```

**Request:**
```json
{
  "query": "What documents do you have?",
  "session_id": "user_123",
  "context": "Optional context from retriever"
}
```

**Response:**
```json
{
  "success": true,
  "result": "Based on the documents...",
  "agent": "rag-agent",
  "error": null
}
```

#### 4. Available Agents
```
GET /api/agents
```

**Response:**
```json
{
  "agents": [
    {
      "id": "tool-agent",
      "name": "Tool Agent",
      "description": "...",
      "endpoint": "/api/tool-agent",
      "capabilities": [...]
    },
    ...
  ]
}
```

## Agent Architecture

### Tool Agent Flow

```
User Query
    ↓
Supervisor Agent (Routes to appropriate sub-agent)
    ↓
    ├─→ Query Sub-Agent (Business queries)
    ├─→ Feedback Sub-Agent (Customer feedback)
    ├─→ Career Sub-Agent (Job matching)
    └─→ Task Sub-Agent (Task assignment)
    ↓
Response
```

### RAG Agent Flow

```
User Query
    ↓
Retriever (Fetch relevant documents)
    ↓
Context Assembly
    ↓
LLM Processing
    ↓
Response Generation
```

### Sub-Agent Capabilities

#### Query Agent
- Classifies queries as: general, high priority, normal
- Routes to appropriate email recipients
- Sends summary emails

#### Feedback Agent
- Classifies sentiment: good, bad
- Routes to support team
- Maintains feedback history

#### Career Agent
- Matches skills against job positions
- Calculates skill score
- Notifies HR on match

#### Task Agent
- Routes tasks to employees
- Sends email notifications
- Tracks assignments

## Frontend Integration

### Configuration

The frontend connects to the backend via environment variable:

**In your `.env.local` or `.env`:**
```
NEXT_PUBLIC_API_URL=http://localhost:8000
```

For production:
```
NEXT_PUBLIC_API_URL=https://your-api-domain.com
```

### API Calls

The chat component automatically:
1. Sends queries to the appropriate endpoint
2. Handles responses
3. Displays results in real-time
4. Shows error messages if needed

### Component Structure

**AiChatOverlay.tsx** handles:
- Agent selection (RAG vs Tool)
- Message history
- Real-time API calls
- Error handling
- UI state management

## Troubleshooting

### Backend Won't Start

**Error:** `ModuleNotFoundError: No module named 'agent'`

**Solution:**
```bash
# Make sure you're in the correct directory
cd c:\AYUSH\openeyes\production-ai-agent

# Run from project root
python -m uvicorn agent.api:app --reload
```

### Import Errors in Python

**Error:** `ImportError: cannot import name 'X' from 'agent.tool'`

**Solution:**
1. Verify `__init__.py` files exist in all agent directories
2. Check Python path: `echo $PYTHONPATH`
3. Reinstall with: `pip install -e .`

### Frontend Can't Connect to Backend

**Error:** `API error: 404` or `Failed to connect to backend`

**Solution:**
1. Verify FastAPI server is running: `http://localhost:8000/health`
2. Check `NEXT_PUBLIC_API_URL` in frontend
3. Verify CORS is enabled in `agent/api.py`
4. Check browser console for actual error message

### Email Not Sending

**Error:** `Mail failed: ...`

**Solution:**
1. Verify `EMAIL_USER` and `EMAIL_PASS` in `.env`
2. Check email credentials are correct
3. For Gmail: Ensure app password is used (not regular password)
4. Check `MAIL_MODE` setting (use "local" for testing)

### Virtual Environment Issues

**Error:** `venv not found` or `python: command not found`

**Solution:**
```bash
# On Windows
python -m venv venv
venv\Scripts\activate

# On macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### Port Already in Use

**Error:** `Address already in use`

**Solution:**
```bash
# Change port for FastAPI
python -m uvicorn agent.api:app --reload --port 8001

# Change port for Next.js
npm run dev -- -p 3001
```

## Support & Contact

For issues or questions:
1. Check the troubleshooting section
2. Review environment variables
3. Check API logs in terminal
4. Review console errors in browser

---

**Last Updated:** 2026-05-10
**Version:** 1.0.0
