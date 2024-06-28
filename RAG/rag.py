# RAG.py
# Used to Generate AI Responses

# Importing Required Libraries
import os
from llama_index.core import (
    VectorStoreIndex,
    SimpleDirectoryReader,
    SummaryIndex,
    load_index_from_storage,
    StorageContext,
    Settings,
)
from llama_index.core.objects import ObjectIndex
from llama_index.core.tools import QueryEngineTool, ToolMetadata
from llama_index.llms.openai import OpenAI
from llama_index.agent.openai import OpenAIAgent
from llama_index.core.node_parser import SemanticSplitterNodeParser
from llama_index.embeddings.openai import OpenAIEmbedding


def get_docs_names(folder_path: str) -> list:
    """
    Retrieve the names of PDF files in the specified folder.

    Args:
    - folder_path (str): Path to the folder containing PDF files.

    Returns:
    - list: List of PDF file names (without path).
    """
    return [os.path.splitext(filename)[0] for filename in os.listdir(folder_path) if filename.endswith(".pdf")]


def build_agents_and_query_engines(documents: list) -> tuple:
    """
    Builds agents and query engines for a list of documents.

    Args:
        documents (list): A list of document names.

    Returns:
        tuple: A tuple containing two dictionaries:
            - agents: A dictionary mapping document names to agents.
            - query_engines: A dictionary mapping document names to query engines.
    """

    embed_model = OpenAIEmbedding(model="text-embedding-ada-002")
    node_parser = SemanticSplitterNodeParser(buffer_size=1, breakpoint_percentile_threshold=95, embed_model=embed_model)

    agents = {}
    query_engines = {}

    for idx, doc_name in enumerate(documents):
        print(f"Building agent for document {doc_name} ({idx + 1}/{len(documents)})...")
        document_path = f"docs/{doc_name}.pdf"
        document = SimpleDirectoryReader(input_files=[document_path]).load_data()
        nodes = node_parser.get_nodes_from_documents(document)

        doc_dir = f"./docs/{doc_name}"
        if not os.path.exists(doc_dir):
            print(f"Building vector index for document {doc_name} ({idx + 1}/{len(documents)})...")
            vector_index = VectorStoreIndex(nodes)
            vector_index.storage_context.persist(persist_dir=doc_dir)
        else:
            print(f"Fetching vector index for document {doc_name} ({idx + 1}/{len(documents)})...")
            vector_index = load_index_from_storage(StorageContext.from_defaults(persist_dir=doc_dir))

        summary_index = SummaryIndex(nodes)
        vector_query_engine = vector_index.as_query_engine(llm=Settings.llm)
        summary_query_engine = summary_index.as_query_engine(llm=Settings.llm)

        query_engine_tools = [
            QueryEngineTool(
                query_engine=vector_query_engine,
                metadata=ToolMetadata(
                    name="vector_tool",
                    description=(
                        f"Useful for questions related to specific aspects of {doc_name} "
                        "(e.g. the history, arts and culture, sports, demographics, or more)."
                    ),
                ),
            ),
            QueryEngineTool(
                query_engine=summary_query_engine,
                metadata=ToolMetadata(
                    name="summary_tool",
                    description=(
                        f"Useful for any requests that require a holistic summary of EVERYTHING about {doc_name}. "
                        "For questions about more specific sections, please use the vector_tool."
                    ),
                ),
            ),
        ]

        function_llm = OpenAI(model="gpt-3.5-turbo")
        agent = OpenAIAgent.from_tools(
            query_engine_tools,
            llm=function_llm,
            verbose=True,
            system_prompt=(
                f"You are a specialized agent designed to answer queries about {doc_name}. "
                "You must ALWAYS use at least one of the tools provided when answering a question; do NOT rely on prior knowledge."
            ),
        )

        agents[doc_name] = agent
        query_engines[doc_name] = vector_index.as_query_engine(similarity_top_k=2)

    return agents, query_engines


def rag_response(prompt: str) -> str:
    """
    Generate a response using the RAG model.

    Args:
        prompt (str): The input prompt for generating the response.

    Returns:
        str: The generated response as a string.
    """
    response = top_agent.query(prompt)
    return str(response)


# Initialization block


Settings.llm = OpenAI(temperature=0, model="gpt-3.5-turbo")
Settings.embed_model = OpenAIEmbedding(model="text-embedding-ada-002")

documents = get_docs_names("docs")

print("Building agents and query engines...(This may take a while based on the number of documents)")
agents, query_engines = build_agents_and_query_engines(documents)

all_tools = [
    QueryEngineTool(
        query_engine=agents[doc_name],
        metadata=ToolMetadata(
            name=f"tool_{doc_name}",
            description=(
                f"This content contains information about {doc_name}. "
                f"Use this tool if you want to answer any questions about {doc_name}.\n"
            ),
        ),
    )
    for doc_name in documents
]

obj_index = ObjectIndex.from_objects(all_tools, index_cls=VectorStoreIndex)

top_agent = OpenAIAgent.from_tools(
    tool_retriever=obj_index.as_retriever(similarity_top_k=3),
    llm=OpenAI(model="gpt-3.5-turbo"),
    system_prompt=(
        "You are an agent designed to answer queries about a set of given documents. "
        "Please always use the tools provided to answer a question. Do not rely on prior knowledge."
    ),
    verbose=True,
)
