import os
os.environ['GROQ_API_KEY']='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'
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
from langchain_core.pydantic_v1 import BaseModel, Field
warnings.filterwarnings('ignore')
# from chromadb import Documents, EmbeddingFunction, Embeddings
from langchain.memory import ChatMessageHistory
from typing import Literal

history = ChatMessageHistory()
model_name="BAAI/bge-small-en"
model_kwargs={"device":"cpu"}
encode_kwargs={"normalize_embeddings":True}
hf_embeddings=HuggingFaceBgeEmbeddings(model_name=model_name,model_kwargs=model_kwargs,encode_kwargs=encode_kwargs)
llm=ChatGroq(model="llama3-8b-8192",temperature=0)    
BNS_vectorstore=FAISS.load_local("/Users/sreyaskv/Documents/nyayamitra/NyayMitra-SIH/Vectordatabases/BNS_index_1",hf_embeddings,allow_dangerous_deserialization=True)
CCP_vectorstore=FAISS.load_local("/Users/sreyaskv/Documents/nyayamitra/NyayMitra-SIH/Vectordatabases/CCP_index_1",hf_embeddings,allow_dangerous_deserialization=True)
FAISS_vectorstore=FAISS.load_local("/Users/sreyaskv/Documents/nyayamitra/NyayMitra-SIH/Vectordatabases/faiss_index_2",hf_embeddings,allow_dangerous_deserialization=True)
retriever=CCP_vectorstore.as_retriever()
default_judiciary_template = """You are an AI assistant specializing in judiciary matters in India. \
You provide general legal information and help users navigate through the various Indian legal documents. \
When you don't know the answer to a question, you admit that you don't know.

Here is a question:
{query}"""

template_format=default_judiciary_template
a=5
def loading():
    def format_docs(docs):
        str1 = "\n\n".join(doc[0].page_content for doc in docs)
        return str1[0:10000]

    def source(docs):
        return "\n\n".join(str(doc[0].metadata['page']) for doc in docs)
    
    def routing(query):
        # Routing logic based on query keywords (modify as needed)
        class RouteQuery(BaseModel):
            """Route a user query to the most relevant datasource."""
            datasource: Literal[
                "Indian Penal Code", 
                "code of civil procedure",  
                "Indian constitution",
                "Other stuff"
            ] = Field(
                ...,
                description='''You are an intelligent routing model designed to direct user queries to the most relevant data source based on their content. Here are the three data sources you will consider:

CCP (Civil Court Proceedings): This source contains detailed information regarding civil court cases, including procedural rules, case law, and legal interpretations related to civil matters in India.

BNS (Indian Penal Code - IPC): This data source encompasses the Indian Penal Code, providing comprehensive details on criminal laws, definitions of offenses, and corresponding penalties applicable in India.

Constitution: This source includes the full text of the Constitution of India, providing foundational legal principles, rights, and duties of citizens, as well as the structure and functioning of government institutions.

Routing Task: Analyze the following user query and determine which data source (CCP, BNS,Constitution or General) is the most appropriate for retrieving the relevant information. Provide a brief justification for your choice based on the content of the query.
''',
            )

            class Config:
                arbitrary_types_allowed = True
        
        structured_llm = llm.with_structured_output(RouteQuery)

        system = """You are an expert at routing a user question to the appropriate data source.
        Based on the content or legal context the question is referring to, route it to the relevant data source."""

        # Create the prompt template
        prompt = ChatPromptTemplate.from_messages(
            [
                ("system", system),
                ("human", "{question}"),
            ]
        )
        router = prompt | structured_llm
        print(query)
        try:
            result = router.invoke(query)
            result=result.datasource
        except:
            result="Indian constitution"
        print(result)
        if result=='Indian Penal Code':
            return BNS_vectorstore.as_retriever()
        elif result=="code of civil procedure":
            return CCP_vectorstore.as_retriever()
        elif result=="Indian constitution":
            return FAISS_vectorstore.as_retriever()
        else:
            return CCP_vectorstore.as_retriever() 
    
    # Query generation
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

    # Reciprocal rank fusion
    def reciprocal_rank_fusion(results: list[list], k=60):
        fused_scores = {}
        for docs in results:
            for rank, doc in enumerate(docs):
                doc_str = dumps(doc)
                if doc_str not in fused_scores:
                    fused_scores[doc_str] = 0
                previous_score = fused_scores[doc_str]
                fused_scores[doc_str] += 1 / (rank + k)
        
        reranked_results = [
            (loads(doc), score)
            for doc, score in sorted(fused_scores.items(), key=lambda x: x[1], reverse=True)
        ]

        return reranked_results

    # Retrieval chain
    def retrieval_chain(retriever):
        return generate_queries | retriever.map() | reciprocal_rank_fusion
    
    def add_question_to_history(question):
        history.add_user_message(question)
        return question

    def add_output_to_history(output):
        history.add_ai_message(output)
        return output

    def get_history(question):
        return str(history.messages)

    # RAG chain with dynamic retriever passed
    prompt_template = PromptTemplate.from_template('''Welcome Message:

                                                "Namaste! I’m here to assist with your legal questions. Feel free to ask me anything related to legal matters."

                                                Response Instructions:

                                                Legal Queries:

                                                Provide clear, structured answers based on relevant laws, legal principles, or case precedents.
                                                If the user's query pertains to specific individuals or scenarios, refer to the chat history to ensure accurate context.
                                                Clarifying Ambiguities:

                                                If the query uses general terms like "him/her" and it's unclear who is being referred to, ask the user for additional details or context.
                                                Irrelevant Questions:

                                                Politely inform the user if their question is not related to legal matters and gently ask them to provide a relevant legal query.
                                                Summarizing Conversations:

                                                If requested, provide a summary of previous conversations in a clear and concise manner, focusing on key points.
                                                Note:

                                                Avoid mentioning specific context or technical details. Instead, focus on delivering helpful and accurate legal guidance.

                                                The pages used are {page}\n Question:{question} \n Context:{context}\n
                                                
                                                These are the previous conversations: {chat_history}''')
    
    def rag_chain(query):
        selected_retriever = routing(query)  # Get the retriever based on the query
        return (
            {"context": retrieval_chain(selected_retriever) | format_docs, 
             "question": RunnablePassthrough() | add_question_to_history,
             "page": retrieval_chain(selected_retriever) | source,
             "chat_history": get_history}
            | prompt_template
            | llm
            | StrOutputParser()
            | add_output_to_history   
        )

    return rag_chain

def generate(chain, query):
    output = chain(query).invoke(query)  # Pass query to dynamic chain
    return output

if __name__ == '__main__':
    print("hello")
    
    query = str(input("Enter your query: "))
    while query != "Exit":
        rag_chain = loading()  # Get a new chain for each query
        print(generate(rag_chain, query))
        print(a)
        query = str(input("Enter a follow-up question: "))
