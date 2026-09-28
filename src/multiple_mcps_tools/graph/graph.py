from langgraph.graph import END, START, StateGraph

from multiple_mcps_tools.graph.graph_state import GraphState
from multiple_mcps_tools.graph.nodes.agent_node import agent_node
from multiple_mcps_tools.graph.nodes.intent_node import intent_node
from multiple_mcps_tools.services.open_router_service import OpenRouterService


def build_chat_graph(open_router_service: OpenRouterService):
    workflow = StateGraph(GraphState)

    workflow.add_node("intent_parser", intent_node(open_router_service))
    workflow.add_node("agent", agent_node(open_router_service))

    workflow.add_edge(START, "intent_parser")
    workflow.add_conditional_edges(
        "intent_parser",
        lambda state: END if state.get("error") else "agent",
        {"end": END, "agent": "agent"},
    )

    workflow.add_edge("agent", END)

    return workflow.compile()
