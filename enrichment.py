from glpi_lookup import find_user_by_email, find_computer_by_keyword


def enrich_issue(sender_email, issue, level, priority):
    text = issue.lower()

    issue_type = "general issue"
    username = "unknown"
    device = "unknown"

    # ---------- Identify sender ----------
    user = find_user_by_email(sender_email)

    if user:
        username = user["name"]

    # ---------- Device mapping ----------
    if username == "ceo":
        computer = find_computer_by_keyword("CEO")
    elif username == "finance.manager":
        computer = find_computer_by_keyword("FINANCE")
    else:
        computer = None

    if computer:
        device = computer["name"]

    # ---------- Issue type ----------
    if "wifi" in text or "network" in text:
        issue_type = "network issue"

    elif "printer" in text:
        issue_type = "printer issue"

    elif "email" in text or "outlook" in text:
        issue_type = "email issue"

    elif "vpn" in text:
        issue_type = "vpn issue"

    elif "boot" in text or "start" in text or "dead" in text:
        issue_type = "device boot failure"

    summary = issue[:80]

    enriched = {
    "user": username,
    "user_id": user["id"] if user else None,
    "device": device,
    "issue_type": issue_type,
    "urgency": priority,
    "summary": summary,
    "original_complaint": issue,
    "resolution_source": sender_email
}

    return enriched