## Note: you need to be using OpenAI Python v0.27.0 for the code below to work
import openai
import streamlit as st
import os


def main():
    # Initialization
    if "key" not in st.session_state:
        st.session_state["messages"] = []

    st.sidebar.header("Settings")
    with st.sidebar.form("Set Primer"):
        primer = st.text_area(
            "Primer Message",
            "You are a friendly and helpful assistant.",
        )

        if st.form_submit_button():
            st.session_state.messages = [{"role": "system", "content": primer}]
            st.success("Updated the system primer")

    history = st.container()

    with st.form("Chat"):
        input = st.text_input("You:", "")
        if st.form_submit_button():
            st.session_state.messages.append({"role": "user", "content": input})

            r = openai.ChatCompletion.create(
                model="gpt-3.5-turbo", messages=st.session_state.messages
            )

            with st.expander("Result"):
                st.write(r)

            st.session_state.messages.append(
                {"role": "assistant", "content": r["choices"][0]["message"]["content"]}
            )

    with history:
        for message in st.session_state.messages:
            c1, c2 = st.columns([2, 10])
            with c1:
                st.write(message["role"])
            with c2:
                st.write(message["content"])


st.title("AdamBot")

key = st.text_input("Your Open API Key", "sk...")
if key == "sk...":
    st.error("Please add a valid Open API Key")

else:
    openai.api_key = key
    main()
