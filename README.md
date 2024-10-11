# Agentic Retrieval Augmented Generation (ARAG) GUI

## Overview
This project presents a simple implementation of Agentic Retrieval Augmented Generation (ARAG) in a GUI. We provide a user-friendly graphical user interface (GUI) for interacting ARAG. It empowers users to efficiently query a large corpus of documents for various purposes, including:

* **Question Answering**: Ask specific questions about a single document or compare answers across multiple documents.
* **Summarization**: Generate summaries of individual documents or compare summaries to gain deeper insights.
* **Comparative Analysis**: Leverage ARAG's capabilities to analyze and compare information across different documents.

ARAG GUI leverages a novel architecture:

* **Document Agents**: Each document within the corpus is equipped with its own "document agent," a specialized tool capable of performing question-answering and summarization tasks within its assigned document.
* **Top-Level Agent**: A central agent oversees the set of document agents. It retrieves the appropriate tool (document agent) based on the user's query and employs the Chain of Thought ([CoT](https://arxiv.org/abs/2201.11903)) approach to process the collected responses, generating a comprehensive answer or summary.

## Implementation Details
ARAG GUI utilizes cutting-edge large language models (LLMs) to power its functionality:

* **GPT-3.5-turbo**: Serves as the underlying LLM acting as the agents, processing user queries and generating responses for each document.
* **LlamaIndex**: Provides the core functionalities for interacting with the document corpus, enabling efficient retrieval and indexing.

## Usage

1. Clone the repository:
   ```
   git clone https://github.com/oorejola/RAGapp.git
   ```

2. Navigate to the project directory:
   ```
   cd RAGapp
   ```

3. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Add OpenAI API key:
   * Open the `main.py` file and update the line:
     ```python
     os.environ["OPENAI_API_KEY"] = "sk-..."
     ```

5. Running the Application:
   ```
   python main.py
   ```

6. Load documents to query:
   * Add documents you want to query to `/docs/`. (As a placeholder, there are currently LLM papers on SelfRAG, CoT, etc.)
   * Currently, only `.pdf` files are supported.

7. Using the GUI:
   * Launch the application using `main.py`.
   * Enter queries or messages in the GUI input field.
   * Click the submit button.
   * The application retrieves relevant information and generates responses using ARAG.