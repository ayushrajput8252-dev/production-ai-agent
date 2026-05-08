import os
from typing import Literal

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI

from memory import load_memory, save_chat
from retriever import retrieve_docs
from agent.agent import app as langgraph_app


load_dotenv()

app = FastAPI(title="OpenEyes API", version="1.0.0")

MODEL_NAME = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")
llm = ChatOpenAI(
    model=MODEL_NAME,
    temperature=0.3,
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1",
)

prompt = PromptTemplate(
    input_variables=["context", "question"],
    template="""
You are a helpful AI assistant.

Answer only from the given context.

If answer is not present in context, say:
"I could not find this in documents."

Context:
{context}

Question:
{question}
""",
)
chain = prompt | llm | StrOutputParser()


class ChatRequest(BaseModel):
    message: str
    mode: Literal["normal", "agent"] = "normal"
    session_id: str = "default"


class ChatResponse(BaseModel):
    mode: str
    reply: str


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest):
    query = req.message.strip()
    if not query:
        raise HTTPException(status_code=400, detail="Message cannot be empty.")

    try:
        if req.mode == "agent":
            result = langgraph_app.invoke({"query": query})
            return ChatResponse(mode="agent", reply=str(result.get("result", "")))

        history = load_memory(req.session_id)
        docs = retrieve_docs(query)
        context = "\n\n".join(doc.page_content for doc in docs)
        final_context = f"""
Previous Conversation:
{history}

Context:
{context}
"""
        response = chain.invoke({"context": final_context, "question": query})
        save_chat(req.session_id, query, response)
        return ChatResponse(mode="normal", reply=response)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Processing failed: {exc}") from exc
