from dotenv import load_dotenv
import os
import utils
import pandas as pd
from llama_index.llms.azure_openai import AzureOpenAI
from llama_index.core import VectorStoreIndex,Settings
from llama_index.readers.web import SimpleWebPageReader
from llama_index.core.node_parser import TokenTextSplitter
from llama_index.embeddings.azure_openai import AzureOpenAIEmbedding
from llama_index.core import SummaryIndex

load_dotenv()
os.environ["OPENAI_API_KEY"] = os.getenv('API_KEY')
os.environ["AZURE_OPENAI_ENDPOINT"] = os.getenv('OPENAI_API_BASE')
os.environ["OPENAI_API_VERSION"] = "2023-07-01-preview"

#Define Openai Embeddings
openai_embed_model = AzureOpenAIEmbedding(
    model="text-embedding-ada-002",
    api_key=os.environ["OPENAI_API_KEY"],
    azure_endpoint=os.environ["AZURE_OPENAI_ENDPOINT"],
    api_version=os.environ["OPENAI_API_VERSION"],
    
)

# Define embedding model:
# embedding = HuggingFaceEmbedding(model_name="BAAI/bge-base-en-v1.5")

llm = AzureOpenAI(
    engine="stb-gpt-35-turbo", model="gpt-35-turbo", temperature=0.0
    #engine="STB-POC-JUNE", model="gpt-4", temperature=0.0
)

text_splitter = TokenTextSplitter(
  chunk_size=512,
  chunk_overlap=20,
)

#Settings
Settings.llm = llm
Settings.node_parser = text_splitter
Settings.embed_model = openai_embed_model


url_list = utils.read_excel_to_list(pd,'data/urls.xlsx')
urls = utils.get_values(url_list)
#print(urls)

documents = SimpleWebPageReader(html_to_text=True).load_data(urls)
#print(documents)

index = VectorStoreIndex.from_documents(documents)
query_engine = index.as_query_engine()
response = query_engine.query("Graduate and Fresh Graduate opportunities at STB")
print(response)
print("SOURCE +++++++>>>>>>",response.get_formatted_sources())