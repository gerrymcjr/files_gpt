import sys

from langchain.document_loaders import DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import SentenceTransformerEmbeddings
from langchain.llms import GPT4All
from langchain.prompts import PromptTemplate
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.chains import RetrievalQA
from langchain.vectorstores.pgvector import PGVector

CONNECTION_STRING = "postgresql+psycopg2://postgres:supersecretpassword@localhost:5432/vector_db"
COLLECTION_NAME = 'private_docs'

prompt = """
{user_prompt}:
{essay}
SUMMARY:
"""

directory = "data/"

def load_docs(directory):
  loader = DirectoryLoader(directory)
  documents = loader.load()
  return documents

def split_docs(documents,chunk_size=1000,chunk_overlap=200):
  text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap, separators=['/n/n', '/n', ' ', ''])
  docs = text_splitter.split_documents(documents)
  return docs


callback_manager = ([StreamingStdOutCallbackHandler()])
llm = GPT4All(model="model/orca-2-7b.Q4_0.gguf", callbacks=callback_manager, streaming=True)
embeddings = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
db = PGVector(embedding_function=embeddings,connection_string=CONNECTION_STRING,collection_name=COLLECTION_NAME)

while True:
  option=input(str.lower("Please Enter q,a,s, or x: "))
  # question and answer type, uses the documents saved on the vectordb
  if option.lower() == 'q':
      while True:
        question = input("Enter your question: ")
        print("\n")
        if '-x' in question:
           print("Exiting q and a function")
           print("\n")
           break
        else:
          qa = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=db.as_retriever())
          qa.run(question)
          print("\n")
  # adds the documents that are in the data folder to the vector db i am just using text file
  elif option.lower() == 'a':
      loaded_docs = load_docs(directory)
      docs = split_docs(loaded_docs)
      db.add_documents(docs)
      print("Documents loaded and added to the vector database!")
      print("\n")
  # it summarises the text file under the summary folder
  elif option.lower() == 's':
      while True:
        user_prompt = input("Enter prompt: ")
        print("\n")
        if '-x' in user_prompt:
           print("Exiting summary function")
           print("\n")
           break
        else:
          print("Summarizing started.....")
          print("\n")
          to_summarize = 'summary/data.txt'
          with open(to_summarize, 'r') as file:
            essay = file.read()
          prompt = PromptTemplate(template=prompt, input_variables=["essay", "user_prompt"])
          summary_prompt = prompt.format(essay=essay, user_prompt=user_prompt)
          summary = llm(summary_prompt)
          print("\n")
  elif option.lower() == 'x':
     sys.exit(0)
  else:
    print("option is not valid! please enter q,a,s, or x")
    print("\n")
