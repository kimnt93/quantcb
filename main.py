import logging
from langchain.schema.runnable.config import RunnableConfig
import chainlit as cl
from langsmith import traceable
from src.runner import clarify_query_topics, get_companies_from_query, download_data, default_chat_chain, \
    synthesise_query_result_chain


@cl.step
async def _clarify_query_topics(question):
    topics = clarify_query_topics(question)
    return list(topics)


@cl.step
async def _get_companies_from_query(question):
    return list(get_companies_from_query(question))


@cl.step
async def _download_data(topics, companies) -> list:
    return list(download_data(topics, companies))


@cl.on_message
@traceable
async def market_chat(message: cl.Message):
    # Step 1: User Asks a Question
    question = message.content

    # Step 2: Generate SQL Query
    topics = await _clarify_query_topics(question)
    data = list()
    if len(topics) == 0:
        chain = default_chat_chain()
    else:
        companies = await _get_companies_from_query(question)
        if len(companies) == 0:
            chain = default_chat_chain()
        else:
            data = await _download_data(topics, companies)
            chain = synthesise_query_result_chain(companies, [d[0] for d in data])

    msg = cl.Message(content="")
    output_msg = ""
    # Stream the response to the user (Step 4)
    async for chunk in chain.astream(
        {"question": question},
        config=RunnableConfig(callbacks=[cl.LangchainCallbackHandler()]),
    ):
        await msg.stream_token(chunk)
        output_msg += chunk

    for _, fig in data:
        if fig is not None:
            print("================== Include the fig")
            msg.elements.append(cl.Plotly(figure=fig, display="inline"))

    await msg.send()
    return output_msg
