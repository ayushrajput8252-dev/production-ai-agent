import json
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"


def load_employee_data():
    with open(DATA_DIR / "employee.json", "r", encoding="utf-8") as f:
        return json.load(f)
    

def load_career_data():
    with open(DATA_DIR / "careers.json", "r", encoding="utf-8") as f:
        return json.load(f)
    

def calculate_match(resume_text, skills):

    matched = 0

    for skill in skills:

        if skill.lower() in resume_text.lower():
            matched += 1

    score = (matched / len(skills)) * 100

    return score