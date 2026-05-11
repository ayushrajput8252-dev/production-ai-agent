from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os

load_dotenv()

llm = ChatOpenAI(
    model=os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile"),
    temperature=0.3,
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)


def supervisor_agent(user_query: str) -> str:
    """
    Supervisor agent that routes queries to appropriate sub-agents.
    
    Args:
        user_query: The user's query
    
    Returns:
        Route as a string: one of ["query", "feedback", "career", "task"]
    """
    
    prompt = f"""
    You are supervisor agent.

    Decide which agent should handle the query.

    Available agents:
    - query
    - feedback
    - career
    - task

    Return only one word.

    Query:
    {user_query}
    """

    try:
        response = llm.invoke(prompt)
        route = response.content.strip().lower()
        
        # Validate route
        valid_routes = {"query", "feedback", "career", "task"}
        if route not in valid_routes:
            route = "query"
        
        return route
    except Exception:
        # Safe fallback to keep the graph running when LLM provider is unavailable.
        text = user_query.lower()
        if "feedback" in text or "complaint" in text or "review" in text:
            return "feedback"
        if "career" in text or "resume" in text or "job" in text:
            return "career"
        if "task" in text or "assign" in text:
            return "task"
        return "query"