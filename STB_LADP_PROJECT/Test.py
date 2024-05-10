
import openai
from openai import AzureOpenAI
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv("API_KEY")
deployment_name = os.getenv("DEPLOYMENT_NAME")
api_base = os.getenv("OPENAI_API_BASE")

# Set API version:
api_version = '2023-05-15'

client = AzureOpenAI(
    azure_endpoint = api_base,
    api_key=api_key,
    api_version=api_version
)

# Import OpenAI modules into Python:
import openai
from llama_index import VectorStoreIndex, SimpleDirectoryReader
from llama_index.llms import AzureOpenAI

# Import environment modules:
from dotenv import load_dotenv
import os

# Import display/formatting modules:
from IPython.display import Markdown, display

# Store our earlier API credentials in environmental variables for LlamaIndex:
load_dotenv()
os.environ["OPENAI_API_KEY"] = os.getenv("API_KEY")
os.environ["OPENAI_API_TYPE"] = "azure"
os.environ["OPENAI_API_VERSION"] = "2023-05-15"
