from document_rag import search_documents

query = input("Ask a question: ")

result = search_documents(query)

if result:

    print("\nDOCUMENT SOURCE:")
    print(result["source"])

    print("\nRETRIEVED CONTENT:")
    print(result["content"])

else:

    print("No relevant document found.")