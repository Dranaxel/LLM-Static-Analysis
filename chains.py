from loguru import logger
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.memory import ConversationSummaryMemory
from langchain.chains import ConversationalRetrievalChain
from langchain.text_splitter import Language
from langchain.document_loaders.generic import GenericLoader
from langchain.document_loaders.parsers import LanguageParser
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Chroma


async def review_file(code, filename):
    logger.debug(f"reviewing {filename}")
    template = PromptTemplate.from_template(
        """
     Please review the following code according to the criteria outlined below. Your review should be returned as a JSON objects. Each JSON object should contain the following keys:

    1. "filename": the name of the file
    2. "codeQuality": A score out of ten that represents the overall quality of the code. Please consider factors such as readability, efficiency, and adherence to best practices when determining this score.
    3. "goodPoints": An array of points that highlight the strengths of the code. This could include things like effective use of data structures, good commenting, efficient algorithms, etc.
    4. "badPoints": An array of points that highlight areas where the code could be improved. This could include things like unnecessary repetition, lack of comments, inefficient algorithms, etc.

    Please ensure that your review is thorough and constructive. Remember, the goal is to help the coder improve, not to criticize them unnecessarily.

    Example of expected output:
        {{
            "filename": {{filename}},
            "codeQuality": 5,
            "goodPoints": ["Efficient algorithms"],
            "badPoints": ["Lack of comments", "Inefficient data structures"]
        }}

    output only the json

    Filename: {filename}
    Code: {code}

    """
    )
    llm = ChatOpenAI(temperature=0.8, model="gpt-4")
    chain = LLMChain(llm=llm, prompt=template)
    review = await chain.arun(code=code, filename=filename)
    logger.debug(review)
    return review


def review_directory(directory, glob=None):
    loader = GenericLoader.from_filesystem(
        directory,
        glob=glob,
        parser=LanguageParser(language=Language.PYTHON, parser_threshold=500),
    )
    documents = loader.load()
    python_splitter = RecursiveCharacterTextSplitter.from_language(
        language=Language.PYTHON, chunk_size=2000, chunk_overlap=200
    )
    texts = python_splitter.split_documents(documents)
    db = Chroma.from_documents(texts, OpenAIEmbeddings(disallowed_special=()))
    retriever = db.as_retriever(
        search_type="mmr",  # Also test "similarity"
        search_kwargs={"k": 8},
    )
    llm = ChatOpenAI(model_name="gpt-4")
    memory = ConversationSummaryMemory(
        llm=llm, memory_key="chat_history", return_messages=True
    )
    qa = ConversationalRetrievalChain.from_llm(llm, retriever=retriever, memory=memory)
    resp = qa(
        "Make a full analysis of the code in the memory. This mean a section readability, optimization and structure. Respond in markdown"
    )
    from rich.console import Console
    from rich.markdown import Markdown

    console = Console()
    md = Markdown(resp["answer"])
    console.print(md)
