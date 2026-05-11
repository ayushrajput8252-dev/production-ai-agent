from typing import TypedDict
from langgraph.graph import StateGraph, END

from agent.tool.sub_agent.career import career_agent
from agent.tool.sub_agent.feedback import feedback_agent
from agent.tool.sub_agent.query import query_agent
from agent.tool.sub_agent.supervisor import supervisor_agent
from agent.tool.sub_agent.task import task_agent


class AgentState(TypedDict):
    """State structure for the Tool Agent graph."""
    query: str
    route: str
    result: str


def supervisor_node(state: AgentState) -> dict:
    """Route the query to appropriate sub-agent."""
    route = supervisor_agent(state["query"])

    # Validate route
    valid_routes = {"query", "feedback", "career", "task"}
    if route not in valid_routes:
        route = "query"

    return {"route": route}


def query_node(state: AgentState) -> dict:
    """Process through query sub-agent."""
    return {
        "result": query_agent(state["query"])
    }


def feedback_node(state: AgentState) -> dict:
    """Process through feedback sub-agent."""
    return {
        "result": feedback_agent(state["query"])
    }


def career_node(state: AgentState) -> dict:
    """Process through career sub-agent."""
    return {
        "result": career_agent(state["query"])
    }


def task_node(state: AgentState) -> dict:
    """Process through task sub-agent."""
    return {
        "result": task_agent(state["query"])
    }


def router(state: AgentState) -> str:
    """Router function to determine next node."""
    return state["route"]


# Build the LangGraph
graph = StateGraph(AgentState)

# Add nodes
graph.add_node("supervisor", supervisor_node)
graph.add_node("query", query_node)
graph.add_node("feedback", feedback_node)
graph.add_node("career", career_node)
graph.add_node("task", task_node)

# Set entry point
graph.set_entry_point("supervisor")

# Add conditional edges for routing
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

# Add edges to END
graph.add_edge("query", END)
graph.add_edge("feedback", END)
graph.add_edge("career", END)
graph.add_edge("task", END)

# Compile the graph
tool_agent_graph = graph.compile()


def run_tool_agent(query: str) -> str:
    """
    Run the Tool Agent on a query.
    
    Args:
        query: User query
    
    Returns:
        Result from the appropriate sub-agent
    """
    try:
        state = {"query": query, "route": "", "result": ""}
        output = tool_agent_graph.invoke(state)
        return output.get("result", "No result")
    except Exception as e:
        return f"Error in tool agent: {str(e)}"