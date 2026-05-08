# AI Chatbot with RAG and Agent Support

A simple, modern web-based chatbot interface that connects to both RAG (Retrieval-Augmented Generation) and regular AI agents using FastAPI with WebSocket streaming.

## Features

- 🤖 **Dual Agent Support**: Switch between RAG and regular agents
- 📱 **Modern UI**: Clean, responsive interface with real-time streaming
- 💭 **Thinking Indicators**: Visual feedback when agents are processing
- 🔌 **WebSocket Streaming**: Real-time message streaming for better UX
- 🎨 **Simple Design**: Minimal, user-friendly interface

## Quick Start

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure Environment**
   - Copy `.env.example` to `.env`
   - Add your `GROQ_API_KEY` to the `.env` file

3. **Start the Server**
   ```bash
   python start_server.py
   ```
   Or run directly:
   ```bash
   python app.py
   ```

4. **Open Browser**
   Navigate to: http://localhost:8000

## Usage

### Agent Types

1. **📚 RAG Agent**
   - Uses document retrieval for context-aware answers
   - Connects to your existing document database
   - Best for questions about your documents

2. **🤖 Agent**
   - General-purpose AI assistant
   - Uses the LangGraph agent system
   - Handles various tasks and queries

### Interface

- **Agent Selection**: Click the agent buttons to switch between RAG and Agent modes
- **Chat Messages**: Type your message and press Enter or click Send
- **Real-time Streaming**: See responses appear word by word
- **Thinking Indicator**: Dots show when the agent is processing

## Architecture

```
├── app.py                 # FastAPI server with WebSocket endpoints
├── static/
│   └── index.html        # Frontend HTML/CSS/JS
├── start_server.py       # Startup script
├── test_connection.py    # Test script
├── agent/               # Agent system
├── rag_agent.py         # RAG implementation
├── memory.py            # Chat memory
└── retriever.py         # Document retrieval
```

## API Endpoints

- `GET /` - Serves the chatbot interface
- `WS /ws/{agent_type}` - WebSocket endpoint for chat messages
  - `agent_type`: either "rag" or "agent"

## WebSocket Message Format

**Send Message:**
```json
{
  "type": "message",
  "content": "Your message here",
  "session_id": "optional_session_id"
}
```

**Receive Messages:**
```json
{
  "type": "thinking",
  "content": true/false
}
```
```json
{
  "type": "message",
  "content": "Response text"
}
```

## Testing

Run the test script to verify everything is working:
```bash
python test_connection.py
```

## Requirements

- Python 3.8+
- FastAPI
- Uvicorn
- WebSockets
- LangChain
- Groq API key

## Troubleshooting

1. **Port 8000 already in use**: Change the port in `start_server.py`
2. **API key issues**: Verify your `.env` file has the correct `GROQ_API_KEY`
3. **Agent errors**: Check that all agent modules are properly configured
4. **Document retrieval**: Ensure your document database is set up for RAG

## Development

The server supports hot reload when running with `start_server.py`. Changes to the frontend files will be reflected immediately on browser refresh.
