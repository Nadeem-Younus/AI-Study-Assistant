# AI-Study-Assistant
ai based study assistant/planner

The system uses three LangGraph nodes. The classify node identifies user intent, the tool node routes execution to one of three integrated tools (study planner, Wikipedia API, Dictionary API), and the response node formats the final output. Memory is maintained through LangGraph checkpointing.
