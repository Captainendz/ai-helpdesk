from rag.faiss_rag import faiss_search

issue = input("Enter issue: ")

result = faiss_search(issue)

print("\nSuggested Solution:")

print(result)