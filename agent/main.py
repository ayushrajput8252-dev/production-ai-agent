from agent import app

while True:

    query = input("\nEnter Query: ").strip()
    if not query:
        continue
    if query.lower() == "exit":
        print("Exiting.")
        break

    result = app.invoke({
        "query": query
    })

    print("\nResult:")
    print(result["result"])