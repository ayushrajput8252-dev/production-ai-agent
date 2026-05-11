from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
import os
from agent.tool.mail import send_mail

load_dotenv()

llm = ChatOpenAI(
    model=os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile"),
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1",
    temperature=0.3
)


def feedback_agent(user_query: str) -> str:
    """
    Process customer feedback and classify sentiment.
    
    Args:
        user_query: The customer feedback
    
    Returns:
        Response indicating feedback has been recorded
    """

    prompt = f"""
    Classify sentiment as:
    good or bad

    Feedback:
    {user_query}
    """

    try:
        sentiment = llm.invoke(prompt).content.strip().lower()
    except Exception:
        sentiment = "bad"

    subject = (
        "Positive Customer Feedback"
        if sentiment == "good"
        else "Negative Customer Feedback"
    )

    ok, err = send_mail(
        "feedback@theopeneyes.com",
        subject,
        user_query
    )

    if ok:
        return f"{sentiment.capitalize()} feedback mail sent"

    return f"Mail failed: {err}"