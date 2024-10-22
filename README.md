
# L&D Chat Application

This is an interactive chat application built with Streamlit that allows users to ask questions about UseReady's company policies, projects, and guidelines. The app leverages OpenAI's GPT-4 model and the `llama_index` library to provide accurate and relevant answers based on provided documentation.

## Features

- **Interactive Chat Interface**: Engage in a conversation with an AI assistant specialized in UseReady's policies.
- **Document Indexing**: Automatically indexes documents in the `./data` directory for efficient querying.
- **Customizable Responses**: Configured to provide technical and fact-based answers without hallucinations.

## Prerequisites

- **Python 3.7 or higher**
- **OpenAI API Key**: Access to OpenAI's GPT-4 model.
- **Documents**: Place your policy and guideline documents in the `./data` directory.

## Installation

### 1. Clone the Repository

```bash
git clone <repository_url>
cd <repository_directory>
```

### 2. Create a Virtual Environment

It's recommended to use a virtual environment to manage dependencies.

```bash
python -m venv venv
```

Activate the virtual environment:

- On Windows:

  ```bash
  venv\Scripts\activate
  ```

- On macOS/Linux:

  ```bash
  source venv/bin/activate
  ```

### 3. Install Required Packages

Install the necessary Python packages using `pip`:

```bash
pip install streamlit openai python-dotenv llama_index
```

### 4. Set Up Environment Variables

Create a `.env` file in the root directory and add your OpenAI API key:

```env
OPENAI_API_KEY=your-openai-api-key
```

### 5. Prepare the Data Directory

Ensure you have a `./data` directory in the root of your project and place all relevant documents inside it. These documents will be indexed and used to answer user queries.

## Running the Application

Start the Streamlit app by running:

```bash
streamlit run main.py
```

The application will open in your default web browser at `http://localhost:8501`.

## Usage

- **Ask Questions**: Use the chat input to ask questions about UseReady's policies and guidelines.
- **View Responses**: The assistant will provide answers based on the indexed documents and the GPT-4 model.
- **Chat History**: Scroll through the conversation to review previous questions and answers.

## Code Overview

### Main Components

- **Environment Setup**: Loads environment variables and sets the OpenAI API key.
  
  ```python
  load_dotenv()
  openai_apikey = os.getenv('OPENAI_API_KEY')
  openai.api_key = openai_apikey
  ```

- **Data Loading and Indexing**: Reads documents from `./data`, sets up the LLM with a system prompt, and creates a `VectorStoreIndex`.

  ```python
  @st.cache_resource(show_spinner=False)
  def load_data():
      reader = SimpleDirectoryReader(input_dir="./data")
      docs = reader.load_data()
      Settings.llm = OpenAI(
          model="gpt-4",
          temperature=0.2,
          system_prompt="""You are an expert on UseReady's company policies and guidelines."""
      )
      index = VectorStoreIndex.from_documents(docs)
      return index
  ```

- **Streamlit UI Setup**: Configures the page and initializes session state for messages and the chat engine.

  ```python
  class UseReadyChatApp:
      def __init__(self):
          self.index = load_data()
          self.setup_ui()
          self.initialize_chat_engine()
          self.handle_chat()
  ```

- **Chat Handling**: Manages user input, displays messages, and generates assistant responses.

  ```python
  def handle_chat(self):
      if prompt := st.chat_input("Ask a question"):
          st.session_state.messages.append({"role": "user", "content": prompt})
      # Display messages and generate responses
  ```

### File Structure

- `main.py`: The main application script.
- `./data`: Directory containing policy and guideline documents.
- `.env`: File storing environment variables like the OpenAI API key.

## Dependencies

- **streamlit**: For building the web application interface.
- **openai**: To interact with the OpenAI API.
- **python-dotenv**: To load environment variables from a `.env` file.
- **llama_index**: For indexing and querying the documents.

Install all dependencies using:

```bash
pip install streamlit openai python-dotenv llama_index
```
