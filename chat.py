import streamlit as st
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
from langchain_groq import ChatGroq

st.set_page_config(page_title="Ai Chatbot by Deepak", page_icon="🤖")
st.header("🤖 Ai Chatbot By Deepak kumar Harwani")

# --- Ask for API key using a form ---
if "api_key" not in st.session_state:
    st.session_state.api_key = None

if st.session_state.api_key is None:
    with st.form("api_key_form"):
        api_input = st.text_input("Enter your Groq API Key", type="password")
        submitted = st.form_submit_button("Submit")
      
        
        if submitted and api_input.strip() != "":
            st.session_state.api_key = api_input.strip()
            st.success("API key set! You can now start chatting.")
            st.balloons() 
          
# --- Initialize model only if API key is set ---
if st.session_state.api_key:
    model = ChatGroq(
        model="llama-3.3-70b-versatile",
        groq_api_key=st.session_state.api_key
    )

    # --- Sidebar: Dark / Light mode toggle & Clear Chat button ---
    mode = st.sidebar.radio("Theme", ["Dark"])
    if st.sidebar.button("🗑️ Clear Chat"):
        st.session_state.history = [SystemMessage(content="You are a helpful assistant.")]
        st.toast("Chat cleared!")


    if mode == "Dark":
        user_color = "#000000"  # blue user bubble
        ai_color = "#702CE7"    # green AI bubble
        bg_color = "#1e1e1e"
        text_color = "wheat"
    else:
        user_color = "#D0E6FF"  # light blue user bubble
        ai_color = "#C8F7C5"    # light green AI bubble
        bg_color = "#ffffff"
        text_color = "#000000"

    # Apply background color
    st.markdown(
        f"""
        <style>
        .stApp {{ background-color: {bg_color}; color: {text_color}; }}
        .stMarkdown p {{ color: {text_color}; }}
        </style>
        """,
        unsafe_allow_html=True
    )

    # --- Initialize chat history ---
    if "history" not in st.session_state:
        st.session_state.history = [SystemMessage(content="You are a helpful assistant.")]

    # --- Chat container ---
    chat_container = st.container()

    # Display chat messages with colored bubbles
    with chat_container:
        for msg in st.session_state.history:
            if isinstance(msg, HumanMessage):
                with st.chat_message("user"):
                    st.markdown(
                        f"<div style='background-color:{user_color}; color:{text_color}; padding:10px; border-radius:15px; max-width:70%; margin-left:auto; margin-bottom:5px'>{msg.content}</div>",
                        unsafe_allow_html=True
                    )
            elif isinstance(msg, AIMessage):
                with st.chat_message("assistant"):
                    st.markdown(
                        f"<div style='background-color:{ai_color}; color:{text_color}; padding:10px; border-radius:15px; max-width:70%; margin-right:auto; margin-bottom:5px'>{msg.content}</div>",
                        unsafe_allow_html=True
                    )

    # --- Chat input ---
    user_input = st.chat_input("Type your message...")

    if user_input:
        # Show user message instantly
        with chat_container:
            with st.chat_message("user"):
                st.markdown(
                    f"<div style='background-color:{user_color}; color:{text_color}; padding:10px; border-radius:15px; max-width:70%; margin-left:auto; margin-bottom:5px'>{user_input}</div>",
                    unsafe_allow_html=True
                )

        st.session_state.history.append(HumanMessage(content=user_input))

        # Get AI response
        response = model.invoke(st.session_state.history)
        st.session_state.history.append(AIMessage(content=response.content))

        # Show AI response
        with chat_container:
            with st.chat_message("assistant"):
                st.markdown(
                    f"<div style='background-color:{ai_color}; color:{text_color}; padding:10px; border-radius:15px; max-width:70%; margin-right:auto; margin-bottom:5px'>{response.content}</div>",
                    unsafe_allow_html=True
                )
