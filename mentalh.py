import streamlit as st
from langchain_openai import OpenAI

# Page Config
st.set_page_config(
    page_title="Mental Health Assistant",
    page_icon="🌸"
)

st.title("🌸 Mental Health Chatbot")

# Session State
if "messages" not in st.session_state:
    st.session_state.messages = []

if "api_key" not in st.session_state:
    st.session_state.api_key = ""

# Sidebar
with st.sidebar:
    st.header("✨ Wellness Corner")
    if st.button("🧼 Clear Chat"):
        st.session_state.messages = []
        st.rerun()

# STEP 1: API KEY INPUT
if not st.session_state.api_key:

    st.info("Enter your OpenAI API Key to start")

    user_key = st.text_input("API Key 🔑", type="password")

    if st.button("Start Chat"):
        if user_key.strip():
            st.session_state.api_key = user_key.strip()
            st.success("API Key Added ✅")
            st.rerun()
        else:
            st.error("Enter valid API key")

# STEP 2: CHAT
else:

    client = OpenAI(api_key=st.session_state.api_key)

    # System message (mental health)
    SYSTEM_MSG = {
        "role": "system",
        "content": "You are a kind and supportive mental health assistant. Only answer mental health related queries."
    }

    # Show chat history
    for msg in st.session_state.messages:
        if msg["role"] == "user":
            with st.chat_message("user"):
                st.write(msg["content"])
        else:
            with st.chat_message("assistant"):
                st.write(msg["content"])

    # Input
    if prompt := st.chat_input("How are you feeling today?"):

        # Save user message
        st.session_state.messages.append({"role": "user", "content": prompt})

        with st.chat_message("user"):
            st.write(prompt)

        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):

                try:
                    response = client.chat.completions.create(
                        model="gpt-4o-mini",
                        messages=[SYSTEM_MSG] + st.session_state.messages
                    )

                    reply = response.choices[0].message.content

                    st.write(reply)

                    # Save AI reply
                    st.session_state.messages.append(
                        {"role": "assistant", "content": reply}
                    )

                except Exception as e:
                    st.error(f"Error: {e}")