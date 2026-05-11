from glpi_lookup import find_user, find_computer_by_keyword


def enrich_issue(issue, level, priority):
    text = issue.lower()

    issue_type = "general issue"
    username = "unknown"
    device = "unknown"

    # ---------- Detect user ----------
    if "ceo" in text:
        user = find_user("ceo")
    elif "finance" in text:
        user = find_user("finance.manager")
    else:
        user = find_user("normal")

    if user:
        username = user["name"]

    # ---------- Detect device ----------
    if "ceo" in text:
        computer = find_computer_by_keyword("CEO")
    elif "finance" in text:
        computer = find_computer_by_keyword("FINANCE")
    elif "hr" in text:
        computer = find_computer_by_keyword("HR")
    elif "smc" in text:
        computer = find_computer_by_keyword("SMC_IT")
    elif "data" in text or "ai" in text:
        computer = find_computer_by_keyword("DATA")
    else:
        computer = None

    if computer:
        device = computer["name"]

    # ---------- Detect issue type ----------
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
        "device": device,
        "issue_type": issue_type,
        "urgency": priority,
        "summary": summary,
        "original_complaint": issue
    }

    return enriched