import os
import requests
from dotenv import load_dotenv
from imap_tools import MailBox, MailMessageFlags, AND
from main import agent  
from replier import send_reply  

load_dotenv()
EMAIL = os.getenv("EMAIL")
APP_PASSWORD = os.getenv("EMAIL_APP_PASSWORD", "").replace(" ", "")
WEBHOOK_URL = os.getenv("ESCALATION_WEBHOOK")

def send_slack_alert(sender, subject, reason, draft=""):
    if not WEBHOOK_URL: return
    payload = {"text": f"🚨 *HUMAN REVIEW REQUIRED*\n*From:* {sender}\n*Subject:* {subject}\n*Reason:* {reason}\n*Draft Reply:* {draft}"}
    try:
        requests.post(WEBHOOK_URL, json=payload, timeout=10)
        print("🔔 Escalation alert sent to Slack!")
    except Exception as e:
        print(f"Failed to send Slack alert: {e}")

def process_inbox():
    print("🚀 Waking up Email Agent...")
    try:
        with MailBox("imap.gmail.com").login(EMAIL, APP_PASSWORD, initial_folder="INBOX") as box:
            unseen_emails = list(box.fetch(AND(seen=False)))
            if not unseen_emails:
                print("📭 No new emails. Going back to sleep.")
                return

            for msg in unseen_emails:
                print(f"\n--- Processing: {msg.subject} ---")
                
                result = agent.invoke({
                    "sender": msg.from_ or "",
                    "email_subject": msg.subject or "",
                    "email_body": msg.text or msg.html or "",
                })

                category = result.get("category", "Misc").strip()
                needs_reply = result.get("needs_reply", False)
                draft_reply = result.get("draft_reply", "")
        
                msg_id_header = msg.headers.get("Message-Id", ("",))[0]

                if not box.folder.exists(category):
                    box.folder.create(category)
                box.copy([msg.uid], category)
                print(f"🏷️ Labeled as: {category}")

                if result.get("human_review", False):
                    if not box.folder.exists("Needs Review"):
                        box.folder.create("Needs Review")
                    box.copy([msg.uid], "Needs Review")
                    
                    send_slack_alert(
                        msg.from_, 
                        msg.subject, 
                        result.get("review_reason", "No reason."),
                        draft_reply 
                    )
                    print("🛡️ High-risk: Draft sent to Slack for approval (not auto-sent).")

                elif needs_reply and draft_reply:
                    try:
                        send_reply(msg.from_, msg.subject, draft_reply, msg_id_header)
             
                        if not box.folder.exists("Replied"):
                            box.folder.create("Replied")
                        box.copy([msg.uid], "Replied")
                        print("📨 Auto-reply sent and labeled.")
                    except Exception as e:
                        print(f"❌ Failed to send auto-reply: {e}")
                        
                else:
                    print("📪 No reply needed.")

                box.flag([msg.uid], MailMessageFlags.SEEN, True)
            
            print("✅ Batch processing complete. Shutting down.")

    except Exception as e:
        print(f"⚠️ Error during execution: {e}")

if __name__ == "__main__":
    process_inbox()