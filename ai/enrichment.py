from api.glpi_lookup import (
    find_user_by_email,
    find_user_computer
)


def enrich_issue(sender_email, issue, level, priority):

    text = issue.lower()

    issue_type = "general issue"

    username = "unknown"

    device = "unknown"

    user_id = None

    # ---------- Identify sender ----------
    user = find_user_by_email(sender_email)

    if user:

        username = user["name"]

        user_id = user["id"]

    # ---------- Dynamic GLPI asset lookup ----------
    if user:

        computer = find_user_computer(user["id"])

    else:

        computer = None

    if computer:

        device = computer["name"]

    # ---------- Intelligent Issue Typing ----------
    if (
        "email" in text
        or "outlook" in text
        or "mail" in text
    ):

        issue_type = "email issue"

    elif (
        "vpn" in text
        or "remote access" in text
    ):

        issue_type = "vpn issue"

    elif (
        "wifi" in text
        or "network" in text
    ):

        issue_type = "network issue"

    elif "printer" in text:

        issue_type = "printer issue"

    elif (
        "password" in text
        or "login" in text
        or "log in" in text
        or "log into" in text
        or "sign in" in text
        or "signin" in text
    ):

        issue_type = "authentication issue"

    elif (
        "slow" in text
        or "performance" in text
    ):

        issue_type = "performance issue"

    elif (
        "boot" in text
        or "start" in text
        or "dead" in text
    ):

        issue_type = "device boot failure"

    # ---------- Summary ----------
    summary = issue[:80]

    # ---------- Final enrichment object ----------
    enriched = {

        "user": username,

        "user_id": user_id,

        "device": device,

        "issue_type": issue_type,

        "urgency": priority,

        "summary": summary,

        "original_complaint": issue,

        "resolution_source": sender_email
    }

    return enriched