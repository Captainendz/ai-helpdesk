import json
import faiss
import numpy as np

from sentence_transformers import SentenceTransformer

# ---------- Load embedding model ----------
model = SentenceTransformer("all-MiniLM-L6-v2")

# ---------- Load knowledge base ----------
with open("knowledge_base.json", "r") as file:
    knowledge_base = json.load(file)

# ---------- Load FAISS index ----------
index = faiss.read_index("knowledge_index.faiss")


def faiss_search(issue):

    # ---------- Convert issue into embedding ----------
    query_vector = model.encode([issue])

    # ---------- Convert to numpy ----------
    query_vector = np.array(query_vector).astype("float32")

    # ---------- Search vector database ----------
    distances, indices = index.search(query_vector, 1)

    # ---------- Get best match ----------
    best_match_index = indices[0][0]

    best_distance = distances[0][0]

    print("Best vector distance:", best_distance)

    # ---------- Distance threshold ----------
    if best_distance < 1.5:

        solution = knowledge_base[best_match_index]["solution"]

        return solution

    return "No semantic solution found. Please escalate."