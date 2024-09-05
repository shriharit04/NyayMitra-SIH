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
from langchain_core.prompts import PromptTemplate
from langchain.load import loads,dumps
from langchain_core.prompts import ChatPromptTemplate
warnings.filterwarnings('ignore')
# from chromadb import Documents, EmbeddingFunction, Embeddings
def loading():
    model_name="BAAI/bge-small-en"
    model_kwargs={"device":"cpu"}
    encode_kwargs={"normalize_embeddings":True}
    hf_embeddings=HuggingFaceBgeEmbeddings(model_name=model_name,model_kwargs=model_kwargs,encode_kwargs=encode_kwargs)
    vectorstore=FAISS.load_local("faiss_index_2",hf_embeddings,allow_dangerous_deserialization=True)
    retriever=vectorstore.as_retriever()
    llm=ChatGroq(model="llama3-8b-8192",temperature=0)
    
    def format_docs(docs):
        str1="\n\n".join(doc.page_content for doc in docs)
        return str1[0:10000]
    def source(docs):
        return "\n\n".join(str(doc.metadata['page']) for doc in docs)
    
    ##query generation
    template = """You are an AI language model assistant. Your task is to generate five 
    different versions of the given user question to retrieve relevant documents from a vector 
    database. By generating multiple perspectives on the user question, your goal is to help
    the user overcome some of the limitations of the distance-based similarity search. 
    Provide these alternative questions separated by newlines. Original question: {question}"""
    prompt_perspectives = ChatPromptTemplate.from_template(template)
    generate_queries = (
        prompt_perspectives 
        | ChatGroq(temperature=0) 
        | StrOutputParser() 
        | (lambda x: x.split("\n"))
    )

    #retrieval chain
    def get_unique_union(documents: list[list]):
        flattened_docs=[dumps(doc) for sublist in documents for doc in sublist]
        unique_docs=list(set(flattened_docs))
        return [loads(doc) for doc in unique_docs]

    retrieval_chain=generate_queries|retriever.map()|get_unique_union
    

    #rag_chain
    prompt_template=PromptTemplate.from_template('''You are a legal expert who answers queries asked by a customer. 
                                                 Answer the following question based on the given context.
                                                 Never mention about the context in the output. The context is just for your reference.
                                                 You are a RAG system and you should not mention about the context given in any circumstance.
                                                 Do not cite the context directly but rather explain it in simple words. 
                                                 Do not use any knowledge which is not given in the context. 
                                                 If the question is not relevant to the legal system, do not answer the question and ask the user to give a relevant prompt
                                                 Also list the pages used.(Neccessary). 
                                                 The pages used are {page}\n Question:{question} \n Context:{context}''')
    rag_chain=(
        {"context": retrieval_chain | format_docs, "question": RunnablePassthrough(),"page":retrieval_chain|source}
        | prompt_template
        | llm
        | StrOutputParser()   
    )
    return rag_chain

def generate(rag_chain,query):
    output=rag_chain.invoke(query)
    return output
print("hello")
rag_chain=loading()

query=str(input("Enter your query: "))
while query!="Exit":
    print(generate(rag_chain,query))
    query=str(input("Enter a follow-up question: "))









