from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
import os

from agent.tool.mail import send_mail

load_dotenv()

llm = ChatOpenAI(
    model=os.getenv(
        "GROQ_MODEL",
        "llama-3.3-70b-versatile"
    ),
    temperature=0.3,
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)


def query_agent(user_query: str) -> str:
    """
    Process general queries and route them to appropriate recipients via email.
    
    Args:
        user_query: The user's query
    
    Returns:
        Response indicating the action taken
    """

    prompt = f"""
    Classify query.
    Return only:
    - general
    - high
    - normal

    Query:
    {user_query}
    """

    try:
        query_type = (
            llm.invoke(prompt)
            .content
            .strip()
            .lower()
        )
    except Exception:
        query_type = "normal"

    # =========================
    # GENERAL QUERY
    # =========================

    if query_type == "general":

        try:
            message = llm.invoke(
                f"Summarize in 2 lines:\n{user_query}"
            ).content

        except Exception:
            message = user_query

        receiver = "query@theopeneyes.com"
        subject = "General Query"

    # =========================
    # HIGH PRIORITY QUERY
    # =========================

    else:

        receiver = (
            "trushantmehta@gmail.com"
            if query_type == "high"
            else "query@theopeneyes.com"
        )

        subject = "Business Requirement"
        message = user_query

    # =========================
    # SEND MAIL
    # =========================

    ok, err = send_mail(
        receiver,
        subject,
        message
    )

    if ok:
        return f"Mail sent to {receiver}"

    return f"Mail failed: {err}"