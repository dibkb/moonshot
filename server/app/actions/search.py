from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
import os
import dotenv
from pydantic import BaseModel, Field
from typing import Dict
from langchain_core.output_parsers import JsonOutputParser


dotenv.load_dotenv()
from ..extract import ElementMetadata
planner_llm_groq = ChatGroq(
    model="llama3-8b-8192",
    temperature=0.1,
    api_key=os.getenv("GROQ_API_KEY"),
    model_kwargs={"response_format": {"type": "json_object"}}
)

class SearchElement(BaseModel):
    id: str = Field(description="Id of the element")
    name: str = Field(description="Name of the element")
    type: str = Field(description="Type of element (input, button, etc.)")
    tag: str = Field(description="Tag of the element (input, button, etc.)")
class SearchAction(BaseModel):
    search_query_element: SearchElement = Field(description="Element to input search query")
    submit_element: SearchElement = Field(description="Element to submit the search")

def extract_search_elements(page_html: list[ElementMetadata])->SearchAction:
    prompt = ChatPromptTemplate.from_template(
        """
        You are a web automation agent. You are given the page html to select which element to fill the search query and which element to click to submit the search query.
        Page HTML: {page_html}

        input_elements_format : [{{"tag": "input", "title": None, "type": "text", "value": "", "text": "", "placeholder": "Search Amazon.in", "aria_label": "Search Amazon.in"}}.....]

        Return JSON format:
        {{
            "search_query_element": {{"id": "search_query_element_id", "name": "search_query_element_name", "type": "input", "tag": "input"}},
            "submit_element": {{"id": "submit_element_id", "name": "submit_element_name", "type": "button", "tag": "button"}}
        }}
        
        Popluate the search_query_element and submit_element with the correct id, name, type and tag. from the given page_html.

        """
    )
    # Add JsonOutputParser with the Pydantic model
    chain = prompt | planner_llm_groq | JsonOutputParser(pydantic_object=SearchAction)
    input = [m.model_dump() for m in page_html]
    print(input)
    return chain.invoke({"page_html": input})