"""
FastAPI server for AI Agent backend.
Provides REST endpoints for both RAG and Tool agents.
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import logging

from agent.tool.agent import run_tool_agent
from agent.rag.rag_agent import rag_agent

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="OpenEyes AI Agent API",
    description="API for RAG and Tool agents",
    version="1.0.0"
)

# Add CORS middleware to allow frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ========================
# Request/Response Models
# ========================

class QueryRequest(BaseModel):
    """Request model for agent queries."""
    query: str
    session_id: Optional[str] = "default"
    context: Optional[str] = None


class QueryResponse(BaseModel):
    """Response model for agent queries."""
    success: bool
    result: str
    agent: str
    error: Optional[str] = None


class HealthCheck(BaseModel):
    """Health check response."""
    status: str
    message: str


# ========================
# Health Check Endpoint
# ========================

@app.get("/health", response_model=HealthCheck)
async def health_check():
    """
    Health check endpoint to verify API is running.
    
    Returns:
        HealthCheck: Status and message
    """
    return {
        "status": "healthy",
        "message": "OpenEyes AI Agent API is running"
    }


# ========================
# Tool Agent Endpoints
# ========================

@app.post("/api/tool-agent", response_model=QueryResponse)
async def tool_agent_endpoint(request: QueryRequest):
    """
    Process query through the Tool Agent.
    
    The Tool Agent routes queries to appropriate sub-agents:
    - Query: General queries and business requirements
    - Feedback: Customer feedback and reviews
    - Career: Job matching and career assistance
    - Task: Task assignment to employees
    
    Args:
        request: QueryRequest with user query
    
    Returns:
        QueryResponse with agent result
    
    Example:
        POST /api/tool-agent
        {
            "query": "I have feedback about your service"
        }
    """
    try:
        if not request.query or not request.query.strip():
            raise HTTPException(status_code=400, detail="Query cannot be empty")
        
        result = run_tool_agent(request.query)
        
        return {
            "success": True,
            "result": result,
            "agent": "tool-agent",
            "error": None
        }
    except Exception as e:
        logger.error(f"Tool agent error: {str(e)}")
        return {
            "success": False,
            "result": "",
            "agent": "tool-agent",
            "error": str(e)
        }


# ========================
# RAG Agent Endpoints
# ========================

@app.post("/api/rag-agent", response_model=QueryResponse)
async def rag_agent_endpoint(request: QueryRequest):
    """
    Process query through the RAG (Retrieval-Augmented Generation) Agent.
    
    The RAG Agent retrieves relevant documents and generates responses
    based on the provided context and knowledge base.
    
    Args:
        request: QueryRequest with user query and optional context
    
    Returns:
        QueryResponse with agent result
    
    Example:
        POST /api/rag-agent
        {
            "query": "What is your company about?",
            "context": "OpenEyes is an AI company..."
        }
    """
    try:
        if not request.query or not request.query.strip():
            raise HTTPException(status_code=400, detail="Query cannot be empty")
        
        result = rag_agent(
            query=request.query,
            session_id=request.session_id,
            context=request.context or ""
        )
        
        return {
            "success": True,
            "result": result,
            "agent": "rag-agent",
            "error": None
        }
    except Exception as e:
        logger.error(f"RAG agent error: {str(e)}")
        return {
            "success": False,
            "result": "",
            "agent": "rag-agent",
            "error": str(e)
        }


# ========================
# Agent Info Endpoints
# ========================

@app.get("/api/agents")
async def get_agents():
    """
    Get information about available agents.
    
    Returns:
        Dictionary with agent information and capabilities
    """
    return {
        "agents": [
            {
                "id": "tool-agent",
                "name": "Tool Agent",
                "description": "Handles specialized tasks like feedback, career matching, and task assignment",
                "endpoint": "/api/tool-agent",
                "capabilities": ["feedback", "career_matching", "task_assignment", "query_routing"]
            },
            {
                "id": "rag-agent",
                "name": "RAG Agent",
                "description": "Retrieval-Augmented Generation agent for knowledge-based Q&A",
                "endpoint": "/api/rag-agent",
                "capabilities": ["document_retrieval", "knowledge_based_qa", "context_aware_responses"]
            }
        ]
    }


# ========================
# Error Handlers
# ========================

@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    """Handle HTTP exceptions."""
    return {
        "success": False,
        "result": "",
        "agent": "unknown",
        "error": exc.detail
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
