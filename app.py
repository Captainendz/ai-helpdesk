import streamlit as st
from ai.router import route_issue
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

        # ---------- Confidence Threshold ----------
        CONFIDENCE_THRESHOLD = 1.0

        # =========================================================
        # IMPORTANT:
        # DO NOT overwrite issue_type using document_result content
        # The enrichment.py already detects issue type correctly
        # from the user's original complaint.
        # =========================================================

        # ---------- Department Routing ----------
        department = route_issue(
            enriched["issue_type"]
        )

        # ---------- Display Enrichment ----------
        st.subheader("Enriched Request")

        st.write(f"Resolved From: {enriched['resolution_source']}")
        st.write(f"User: {enriched['user']}")
        st.write(f"Device: {enriched['device']}")
        st.write(f"Issue Type: {enriched['issue_type']}")
        st.write(f"Assigned Department: {department}")
        st.write(f"Urgency: {enriched['urgency']}")
        st.write(f"Summary: {enriched['summary']}")

        # ---------- Ticket Content ----------
        ticket_content = f"""
Time: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
User: {enriched['user']}
Device: {enriched['device']}
Issue Type: {enriched['issue_type']}
Assigned Department: {department}
Urgency: {enriched['urgency']}
Summary: {enriched['summary']}
Original Complaint: {enriched['original_complaint']}
"""

        # ---------- L1 AI Resolution ----------
        if level == "L1":

            if (
                document_result
                and document_result["distance"] < CONFIDENCE_THRESHOLD
            ):

                st.success(
                    "AI found a reliable knowledge base match."
                )

                st.write(
                    f"Vector Distance: "
                    f"{document_result['distance']:.3f}"
                )

                # ---------- Generate AI Resolution ----------
                ai_response = generate_response(
                    issue,
                    document_result["content"]
                )

                st.subheader("AI Generated Resolution")
                st.write(ai_response)

                st.subheader("Knowledge Source")
                st.write(document_result["source"])

            else:

                st.warning(
                    "No reliable AI resolution found."
                )

                st.error(
                    "Escalating issue to GLPI."
                )

                result = create_ticket(
                    title="AI Helpdesk Escalation",
                    content=ticket_content,
                    user_id=enriched["user_id"]
                )

                if "id" in result:

                    st.success(
                        f"Ticket created in GLPI. "
                        f"Ticket ID: {result.get('id')}"
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
                    f"Ticket created in GLPI. "
                    f"Ticket ID: {result.get('id')}"
                )

            else:

                st.error("Ticket creation failed.")