# A bare bones UI for the Open AI Chat Completion used in ChatGPT
# Created by Adam Tomkins

import openai
import streamlit as st

# Set up Session State
if "messages" not in st.session_state:
    st.session_state["messages"] = []
if "primer" not in st.session_state:
    st.session_state["primer"] = "You are a friendly and helpful assistant."
if "context_length" not in st.session_state:
    st.session_state["context_length"] = 10


def main():
    # Initialization your state messages

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

        # Allow Users to reset the memory
        if st.button("Clear Chat"):
            st.session_state.messages = []
            st.info("Chat Memory Cleared")

    # A place to draw the chat history
    history = st.container()

    with st.form("Chat"):
        input = st.text_input("You:", "")
        if st.form_submit_button():
            st.session_state.messages.append({"role": "user", "content": input})

            # Create an on the fly message stack
            messages = [{"role": "system", "content": st.session_state.primer}]
            messages.extend(
                st.session_state.messages[-st.session_state.context_length :]
            )

            # Call the OpenAI API
            r = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=messages)
            tokens = r["usage"]["total_tokens"]
            cost = round((tokens / 1000) * 0.02, 3)
            st.info(f"Message uses {tokens} tokens for a total cost of {cost} cents")

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


st.info("Created by Adam Tomkins. Source Code: https://github.com/AdamRTomkins/StreamlitChatGPT")
