import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from retriever import retrieve_docs
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

load_dotenv()

llm = ChatGoogleGenerativeAI(
    model = "gemini-3.1-flash",
    temperature = 0.3,
    google_api_key = os.getenv("GOOGLE_API_KEY")
)

prompt = PromptTemplate(
    input_variables=["context", "question"],
    template="""
You are a helpful AI assistant.

Answer only from the given context.

If answer is not present,
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

while True:

    query = input("\nAsk: ")

    if query.lower() == "exit":
        break

    # RETRIEVE DOCS
    docs = retrieve_docs(query)

    # MAKE CONTEXT
    context = "\n\n".join([
        doc.page_content
        for doc in docs
    ])

    # GET RESPONSE
    response = chain.invoke({
        "context": context,
        "question": query
    })
    print("\nAnswer:\n")
    print(response)