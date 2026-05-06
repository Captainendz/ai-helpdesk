import streamlit as st
from classifier import classify_issue
from rag import search_solution
from glpi_api import create_ticket
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

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        enriched_issue = f"""
Time: {timestamp}
Original complaint: {issue}
Predicted support level: {level}
Predicted priority: {priority}
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
                    content=enriched_issue
                )

                st.success(f"Ticket created in GLPI. Ticket ID: {result.get('id')}")

        else:
            st.error("Escalation required.")

            result = create_ticket(
                title="AI Helpdesk Escalation",
                content=enriched_issue
            )

            st.success(f"Ticket created in GLPI. Ticket ID: {result.get('id')}")