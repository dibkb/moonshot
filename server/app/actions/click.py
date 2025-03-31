from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
import os
import dotenv
from pydantic import BaseModel, Field
from typing import Dict,Any, Optional
from langchain_core.output_parsers import JsonOutputParser
from ..filter.filter_response import filter_input,remove_input_tags,get_only_inner_text

dotenv.load_dotenv()
planner_llm_groq = ChatGroq(
    model="llama3-8b-8192",
    temperature=0.1,
    api_key=os.getenv("GROQ_API_KEY"),
    model_kwargs={"response_format": {"type": "json_object"}}
)

class SearchElement(BaseModel):
    inner_text: str

class SearchAction(BaseModel):
    click_element: SearchElement = Field(description="Element to click")

def extract_click_elements(page_html: list[Dict[str,Any]],description: str):
    prompt = ChatPromptTemplate.from_template(
        """
        You are a web automation agent. You are given the page html to select which element to click.
        Page HTML: {page_html}

        The description of the action is: {description}

        You must return a valid JSON object with the following structure:
        
        "click_element": {{
            "inner_text": str
        }}
        
        
        Instructions:
            Based on the description, select the element to click to fulfill the action.
            - based on the inner_text of the html element, select the element to click.
        """
    )
    chain = prompt | planner_llm_groq | JsonOutputParser(pydantic_object=SearchAction)
    input = [m.model_dump() for m in page_html]
    filtered_input = remove_input_tags(filter_input(input))
    filtered_input = get_only_inner_text(filtered_input)
    try:
        response = chain.invoke({"page_html": filtered_input[0: min(len(filtered_input),50)],"description":description})
        return response
    except Exception as e:
        print(f"Error parsing response: {e}")
        # Return default structure with all null values
        return SearchAction(
            click_element=SearchElement()
        )