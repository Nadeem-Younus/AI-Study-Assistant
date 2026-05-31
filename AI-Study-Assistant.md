AI-Study-Assistant

AI based study assistant/planner

The system uses three LangGraph nodes. The classify node identifies user intent, the tool node routes execution to one of three integrated tools (study planner, Wikipedia API, Dictionary API), and the response node formats the final output. Memory is maintained through LangGraph checkpointing.
Selected Use Case

This project is an AI-powered study planning assistant that helps users:

    Generate structured study plans (e.g., 5-day plans)
    Get definitions of terms
    Fetch Wikipedia summaries
    Provide unified responses through a conversational interface The system interprets user intent dynamically and routes queries to the appropriate tool using a stateful LangGraph workflow.

Tools Used

    Python 🐍
    LangGraph (stateful workflow engine)
    Gradio (interactive web UI)
    Wikipedia API (wikipedia-api)
    Requests (external API calls)
    Dotenv (environment variable management)
    OpenAI Generative AI SDK (Open API integration)

APIs Integrated

    Google Gemini API (via google.genai)
        Used for generating study plans
    Dictionary API
        https://api.dictionaryapi.dev/
        Used for word definitions
    Wikipedia API
        Used for retrieving article summaries

LangGraph Workflow Explanation

State Structure The workflow maintains state using: State = { user_input: str, intent: str, result: str }
Workflow Steps

User Input ↓ [Classify Node] ↓ (Intent Detection: plan / define / wiki) ↓ [Tool Node] ↓ (Calls appropriate external tool/API) ↓ [Response Node] ↓ Formatted AI Response ↓ Gradio UI Output
Nodes Explained

    Classify Node
        Detects user intent
        Classifies into: Study Plan → "plan" Definition → "define" Wikipedia → "wiki"

    Tool Node Executes appropriate tool:
        Plan Tool → Gemini API generates study plan
        Dictionary Tool → Fetches meaning via API
        Wikipedia Tool → Retrieves summary

    Response Node Formats output into readable structure Ensures consistent UI response

Memory Implementation

The system uses LangGraph MemorySaver checkpointing: from langgraph.checkpoint.memory import MemorySaver

How it works: Stores session state using thread_id Enables continuity across user queries Maintains conversational context per session

Example: config={"configurable": {"thread_id": "student-session-1"}}
How to Run the Application

    Install dependencies pip install gradio langgraph wikipedia-api requests python-dotenv google-generativeai
    Set environment variables Create a .env file: GOOGLE_API_KEY=your_api_key_here or OPENAI_API_KEY=your_api_key_here
    Run the app python app.py
    Open in browser Gradio will provide: Local URL or shared URL if interface share=True

Example Prompts

    Study Planning “Create a study plan for Python programming” “Help me plan 5 days for learning machine learning”
    Definitions “Define recursion” “What is an algorithm?”
    Wikipedia “Python programming” “Artificial intelligence”

Challenges Faced

    Integration mismatch between Google Gemini and OpenAI-style APIs
    LangGraph state inconsistency causing missing outputs
    Wikipedia API returning empty summaries for some queries
    Debugging silent failures in Gradio UI
    Handling dynamic intent classification reliably
    Ensuring proper state propagation between nodes

image