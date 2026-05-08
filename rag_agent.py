import os

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from memory import save_chat, load_memory
from retriever import retrieve_docs

load_dotenv()
# =========================
# GEMINI MODEL
# =========================

llm = ChatOpenAI(
    model=os.getenv("GROQ_MODEL"),
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

try:
    session_id = input("Session ID: ").strip()
except EOFError:
    print("\nExiting chat.")
    raise SystemExit(0)

if not session_id:
    session_id = "default"

while True:

    try:
        query = input("\nAsk: ").strip()
    except EOFError:
        print("\nExiting chat.")
        break

    if not query:
        continue
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

    try:
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
    except Exception as exc:
        print("\nError while generating response:")
        print(exc)