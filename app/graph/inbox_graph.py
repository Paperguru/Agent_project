from typing import TypedDict

from langgraph.graph import END, START, StateGraph

from app.agents.inbox_agent import(
    analyze_inbox_item,
    build_inbox_items,
)

from app.schemas.inbox import InboxAnalysis, InboxItem

class InboxState(TypedDict, total=False):
    content:str
    source:str

    analysis: InboxAnalysis
    inbox_item: InboxItem

    error: str

def analyze_node(state:InboxState) -> InboxState:
    analysis = analyze_inbox_item(
        content=state["content"],
        source=state.get("source","manual"),
    )

    return {
        "analysis": analysis,
    }

def build_item_node(state: InboxState) -> InboxState:
    item = build_inbox_items(
        content=state["content"],
        source=state.get("source","mnaual"),
        analysis=state["analysis"]
    )

    return {
        "inbox_item": item,
    }

def build_inbox_graph():
    graph = StateGraph(InboxState)

    graph.add_node("analyze",analyze_node)
    graph.add_node("build", build_item_node)

    graph.add_edge(START, "analyze")
    graph.add_edge("analyze","build")
    graph.add_edge("build", END)

    return graph.compile()

inbox_graph= build_inbox_graph()