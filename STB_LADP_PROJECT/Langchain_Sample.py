import openai
from dotenv import load_dotenv
from langchain.embeddings import OpenAIEmbeddings
import os

load_dotenv()
openai.api_key = os.getenv("API_KEY")
deployment_name = os.getenv("DEPLOYMENT_NAME")
openai.api_base = os.getenv("OPENAI_API_BASE")

openai.api_type = 'azure'
openai.api_version = '2023-05-15'

embedding_model = OpenAIEmbeddings(
    openai_api_key=os.getenv("API_KEY"),
    openai_api_base=os.getenv("OPENAI_API_BASE"),
    openai_api_type="azure",
    openai_api_version="2023-05-15",
    model_kwargs={'deployment_id': deployment_name},
    model="text-embedding-ada-002"
)

from langchain.document_loaders import WebBaseLoader
loader = WebBaseLoader("https://www.stb.gov.sg/content/stb/en.html")

from langchain.text_splitter import RecursiveCharacterTextSplitter
text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=0)
splits = text_splitter.split_documents(loader.load())


from langchain.vectorstores import Chroma
from langchain.embeddings import OpenAIEmbeddings

vectorstore = Chroma.from_documents(
    documents=splits,
    embedding=OpenAIEmbeddings(
        openai_api_key=os.getenv("API_KEY"),
        openai_api_base=os.getenv("OPENAI_API_BASE"),
        openai_api_type="azure",
        openai_api_version="2023-05-15",
        model_kwargs={'deployment_id': deployment_name},
        model="text-embedding-ada-002"
    )
)
retriever = vectorstore.as_retriever()

from langchain import hub
rag_prompt = hub.pull("rlm/rag-prompt")

from langchain.chat_models import ChatOpenAI
llm = ChatOpenAI(
    model_name="gpt-3.5-turbo",
    openai_api_key=os.getenv("API_KEY"),
    openai_api_base=os.getenv("OPENAI_API_BASE"),
    model_kwargs={'deployment_id': deployment_name},
    temperature=0,
)

# Instantiate RAG chain:
from langchain.schema.runnable import RunnablePassthrough
rag_chain = (
    {"context": retriever, "question": RunnablePassthrough()}
    | rag_prompt
    | llm
)

# Get completion:
completion = rag_chain.invoke("Explain STAN in 10 lines")
print(completion.content)