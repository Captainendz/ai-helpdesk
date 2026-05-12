import streamlit as st
from classifier import classify_issue
from semantic_rag import semantic_search
from glpi_api import create_ticket
from enrichment import enrich_issue
from datetime import datetime

st.set_page_config(page_title="AI Helpdesk", layout="wide")

st.title("🤖 AI Helpdesk + GLPI")

issue = st.text_area("Describe your IT problem:")
sender_email = st.text_input("Sender email:")

if st.button("Submit"):

    if not issue.strip():
        st.warning("Please describe your issue.")

    else:

        # ---------- Classification ----------
        level, priority = classify_issue(issue)

        st.success("Issue received.")

        st.subheader("Classification Result")
        st.info(f"Support Level: {level}")
        st.info(f"Priority: {priority}")

        # ---------- Enrichment ----------
        enriched = enrich_issue(
            sender_email,
            issue,
            level,
            priority
        )

        # ---------- Semantic AI Retrieval ----------
        solution = semantic_search(issue)

        # ---------- Smarter semantic issue typing ----------
        if "vpn" in solution.lower():
            enriched["issue_type"] = "vpn issue"

        elif "printer" in solution.lower():
            enriched["issue_type"] = "printer issue"

        elif "outlook" in solution.lower() or "mail" in solution.lower():
            enriched["issue_type"] = "email issue"

        elif "network" in solution.lower() or "wifi" in solution.lower():
            enriched["issue_type"] = "network issue"

        elif "password" in solution.lower() or "login" in solution.lower():
            enriched["issue_type"] = "authentication issue"

        elif "slow" in solution.lower() or "performance" in solution.lower():
            enriched["issue_type"] = "performance issue"

        elif "boot" in solution.lower() or "startup" in solution.lower():
            enriched["issue_type"] = "device boot failure"

        # ---------- Display enrichment ----------
        st.subheader("Enriched Request")

        st.write(f"Resolved From: {enriched['resolution_source']}")
        st.write(f"User: {enriched['user']}")
        st.write(f"Device: {enriched['device']}")
        st.write(f"Issue Type: {enriched['issue_type']}")
        st.write(f"Urgency: {enriched['urgency']}")
        st.write(f"Summary: {enriched['summary']}")

        # ---------- Ticket body ----------
        ticket_content = f"""
Time: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
User: {enriched['user']}
Device: {enriched['device']}
Issue Type: {enriched['issue_type']}
Urgency: {enriched['urgency']}
Summary: {enriched['summary']}
Original Complaint: {enriched['original_complaint']}
"""

        # ---------- L1 AI Resolution ----------
        if level == "L1":

            if solution != "No semantic solution found. Please escalate.":

                st.success("AI can attempt Level 1 resolution.")

                st.subheader("Suggested Solution")
                st.write(solution)

            else:

                st.error("No Level 1 solution found. Escalating...")

                result = create_ticket(
                    title="AI Helpdesk Escalation",
                    content=ticket_content,
                    user_id=enriched["user_id"]
                )

                if "id" in result:
                    st.success(
                        f"Ticket created in GLPI. Ticket ID: {result.get('id')}"
                    )
                else:
                    st.error("Ticket creation failed.")

        # ---------- Escalation ----------
        else:

            st.error("Escalation required.")

            result = create_ticket(
                title="AI Helpdesk Escalation",
                content=ticket_content,
                user_id=enriched["user_id"]
            )

            if "id" in result:
                st.success(
                    f"Ticket created in GLPI. Ticket ID: {result.get('id')}"
                )
            else:
                st.error("Ticket creation failed.")