from langchain_openai import ChatOpenAI
from mail import send_mail
from dotenv import load_dotenv
import os

load_dotenv()

MODEL_NAME = os.getenv(
    "GROQ_MODEL",
    "llama-3.3-70b-versatile"
)

llm = ChatOpenAI(
    model=MODEL_NAME,
    temperature=0.3,
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)
def query_agent(user_query):

    prompt = f"""
    Check query.

    Return only:
    - general
    - high
    - normal

    Rules:
    - If normal user query -> general
    - If big business/client -> high
    - Else -> normal

    Query:
    {user_query}
    """

    try:
        result = llm.invoke(prompt).content.strip().lower()
    except Exception:
        result = "normal"

    # ====================================
    # GENERAL QUERY
    # ====================================

    if result == "general":

        try:
            summary = llm.invoke(f"""
            Summarize in 2 lines:

            {user_query}
            """).content
        except Exception:
            summary = user_query

        ok, err = send_mail("normlopeyes@gmail.com", "General Query", summary)
        if ok:
            if err:
                return f"Summary mail sent ({err})"
            return "Summary mail sent"
        return f"Summary created, but mail failed: {err}"

    # ====================================
    # BUSINESS QUERY
    # ====================================

    else:

        if result == "high":
            receiver = "trushantmehta@gmail.com"
        else:
            receiver = "info@theOpenEyes.com"

        ok, err = send_mail(receiver, "Business Requirement", user_query)
        if ok:
            if err:
                return f"Mail sent to {receiver} ({err})"
            return f"Mail sent to {receiver}"
        return f"Routed to {receiver}, but mail failed: {err}"