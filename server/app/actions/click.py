
from langchain_core.prompts import ChatPromptTemplate
import dotenv
from pydantic import BaseModel, Field
from typing import Dict,Any, Optional
from langchain_core.output_parsers import JsonOutputParser
from ..filter.filter_response import filter_input,remove_input_tags,get_only_inner_text
from ..llms.main import LLM
dotenv.load_dotenv()
llm = LLM()

class SearchElement(BaseModel):
    id: Optional[str] = None
    tag: Optional[str] = None
    type: Optional[str] = None
    value: Optional[str] = None
    inner_text: Optional[str] = None
    placeholder: Optional[str] = None
    aria_label: Optional[str] = None
    class_name: Optional[str] = None
    href: Optional[str] = None


class SearchAction(BaseModel):
    click_element: SearchElement = Field(description="Element to click")

# def extract_click_elements(page_html: list[Dict[str,Any]],description: str):
#     prompt = ChatPromptTemplate.from_template(
#         """
#         You are a web automation agent. You are given the page html to select which element to click.
#         Page HTML: {page_html}

#         The description of the action is: {description}

#         You must return a valid JSON object with the following structure:
        
#         "click_element": {{
#             "inner_text": str,...
#         }}
        
#         Instructions:
#             Based on the description, select the element to click to fulfill the action.
#             - Find the matching element based on the inner_text
#             - Return the element with all its original key-value pairs intact
#             - Do not add any new fields that weren't in the original element
#         """
#     )
#     chain = prompt | llm.get_groq_llm() | JsonOutputParser(pydantic_object=SearchAction)
#     input = [m.model_dump() for m in page_html]
#     filtered_input = filter_input(input)
#     try:
#         response = chain.invoke({"page_html": filtered_input[0: min(len(filtered_input),50)],"description":description})
#         return response
#     except Exception as e:
#         print(f"Error parsing response: {e}")
#         # Return default structure with all null values
#         return SearchAction(
#             click_element=SearchElement()
#         )
    
def extract_click_elements(page_html: list[Dict[str,Any]],description: str):
    prompt = ChatPromptTemplate.from_template(
        """
        You are a web automation agent. You are given the page html to select which element to click.
        Page HTML: {page_html}

        The description of the action is: {description}

        You must return a valid JSON object with the following structure:
        
        "click_element": {{
            "inner_text": str,...
        }}
        
        Instructions:
            Based on the description, select the element to click to fulfill the action.
            - Find the matching element based on the inner_text
            - Return the element with all its original key-value pairs intact
            - Do not add any new fields that weren't in the original element
        """
    )
    chain = prompt | llm.get_groq_llm() | JsonOutputParser(pydantic_object=SearchAction)
    input = [m.model_dump() for m in page_html]
    filtered_input = filter_input(input)
    try:
        response = chain.invoke({"page_html": filtered_input[0: min(len(filtered_input),50)],"description":description})
        return response
    except Exception as e:
        print(f"Error parsing response: {e}")
        # Return default structure with all null values
        return SearchAction(
            click_element=SearchElement()
        )