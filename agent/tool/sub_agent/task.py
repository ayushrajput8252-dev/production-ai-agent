from agent.tool.utils import load_employee_data
from agent.tool.mail import send_mail


def task_agent(user_query: str) -> str:
    """
    Assign tasks to employees based on query.
    
    Args:
        user_query: The task assignment query
    
    Returns:
        Response indicating whether task was assigned
    """
    
    try:
        employees = load_employee_data()

        for employee in employees:

            employee_name = employee.get("name", "").lower()

            if employee_name and employee_name in user_query.lower():

                ok, err = send_mail(
                    employee.get("email", ""),
                    "New Task Assigned",
                    user_query
                )

                if ok:
                    return f"Task assigned to {employee.get('name', 'Unknown')}"

                return f"Mail failed: {err}"

        return "Employee not found"
    except Exception as e:
        return f"Error in task agent: {str(e)}"