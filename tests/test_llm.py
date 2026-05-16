from ai.llm_generator import generate_response

issue = "VPN not connecting remotely"

knowledge = """
Verify internet connection then reconnect VPN client.
"""

response = generate_response(issue, knowledge)

print("\nAI Response:\n")
print(response)