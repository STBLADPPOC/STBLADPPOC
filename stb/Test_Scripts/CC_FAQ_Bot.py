import sys
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
import streamlit as st
#create a storage
col1, col2, col3,col4,col5,col6 = st.columns(6)
st.sidebar.markdown("")
st.sidebar.image('logo4.png',width=170,)
st.sidebar.title("STB Contact Center Assistant")
st.sidebar.divider()

dataFresh = st.sidebar.button("Data Refresh")
clearChat = st.sidebar.button("Clear Chat")
if clearChat:
     st.session_state.messages = []

if "messages" not in st.session_state.keys(): # Initialize the chat message history
    st.session_state.messages = [
        {"role": "assistant", "content": "Ask me a question about Streamlit's open-source Python library!"}
    ]

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
)

#Settings
Settings.llm = llm
Settings.node_parser = text_splitter
Settings.embed_model = openai_embed_model

@st.cache_resource(show_spinner=False)
def load_data():
 with st.spinner(text="Loading Knowledge base – hang tight! This should take 1-2 minutes."):
        # reader = SimpleDirectoryReader(input_dir="./data", recursive=True)
        # docs = reader.load_data()
        # storage_context = StorageContext.from_defaults(persist_dir="storage1")
        # index = VectorStoreIndex.from_documents(docs, storage_context)
        # return index
  print("START")
  url_list = utils.read_excel_to_list(pd,'data/urls.xlsx')
  urls = utils.get_values(url_list)
  print(urls)

  documents = SimpleWebPageReader(html_to_text=True).load_data(urls)
  index_web = VectorStoreIndex.from_documents(documents)
 
  documents = SimpleDirectoryReader('data/docs').load_data()
  index_doc = VectorStoreIndex.from_documents(documents,show_progress=True)
 
  index_web.storage_context.persist(persist_dir="storage1")
  storage_context = StorageContext.from_defaults(persist_dir="storage1")   
 
#  index_doc.storage_context.persist(persist_dir="storage1")
#  storage_context = StorageContext.from_defaults(persist_dir="storage1")

#------------------ END of vector embedding + index ------------------
#index1 = load_index_from_storage(storage_context, index_id=index_web)
#index2 = load_index_from_storage(storage_context, index_id=index_doc)
  index = load_index_from_storage(storage_context)

index = load_data()
print(index)

if "chat_engine" not in st.session_state.keys(): # Initialize the chat engine
        st.session_state.chat_engine = index.as_chat_engine(chat_mode="condense_question", verbose=True)

if prompt := st.chat_input("Your question"): # Prompt for user input and save to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

for message in st.session_state.messages: # Display the prior chat messages
    with st.chat_message(message["role"]):
        st.write(message["content"])

# If last message is not from assistant, generate a new response
if st.session_state.messages[-1]["role"] != "assistant":
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            query_engine = index.as_query_engine()
            response = query_engine.query(prompt)
            st.write(response.response)
            message = {"role": "assistant", "content": response.response}
            st.session_state.messages.append(message) # Add response to message history