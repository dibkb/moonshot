from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
import os
import dotenv
from pydantic import BaseModel, Field
from typing import Dict,Any, Optional
from langchain_core.output_parsers import JsonOutputParser
from ..filter.filter_response import filter_input, remove_anchor_tags

dotenv.load_dotenv()
from ..extract import ElementMetadata
planner_llm_groq = ChatGroq(
    model="llama3-8b-8192",
    temperature=0.1,
    api_key=os.getenv("GROQ_API_KEY"),
    model_kwargs={"response_format": {"type": "json_object"}}
)

class SearchElement(BaseModel):
    id: Optional[str] = Field(default=None, description="Id of the element")
    name: Optional[str] = Field(default=None, description="Name of the element")
    type: Optional[str] = Field(default=None, description="Type of element (input, button, etc.)")
    tag: Optional[str] = Field(default=None, description="Tag of the element (input, button, etc.)")
    title: Optional[str] = Field(default=None, description="Title of the element")
    text: Optional[str] = Field(default=None, description="Text of the element")

class SearchAction(BaseModel):
    search_query_element: SearchElement = Field(description="Element to input search query")
    submit_element: SearchElement = Field(description="Element to submit the search")

def extract_fill_click_elements(page_html: list[Dict[str,Any]],description: str):
    prompt = ChatPromptTemplate.from_template(
        """
        You are a web automation agent. You are given the page html to select which element to fill the search query and which element to click to submit the search query.
        Page HTML: {page_html}

        The description of the action is: {description}

        You must return a valid JSON object with the following structure:
        {{
            "search_query_element": {{
                "id": null,
                "name": null,
                "type": null,
                "tag": null,
                "title": null,
                "inner_text": null,
                "class": null
            }},
            "submit_element": {{
                "id": null,
                "name": null,
                "type": null,
                "tag": null,
                "title": null,
                "inner_text": null,
                "class": null
            }}
        }}
        
        Instructions:
        - All fields (id, name, type, tag) must be included in both elements
        - Use null for any missing values
        - Do not include any comments or additional text in the JSON
        - The response must be a valid JSON object
        """
    )
    chain = prompt | planner_llm_groq | JsonOutputParser(pydantic_object=SearchAction)
    input = [m.model_dump() for m in page_html]
    filtered_input = filter_input(input)
    filtered_input = remove_anchor_tags(filtered_input)
    try:
        response = chain.invoke({"page_html": filtered_input,"description":description})
        return response
    except Exception as e:
        print(f"Error parsing response: {e}")
        # Return default structure with all null values
        return SearchAction(
            search_query_element=SearchElement(),
            submit_element=SearchElement()
        )