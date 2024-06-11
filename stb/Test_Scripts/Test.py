import os
from dotenv import load_dotenv
from llama_index.core.chat_engine import SimpleChatEngine
from llama_index.llms.azure_openai import AzureOpenAI
from llama_index.llms.openai import OpenAI

load_dotenv()
os.environ["OPENAI_API_KEY"] = os.getenv('API_KEY')
os.environ["AZURE_OPENAI_ENDPOINT"] = os.getenv('OPENAI_API_BASE')
os.environ["OPENAI_API_VERSION"] = "2023-07-01-preview"

llm = AzureOpenAI(
    engine="stb-gpt-35-turbo", model="gpt-4", temperature=0.0
    #engine="STB-POC-JUNE", model="gpt-4", temperature=0.0
)

# client = AzureOpenAI(
#   api_key = os.getenv("AZURE_API_KEY"),
#   api_version = "2023-05-15",
#   azure_endpoint = os.getenv("AZURE_ENDPOINT")
# )
response = llm.complete("The sky is a beautiful blue and")
print(response)