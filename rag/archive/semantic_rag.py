import json
from sentence_transformers import SentenceTransformer, util

model = SentenceTransformer("all-MiniLM-L6-v2")


def load_knowledge_base():

    with open("knowledge_base.json", "r") as file:
        return json.load(file)


knowledge_base = load_knowledge_base()

problems = [item["problem"] for item in knowledge_base]

problem_embeddings = model.encode(
    problems,
    convert_to_tensor=True
)


def semantic_search(issue):

    issue_embedding = model.encode(
        issue,
        convert_to_tensor=True
    )

    similarities = util.cos_sim(
        issue_embedding,
        problem_embeddings
    )

    best_match_index = similarities.argmax().item()

    best_score = similarities[0][best_match_index].item()

    print("Best similarity score:", best_score)

    if best_score > 0.2:
        return knowledge_base[best_match_index]["solution"]

    return "No semantic solution found. Please escalate."