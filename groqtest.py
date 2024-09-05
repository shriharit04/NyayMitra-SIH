import os
os.environ['GROQ_API_KEY']=os.getenv("GROQ_API_KEY")
from groq import Groq
import chromadb
from dotenv import load_dotenv
from chromadb.utils import embedding_functions 
from langchain_groq import ChatGroq
from langchain_community.embeddings import HuggingFaceBgeEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain.document_loaders import PyPDFLoader

# from chromadb import Documents, EmbeddingFunction, Embeddings

default_ef = embedding_functions.DefaultEmbeddingFunction()

loader = PyPDFLoader("/Users/sreyaskv/Documents/SIH_project/Source_material/Constitution.pdf")
documents = loader.load()


from langchain.text_splitter import RecursiveCharacterTextSplitter

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,  # Adjust chunk size as needed
    chunk_overlap=100,  # Adjust overlap as needed
)

docs = text_splitter.split_documents(documents)

print(type(docs))

# text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
# splits = text_splitter.split_documents(pdf_text)



# class MyEmbeddingFunction(EmbeddingFunction):
#     def __call__(self, input: Documents) -> Embeddings:
#         model_name = "BAAI/bge-small-en"
#         model_kwargs = {"device": "cpu"}
#         encode_kwargs = {"normalize_embeddings": True}
#         embedding_model = HuggingFaceBgeEmbeddings(
#             model_name=model_name, model_kwargs=model_kwargs, encode_kwargs=encode_kwargs
#         )
#         embeddings=embedding_model.embed_documents(Documents)
#         return embeddings

chroma_client=chromadb.PersistentClient(path="rial_storage")
collection_name="trial"
collection=chroma_client.get_or_create_collection(name=collection_name,embedding_function=default_ef)




collection.add(documents=docs,embeddings=default_ef(docs))


# llm = ChatGroq(
#     model="llama3-8b-8192",
#     temperature=0,
#     max_tokens=None,
#     timeout=None,
#     max_retries=2,
# )

# messages = [
#     (
#         "system",
#         "You are a helpful assistant that translates English to French. Translate the user sentence.",
#     ),
#     ("human", "I love programming."),
# ]
# ai_msg = llm.invoke(messages)
# print(ai_msg.content)
# String="Hello how are you"


