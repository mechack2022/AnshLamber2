from langchain_core.messages import SystemMessage, BaseMessage, ToolMessage  
from langchain_core.messages import HumanMessage, AIMessage                  
from langchain_core.tools import tool                                        
from typing import TypedDict, Annotated, Sequence
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, END, START
from langgraph.prebuilt import ToolNode
from langgraph.graph.message import add_messages
from dotenv import load_dotenv

load_dotenv()

class AgentState(TypedDict):
    messages : Annotated[Sequence[BaseMessage], add_messages]

@tool
def add(a: int, b: int):
    """ addition function that add two numbers"""
    return a+b

tools =[add]    

model = ChatOpenAI(model="gpt-4o").bind_tools(tools)

def model_call(state:AgentState)-> AgentState:
    system_prompt = SystemMessage(content="You are my AI agent please answer my question to the best to the best of your ability")
    response = model.invoke([system_prompt] + list(state["messages"]))  
    return {"messages" : [response]}


def should_continue(state: AgentState):
    messages = state["messages"]
    last_message= messages[-1]
    if not last_message.tool_calls:
        return "end"
    else:
        return "continue"    

graph = StateGraph(AgentState)
graph.add_node("our_agent", model_call)       

tool_node = ToolNode(tools=tools)
graph.add_node("tool_node", tool_node)                

graph.add_edge(START, "our_agent") 

graph.add_conditional_edges(
    "our_agent",
    should_continue,
    {
        "continue": "tool_node",
        "end": END
    }
)

graph.add_edge("tool_node", "our_agent") 
app = graph.compile();

def print_stream(stream):
    for s in stream:
        message = s["messages"][-1]
        if isinstance(message, tuple):
            print(message)
        else:
            message.pretty_print()


inputs = {"messages": [("user", "Add 3 + 4")]}
print_stream(app.stream(inputs, stream_mode="values"))                