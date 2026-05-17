def generate_response(issue, knowledge):

    lines = knowledge.splitlines()

    steps = []

    for line in lines:

        cleaned = line.strip()

        if (
            cleaned
            and "guide" not in cleaned.lower()
            and "if " not in cleaned.lower()
            and len(cleaned) > 5
        ):
            steps.append(cleaned)

    response = "Recommended Troubleshooting Steps:\n\n"

    for step in steps:

        response += f"{step}\n"

    return response