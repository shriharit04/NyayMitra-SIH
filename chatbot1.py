import os
#os.environ['GROQ_API_KEY']=os.getenv("GROQ_API_KEY")
os.environ["TOKENIZERS_PARALLELISM"] = "false"
from langchain_groq import ChatGroq
from langchain_community.embeddings import HuggingFaceBgeEmbeddings
from langchain_community.vectorstores import FAISS
from langchain import hub
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
import warnings
warnings.filterwarnings('ignore')
# from chromadb import Documents, EmbeddingFunction, Embeddings
model_name="BAAI/bge-small-en"
model_kwargs={"device":"cpu"}
encode_kwargs={"normalize_embeddings":True}
hf_embeddings=HuggingFaceBgeEmbeddings(model_name=model_name,model_kwargs=model_kwargs,encode_kwargs=encode_kwargs)


vectorstore=FAISS.load_local("faiss_index",hf_embeddings,allow_dangerous_deserialization=True)
retriever=vectorstore.as_retriever()

prompt=hub.pull("rlm/rag-prompt")
llm=ChatGroq(model="llama3-8b-8192",temperature=0)

def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)
rag_chain=(
    {"context": retriever | format_docs, "question": RunnablePassthrough()}
    | prompt
    | llm
    | StrOutputParser()   
)
query=str(input("Enter your query: "))
while query!="Exit":
    print(rag_chain.invoke(query))
    query=str(input("Enter query"))









