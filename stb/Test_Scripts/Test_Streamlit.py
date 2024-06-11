import os
from dotenv import load_dotenv
from llama_index.core.chat_engine import SimpleChatEngine
from llama_index.llms.azure_openai import AzureOpenAI
from llama_index.llms.openai import OpenAI
import streamlit as st


load_dotenv()
os.environ["OPENAI_API_KEY"] = os.getenv('API_KEY')
os.environ["AZURE_OPENAI_ENDPOINT"] = os.getenv('OPENAI_API_BASE')
os.environ["OPENAI_API_VERSION"] = "2023-07-01-preview"

llm = AzureOpenAI(
    engine="stb-gpt-35-turbo", model="gpt-4", temperature=0.0
    #engine="STB-POC-JUNE", model="gpt-4", temperature=0.0
)

col1, col2, col3,col4,col5,col6 = st.columns(6)
st.sidebar.markdown("")
#st.sidebar.image('logo4.png')
st.sidebar.title("STB Contact Center Assistant")
st.sidebar.divider()

st.sidebar.button("Data Refresh")
clearChat = st.sidebar.button("Clear Chat")
if clearChat:
     st.session_state.messages = []
  #create a storage
if "messages" not in st.session_state:
     st.session_state.messages = []

#Display chat history
for message in st.session_state.messages:
    with st.chat_message(message.get("role")):
        st.write(message.get("content"))
# client = AzureOpenAI(
#   api_key = os.getenv("AZURE_API_KEY"),
#   api_version = "2023-05-15",
#   azure_endpoint = os.getenv("AZURE_ENDPOINT")
# )

prompt = st.chat_input("Type your query")
if prompt:
 #Add to storage
 st.session_state.messages.append({"role":"user","content":prompt})
 with st.chat_message("user"):
  st.write(prompt)
  print("88888888888888888888888888888888888888") 
response = llm.complete(prompt)
print(response)

#store response
st.session_state.messages.append({"role":"assistant","content":response})
with st.chat_message("assistant"):
    st.markdown(response)
#"The sky is a beautiful blue and"
#{"role":"assistant","content":prompt}