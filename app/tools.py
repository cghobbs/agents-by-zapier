from langchain.llms import OpenAI
from langchain.agents import Tool
from langchain.chains import RetrievalQA
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.document_loaders import WebBaseLoader

from langchain.agents.agent_toolkits import ZapierToolkit
from langchain.utilities.zapier import ZapierNLAWrapper


# create a document retriever for Q&A
def doc_search_tools(url):
  loader = WebBaseLoader(url)
  docs = loader.load()
  text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000,
                                                 chunk_overlap=0)
  texts = text_splitter.split_documents(docs)
  llm = OpenAI(temperature=0)
  embeddings = OpenAIEmbeddings()
  db = Chroma.from_documents(texts, embeddings, collection_name="web-url")
  doc_search = RetrievalQA.from_chain_type(llm=llm,
                                           chain_type="stuff",
                                           retriever=db.as_retriever())
  return [
    Tool(
      name="Search Web Page",
      func=doc_search.run,
      description=
      "useful for searching the web page the user provided. It could contain up to date information, api documentation, or other useful information."
    )
  ]


# create a set of tools available to the agent
def nla_tools():
  zapier = ZapierNLAWrapper()
  toolkit = ZapierToolkit.from_zapier_nla_wrapper(zapier)
  return toolkit.get_tools()
