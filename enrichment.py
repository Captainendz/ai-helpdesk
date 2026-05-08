from glpi_lookup import find_user


def enrich_issue(issue, level, priority):
    text = issue.lower()

    issue_type = "general issue"
    device = "unknown"

    if "laptop" in text or "pc" in text or "computer" in text:
        device = "computer"

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