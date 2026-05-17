def route_issue(issue_type):

    routing_table = {

        "vpn issue": "Network Team",

        "printer issue": "Hardware Support",

        "email issue": "Messaging Team",

        "network issue": "Network Team",

        "authentication issue": "Identity & Access Management",

        "performance issue": "Desktop Support",

        "device boot failure": "Infrastructure Team"

    }

    return routing_table.get(
        issue_type,
        "General IT Support"
    )