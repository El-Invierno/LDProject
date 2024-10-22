import streamlit as st
import openai
import os
from dotenv import load_dotenv
from llama_index.llms.openai import OpenAI
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, Settings

# Load environment variables
load_dotenv()

# Set OpenAI API key
openai_apikey = os.getenv('OPENAI_API_KEY')
openai.api_key = openai_apikey

@st.cache_resource(show_spinner=False)
def load_data():
    """Load and initialize the document index."""
    reader = SimpleDirectoryReader(input_dir="./data")
    docs = reader.load_data()
    Settings.llm = OpenAI(
        model="gpt-4",
        temperature=0.2,
        system_prompt="""You are an expert on 
        the UseReady's company policies and guidelines and your 
        job is to answer all the questions related to the company, it's projects, guidelines etc. 
        Assume that all questions are related 
        to the UseReady policies and guidelines and the related documentation. Keep 
        your answers technical and based on 
        facts. Do not hallucinate features.""",
    )
    index = VectorStoreIndex.from_documents(docs)
    return index

class UseReadyChatApp:
    def __init__(self):
        self.index = load_data()
        self.setup_ui()
        self.initialize_chat_engine()
        self.handle_chat()

    def setup_ui(self):
        """Set up the Streamlit page and initialize session state."""
        st.set_page_config(
            page_title="UseReady L&D Page",
            layout="centered",
            initial_sidebar_state="auto",
            menu_items=None
        )
        st.title("UseReady L&D Chat 💬")

        if "messages" not in st.session_state:
            st.session_state.messages = [
                {
                    "role": "assistant",
                    "content": "Ask me a question about UseReady's work policies!",
                }
            ]

    def initialize_chat_engine(self):
        """Initialize the chat engine in the session state."""
        if "chat_engine" not in st.session_state:
            st.session_state.chat_engine = self.index.as_chat_engine(
                chat_mode="condense_question", verbose=True, streaming=True
            )

    def handle_chat(self):
        """Handle the chat interaction with the user."""
        if prompt := st.chat_input("Ask a question"):
            st.session_state.messages.append({"role": "user", "content": prompt})

        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.write(message["content"])

        # If the last message is from the user, generate a response
        if st.session_state.messages[-1]["role"] != "assistant":
            with st.chat_message("assistant"):
                prompt = st.session_state.messages[-1]["content"]
                response_stream = st.session_state.chat_engine.stream_chat(prompt)
                st.write_stream(response_stream.response_gen)
                message = {"role": "assistant", "content": response_stream.response}
                st.session_state.messages.append(message)

# Run the app
if __name__ == "__main__":
    UseReadyChatApp()
