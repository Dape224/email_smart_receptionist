# 📬 Inbox Autopilot — The AI Receptionist

**An autonomous email-routing agent that reads your Gmail, files every message into the right department, and pings a human on Slack the moment something needs attention.**

Every morning, an inbox is a battlefield: invoices, job applications, security alerts, newsletters, and spam — all dumped into one pile. A human has to read, sort, and escalate each one. **Inbox Autopilot does it for you, 24/7, for free.**

---

## ✨ What It Does

1.  **👂 Listens** to a real Gmail inbox over IMAP (with IDLE push support).
2.  **🧠 Routes** each email to the right department using a LangGraph **multi-way router** (Structured Output).
3.  **📝 Summarizes** with a *specialized handler* per department — a finance analyst for invoices, an IT analyst for outages, etc.
4.  **🏷️ Labels** the email in Gmail (Sport / Finance / Tech / Applications / Misc).
5.  **🚨 Escalates** high-risk mail: applies a "Needs Review" label, stars the email, and posts a contextual alert to **Slack**.
6.  **☁️ Runs itself** as a scheduled cloud pipeline on **GitHub Actions** (every 10 minutes, free).

---

## 🏗️ Architecture (The Routing Pattern)

```
        ┌──────────────────────────────┐
        │   Gmail Inbox (IMAP + IDLE)  │
        └──────────────┬───────────────┘
                       ▼
               [ router_node ]   ← Pydantic Structured Output
                       │
   ┌─────────┬─────────┼─────────┬───────────┐
   ▼         ▼         ▼         ▼           ▼
[sport]  [finance]   [tech] [applications] [misc]   ← specialized handlers
   └─────────┴─────────┬─────────┴───────────┘
                       ▼
        [ Gmail Labels + Slack Escalation ]
```

Unlike a simple chain (where every email takes the same path), this uses the **Routing pattern**: each email travels down *exactly one* road, chosen dynamically, then all roads converge (**fan-in**) into the action layer.

---

## 🤖 The Intelligence Layer

| Stage | What happens |
|---|---|
| **Router** | Classifies into `sport / finance / tech / applications / misc` with reasoning. |
| **Handlers** | Each department extracts `summary`, `key_points`, `human_review`, `review_reason`. |
| **Escalation logic** | Rule-based triggers (e.g. payment > $500, phishing indicators, interview invites). |

Everything is enforced with **Pydantic Structured Output** (`Literal` enums + `bool`), so the LLM can never return messy, unparseable data.

---

## 🦾 The "Arms & Legs" (Real-World Integrations)

The brain is only half the product. This agent *acts* on the world:

*   **Gmail Labels** — In IMAP, a Gmail label is a folder. The agent `copy()`s each email into its category folder to apply the colored label.
*   **Needs Review + Star** — High-risk mail is copied to a "Needs Review" label and flagged.
*   **Slack Webhook** — `human_review == True` triggers a formatted alert with the exact reason, e.g.:
    > 🚨 **HUMAN REVIEW REQUIRED**
    > **From:** billing@vendor.com
    > **Reason:** Payment exceeds $500

---

## ☁️ Deployment — Serverless & Free

No $5 server. No laptop left open. The agent runs as a **GitHub Actions cron job**:

```yaml
on:
  schedule:
    - cron: '*/10 * * * *'   # every 10 minutes
  workflow_dispatch:          # manual trigger for testing
```

GitHub spins up a Linux runner, installs dependencies, injects secrets, processes the inbox, and shuts down. **Zero maintenance.**

---

## 🚀 Run It Yourself

**1. Prerequisites**
*   Python 3.10+
*   A Gmail account with **IMAP enabled** + an **App Password** (2-Step Verification required)
*   A Slack **Incoming Webhook**

**2. Environment (`.env` — never commit this!)**
```
EMAIL=you@gmail.com
EMAIL_APP_PASSWORD=abcdefghijklmnop
ESCALATION_WEBHOOK=https://hooks.slack.com/services/...
MISTRAL_API_KEY=sk-...
```

**3. Local run**
```bash
pip install -r requirements.txt
python mail_reader.py
```

**4. Cloud secrets** — add the same values under **Settings → Secrets → Actions** on GitHub.

---

## 🧠 Key Engineering Lessons Baked In

*   **Routing vs. Chaining** — multi-way conditional edges, not a fixed pipeline.
*   **Gmail labels = IMAP folders** — label by `copy()`, not by flags.
*   **Structured Output** — Pydantic schemas make LLM output deterministic.
*   **Defensive programming** — `.get()` fallbacks, `.replace(" ", "")` on App Passwords, auto-reconnect on dropped IMAP connections.
*   **Secrets management** — GitHub Secrets, never `.env` in git.

---

## 🗺️ Roadmap

- [ ] Auto-create **Jira / Zendesk tickets** for the tech & support desks (LangChain Tools)
- [ ] Persistent memory across sessions (Postgres checkpointer)
- [ ] Web dashboard to view the routed inbox

---

**Built by Oladapo** · Part of a structured AI-engineering curriculum — *Project 2: The Receptionist*