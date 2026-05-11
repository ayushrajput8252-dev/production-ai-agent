import json
from pathlib import Path
from typing import List, Dict, Any


BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"


def load_employee_data() -> List[Dict[str, Any]]:
    """Load employee data from JSON file."""
    try:
        with open(DATA_DIR / "employee.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        return []

    
def load_career_data() -> List[Dict[str, Any]]:
    """Load career data from JSON file."""
    try:
        with open(DATA_DIR / "careers.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        return []
    

def calculate_match(resume_text: str, skills: List[str]) -> float:
    """
    Calculate skill match percentage.
    
    Args:
        resume_text: The resume or skills text
        skills: List of required skills
    
    Returns:
        Match percentage (0-100)
    """
    if not skills:
        return 0.0

    matched = 0
    for skill in skills:
        if skill.lower() in resume_text.lower():
            matched += 1

    score = (matched / len(skills)) * 100
    return score