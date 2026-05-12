import json


def load_knowledge_base():

    with open("knowledge_base.json", "r") as file:
        return json.load(file)


def search_solution(issue):

    text = issue.lower()

    knowledge_base = load_knowledge_base()

    for item in knowledge_base:

        keyword = item["keyword"]
        solution = item["solution"]

        if keyword in text:
            return solution

    return "No direct solution found. Please escalate."