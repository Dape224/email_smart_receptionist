from state import RouteDecision, RouterState
from llm import model

def router_node(state: RouterState):
    
    subject = state.get('email_subject', '')
    body = state.get('email_body', '')
    sender = state.get('sender', '')
    

    agent = model()
    structured_llm = agent.with_structured_output(RouteDecision)

    prompt = f"""
    ### Role
    You are an advanced email classification assistant. Analyze the metadata and content of an incoming email and classify it into exactly one of five predefined categories.

    ### Predefined Categories
    1. "sport": Athletic events, team updates, scores, sports gear, fitness.
    2. "finance": Banking, investments, stocks, crypto, invoices, bills, taxes.
    3. "tech": Software updates, gadgets, programming, IT, AI, cybersecurity, tech news.
    4. "applications": Job applications, admissions, software API integrations, or status updates from services (e.g., github.com, spotify.com).
    5. "miscellaneous": Casual personal chat, general spam, store promotions, or anything not fitting above.

    ### Instructions
    - Read the Sender, Subject, and Body carefully.
    - Rely on the context of the message and the sender's domain.
    - Explain your reasoning briefly before selecting the final category.


    ### Input Data:
    Sender: {sender}
    Subject: {subject}
    Body: {body}
    """
    output=structured_llm.invoke(prompt)

    return {
        "category": output.category
    }
