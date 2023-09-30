from langchain.document_loaders import DirectoryLoader
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Chroma


def create_embedings_from_files(folder, extension):
    loader = DirectoryLoader(folder, extension)
    documents = loader.load()
    db = Chroma.from_documents(documents, OpenAIEmbeddings(disallowed_special=()))
    return db
