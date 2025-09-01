import uuid
import streamlit as st
from langchain_core.messages import HumanMessage, ToolMessage, AIMessage
from langgraph_helper import retrieve_all_threads, chatbot

def generate_threadId():
    """Generates Thread ID for chat."""
    return uuid.uuid4()

def add_thread(thread_id: str):
    """

    Add current Thread-ID in chat_threads.
    Args:
        thread_id (str): Thread-ID of the conversation
    """
    if thread_id not in st.session_state["chat_threads"]:
        st.session_state["chat_threads"].append(thread_id)

def reset_chat():
    """Helpful for starting new chat."""
    thread_id = generate_threadId()
    st.session_state["thread_id"] = thread_id
    add_thread(thread_id)
    st.session_state["chat_history"] = []

def load_conversation(thread_id: str):
    """
    Load Conversation on the basis of Thread-ID.
    Args:
        thread_id(str): Thread-ID of the conversation
    """
    state = chatbot.get_state(config={"configurable": {"thread_id": thread_id}})
    return state.values.get("messages", [])

# Initialize session state
if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []

if "thread_id" not in st.session_state:
    st.session_state["thread_id"] = generate_threadId()

if "chat_threads" not in st.session_state:
    st.session_state["chat_threads"] = retrieve_all_threads()

add_thread(st.session_state["thread_id"])

# Sidebar
st.sidebar.title("Chatbot")
if st.sidebar.button("New Chat"):
    reset_chat()

st.sidebar.header("Conversations:")
for thread_id in st.session_state["chat_threads"][::-1]:
    if st.sidebar.button(str(thread_id)):
        st.session_state["thread_id"] = thread_id
        messages = load_conversation(thread_id=thread_id)
        temp_messages = []
        for message in messages:
            role = "user" if isinstance(message, HumanMessage) else "assistant"
            temp_messages.append({"role": role, "content": message.content})
        st.session_state["chat_history"] = temp_messages

# Render chat history
for message in st.session_state["chat_history"]:
    with st.chat_message(message["role"]):
        st.text(message["content"])

# User input
user_input = st.chat_input("Ask...")
if user_input:
    st.session_state["chat_history"].append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.text(user_input)

    CONFIG = {
        "configurable": {"thread_id": str(st.session_state["thread_id"])},
        "metadata":{"thread_id": str(st.session_state["thread_id"])},
        "run_name": str(uuid.uuid4())
        
    }

    with st.chat_message("assistant"):
        
        status_holder = {"box": None}

        def stream_ai_content():
            
            for message_chunk, metadata in chatbot.stream(
                {"messages": [HumanMessage(content=user_input)]},
                config=CONFIG,
                stream_mode="messages"
            ):
                if isinstance(message_chunk, ToolMessage):
                    tool_name = getattr(message_chunk, "name", "tool")
                    if status_holder["box"] is None:
                        status_holder['box'] = st.status(
                            f"Using tool: {tool_name}", expanded=True
                        )
                    else:
                        status_holder["box"].update(
                            label=f"Using tool: {tool_name}",
                            state="running",
                            expanded=True
                        )
                if isinstance(message_chunk, AIMessage):
                    yield message_chunk.content or ""  

        # Stream output
        ai_message = st.write_stream(stream_ai_content())

        # Update status box
        if status_holder["box"] is not None:
            status_holder["box"].update(
                label="Tool Finished",
                expanded=False,
                state="complete"
            )

    st.session_state["chat_history"].append(
        {"role": "assistant", "content": ai_message}
    )
