from api.glpi_lookup import (
    find_user_by_email,
    find_user_computer
)


def enrich_issue(sender_email, issue, level, priority):

    text = issue.lower()

    issue_types = []

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

    # ---------- Multi-Issue Detection ----------

    if (
        "email" in text
        or "outlook" in text
        or "mail" in text
    ):

        issue_types.append("email issue")

    if (
        "vpn" in text
        or "remote access" in text
    ):

        issue_types.append("vpn issue")

    if (
        "wifi" in text
        or "network" in text
    ):

        issue_types.append("network issue")

    if "printer" in text:

        issue_types.append("printer issue")

    if (
        "password" in text
        or "login" in text
        or "log in" in text
        or "log into" in text
        or "sign in" in text
        or "signin" in text
    ):

        issue_types.append("authentication issue")

    if (
        "slow" in text
        or "performance" in text
    ):

        issue_types.append("performance issue")

    if (
        "boot" in text
        or "start" in text
        or "dead" in text
    ):

        issue_types.append("device boot failure")

    # ---------- Default ----------
    if not issue_types:

        issue_types.append("general issue")

    # ---------- Primary Issue ----------
    primary_issue = issue_types[0]

    # ---------- Summary ----------
    summary = issue[:80]

    # ---------- Final enrichment object ----------
    enriched = {

        "user": username,

        "user_id": user_id,

        "device": device,

        "issue_type": primary_issue,

        "all_issue_types": issue_types,

        "urgency": priority,

        "summary": summary,

        "original_complaint": issue,

        "resolution_source": sender_email
    }

    return enriched