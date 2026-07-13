import time

import streamlit as st

if "session_id" not in st.session_state:
    st.session_state["session_id"] = ""

if "login" not in st.session_state:
    st.session_state["login"] = True

if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []

if st.session_state.login:
    st.title("Synora AI")
    user_request = st.chat_input("Savollaringiz")

    with st.sidebar:
        st.button("New Chat")
        user_created_image = st.button("Your created image")
        if user_created_image:
            st.switch_page(page="pages/Images.py")
        st.subheader("Chat History")

    if user_request:
        with st.chat_message(""):
            st.write(user_request)

        with st.spinner("Analiz qilinmoqda ...", show_time=True):
            time.sleep(11111111)
