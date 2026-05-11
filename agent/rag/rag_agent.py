import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

load_dotenv()

# =========================
# GROQ LLM
# =========================

llm = ChatOpenAI(
    model=os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile"),
    temperature=0.3,
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)

# =========================
# PROMPT TEMPLATE
# =========================

prompt = PromptTemplate(
    input_variables=["context", "question"],
    template="""
You are a helpful and professional AI assistant representing OpenEyes Technologies.

Your primary task is to answer the user's question based strictly on the provided context.

Context:
{context}

Question:
{question}

Instructions:
1. If the answer is present in the context, provide a complete and comprehensive answer including ALL relevant locations mentioned.
2. If the context mentions multiple locations (like headquarters and offices), include ALL of them in your response.
3. If the context is "No relevant documents found." or if the answer is completely missing from the context, respond gracefully with:
   "I could not find the exact answer to your question in the provided documents. Please rephrase or contact support for more details."
4. Do not invent answers or hallucinate information not present in the context.
5. Do not output generic phrases like 'no response from document'.
6. When asked about headquarters or locations, always mention all locations found in the context.
"""
)

chain = prompt | llm | StrOutputParser()


# =========================
# RAG AGENT FUNCTION
# =========================

def rag_agent(query: str, session_id: str = "default", context: str = "") -> str:
    """
    Process a query through the RAG agent.
    
    Args:
        query: User query
        session_id: Session ID for memory tracking
        context: Pre-retrieved context (optional)
    
    Returns:
        Response from the RAG agent
    """
    try:
        # Import retriever function
        from agent.rag.retriever import retrieve_docs
        
        # If no context provided, retrieve documents
        if not context:
            retrieved_docs = retrieve_docs(query)
            if retrieved_docs:
                context = "\n\n".join([doc.page_content for doc in retrieved_docs])
            else:
                context = "No relevant documents found."
        
        response = chain.invoke({
            "context": context,
            "question": query
        })
        return response
    except Exception as e:
        return f"Error processing query: {str(e)}"