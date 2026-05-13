import json
import faiss
import numpy as np

from sentence_transformers import SentenceTransformer

# ---------- Load embedding model ----------
model = SentenceTransformer("all-MiniLM-L6-v2")

# ---------- Load knowledge base ----------
with open("knowledge_base.json", "r") as file:
    knowledge_base = json.load(file)

# ---------- Extract problem texts ----------
problems = [item["problem"] for item in knowledge_base]

# ---------- Generate embeddings ----------
embeddings = model.encode(problems)

# ---------- Convert to numpy array ----------
embedding_matrix = np.array(embeddings).astype("float32")

# ---------- Create FAISS index ----------
dimension = embedding_matrix.shape[1]

index = faiss.IndexFlatL2(dimension)

# ---------- Add embeddings to index ----------
index.add(embedding_matrix)

# ---------- Save index ----------
faiss.write_index(index, "knowledge_index.faiss")

print("FAISS index created successfully.")
print("Total vectors stored:", index.ntotal)