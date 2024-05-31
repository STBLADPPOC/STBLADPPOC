import os
import utils
import pandas as pd
from dotenv import load_dotenv
from llama_index.llms.azure_openai import AzureOpenAI
from llama_index.core import VectorStoreIndex,Settings
from llama_index.readers.web import SimpleWebPageReader
from llama_index.core.node_parser import TokenTextSplitter
from llama_index.embeddings.azure_openai import AzureOpenAIEmbedding
from llama_index.core import SummaryIndex
from llama_index.core.storage.docstore import SimpleDocumentStore
from llama_index.core.storage.index_store import SimpleIndexStore
from llama_index.core.vector_stores import SimpleVectorStore
from llama_index.core import (
    VectorStoreIndex,
    Settings,
    SimpleDirectoryReader,
    load_indices_from_storage,
    load_index_from_storage,
    StorageContext
)

load_dotenv()
os.environ["OPENAI_API_KEY"] = os.getenv('API_KEY')
os.environ["AZURE_OPENAI_ENDPOINT"] = os.getenv('OPENAI_API_BASE')
os.environ["OPENAI_API_VERSION"] = "2023-07-01-preview"

llm = AzureOpenAI(
    engine="stb-gpt-35-turbo", model="gpt-35-turbo", temperature=0.0
    #engine="STB-POC-JUNE", model="gpt-4", temperature=0.0
)

openai_embed_model = AzureOpenAIEmbedding(
    model="text-embedding-ada-002",
    api_key=os.environ["OPENAI_API_KEY"],
    azure_endpoint=os.environ["AZURE_OPENAI_ENDPOINT"],
    api_version=os.environ["OPENAI_API_VERSION"],
)

#Settings
Settings.llm = llm
Settings.embed_model = openai_embed_model

#------------------ START of vector embedding + index ------------------
#--------------Executed only on click of refresh button on ui-----------

#Read url list from excel
url_list = utils.read_excel_to_list(pd,'data/urls.xlsx')
urls = utils.get_values(url_list)
print(urls)

documents = SimpleWebPageReader(html_to_text=True).load_data(urls)
index_web = VectorStoreIndex.from_documents(documents)

documents = SimpleDirectoryReader('data/docs').load_data()
index_doc = VectorStoreIndex.from_documents(documents,show_progress=True)

# ERROR No such file or directory: 'C:/VSCode/stb/storage1/docstore.json'  
storage_context = StorageContext.from_defaults(persist_dir="storage1")

# storage_context = StorageContext.from_defaults(
#     docstore=SimpleDocumentStore.from_persist_dir(persist_dir="storage"),
#     vector_store=SimpleVectorStore.from_persist_dir(persist_dir="storage"),
#     index_store=SimpleIndexStore.from_persist_dir(persist_dir="storage"),
# )
#------------------ END of vector embedding + index ------------------
index = load_index_from_storage(storage_context, index_id=["index_web","index_doc"])
print(index)

query_engine = index.as_query_engine()
response = query_engine.query("Graduate and Fresh Graduate programmes at STB")
print(response)
print("SOURCE +++++++>>>>>>",response.get_formatted_sources())