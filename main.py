from langgraph.graph import START, END, StateGraph
from state import RouterState
from router import router_node
from handler import tech_handler, applications_handler, misc_handler, finance_handler, sport_handler


def report(state: RouterState) -> dict:
    print(state['category'])
    print(state['key_points'])
    print(state['summary'])
    if state['human_review']:
        print(state["review_reason"])
    return {}

def router_func(state: RouterState):
    c = state.get("category", "miscellaneous")
    if c == "sport": return "sport"
    elif c == "finance": return "finance"
    elif c == "tech": return "tech"
    elif c == "applications": return "applications"
    else: return "miscellaneous"
    

graph = StateGraph(RouterState)

graph.add_node("route", router_node)
graph.add_node("tech", tech_handler)
graph.add_node("applications", applications_handler)
graph.add_node("misc", misc_handler)
graph.add_node("finance", finance_handler)
graph.add_node("sport", sport_handler)
graph.add_node("report", report)

graph.add_edge(START, "route")
graph.add_conditional_edges(
    "route",
    router_func,
    {
        "sport": "sport",
        "finance": "finance",
        "tech": "tech", 
        "applications": "applications", 
        "miscellaneous": "misc"
    }
)
graph.add_edge("sport", "report")
graph.add_edge("finance", "report")
graph.add_edge("tech", "report")
graph.add_edge("applications", "report")
graph.add_edge("misc", "report")
graph.add_edge("report", END)

agent = graph.compile()


if __name__ == "__main__":

    r = agent.invoke({
    "email_subject": "Your weekly team standings",
    "email_body": "Your fantasy team scored 82 points this week. You're in 3rd place.",
    "sender": "updates@fantasysports.com",
    })
    print(r["category"], "|", r["human_review"])
    print(r["category"], "|", r["human_review"], "|", r["review_reason"])
