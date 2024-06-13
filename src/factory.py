import dataclasses
import datetime
import os

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_groq import ChatGroq

from src.prompt import EXTRACT_COMPANY_NAME_PROMPT, ACTION_ROUTE_PROMPT, SYNTHETIC_PROMPT, DEFAULT_PROMPT
from src.services import list_all_topics


@dataclasses.dataclass
class Model:
    DEFAULT_LLM = ChatGroq(
        groq_api_key=os.environ['GROQ_API_KEY'],
        model_name="llama3-8b-8192"
    )
    FUNCTION_CALL_LLM = ChatGroq(
        groq_api_key=os.environ['GROQ_API_KEY'],
        model_name="llama3-70b-8192"
    )
    LARGE_LLM = FUNCTION_CALL_LLM


class ChainFactory:
    @staticmethod
    def create_extract_company_chain():
        return (
            {"question": RunnablePassthrough()}
            | PromptTemplate(
                template=EXTRACT_COMPANY_NAME_PROMPT,
                input_variables=["question"],
            )
            | Model.DEFAULT_LLM
            | StrOutputParser()
        )

    @staticmethod
    def create_action_route_chain():
        topics = list_all_topics()
        return (
            {"question": RunnablePassthrough()}
            | PromptTemplate(
                template=ACTION_ROUTE_PROMPT,
                input_variables=["question"],
                partial_variables={"topics": topics}
            )
            | Model.DEFAULT_LLM
            | StrOutputParser()
        )

    @staticmethod
    def create_synthetic_chain(companies, data):
        return (
            {"question": RunnablePassthrough()}
            | PromptTemplate(
                template=SYNTHETIC_PROMPT,
                input_variables=["question"],
                partial_variables={
                    "companies": companies,
                    "data": data,
                    "today": datetime.datetime.now()
                }
            )
            | Model.DEFAULT_LLM
            | StrOutputParser()
        )

    @staticmethod
    def create_default_chain():
        return (
            {"question": RunnablePassthrough()}
            | PromptTemplate(
                template=DEFAULT_PROMPT,
                input_variables=["question"],
                partial_variables={
                    "today": datetime.datetime.now()
                }
            )
            | Model.DEFAULT_LLM
            | StrOutputParser()
        )
