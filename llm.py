import json
import time
from typing import List
from langchain_openai import ChatOpenAI
import os
from langchain.tools import tool
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.memory import ChatMessageHistory
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.documents import Document
from langchain_chroma import Chroma
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.prompts import PromptTemplate
from data import my_data

class DictLoader:
    def __init__(self, data):
        self.data = data

    def load(self) -> List[Document]:
        # Process the data using the dictionary
        documents = []
        for seq_num, item in enumerate(self.data['content'], start=1):
            page_content = json.dumps(item)
            metadata = {'seq_num': seq_num}
            documents.append(Document(page_content=page_content, metadata=metadata))

        return documents

class Retriever:
    loader = None
    retriever = None

    def __init__(self, data):
        loader = DictLoader(
            data=data
        )

        docs = loader.load()
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        splits = text_splitter.split_documents(docs)
        vectorstore = Chroma.from_documents(documents=splits, embedding=OpenAIEmbeddings(model="text-embedding-3-large"))

        # Retrieve and generate using the relevant snippets of the blog.
        retriever = vectorstore.as_retriever(
            search_type='mmr',
            search_kwargs={'k': 6, 'lambda_mult': 0.25}
        )
        self.retriever = retriever

retriever = Retriever(data=my_data).retriever

prompt = """You are Jefferson, a passionate software developer. Use the following pieces of retrieved context to answer the question. If you don't know the answer, just say that you don't know. Use three sentences maximum and keep the answer concise.

Question: {question} 

Context: {context} 

Answer:
"""

prompt_ = PromptTemplate.from_template(
    prompt
)

def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

@tool
def get_rag_response(question):
    """
    Get a response from the RAG model.
    """
    llm = ChatOpenAI(model="gpt-4o", temperature=0, verbose=False)
    rag_chain = (
        {"context": retriever | format_docs, "question": RunnablePassthrough()}
        | prompt_
        | llm
        | StrOutputParser()
    )

    res = rag_chain.invoke(question)
    return res


llm = ChatOpenAI(
    model="gpt-4o",
)
system_prompt = f"""
You are a software engineer. Your name is Jefferson. You are being talked to by people in your field, potentially those looking to hire you.
You must answer professionally, and accurately without making stuff up, and pull information with rag tool as needed.

You are interactive with people on a terminal, so structure your responses accordingly. This terminal does not support text formatting including new lines.

You can use RAG to get the following information:
basic_info, timeline, education, experience, projects, hobbies, skills, certifications, languages_known, other_info and faqs.

basic_info: name, location, email, phone, github, linkedin, experience, expertise, summary
other_info: life experiences, personal opinions, career goals

When invoking rag, provide context from chat history if required, and rephrase the text to optimize relevant hits.
You can invoke rag multiple times to get all the information needed.

Do not answer questions unrelated to you and your experiences.

If you cannot find a relevant answer to the question based on your knowledge and the rag response, provide contact information to directly reach out
to Jefferson, which can be obtained using RAG.

Use Timeline to answer questions on projects, education and experience if needed.

Current Date is {time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())}

"""

# Create an agent executor by passing in the agent and tools
prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            system_prompt,
        ),
        MessagesPlaceholder(variable_name="chat_history"),
        ("human", "{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ]
)
agent = create_tool_calling_agent(llm, [get_rag_response], prompt)
agent_executor = AgentExecutor(agent=agent, tools=[get_rag_response], verbose=False)

ephemeral_chat_history_for_chain = ChatMessageHistory()  

conversational_agent_executor = RunnableWithMessageHistory(
    agent_executor,
    lambda session_id: ephemeral_chat_history_for_chain,
    input_messages_key="input",
    output_messages_key="output",
    history_messages_key="chat_history",
    verbose=False,
)

async def get_llm_response(question):
    if conversational_agent_executor is not None:
        res = await conversational_agent_executor.ainvoke({
                    "input": question
                },{"configurable": {"session_id": "main"}},)
                
        return "JeffAI: " + res['output']