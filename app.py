import os
import asyncio
import json
from typing import AsyncGenerator
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from memory import save_chat, load_memory
from retriever import retrieve_docs

load_dotenv()

app = FastAPI()

# RAG Agent Setup
llm = ChatOpenAI(
    model=os.getenv("GROQ_MODEL"),
    temperature=0.3,
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)

prompt = PromptTemplate(
    input_variables=["context", "question"],
    template="""You are a helpful AI assistant.

Answer only from the given context.

If answer is not present in context, say:
"I could not find this in documents."

Context:
{context}

Question:
{question}"""
)

rag_chain = prompt | llm | StrOutputParser()

class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

manager = ConnectionManager()

@app.get("/", response_class=HTMLResponse)
async def get():
    import os
    try:
        static_path = os.path.join(os.path.dirname(__file__), "static", "index.html")
        with open(static_path, "r", encoding="utf-8") as f:
            return HTMLResponse(content=f.read())
    except FileNotFoundError:
        return HTMLResponse(content="<h1>Error: static/index.html not found</h1>", status_code=404)

@app.websocket("/ws/{agent_type}")
async def websocket_endpoint(websocket: WebSocket, agent_type: str):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            message_data = json.loads(data)
            
            if message_data["type"] == "message":
                query = message_data["content"]
                session_id = message_data.get("session_id", "default")
                
                # Send thinking indicator
                await manager.send_message(json.dumps({
                    "type": "thinking",
                    "content": True
                }), websocket)
                
                try:
                    if agent_type == "rag":
                        response = await process_rag_query(query, session_id)
                    elif agent_type == "agent":
                        response = await process_agent_query(query)
                    else:
                        response = "Invalid agent type"
                    
                    # Send response word by word for streaming effect
                    words = response.split()
                    for i, word in enumerate(words):
                        await manager.send_message(json.dumps({
                            "type": "message",
                            "content": word + (" " if i < len(words) - 1 else "")
                        }), websocket)
                        await asyncio.sleep(0.03)  # Small delay for streaming effect
                    
                    # Send thinking stop indicator
                    await manager.send_message(json.dumps({
                        "type": "thinking",
                        "content": False
                    }), websocket)
                    
                except Exception as e:
                    await manager.send_message(json.dumps({
                        "type": "error",
                        "content": f"Error: {str(e)}"
                    }), websocket)
                    # Send thinking stop indicator on error
                    await manager.send_message(json.dumps({
                        "type": "thinking",
                        "content": False
                    }), websocket)
                    
    except WebSocketDisconnect:
        manager.disconnect(websocket)

async def process_rag_query(query: str, session_id: str) -> str:
    history = load_memory(session_id)
    docs = retrieve_docs(query)
    context = "\n\n".join([doc.page_content for doc in docs])
    
    final_context = f"""Previous Conversation:
{history}

Context:
{context}"""
    
    response = rag_chain.invoke({
        "context": final_context,
        "question": query
    })
    
    save_chat(session_id, query, response)
    return response

async def process_agent_query(query: str) -> str:
    try:
        # Lazy import to avoid initialization issues
        from agent.agent import app as agent_app
        result = agent_app.invoke({"query": query})
        return result.get("result", "No response generated")
    except Exception as e:
        return f"Agent error: {str(e)}. Please check your agent configuration."

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
