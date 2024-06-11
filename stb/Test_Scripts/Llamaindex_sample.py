import openai
from dotenv import load_dotenv
import os

load_dotenv()
os.environ["OPENAI_API_KEY"] = os.getenv('API_KEY')
os.environ["AZURE_OPENAI_ENDPOINT"] = os.getenv('OPENAI_API_BASE')
os.environ["OPENAI_API_VERSION"] = "2023-07-01-preview"

from llama_index.core import SimpleDirectoryReader,Settings
from llama_index.core.chat_engine import SimpleChatEngine
from llama_index.llms.azure_openai import AzureOpenAI
from llama_index.llms.openai import OpenAI
from llama_index.core.node_parser import SimpleNodeParser
from llama_index.core import VectorStoreIndex
# from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.core.node_parser import TokenTextSplitter
from llama_index.embeddings.azure_openai import AzureOpenAIEmbedding

# Load in documents:
documents = SimpleDirectoryReader('data').load_data()

text_splitter = TokenTextSplitter(
  chunk_size=512,
  chunk_overlap=20,
)

llm = AzureOpenAI(
    engine="stb-gpt-35-turbo",
    model="gpt-35-turbo",
    temperature=0.0
)

#Define Openai Embeddings
openai_embed_model = AzureOpenAIEmbedding(
    model="text-embedding-ada-002",
    api_key=os.environ["OPENAI_API_KEY"],
    azure_endpoint=os.environ["AZURE_OPENAI_ENDPOINT"],
    api_version=os.environ["OPENAI_API_VERSION"],
)

# Define embedding model:
embedding = HuggingFaceEmbedding(model_name="BAAI/bge-base-en-v1.5")

#Settings
Settings.llm = llm
# Settings.embed_model = embedding
Settings.node_parser = text_splitter
Settings.embed_model = openai_embed_model

# Instantiate the vector store index:
index = VectorStoreIndex.from_documents(documents,show_progress=True)
print("Indexing Completed")

# Instantiate a query engine with default settings:
query_engine = index.as_query_engine()

# Query the index:
response = query_engine.query("please provide the link for TA complaints")
print('RESPONSE=======>',response)
print(response.get_formatted_sources(length=100))


#Instantiate a chat engine
# chat_engine = index.as_chat_engine()

# response = chat_engine.query("What is STAN")
# print(response.get_formatted_sources(length=5000))

# Instantiate an LLM:
# llm = AzureOpenAI(
#     api_key=os.getenv("API_KEY"),  
#     api_version="2023-12-01-preview",
#     azure_endpoint=os.getenv("OPENAI_API_BASE")
# )