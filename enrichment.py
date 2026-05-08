from glpi_lookup import find_user, find_computer


def enrich_issue(issue, level, priority):
    text = issue.lower()

    issue_type = "general issue"
    detected_device = "unknown"

    if "laptop" in text or "pc" in text or "computer" in text:
        detected_device = "computer"

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

    user = find_user("normal")

    if user:
        username = user["name"]
    else:
        username = "unknown"

    computer = find_computer("CEO-LAPTOP-01")

    if computer:
        device = computer["name"]
    else:
        device = detected_device

    summary = issue[:80]

    enriched = {
        "user": username,
        "device": device,
        "issue_type": issue_type,
        "urgency": priority,
        "summary": summary,
        "original_complaint": issue
    }

    return enriched