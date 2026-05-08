from utils import load_career_data, calculate_match
from mail import send_mail


def career_agent(user_query):

    jobs = load_career_data()

    for job in jobs:

        score = calculate_match(
            user_query,
            job["skills"]
        )

        if score >= 70:

            ok, err = send_mail(
                "info@theOpenEyes.com",
                "Candidate Selected",
                f"""
Candidate matched

Role: {job['title']}

Score: {score}
                """
            )
            if ok:
                if err:
                    return f"Candidate matched for {job['title']} ({err})"
                return f"Candidate matched for {job['title']}"
            return f"Candidate matched for {job['title']}, but mail failed: {err}"

    return "No matching jobs found"