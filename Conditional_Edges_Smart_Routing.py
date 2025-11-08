from dotenv import load_dotenv
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END
from openai import OpenAI
from typing import Optional, Literal
import google.generativeai as genai
import os

load_dotenv()

client = OpenAI()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

class State(TypedDict):
    user_query: str
    llm_output: Optional[str]
    is_good: Optional[bool]

def chatbot(state: State):
    print("ChatBot Node: ", state)
    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {"role": "user", "content": state.get("user_query")}
        ]
    )

    state["llm_output"] = response.choices[0].message.content
    return state

def evaluate_response(state: State) -> Literal["chatbot_gemini", "endnode"]:
    print("Evaluate Response Node: ", state)
    
    evaluation_prompt = f"""
    Evaluate the following response to the user query. Determine if it's accurate, helpful, and complete.
    
    User Query: {state.get("user_query")}
    Response: {state.get("llm_output")}
    
    Reply with only "GOOD" if the response is satisfactory, or "BAD" if it needs improvement.
    """
    
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "user", "content": evaluation_prompt}
        ]
    )
    
    evaluation = response.choices[0].message.content.strip().upper()
    state["is_good"] = evaluation == "GOOD"
    
    if state["is_good"]:
        return "endnode"
    
    return "chatbot_gemini"

def chatbot_gemini(state: State):
    print("ChatBot Gemini Node: ", state)
    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content(state.get("user_query"))

    state["llm_output"] = response.text
    return state

def endnode(state: State):
    print("END Node: ", state)
    return state

graph_builder = StateGraph(State)

graph_builder.add_node("chatbot", chatbot)
graph_builder.add_node("chatbot_gemini", chatbot_gemini)
graph_builder.add_node("endnode", endnode)

graph_builder.add_edge(START, "chatbot")
graph_builder.add_conditional_edges("chatbot", evaluate_response)

graph_builder.add_edge("chatbot_gemini", "endnode")
graph_builder.add_edge("endnode", END)

graph = graph_builder.compile()

updated_state = graph.invoke(State({"user_query": "Hey, what is 2 + 2 ? "}))
print(updated_state)

