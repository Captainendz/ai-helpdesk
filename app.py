import streamlit as st
from ai.router import route_issue
from ai.llm_generator import generate_response
from ai.classifier import classify_issue
from rag.document_rag import search_documents
from api.glpi_api import create_ticket
from ai.enrichment import enrich_issue
from ai.incident_memory import save_incident
from datetime import datetime

st.set_page_config(page_title="AI Helpdesk", layout="wide")

st.title("🤖 AI Helpdesk + GLPI")

# ---------- User Inputs ----------
issue = st.text_area("Describe your IT problem:")
sender_email = st.text_input("Sender email:")

# ---------- Submit ----------
if st.button("Submit"):

    # ---------- Reset displayed steps ----------
    st.session_state.displayed_steps = set()

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
        document_results = search_documents(issue)

        # ---------- Confidence Threshold ----------
        CONFIDENCE_THRESHOLD = 1.0

        # ---------- Department Routing ----------
        department = route_issue(
            enriched["issue_type"]
        )

        # ---------- Display Enrichment ----------
        st.subheader("Enriched Request")

        st.write(f"Resolved From: {enriched['resolution_source']}")
        st.write(f"User: {enriched['user']}")
        st.write(f"Device: {enriched['device']}")

        st.write(
            f"Primary Issue Type: "
            f"{enriched['issue_type']}"
        )

        st.write(
            f"All Detected Issues: "
            f"{', '.join(enriched['all_issue_types'])}"
        )

        st.write(f"Assigned Department: {department}")
        st.write(f"Urgency: {enriched['urgency']}")
        st.write(f"Summary: {enriched['summary']}")

        # ---------- Ticket Content ----------
        ticket_content = f"""
Time: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
User: {enriched['user']}
Device: {enriched['device']}
Primary Issue Type: {enriched['issue_type']}
All Detected Issues: {', '.join(enriched['all_issue_types'])}
Assigned Department: {department}
Urgency: {enriched['urgency']}
Summary: {enriched['summary']}
Original Complaint: {enriched['original_complaint']}
"""

        # ---------- L1 AI Resolution ----------
        if level == "L1":

            if document_results:

                # ---------- Best Match ----------
                best_result = document_results[0]

                if best_result["distance"] < CONFIDENCE_THRESHOLD:

                    st.success(
                        "AI found reliable knowledge base matches."
                    )

                    st.write(
                        f"Best Vector Distance: "
                        f"{best_result['distance']:.3f}"
                    )

                    # =====================================================
                    # Dependency-Aware Resolution Ordering
                    # =====================================================

                    priority_map = {
                        "wifi": 1,
                        "network": 1,
                        "vpn": 2,
                        "login": 3,
                        "authentication": 3,
                        "email": 4,
                        "printer": 5,
                        "performance": 6
                    }

                    def get_priority(source_name):

                        source_lower = source_name.lower()

                        for keyword, priority in priority_map.items():

                            if keyword in source_lower:

                                return priority

                        return 99

                    # ---------- Sort KB Results ----------
                    document_results.sort(
                        key=lambda x: get_priority(
                            x["source"]
                        )
                    )

                    # =====================================================
                    # STRUCTURED MULTI-ISSUE RESOLUTION
                    # =====================================================

                    st.subheader(
                        "AI Generated Resolution"
                    )

                    full_resolution = ""

                    for result in document_results:

                        source_name = result["source"]

                        knowledge = result["content"]

                        # ---------- Generate Clean Steps ----------
                        ai_response = generate_response(
                            issue,
                            knowledge
                        )

                        # =====================================================
                        # Cross-Section Deduplication
                        # =====================================================

                        filtered_lines = []

                        for line in ai_response.splitlines():

                            cleaned = line.strip()

                            # ---------- Keep Header ----------
                            if (
                                "Recommended Troubleshooting Steps"
                                in cleaned
                            ):

                                filtered_lines.append(cleaned)

                                continue

                            # ---------- Skip Empty Lines ----------
                            if not cleaned:

                                continue

                            # ---------- Normalize ----------
                            normalized = cleaned.lower()

                            normalized = normalized.lstrip(
                                "1234567890. "
                            )

                            # ---------- Skip Duplicates ----------
                            if (
                                normalized
                                not in st.session_state.displayed_steps
                            ):

                                filtered_lines.append(cleaned)

                                st.session_state.displayed_steps.add(
                                    normalized
                                )

                        # ---------- Rebuild Response ----------
                        rebuilt_response = []

                        step_counter = 1

                        for line in filtered_lines:

                            # ---------- Keep Header ----------
                            if (
                                "Recommended Troubleshooting Steps"
                                in line
                            ):

                                rebuilt_response.append(line)

                                rebuilt_response.append("")

                                continue

                            # ---------- Remove Existing Numbers ----------
                            cleaned_line = line.lstrip(
                                "1234567890. "
                            )

                            # ---------- Renumber Cleanly ----------
                            rebuilt_response.append(
                                f"{step_counter}. {cleaned_line}"
                            )

                            step_counter += 1

                        # ---------- Final Clean Response ----------
                        ai_response = "\n".join(
                            rebuilt_response
                        )

                        # ---------- Skip Empty Sections ----------
                        if (
                            ai_response.strip()
                            == "Recommended Troubleshooting Steps:"
                        ):

                            continue

                        # ---------- Dynamic Section Titles ----------
                        if "vpn" in source_name.lower():

                            section_title = (
                                "🌐 VPN / NETWORK TROUBLESHOOTING"
                            )

                        elif (
                            "email" in source_name.lower()
                        ):

                            section_title = (
                                "📧 EMAIL TROUBLESHOOTING"
                            )

                        elif (
                            "login" in source_name.lower()
                            or "authentication"
                            in source_name.lower()
                        ):

                            section_title = (
                                "🔐 AUTHENTICATION TROUBLESHOOTING"
                            )

                        elif (
                            "printer" in source_name.lower()
                        ):

                            section_title = (
                                "🖨️ PRINTER TROUBLESHOOTING"
                            )

                        elif (
                            "wifi" in source_name.lower()
                            or "network"
                            in source_name.lower()
                        ):

                            section_title = (
                                "📡 NETWORK TROUBLESHOOTING"
                            )

                        elif (
                            "performance" in source_name.lower()
                        ):

                            section_title = (
                                "⚡ PERFORMANCE TROUBLESHOOTING"
                            )

                        else:

                            section_title = (
                                "🛠️ GENERAL TROUBLESHOOTING"
                            )

                        # ---------- Combine Resolution ----------
                        section_output = (
                            f"{section_title}\n\n"
                            f"{ai_response}\n\n"
                        )

                        full_resolution += section_output

                        # ---------- Display Section ----------
                        st.text(section_output)

                    # ---------- Display Retrieved Sources ----------
                    st.subheader("Knowledge Sources Used")

                    knowledge_sources = []

                    for i, result in enumerate(document_results):

                        st.write(
                            f"{i+1}. "
                            f"{result['source']} "
                            f"(Distance: "
                            f"{result['distance']:.3f})"
                        )

                        knowledge_sources.append(
                            result["source"]
                        )

                    # =====================================================
                    # SAVE INCIDENT MEMORY
                    # =====================================================

                    save_incident(
                        user=enriched["user"],
                        device=enriched["device"],
                        issue=enriched["original_complaint"],
                        issue_types=enriched["all_issue_types"],
                        resolution=full_resolution,
                        knowledge_sources=knowledge_sources
                    )

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

            else:

                st.warning(
                    "No knowledge documents found."
                )

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