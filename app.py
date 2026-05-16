import streamlit as st
from ai.llm_generator import generate_response
from ai.classifier import classify_issue
from rag.document_rag import search_documents
from api.glpi_api import create_ticket
from ai.enrichment import enrich_issue
from datetime import datetime

st.set_page_config(page_title="AI Helpdesk", layout="wide")

st.title("🤖 AI Helpdesk + GLPI")

# ---------- User Inputs ----------
issue = st.text_area("Describe your IT problem:")
sender_email = st.text_input("Sender email:")

# ---------- Submit ----------
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

        # ---------- Search Document Vector DB ----------
        document_result = search_documents(issue)

        # ---------- Semantic Issue Typing ----------
        if document_result:

            solution_text = document_result["content"].lower()
            ai_response = generate_response(
                issue,
                solution_text
            )

            if "vpn" in solution_text:
                enriched["issue_type"] = "vpn issue"

            elif "printer" in solution_text:
                enriched["issue_type"] = "printer issue"

            elif "outlook" in solution_text or "mail" in solution_text:
                enriched["issue_type"] = "email issue"

            elif "network" in solution_text or "wifi" in solution_text:
                enriched["issue_type"] = "network issue"

            elif "password" in solution_text or "login" in solution_text:
                enriched["issue_type"] = "authentication issue"

            elif "slow" in solution_text or "performance" in solution_text:
                enriched["issue_type"] = "performance issue"

            elif "boot" in solution_text or "startup" in solution_text:
                enriched["issue_type"] = "device boot failure"

        # ---------- Display Enrichment ----------
        st.subheader("Enriched Request")

        st.write(f"Resolved From: {enriched['resolution_source']}")
        st.write(f"User: {enriched['user']}")
        st.write(f"Device: {enriched['device']}")
        st.write(f"Issue Type: {enriched['issue_type']}")
        st.write(f"Urgency: {enriched['urgency']}")
        st.write(f"Summary: {enriched['summary']}")

        # ---------- Ticket Content ----------
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

            if document_result:

                st.success("AI can attempt Level 1 resolution.")

                st.subheader("Knowledge Source")
                st.write(document_result["source"])

                st.subheader("AI Generated Resolution")
                st.write(ai_response)

                st.subheader("Knowledge Base Match")
                st.write(document_result["content"])

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