import os

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from memory import save_chat, load_memory
from retriever import retrieve_docs

load_dotenv()

MODEL_NAME = os.getenv(
    "GROQ_MODEL",
    "llama-3.3-70b-versatile"
)

# =========================
# GEMINI MODEL
# =========================

llm = ChatOpenAI(
    model=MODEL_NAME,
    temperature=0.3,
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)

# =========================
# PROMPT
# =========================

prompt = PromptTemplate(
    input_variables=["context", "question"],
    template="""
You are a helpful AI assistant.

Answer only from the given context.

If answer is not present in context,
say:

"I could not find this in documents."

Context:
{context}

Question:
{question}
"""
)

chain = prompt | llm | StrOutputParser()

print("RAG Chatbot Started")

# =========================
# CHAT LOOP
# =========================

session_id = input("Session ID: ")

while True:

    query = input("\nAsk: ").strip()

    if query.lower() == "exit":
        break

    # LOAD OLD MEMORY
    history = load_memory(session_id)

    # RETRIEVE DOCS
    docs = retrieve_docs(query)

    context = "\n\n".join([
        doc.page_content
        for doc in docs
    ])

    # FINAL CONTEXT
    final_context = f"""
Previous Conversation:
{history}

Context:
{context}
"""

    response = chain.invoke({
        "context": final_context,
        "question": query
    })

    print("\nAnswer:\n")
    print(response)

    # SAVE MEMORY
    save_chat(
        session_id,
        query,
        response
    )