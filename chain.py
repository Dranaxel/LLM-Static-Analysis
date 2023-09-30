import re
import os
import json
import sys
import asyncio
from rich.table import Table
from rich.console import Console

from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationSummaryMemory
from langchain.chains import ConversationalRetrievalChain
from langchain.text_splitter import Language
from langchain.document_loaders.generic import GenericLoader
from langchain.document_loaders.parsers import LanguageParser
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.document_loaders import TextLoader
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain.document_loaders import DirectoryLoader
from loguru import logger


async def review_directory(directory, extension=None, include_hidden=False):
    reviews = []

    loader = GenericLoader.from_filesystem(
        directory,
        glob="**/*",
        suffixes=[f".{extension}"],
        parser=LanguageParser(language=Language.PYTHON, parser_threshold=500),
    )
    documents = loader.load()
    python_splitter = RecursiveCharacterTextSplitter.from_language(
        language=Language.JS, chunk_size=2000, chunk_overlap=200
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
        "Review the entire architecture what are the good points and bad points. Give examples. Respond in markdown"
    )
    from rich.console import Console
    from rich.markdown import Markdown

    console = Console()
    md = Markdown(resp["answer"])
    console.print(md)

    # for root, dirs, files in os.walk(directory):
    #    logger.debug(files)
    #    for file in files:
    #        if not include_hidden and file.startswith("."):
    #            continue
    #        if re.search(extension, file):
    #            filename = os.path.join(root, file)
    #            code = load_code_from_file(filename)
    #            reviews.append(review_code(code, filename))
    # if len(reviews) == 0:
    #    logger.info("Nothing to analyse, exiting")
    #    exit(0)
    # reviews = await asyncio.gather(*reviews)
    # reviews = [json.loads(_) for _ in reviews]
    # return reviews


def display_reviews(reviews, sort_by="filename"):
    reviews.sort(key=lambda review: review[sort_by])
    table = Table(show_header=True, header_style="bold magenta", show_lines=True)
    table.add_column("Filename")
    table.add_column("Code Quality")
    table.add_column("Good Points", justify="full")
    table.add_column("Bad Points", justify="full")

    for review in reviews:
        color = (
            "green"
            if review["codeQuality"] > 9
            else "bright_green"
            if review["codeQuality"] > 7
            else "yellow"
            if review["codeQuality"] > 5
            else "orange"
            if review["codeQuality"] > 3
            else "red"
        )
        table.add_row(
            str(review["filename"]),
            str(review["codeQuality"]),
            str("\n".join(review["goodPoints"])),
            str("\n".join(review["badPoints"])),
            style=color,
        )

    console = Console()
    console.print(table)
