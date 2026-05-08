try:
    from agent.utils import load_employee_data
    from agent.mail import send_mail
except ModuleNotFoundError:
    from utils import load_employee_data
    from mail import send_mail


def task_agent(user_query):

    employees = load_employee_data()

    for employee in employees:

        if employee["name"].lower() in user_query.lower():

            ok, err = send_mail(
                employee["email"],
                "New Task Assigned",
                user_query
            )
            if ok:
                if err:
                    return f"Task assigned to {employee['name']} ({err})"
                return f"Task assigned to {employee['name']}"
            return f"Task matched for {employee['name']}, but mail failed: {err}"

    return "Employee not found"