import streamlit as st
import requests

st.title("AI Task Manager")
st.write("Chat with your AI task assistant")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Type a task request..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                response = requests.post(
                    "http://localhost:8000/chat",
                    json={"message": prompt}
                )
                reply = response.json()["reply"]
            except Exception as e:
                reply = f"Error connecting to backend: {str(e)}"
        st.markdown(reply)
    st.session_state.messages.append({"role": "assistant", "content": reply})