import openai
from dotenv import load_dotenv
import os
from llama_index.llms import openai
from llama_index.core import SimpleDirectoryReader, ServiceContext, VectorStoreIndex
# Import SimpleDirectoryReader module:
from llama_index import SimpleDirectoryReader
# Load in documents:
documents = SimpleDirectoryReader('data').load_data()

from llama_index.node_parser import SimpleNodeParser
from llama_index.llms import AzureOpenAI
from llama_index import (
    VectorStoreIndex,
    ServiceContext,
    set_global_service_context
)
from llama_index.embeddings import HuggingFaceEmbedding
from llama_index import LangchainEmbedding
from llama_index.text_splitter import TokenTextSplitter

# Import modules:
from llama_index.node_parser import SimpleNodeParser
from llama_index.llms import AzureOpenAI
from llama_index import (
    VectorStoreIndex,
    ServiceContext,
    set_global_service_context
)
from llama_index.embeddings import HuggingFaceEmbedding
from llama_index import LangchainEmbedding
from llama_index.text_splitter import TokenTextSplitter

# Instantiate a text splitter for the node parser:
text_splitter = TokenTextSplitter(
  chunk_size=512,
  chunk_overlap=20,
)

# Chunking: Instantiate a node parser to parse the documents into Nodes:
parser = SimpleNodeParser(text_splitter=text_splitter)
nodes = parser.get_nodes_from_documents(documents)

# Define embedding model:
embedding = HuggingFaceEmbedding(model_name="BAAI/bge-base-en-v1.5")

# Instantiate an LLM:
llm = AzureOpenAI(
    engine="gpt-35-turbo",
    model="gpt-35-turbo",
    temperature=0
)

# Configure service context:
service_context = ServiceContext.from_defaults(
    llm=llm,
    embed_model=embedding
)
set_global_service_context(service_context)

# Instantiate the vector store index:
index = VectorStoreIndex.from_documents(documents, show_progress=True)

# Instantiate a query engine with default settings:
query_engine = index.as_query_engine()

# Query the index:
response = query_engine.query("")
print(response.get_formatted_sources(length=5000))