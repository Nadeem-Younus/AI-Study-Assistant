# AI-Study-Assistant
AI based study assistant/planner

The system uses three LangGraph nodes. The classify node identifies user intent, the tool node routes execution to one of three integrated tools (study planner, Wikipedia API, Dictionary API), and the response node formats the final output. Memory is maintained through LangGraph checkpointing.

# Selected Use Case

This project is an AI-powered study planning assistant that helps users:
- Generate structured study plans (e.g., 5-day plans)
- Get definitions of terms
- Fetch Wikipedia summaries
- Provide unified responses through a conversational interface
The system interprets user intent dynamically and routes queries to the appropriate tool using a stateful LangGraph workflow.

# Tools Used
- Python 🐍
- LangGraph (stateful workflow engine)
- Gradio (interactive web UI)
- Wikipedia API (wikipedia-api)
- Requests (external API calls)
- Dotenv (environment variable management)
- OpenAI Generative AI SDK (Open API integration)

# APIs Integrated
1. Google Gemini API (via google.genai)
  - Used for generating study plans
2. Dictionary API
  - https://api.dictionaryapi.dev/
- Used for word definitions
3. Wikipedia API
  - Used for retrieving article summaries

# LangGraph Workflow Explanation
State Structure
The workflow maintains state using:
State = {
    user_input: str,
    intent: str,
    result: str
}

# Workflow Steps
User Input
   ↓
[Classify Node]
   ↓
(Intent Detection: plan / define / wiki)
   ↓
[Tool Node]
   ↓
(Calls appropriate external tool/API)
   ↓
[Response Node]
   ↓
Formatted AI Response
   ↓
Gradio UI Output

# Nodes Explained
1. Classify Node
   - Detects user intent
   - Classifies into:
      Study Plan → "plan"
      Definition → "define"
      Wikipedia → "wiki"

2. Tool Node
   Executes appropriate tool:
    - Plan Tool → Gemini API generates study plan
    - Dictionary Tool → Fetches meaning via API
    - Wikipedia Tool → Retrieves summary
  
3. Response Node
   Formats output into readable structure
   Ensures consistent UI response

# Memory Implementation
The system uses LangGraph MemorySaver checkpointing:
from langgraph.checkpoint.memory import MemorySaver

How it works:
  Stores session state using thread_id
  Enables continuity across user queries
  Maintains conversational context per session

Example: config={"configurable": {"thread_id": "student-session-1"}}

# How to Run the Application
1. Install dependencies
   pip install gradio langgraph wikipedia-api requests python-dotenv google-generativeai
2. Set environment variables
   Create a .env file: GOOGLE_API_KEY=your_api_key_here or OPENAI_API_KEY=your_api_key_here
3. Run the app
   python app.py
4. Open in browser
   Gradio will provide: Local URL or shared URL if interface share=True

# Example Prompts
1. Study Planning
    “Create a study plan for Python programming”
    “Help me plan 5 days for learning machine learning”
2. Definitions
    “Define recursion”
    “What is an algorithm?”
3. Wikipedia
    “Python programming”
    “Artificial intelligence”

# Challenges Faced
  - Integration mismatch between Google Gemini and OpenAI-style APIs
  - LangGraph state inconsistency causing missing outputs
  - Wikipedia API returning empty summaries for some queries
  - Debugging silent failures in Gradio UI
  - Handling dynamic intent classification reliably
  - Ensuring proper state propagation between nodes

<img width="113" height="447" alt="image" src="https://github.com/user-attachments/assets/233dc3fe-0573-4566-8261-8a0146f86bf3" />


