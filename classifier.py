def classify_issue(issue):
    text = issue.lower()

    # -------- Support Level --------
    l1_keywords = [
        "password", "reset", "wifi", "printer",
        "email", "vpn", "login"
    ]

    l23_keywords = [
        "server", "database", "network outage",
        "blue screen", "security breach",
        "switch", "application crash"
    ]

    # Default level
    support_level = "L1"

    for word in l23_keywords:
        if word in text:
            support_level = "L2/L3"

    for word in l1_keywords:
        if word in text:
            support_level = "L1"

    # -------- Priority --------
    priority = "Medium"

    critical_keywords = [
        "down", "urgent", "cannot work",
        "outage", "ceo", "director",
        "critical", "production", "security breach"
    ]

    low_keywords = [
        "slow", "later", "minor",
        "toner", "question", "how to"
    ]

    for word in critical_keywords:
        if word in text:
            priority = "Priority"

    for word in low_keywords:
        if word in text:
            priority = "Low"

    return support_level, priority