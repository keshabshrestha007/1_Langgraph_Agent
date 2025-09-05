from typing import TypedDict,Annotated,List,Literal
from dotenv import load_dotenv
import sqlite3
import os

from tools import *
from toolnode import BasicToolNode

from langchain_core.messages import BaseMessage,HumanMessage
from langchain_groq import ChatGroq

from langgraph.graph.message import add_messages
from langgraph.graph import StateGraph,START,END
from langgraph.checkpoint.sqlite import SqliteSaver



load_dotenv()
groq_api_key = st.secrets["GROQ_API_KEY"]
if not groq_api_key:
    raise ValueError("GROQ_API_KEY not set.")


tools = [search_tool,write_to_file,read_file,read_pdf,write_pdf,append_to_file,search_arxiv]
# Initialize LLM
llm = ChatGroq(
            model="llama-3.3-70b-versatile",
            temperature=0.2,
            api_key=groq_api_key,
        )
llm_with_tools = llm.bind_tools(tools = tools)

class ChatConfig(TypedDict):
    """ Represents state of the graph.
        Attributes:
            messages(list) -> list of Basemessages
    """
    messages : Annotated[List[BaseMessage], add_messages]

# Initialize StateGraph
graph = StateGraph(ChatConfig)

conn = sqlite3.connect("chat_history.db",check_same_thread=False)
saver = SqliteSaver(conn)

def chat_node(state:ChatConfig) -> ChatConfig:
    response = llm_with_tools.invoke(state["messages"])
    return {"messages":[response]}

def tools_router(state:ChatConfig) -> Literal["tool_node","__end__"]:
    last_message = state["messages"][-1]
    if hasattr(last_message,"tool_calls") and last_message.tool_calls:
        return "tool_node"
    else:
        return END
    
tool_node = BasicToolNode(tools=tools)

graph.add_node("chat_node",chat_node)
graph.add_node("tool_node",tool_node)
graph.add_edge(START,"chat_node")
graph.add_conditional_edges("chat_node",tools_router)
graph.add_edge("tool_node","chat_node")

chatbot = graph.compile(checkpointer=saver)


def retrieve_all_threads():
    all_threads = set()
    for checkpoint in saver.list(None):
        all_threads.add(checkpoint.config["configurable"]["thread_id"])
    return list(all_threads)

if __name__ == "__main__":
    # Example usage
    response = chatbot.invoke(
        {"messages":[HumanMessage(content="What is LangGraph?")]},
        config = {"configurable":{"thread_id":"test_thread_1"}}
        
        
    )

    print(response)

