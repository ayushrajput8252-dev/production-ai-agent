# AI RAG & Multi-Agent Chatbot

Modern AI chatbot powered by **RAG + Agentic AI** using **FastAPI**, **LangChain**, **Gemini**, and **WebSockets**.

Built for intelligent company support, employee search, automated workflows, and task handling.

---

# ✨ Core Features

- 🤖 Dual Agent Modes
- ⚡ Real-time Streaming Responses
- 🧠 Memory & Context Awareness
- 📄 PDF Knowledge Base Support
- 🔍 Hybrid Retrieval + Reranking
- 🌐 Modern HTML/CSS/JS Frontend
- 🚀 FastAPI + WebSocket Backend

---

# 🧩 Agent Modes

## 📚 RAG Agent — Company & Employee Assistant

Ask anything related to:

- Company information
- Employees and teams
- Skills and departments
- Internal documents
- Policies and workflows
- Project-related queries

### Example Queries

<img width="1908" height="926" alt="Screenshot 2026-05-08 135212" src="https://github.com/user-attachments/assets/45512987-3b5f-4fa9-9d75-e0ec05f82243" />


### How It Works

```txt
Documents → Retrieval → Reranking → Gemini Response
```

### Powered By

- Hybrid Search (Vector + BM25)
- Pinecone Vector Database
- Google Gemini

---

## 🤖 Agent Mode — Automated Business Workflow Agent

Performs real-world business tasks automatically using AI agents.

### Supported Automations

✅ If a candidate matches a job opening  
→ Sends mail to HR

✅ If user gives feedback (good/bad)  
→ Sends mail to Support Team

✅ If business-related query detected  
→ Sends mail to CTO

✅ Assign tasks to employees/teams  
→ Selects relevant employee and assigns task

✅ Smart routing based on query type

---

# ⚡ Example Workflows

## Hiring Workflow

```txt
Candidate Query
    ↓
AI checks required skills
    ↓
Matches employee/job data
    ↓
Sends mail to HR automatically
```

## Support Workflow

```txt
Customer Feedback
    ↓
AI detects sentiment
    ↓
Routes issue to support team
```

## Task Assignment Workflow

```txt
Task Request
    ↓
AI checks employee skills & availability
    ↓
Assigns task to best matching employee
```

---

# ⚙️ Tech Stack

- LangChain
- LangGraph
- Google Gemini
- Pinecone
- FastAPI
- WebSockets
- HTML/CSS/JavaScript

---

# 🚀 Quick Start

## 1. Install Dependencies

```bash
pip install -r requirements.txt
```

## 2. Setup Environment Variables

```bash
cp .env.example .env
```

Add your keys inside `.env`

```env
GOOGLE_API_KEY=
PINECONE_API_KEY=
EMAIL_USER=
EMAIL_PASS=
```

---

## 3. Process Documents

```bash
python ingest.py
```

---

## 4. Start Server

```bash
python start_server.py
```

Open in browser:

```txt
http://localhost:8000
```

---

# 📂 Project Structure

```bash
├── agent/               # Multi-agent workflows
├── data/                # Company documents
├── static/              # Frontend UI
├── app.py               # FastAPI backend
├── rag_agent.py         # RAG system
├── retriever.py         # Retrieval pipeline
├── mail.py              # Email automation
├── employee.json        # Employee database
└── start_server.py      # Server runner
```

---

# 🌟 Highlights

- Intelligent RAG-based company assistant
- Real-time AI streaming chatbot
- Automated business workflows
- AI-powered task assignment
- Email automation system
- Modern scalable architecture

---

# 🔮 Future Improvements

- PostgreSQL memory integration
- Jira automation
- Advanced multi-agent orchestration
- Role-based access control
- AI analytics dashboard

---

Built with modern **RAG + Agentic AI architecture** for scalable enterprise AI systems.
