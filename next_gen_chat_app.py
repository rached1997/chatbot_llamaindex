import os
import time

import streamlit as st
from llama_index import VectorStoreIndex, ServiceContext, Document
from llama_index.llms import OpenAI
import openai
from llama_index import SimpleDirectoryReader

st.set_page_config(page_title="LlamaIndex Test", layout="centered",
                   initial_sidebar_state="auto", menu_items=None)
# openai.api_key = "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"
openai.api_key = "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"
st.title("ChatBot Test")

if "messages" not in st.session_state.keys():  # Initialize the chat messages history
    st.session_state.messages = [
        {"role": "assistant", "content": "Ask me a question about Streamlit's open-source Python library!"}
    ]

st.info("You can ask question related to this documents https://drive.google.com/drive/folders/1-2pMCa7AeBnzUr2BuLg2tRjMmyTg6GZM?usp=drive_link")

@st.cache_resource(show_spinner=False)
def load_data():
    with st.spinner(text="Loading docs"):
        reader = SimpleDirectoryReader(input_dir="data/",
                                       recursive=True)
        docs = reader.load_data()
        service_context = ServiceContext.from_defaults(llm=OpenAI(model="gpt-4-1106-preview", temperature=0.5,
                                                                  system_prompt="You are an expert on the Streamlit Python library and your job is to answer technical questions. Assume that all questions are related to the Streamlit Python library. Keep your answers technical and based on facts – do not hallucinate features."))
        index = VectorStoreIndex.from_documents(docs, service_context=service_context)
        return index


index = load_data()

if "chat_engine" not in st.session_state.keys():  # Initialize the chat engine
    st.session_state.chat_engine = index.as_chat_engine(chat_mode="context", verbose=True)




# uploaded_files = st.sidebar.file_uploader("Choose a CSV file", accept_multiple_files=True)
# for uploaded_file in uploaded_files:
#     if uploaded_file is not None:
#         file_path = os.path.join("data/", uploaded_file.name)
#         with open(file_path, "wb") as file:
#             file.write(uploaded_file.read())
# if uploaded_files:
#     index = load_data()
#     st.session_state.chat_engine = index.as_chat_engine(chat_mode="context", verbose=True)
#     uploaded_files = None


if prompt := st.chat_input("Your question"):  # Prompt for user input and save to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

for message in st.session_state.messages:  # Display the prior chat messages
    with st.chat_message(message["role"]):
        st.write(message["content"])

# If last message is not from assistant, generate a new response
if st.session_state.messages[-1]["role"] != "assistant":
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = st.session_state.chat_engine.chat(prompt)
            st.write(response.response)
            message = {"role": "assistant", "content": response.response}
            st.session_state.messages.append(message)  # Add response to message history

# sk - luOp6YZ1UKsyUqk3aZrHT3BlbkFJDDtvZx3cvYY93sfJnAek

