from typing import TypedDict

from langgraph.graph import END, StateGraph

try:
    from agent.agents.career_agent import career_agent
    from agent.agents.feedback_agent import feedback_agent
    from agent.agents.query_agent import query_agent
    from agent.agents.supervisor_agent import supervisor_agent
    from agent.agents.task_agent import task_agent
except ModuleNotFoundError:
    # Fallback when running `python agent/main.py` directly.
    from agents.career_agent import career_agent
    from agents.feedback_agent import feedback_agent
    from agents.query_agent import query_agent
    from agents.supervisor_agent import supervisor_agent
    from agents.task_agent import task_agent


class AgentState(TypedDict):
    query: str
    route: str
    result: str


def supervisor_node(state: AgentState):
    route = supervisor_agent(state["query"])
    if route not in {"query", "feedback", "career", "task"}:
        route = "query"
    return {"route": route}


def query_node(state: AgentState):
    return {"result": query_agent(state["query"])}


def feedback_node(state: AgentState):
    return {"result": feedback_agent(state["query"])}


def career_node(state: AgentState):
    return {"result": career_agent(state["query"])}


def task_node(state: AgentState):
    return {"result": task_agent(state["query"])}


graph = StateGraph(AgentState)
graph.add_node("supervisor", supervisor_node)
graph.add_node("query", query_node)
graph.add_node("feedback", feedback_node)
graph.add_node("career", career_node)
graph.add_node("task", task_node)
graph.set_entry_point("supervisor")


def router(state: AgentState):
    return state["route"]


graph.add_conditional_edges(
    "supervisor",
    router,
    {
        "query": "query",
        "feedback": "feedback",
        "career": "career",
        "task": "task",
    },
)

graph.add_edge("query", END)
graph.add_edge("feedback", END)
graph.add_edge("career", END)
graph.add_edge("task", END)

app = graph.compile()