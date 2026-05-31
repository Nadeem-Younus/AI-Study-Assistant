from typing import TypedDict
import os
import wikipediaapi
import requests
import gradio as gr
from dotenv import load_dotenv
from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver
from openai import OpenAI


# =========================
# Load API Key
# =========================
load_dotenv()

client =   OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


# =========================
# TOOL 1: Study Plan
# =========================
def plan_tool(topic):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are an AI Study Planner."},
            {"role": "user", "content": f"Create a 5-day study plan for {topic}"}
        ]
    )

    return response.choices[0].message.content


# =========================
# TOOL 2: Wikipedia
# =========================
def wiki_tool(query):
    """Search Wikipedia for a given query."""
    wiki = wikipediaapi.Wikipedia(
        user_agent="study-assistant",
        language="en"
    )

    page = wiki.page(query)

    if page.exists():
        return page.summary[:500]

    return "Page not found."


# =========================
# TOOL 3: Dictionary
# =========================
def dictionary_tool(word):
    url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}"

    res = requests.get(url)

    if res.status_code == 200:
        return res.json()[0]["meanings"][0]["definitions"][0]["definition"]

    return "No definition found."


# =========================
# STATE
# =========================
class State(TypedDict):
    user_input: str
    intent: str
    result: str


# =========================
# Classifier Node
# =========================
def classify_node(state):
    text = state["user_input"].lower()

    if "plan" in text or "study" in text:
        return {"intent": "plan"}

    elif "define" in text:
        return {"intent": "define"}

    return {"intent": "wiki"}


# =========================
# Tool Node
# =========================
def tool_node(state: State):
    try:
        query = state["user_input"]
        intent = state["intent"]

        if intent == "plan":
            result = plan_tool(query)

        elif intent == "define":
            result = dictionary_tool(query)

        else:
            result = wiki_tool(query)

        return {"result": result}

    except Exception as e:
        return {"result": f"Tool Error: {str(e)}"}

# =========================
# Response Node
# =========================
def response_node(state: State):
    result = state.get("result", "")

    if not result:
        result = "No result generated (empty output). Try a different query."

    return {
        "result": f"""
        AI Study Assistant
        
        Query: {state.get('user_input')}
        Intent: {state.get('intent')}
        
        Result:
        {result}"""
        }


# =========================
# Build Graph
# =========================
memory = MemorySaver()

graph = StateGraph(State)

graph.add_node("classify", classify_node)
graph.add_node("tool", tool_node)
graph.add_node("response", response_node)

graph.set_entry_point("classify")
graph.add_edge("classify", "tool")
graph.add_edge("tool", "response")
graph.add_edge("response", END)

app = graph.compile(checkpointer=memory)


# =========================
# Run Agent
# =========================
def run_agent(user_input):
    try:
        result = app.invoke(
            {"user_input": user_input},
            config={"configurable": {"thread_id": "student-session"}}
        )

        print(result)   # Debug output
        return result["result"]

    except Exception as e:
        print("ERROR:", e)
        return f"System Error: {str(e)}"
    
# =========================
# Gradio UI
# =========================
interface = gr.Interface(
    fn=run_agent,
    inputs=gr.Textbox(label="Ask AI Study Assistant"),
    outputs=gr.Textbox(label="Response"),
    title="AI Study Assistant"
)


if __name__ == "__main__":
    interface.launch(share=True)