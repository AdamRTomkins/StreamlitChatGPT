## Note: you need to be using OpenAI Python v0.27.0 for the code below to work
import openai
import streamlit as st


def main():
    # Initialization your state messages
    if "messages" not in st.session_state:
        st.session_state["messages"] = []
    if "primer" not in st.session_state:
        st.session_state["primer"] = "You are a friendly and helpful assistant."
    if "context_length" not in st.session_state:
        st.session_state["context_length"] = 10

    st.sidebar.header("Settings")

    with st.sidebar:
        # Allow the user to set their prompt
        st.session_state.primer = st.text_area(
            "Primer Message",
            "You are a friendly and helpful assistant.",
        )

        st.session_state.context_length = st.slider(
            "Context Message Length", min_value=1, max_value=50, value=10, step=1
        )

        if st.button("Clear Chat"):
            st.session_state.messages = []
            st.info("Chat Memory Cleared")

    history = st.container()

    with st.form("Chat"):
        input = st.text_input("You:", "")
        if st.form_submit_button():
            st.session_state.messages.append({"role": "user", "content": input})

            messages = [{"role": "system", "content": st.session_state.primer}]
            messages.extend(
                st.session_state.messages[-st.session_state.context_length :]
            )

            with st.expander("Messages"):
                st.write(messages)

            r = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=messages)

            with st.expander("Result"):
                st.info("Your Output Response")
                st.write(r)

            st.session_state.messages.append(
                {"role": "assistant", "content": r["choices"][0]["message"]["content"]}
            )

    with history:
        for i, message in enumerate(st.session_state.messages):
            c1, c2 = st.columns([2, 10])
            with c1:
                st.write(message["role"])
            with c2:
                # Lets italisize the messages that are sent in the state
                if (
                    len(st.session_state.messages) - i
                    < st.session_state.context_length + 1
                ):
                    st.markdown(f'_{message["content"]}_')
                else:
                    st.markdown(f'{message["content"]}')


st.title("Open AI Chat GPT Demo")

key = st.text_input("Your Open API Key", "sk...")
if key == "sk...":
    st.error("Please add a valid Open API Key")

else:
    openai.api_key = key
    main()


st.info("Created by Adam Tomkins.")
