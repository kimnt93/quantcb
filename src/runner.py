import logging
from src.factory import ChainFactory
from src.services import extract_companies_from_text, get_ticker_from_name, extract_mentioned_topics
from src.ticker import TickerInfo


def get_companies_from_query(query: str):
    chain = ChainFactory.create_extract_company_chain()
    result = chain.invoke(query)
    companies = extract_companies_from_text(result)

    for company_name in companies:
        yield get_ticker_from_name(company_name)


def clarify_query_topics(query: str):
    chain = ChainFactory.create_action_route_chain()
    result = chain.invoke(query)
    topics = extract_mentioned_topics(result)
    return topics


def download_data(topics, companies):
    for topic in topics:
        for company in companies:
            data, fig = getattr(TickerInfo, topic)(**company)
            logging.info(f"Download data {topic}, {company} ===>>>> {data}")
            yield data, fig


def synthesise_query_result_chain(companies, data):
    chain = ChainFactory.create_synthetic_chain(companies, data)
    return chain


def default_chat_chain():
    chain = ChainFactory.create_default_chain()
    return chain
