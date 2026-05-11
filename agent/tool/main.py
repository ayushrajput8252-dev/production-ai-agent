"""
Main entry point for running the Tool Agent locally.
For FastAPI server, use: python -m agent.api
"""

from agent.tool.agent import run_tool_agent


def main():
    """Run the Tool Agent in interactive mode."""
    print("\n" + "="*50)
    print("OpenEyes - Tool Agent")
    print("="*50 + "\n")
    
    print("Available features:")
    print("  - Query: General queries and business requirements")
    print("  - Feedback: Customer feedback and reviews")
    print("  - Career: Job matching and career assistance")
    print("  - Task: Task assignment to employees")
    print("\nType 'exit' to quit.\n")
    
    while True:
        try:
            query = input("Enter your query: ").strip()
            
            if not query:
                print("Please enter a valid query.\n")
                continue
            
            if query.lower() == "exit":
                print("\nGoodbye!")
                break
            
            result = run_tool_agent(query)
            print(f"\nResult: {result}\n")
            
        except KeyboardInterrupt:
            print("\n\nExiting...")
            break
        except Exception as e:
            print(f"\nError: {str(e)}\n")


if __name__ == "__main__":
    main()

