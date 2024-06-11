import sys
import os
import utils
import pandas as pd
from dotenv import load_dotenv
from llama_index.llms.azure_openai import AzureOpenAI
from llama_index.core import VectorStoreIndex,Settings
from llama_index.readers.web import SimpleWebPageReader
from llama_index.core.chat_engine import SimpleChatEngine
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
import streamlit as st

#bot page layout
st.sidebar.markdown("")
st.sidebar.image('images\logo4.png',width=170)
st.sidebar.title("STB Contact Center Assistant")
st.sidebar.divider()
#Add button for Data load and Clearing chat messages
dataFresh = st.sidebar.button("Data Refresh")
clearChat = st.sidebar.button("Clear Chat")
if clearChat:
     st.session_state.messages = []
     
load_dotenv()
os.environ["OPENAI_API_KEY"] = os.getenv('API_KEY')
os.environ["AZURE_OPENAI_ENDPOINT"] = os.getenv('OPENAI_API_BASE')
os.environ["OPENAI_API_VERSION"] = "2023-07-01-preview"

llm = AzureOpenAI(
    engine="stb-gpt-35-turbo", model="gpt-35-turbo", temperature=0.0
    #engine="STB-POC-JUNE", model="gpt-4", temperature=0.0
)

text_splitter = TokenTextSplitter(
  chunk_size=512,
  chunk_overlap=20,
)

openai_embed_model = AzureOpenAIEmbedding(
    model="text-embedding-ada-002",
    api_key=os.environ["OPENAI_API_KEY"],
    azure_endpoint=os.environ["AZURE_OPENAI_ENDPOINT"],
    api_version=os.environ["OPENAI_API_VERSION"],
    #deployment_name='STB-POC-Embed'
)

#Settings
Settings.llm = llm
Settings.node_parser = text_splitter
Settings.embed_model = openai_embed_model

#------------------ START of vector embedding + index ------------------
#--------------Executed only on click of Data Refresh button-----------
def BuildKnowledgeBase():
#Read url list from excel
 with st.spinner(text="Loading Knowledge base – hang tight! This should take 1-2 minutes."):
  print("START")
  url_list = utils.read_excel_to_list(pd,'data/urls.xlsx')
  urls = utils.get_values(url_list)
  print(urls)

  web_documents = SimpleWebPageReader(html_to_text=True).load_data(urls)
  local_documents = SimpleDirectoryReader('data/docs').load_data()
  combined_documents = web_documents+local_documents
  
  index = VectorStoreIndex.from_documents(combined_documents,show_progress=True)
 
  index.storage_context.persist(persist_dir="storage2")
  storage_context = StorageContext.from_defaults(persist_dir="storage2")

  index = load_index_from_storage(storage_context)
  query_engine = index.as_query_engine()
  st.popover("Data Refresh completed!")
  return index

if dataFresh:
 index=BuildKnowledgeBase()

else:
 storage_context = StorageContext.from_defaults(persist_dir="storage2")
 index = load_index_from_storage(storage_context)
 
if "messages" not in st.session_state:
    st.session_state.messages = []    
#Chat history
for message in st.session_state.messages:
    with st.chat_message(message.get("role")):
        st.write(message.get("content"))

prompt=" " 
prompt = st.chat_input("Type your query")

if prompt:
#Check if prompt is English, else it is considered a translation request
 isEnglish = utils.isEnglish(prompt)
 print("IS ENGLISH",isEnglish)
 if isEnglish:
  print(isEnglish)
  #store prompt
  st.session_state.messages.append({"role":"user","content":prompt})
  with st.chat_message("user"):
    st.markdown(prompt)
  query_engine = index.as_query_engine()
  response = query_engine.query(prompt)
  response_content = response.response
  #store response
  st.session_state.messages.append({"role":"assistant","content":response_content})
  with st.chat_message("assistant"):
    st.markdown(response_content)
    st.markdown(response.get_formatted_sources())
#--------------------------- TRANSLATION SCRIPT START----------------------------------------------------
 else:
  translation_prompt = """
    You are a professional translator. Determine whether the text is in English or not.

    Instructions:
    1. If the text is not in English, translate it to English.
    2. If the text is in English, output the original text without translation or changes.
    3. Refrain from adding any additional comments or information to the text.
    """
 
  chat_engine = SimpleChatEngine.from_defaults(
    llm=llm,
    system_prompt=translation_prompt
  )
  st.session_state.messages.append({"role":"user","content":prompt})
  with st.chat_message("user"):
    st.markdown(prompt)
  eng_response = chat_engine.chat(prompt)
  translation = eng_response.response
  st.session_state.messages.append({"role":"assistant","content":translation})
  with st.chat_message("assistant"):
   #st.code(translation)    -- Keep it if you want copy to clipboard
    st.markdown(translation)
  #------------------------------------- respond to the translated Query start ------------------------------------------------------
  query_engine = index.as_query_engine()
  response = query_engine.query(translation)
  trasnslation_response = response.response
  #store response
  st.session_state.messages.append({"role":"assistant","content":trasnslation_response})
  with st.chat_message("assistant"):
    st.markdown(trasnslation_response)
    st.markdown(response.get_formatted_sources())
  #------------------------------------- respond to the translated Query End ------------------------------------------------------
  print(translation)

 

