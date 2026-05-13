from rag.semantic_rag import semantic_search

issue = input("Enter issue: ")

result = semantic_search(issue)

print("\nSuggested Solution:")

print(result)