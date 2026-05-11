import streamlit as st
from classifier import classify_issue
from rag import search_solution
from glpi_api import create_ticket
from enrichment import enrich_issue
from datetime import datetime

st.set_page_config(page_title="AI Helpdesk", layout="wide")

st.title("🤖 AI Helpdesk + GLPI")

issue = st.text_area("Describe your IT problem:")

if st.button("Submit"):

    if not issue.strip():
        st.warning("Please describe your issue.")

    else:
        level, priority = classify_issue(issue)

        st.success("Issue received.")

        st.subheader("Classification Result")
        st.info(f"Support Level: {level}")
        st.info(f"Priority: {priority}")

        enriched = enrich_issue(issue, level, priority)

        st.subheader("Enriched Request")
        st.write(f"User: {enriched['user']}")
        st.write(f"Device: {enriched['device']}")
        st.write(f"Issue Type: {enriched['issue_type']}")
        st.write(f"Urgency: {enriched['urgency']}")
        st.write(f"Summary: {enriched['summary']}")

        ticket_content = f"""
Time: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
User: {enriched['user']}
Device: {enriched['device']}
Issue Type: {enriched['issue_type']}
Urgency: {enriched['urgency']}
Summary: {enriched['summary']}
Original Complaint: {enriched['original_complaint']}
"""

        if level == "L1":
            solution = search_solution(issue)

            if solution != "No direct solution found. Please escalate.":
                st.success("AI can attempt Level 1 resolution.")
                st.subheader("Suggested Solution")
                st.write(solution)

            else:
                st.error("No Level 1 solution found. Escalating...")

                result = create_ticket(
                    title="AI Helpdesk Escalation",
                    content=ticket_content
                )

                if "id" in result:
                    st.success(f"Ticket created in GLPI. Ticket ID: {result.get('id')}")
                else:
                    st.error("Ticket creation failed.")

        else:
            st.error("Escalation required.")

            result = create_ticket(
                title="AI Helpdesk Escalation",
                content=ticket_content
            )

            if "id" in result:
                st.success(f"Ticket created in GLPI. Ticket ID: {result.get('id')}")
            else:
                st.error("Ticket creation failed.")