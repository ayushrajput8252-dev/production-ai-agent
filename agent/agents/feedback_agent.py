from dotenv import load_dotenv
import os
from langchain_openai import ChatOpenAI

try:
    from agent.mail import send_mail
except ModuleNotFoundError:
    from mail import send_mail

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


def feedback_agent(user_query):

    prompt = f"""
    Analyze the feedback sentiment.

    Types:
    - good
    - bad

    Return only one word.

    Feedback:
    {user_query}
    """

    try:
        sentiment = llm.invoke(prompt).content.strip().lower()
    except Exception:
        sentiment = "bad"

    # ==========================================
    # GOOD FEEDBACK
    # ==========================================

    if sentiment == "good":

        ok, err = send_mail("support@theOpenEyes.com", "Positive Customer Feedback", user_query)
        if ok:
            if err:
                return f"Good feedback mail sent ({err})"
            return "Good feedback mail sent"
        return f"Good feedback detected, but mail failed: {err}"

    # ==========================================
    # BAD FEEDBACK
    # ==========================================

    else:

        ok, err = send_mail("support@theOpenEyes.com", "Negative Customer Feedback", user_query)
        if ok:
            if err:
                return f"Bad feedback mail sent ({err})"
            return "Bad feedback mail sent"
        return f"Bad feedback detected, but mail failed: {err}"

