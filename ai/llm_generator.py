import re


def generate_response(issue, knowledge):

    # ---------- Split knowledge into lines ----------
    lines = knowledge.splitlines()

    # ---------- Remove duplicates ----------
    unique_steps = []

    seen = set()

    for line in lines:

        cleaned = line.strip()

        # ---------- Remove numbering ----------
        cleaned = re.sub(
            r"^\d+[\.\)]\s*",
            "",
            cleaned
        )

        # ---------- Remove bullet points ----------
        cleaned = re.sub(
            r"^[\-\*\•]\s*",
            "",
            cleaned
        )

        lower_cleaned = cleaned.lower()

        # ---------- Ignore weak/useless lines ----------
        if (
            cleaned
            and "guide" not in lower_cleaned
            and "if " not in lower_cleaned
            and len(cleaned) > 8
            and "authentication failure" not in lower_cleaned
            and "timeout connection" not in lower_cleaned
            and "gateway unreachable" not in lower_cleaned
            and "common vpn errors" not in lower_cleaned
        ):

            # ---------- Remove duplicates ----------
            if lower_cleaned not in seen:

                unique_steps.append(cleaned)

                seen.add(lower_cleaned)

    # =====================================================
    # Dependency-Aware Troubleshooting Ordering
    # =====================================================

    infrastructure_steps = []

    authentication_steps = []

    application_steps = []

    other_steps = []

    for step in unique_steps:

        lower_step = step.lower()

        # ---------- Infrastructure / Network ----------
        if (
            "internet" in lower_step
            or "vpn" in lower_step
            or "network" in lower_step
            or "connectivity" in lower_step
            or "connection" in lower_step
        ):

            infrastructure_steps.append(step)

        # ---------- Authentication ----------
        elif (
            "credential" in lower_step
            or "password" in lower_step
            or "login" in lower_step
            or "mfa" in lower_step
            or "authentication" in lower_step
            or "sign in" in lower_step
        ):

            authentication_steps.append(step)

        # ---------- Application Layer ----------
        elif (
            "outlook" in lower_step
            or "mailbox" in lower_step
            or "printer" in lower_step
            or "storage quota" in lower_step
            or "email" in lower_step
        ):

            application_steps.append(step)

        else:

            other_steps.append(step)

    # ---------- Final Ordered Steps ----------
    ordered_steps = (
        infrastructure_steps
        + authentication_steps
        + application_steps
        + other_steps
    )

    # ---------- Build Final Response ----------
    response = (
        "Recommended Troubleshooting Steps:\n\n"
    )

    for i, step in enumerate(ordered_steps):

        response += f"{i+1}. {step}\n"

    return response