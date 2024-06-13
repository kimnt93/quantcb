from functools import cache

import requests

from src import YAHOO_FIN_SEARCH_BASE, DEFAULT_USER_AGENT
from src.ticker import TickerInfo
import re
import os
from diskcache import Cache


CACHE_DIR = ".cache"
os.makedirs(CACHE_DIR, exist_ok=True)
_disk_cache = Cache(CACHE_DIR)  # Specify the directory where cache data will be stored


def extract_companies_from_text(text):
    # Regular expression pattern to match a Python list
    pattern = r'\[.*?\]'

    # Find all occurrences of the pattern in the text and extract lists
    companies = []
    for match in re.findall(pattern, text):
        try:
            extracted_list = eval(match)  # Evaluate the match as Python code
            if isinstance(extracted_list, list):
                companies.extend(extracted_list)
        except SyntaxError:
            pass  # Ignore invalid matches

    # Return a list of unique company names
    return list(set(companies))


@cache
def list_all_topics():
    methods = []
    for name in dir(TickerInfo):
        attr = getattr(TickerInfo, name)
        if callable(attr) and not name.startswith("__"):
            methods.append(name)

    methods = list(set(methods))
    methods.append("none_of_above")
    return methods


def extract_mentioned_topics(text, top=3):
    topics = list_all_topics()
    mentioned_topics = [topic for topic in topics if topic in text]
    return mentioned_topics[:top]


def get_ticker_from_name(name):
    """
    Fetches ticker information for a given company name from Yahoo Finance.

    Args:
        name (str): The company name to search for.

    Returns:
        dict: A dictionary containing ticker information (symbol, short_name, long_name, exchange).
    """
    # Check if the result is already cached
    if name in _disk_cache:
        return _disk_cache[name]

    params = {"q": name}
    response = requests.get(
        YAHOO_FIN_SEARCH_BASE,
        params=params,
        headers={
            'User-Agent': DEFAULT_USER_AGENT,
            "content-type": "application/json"
        }
    )
    data = response.json()  # Directly use the JSON response as a dictionary
    try:
        record = data['quotes'][0]
        result = {
            "symbol": record['symbol'],
            "short_name": record['shortname'],
            "long_name": record['longname'],
            'exchange': record['exchange'],
        }
        # Cache the result
        _disk_cache[name] = result
        return result
    except (KeyError, IndexError):
        return None
