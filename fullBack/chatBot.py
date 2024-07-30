import bs4
# from langchain import hub
# from langchain.text_splitter import RecursiveCharacterTextSplitter
# from langchain_community.document_loaders import WebBaseLoader
# from langchain_community.vectorstores import Chroma
# from langchain_core.output_parsers import StrOutputParser
# from langchain_core.runnables import RunnablePassthrough
# from langchain_openai import ChatOpenAI, OpenAIEmbeddings

# from langchain.llms import OpenAI
from langchain_openai import ChatOpenAI
# from langchain.llms import OpenAI

def testOpenAI():
    
    chat = ChatOpenAI(model="gpt-3.5-turbo-1106", temperature=0.2)
    from langchain_core.messages import HumanMessage, AIMessage

    chat.invoke(
        [
            HumanMessage(
                content="Translate this sentence from English to French: I love programming."
            )
        ]
    )
    # llm = OpenAI(temperature=0.9, openai_api_key="xQbdeEFYqaAseRAsC7pRT3BlbkFJiiz5xCFbk7uvP1zeUrE2")
    # llm = OpenAI(temperature=0.9)
    # text =  "What are 5 vacation destinations for someone who likes to eat pasta?"
    # print(llm(text))
    return AIMessage


# loader = WebBaseLoader(
#     web_paths=("https://lilianweng.github.io/posts/2023-06-23-agent/",),
#     bs_kwargs=dict(
#         parse_only=bs4.SoupStrainer(
#             class_=("post-content", "post-title", "post-header")
#         )
#     ),
# )
# docs = loader.load()

# text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
# splits = text_splitter.split_documents(docs)
# vectorstore = Chroma.from_documents(documents=splits, embedding=OpenAIEmbeddings())

# retriever = vectorstore.as_retriever()
# prompt = hub.pull("rlm/rag-prompt")
# llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0)


# def format_docs(docs):
#     return "\n\n".join(doc.page_content for doc in docs)


# rag_chain = (
#     {"context": retriever | format_docs, "question": RunnablePassthrough()}
#     | prompt
#     | llm
#     | StrOutputParser()
# )