import streamlit as st
import google.generativeai as genai
import pickle
import os
import uuid

st.title('Gemini Chatbot')
if "messages" not in st.session_state:
    st.session_state["messages"] = []
if "current_uuid" not in st.session_state:
    st.session_state["current_uuid"] = str(uuid.uuid4())
    st.session_state["messages"] = []
    filename = st.session_state["current_uuid"] + ".pkl"
    with open(f"data/{filename}", "wb") as f:
        pickle.dump(st.session_state["messages"], f)

    
messages = st.session_state["messages"]
def get_response(messages, model="gemini-pro"):
    model = genai.GenerativeModel(model)
    res = model.generate_content(messages, stream=True,
                                safety_settings={'HARASSMENT':'block_none'})
    return res
def get_history_messages():
    """
    search all the pickle file in data folder
    return the list of messages
    """
    return [f for f in os.listdir("data") if f.endswith(".pkl")]
    

if st.secrets["api_key"] == "":
    st.warning("Please input the API Key in the secrets.toml file")
else:
    genai.configure(api_key=st.secrets["api_key"])
    with st.sidebar:
        st.title("Gemini API")
        select_model = st.sidebar.selectbox("Select model", ["gemini-pro"])
        if st.button("New Chat"):
            st.session_state["messages"] = []
            st.rerun()
        st.sidebar.markdown("History")
        history_files = get_history_messages()
        selected_file = st.sidebar.selectbox("Select a chat history", history_files)
        # Display chat messages
    for item in messages:
        role, parts = item.values()
        if role == "user":
            st.chat_message("user").markdown(parts[0])
        elif role == "model":
            st.chat_message("assistant").markdown(parts[0])

    # Chat input
    chat_message = st.chat_input("Say something")
    # Get response
    if chat_message:
        st.chat_message("user").markdown(chat_message)
        res_area = st.chat_message("assistant").empty()
        messages.append(
            {"role": "user", "parts":  [chat_message]},
        )

        res = get_response(messages)

        res_text = ""
        for chunk in res:
            res_text += chunk.text
            res_area.markdown(res_text)
        messages.append(
            {"role": "model", "parts": [res_text]},
        )
        # update the pickle file
        with open(f"data/{st.session_state['current_uuid']}.pkl", "wb") as f:
            pickle.dump(st.session_state["messages"], f)
