        
import os
from typing import Union, List
from typing import TypedDict
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, END, START
from dotenv import load_dotenv

load_dotenv()


class AgentState(TypedDict):
    messages: List[Union[HumanMessage, AIMessage]]

llm = ChatOpenAI(model="gpt-4o")

def process(state: AgentState) -> AgentState:
    """This node will solve the request you input"""
    system = SystemMessage(content="You are a helpful assistant.")
    messages_with_system = [system] + state["messages"]
    response = llm.invoke(messages_with_system)
    state["messages"].append(AIMessage(content=response.content))
    return state


graph = StateGraph(AgentState)
graph.add_node("process", process)
graph.add_edge(START, "process")
graph.add_edge("process", END)
agent = graph.compile()


conversation_history = []

print("Chat started! Type 'exit' to quit.\n")
user_input = input("You: ")

while user_input != "exit":
    conversation_history.append(HumanMessage(content=user_input))

    result = agent.invoke({"messages": conversation_history})

    conversation_history = result["messages"]

    print(f"AI: {conversation_history[-1].content}\n")

    user_input = input("You: ")

# ── Save to file 
os.makedirs("logs", exist_ok=True) 

with open("logs/logging.txt", "a") as file:
    file.write("Your conversation log:\n")
    for message in conversation_history:
        if isinstance(message, HumanMessage):
            file.write(f"You: {message.content}\n")
        elif isinstance(message, AIMessage):
            file.write(f"AI: {message.content}\n")
    file.write("End of conversation\n")
    file.write("-" * 40 + "\n")  

print(f"Conversation saved to logs/logging.txt")
print(f"File location: {os.getcwd()}/logs/logging.txt")  