from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.embeddings import HuggingFaceEmbeddings
import os
from dotenv import load_dotenv

load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
embeddings = GoogleGenerativeAIEmbeddings(model="models/text-embedding-004")


# loading
def load_all_docs():
    file1 = TextLoader('/Users/bishikachhetri/Desktop/hms/data.txt').load()
    file2 = TextLoader('/Users/bishikachhetri/Desktop/hms/navigation.txt').load()
    return file1,file2

doc1,doc2= load_all_docs()


# splitting
splitter = RecursiveCharacterTextSplitter(
    chunk_size = 1000,
    chunk_overlap = 250,
    separators= ['\n\n','\n','.',' ','']
)
splitted1 = splitter.split_documents(doc1)
splitted2 = splitter.split_documents(doc2)


def vectorstore(collection_name, directory, documents):
    vector_store = Chroma(
        collection_name=collection_name,
        embedding_function=embeddings,
        persist_directory=directory
    )
    vector_store.add_documents(documents)
    return vector_store

vs1 = vectorstore('healthdata', 'healthdata.db', splitted1)
vs2 = vectorstore('navigation', 'navigation.db', splitted2)


