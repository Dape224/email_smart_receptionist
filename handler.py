from llm import model
from state import RouterState, DepartmentExtraction


def finance_handler(state: RouterState):
    body = state.get('email_body', '')
    subject= state.get("email_subject", "")

    agent= model()
    structured_llm= agent.with_structured_output(DepartmentExtraction)

    prompt = f"""
    You are an expert Financial Analyst and Security Auditor. Analyze this financial email
(invoices, payment requests, bank alerts, tax documents) and extract the key information.

### Escalation Logic for human_review
Set human_review to true ONLY if at least one high-risk trigger is met:
1. The email requests, demands, invoices, or references a payment or transfer GREATER THAN $500.
2. The email resembles a suspicious, urgent, or potentially fraudulent banking alert
   (unexpected password resets, unusual login locations, unverified wire confirmations, phishing).
Otherwise set human_review to false. Always explain your decision in review_reason.

REPLY DECISION:
- needs_reply: True ONLY if the sender expects a response (a question, a request,
  an application awaiting acknowledgment, an invoice needing confirmation).
  Newsletters / notifications / FYI = False.
- draft_reply: If needs_reply is True, write the IDEAL reply. It must directly
  reflect the sender's actual message — acknowledge their specific points and
  answer their questions. Write in first person as Oladapo. No generic templates.

### Input Data
Subject: {subject}
Body: {body}

"""

    output = structured_llm.invoke(prompt)

    return {
        "summary": output.summary,
        "key_points": output.key_points,
        "human_review": output.human_review,
        "review_reason": output.review_reason,
        "needs_reply": output.needs_reply,   
        "draft_reply": output.draft_reply,  
    }


def tech_handler(state: RouterState):
    body = state.get('email_body', '')
    subject = state.get('email_subject', '')

    agent = model()
    structured_llm = agent.with_structured_output(DepartmentExtraction)

    prompt = f"""
You are an expert Tech/IT Analyst. Analyze this technology email (software updates,
security patches, bug reports, API changes, service outages) and extract key information.

### Escalation Logic for human_review
Set human_review to true ONLY if:
1. It reports a CRITICAL security vulnerability or data breach.
2. It announces a service outage or downtime affecting active systems.
3. It requires an urgent technical action (e.g., rotate API keys, patch immediately).
Otherwise set human_review to false. Always explain your decision in review_reason.

REPLY DECISION:
- needs_reply: True ONLY if the sender expects a response (a question, a request,
  an application awaiting acknowledgment, an invoice needing confirmation).
  Newsletters / notifications / FYI = False.
- draft_reply: If needs_reply is True, write the IDEAL reply. It must directly
  reflect the sender's actual message — acknowledge their specific points and
  answer their questions. Write in first person as Oladapo. No generic templates.

### Input Data
Subject: {subject}
Body: {body}
"""
    output = structured_llm.invoke(prompt)
    return {
        "summary": output.summary,
        "key_points": output.key_points,
        "human_review": output.human_review,
        "review_reason": output.review_reason,
        "needs_reply": output.needs_reply,   
        "draft_reply": output.draft_reply,  
    }


def sport_handler(state: RouterState):
    body = state.get('email_body', '')
    subject = state.get('email_subject', '')

    agent = model()
    structured_llm = agent.with_structured_output(DepartmentExtraction)

    prompt = f"""
You are a Sports Desk Analyst. Analyze this sports email (match updates, scores, team
news, fitness activity, sports gear) and extract key information.

### Escalation Logic for human_review
Set human_review to true ONLY if:
1. It involves a payment or purchase (tickets, gear) of notable amount.
2. It announces a schedule change requiring immediate action (match moved, booking deadline).
Otherwise set human_review to false. Always explain your decision in review_reason.

REPLY DECISION:
- needs_reply: True ONLY if the sender expects a response (a question, a request,
  an application awaiting acknowledgment, an invoice needing confirmation).
  Newsletters / notifications / FYI = False.
- draft_reply: If needs_reply is True, write the IDEAL reply. It must directly
  reflect the sender's actual message — acknowledge their specific points and
  answer their questions. Write in first person as Oladapo. No generic templates.

### Input Data
Subject: {subject}
Body: {body}
"""
    output = structured_llm.invoke(prompt)
    return {
        "summary": output.summary,
        "key_points": output.key_points,
        "human_review": output.human_review,
        "review_reason": output.review_reason,
        "needs_reply": output.needs_reply,   
        "draft_reply": output.draft_reply,  
    }


def applications_handler(state: RouterState):
    body = state.get('email_body', '')
    subject = state.get('email_subject', '')

    agent = model()
    structured_llm = agent.with_structured_output(DepartmentExtraction)

    prompt = f"""
You are an Applications & Requests Tracker. Analyze this email about job applications,
admissions, submitted forms, or service account updates (GitHub, Spotify, Google).

### Escalation Logic for human_review
Set human_review to true ONLY if:
1. It is an interview invite, admission/acceptance decision, or offer.
2. It requires an action or has a deadline (verify email, complete application, respond by date).
3. It reports a rejected or failed request that needs follow-up.
Otherwise set human_review to false. Always explain your decision in review_reason.

REPLY DECISION:
- needs_reply: True ONLY if the sender expects a response (a question, a request,
  an application awaiting acknowledgment, an invoice needing confirmation).
  Newsletters / notifications / FYI = False.
- draft_reply: If needs_reply is True, write the IDEAL reply. It must directly
  reflect the sender's actual message — acknowledge their specific points and
  answer their questions. Write in first person as Oladapo. No generic templates.

### Input Data
Subject: {subject}
Body: {body}
"""
    output = structured_llm.invoke(prompt)
    return {
        "summary": output.summary,
        "key_points": output.key_points,
        "human_review": output.human_review,
        "review_reason": output.review_reason,
        "needs_reply": output.needs_reply,   
        "draft_reply": output.draft_reply,  
    }


def misc_handler(state: RouterState):
    body = state.get('email_body', '')
    subject = state.get('email_subject', '')

    agent = model()
    structured_llm = agent.with_structured_output(DepartmentExtraction)

    prompt = f"""
You are a General Triage Assistant. Analyze this miscellaneous email (personal chat,
store promotions, spam, or anything that doesn't fit the other categories).

### Escalation Logic for human_review
Set human_review to true ONLY if:
1. It appears to be a legal, government, or official notice.
2. It is an urgent personal matter that doesn't fit other categories.
3. It is clearly NOT spam but its importance is uncertain (better safe than sorry).
Otherwise set human_review to false (treat promotions/spam as no review needed).
Always explain your decision in review_reason.

REPLY DECISION:
- needs_reply: True ONLY if the sender expects a response (a question, a request,
  an application awaiting acknowledgment, an invoice needing confirmation).
  Newsletters / notifications / FYI = False.
- draft_reply: If needs_reply is True, write the IDEAL reply. It must directly
  reflect the sender's actual message — acknowledge their specific points and
  answer their questions. Write in first person as Oladapo. No generic templates.

### Input Data
Subject: {subject}
Body: {body}
"""
    output = structured_llm.invoke(prompt)
    return {
        "summary": output.summary,
        "key_points": output.key_points,
        "human_review": output.human_review,
        "review_reason": output.review_reason,
        "needs_reply": output.needs_reply,   
        "draft_reply": output.draft_reply,  
    }