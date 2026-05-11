from agent.tool.utils import load_career_data, calculate_match
from agent.tool.mail import send_mail


def career_agent(user_query: str) -> str:
    """
    Match user skills against available job positions.
    
    Args:
        user_query: User query containing skills or requirements
    
    Returns:
        String response with job matching result
    """
    try:
        jobs = load_career_data()
        
        for job in jobs:
            # Get the title or job_title field
            job_title = job.get("job_title") or job.get("title", "Unknown")
            job_skills = job.get("skills", [])
            
            if not job_skills:
                continue
                
            score = calculate_match(user_query, job_skills)

            if score >= 70:
                send_mail(
                    "hr@openeyes.com",
                    "Candidate Selected",
                    f"""
Candidate matched

Role: {job_title}
Score: {score:.1f}%
                    """
                )

                return f"You matched for {job_title}, response sent to hr"

        return "No matching jobs found, kindly visit again"
    except Exception as e:
        return f"Error in career agent: {str(e)}"