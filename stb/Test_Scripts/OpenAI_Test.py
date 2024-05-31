
from dotenv import load_dotenv
import os
from llama_index.llms.openai import OpenAI


load_dotenv()
os.environ["OPENAI_API_KEY"] = os.getenv('API_KEY')
os.environ["AZURE_OPENAI_ENDPOINT"] = os.getenv('OPENAI_API_BASE')
os.environ["OPENAI_API_VERSION"] = "2023-07-01-preview"


# non-streaming
resp = OpenAI().complete("Paul Graham is ")
print(resp)

# using streaming endpoint
from llama_index.llms.openai import OpenAI

llm = OpenAI()
resp = llm.stream_complete("Paul Graham is ")
for delta in resp:
    print(delta, end="")