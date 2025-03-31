from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
import os
import dotenv
from pydantic import BaseModel, Field
from typing import Dict,Any, Optional
from langchain_core.output_parsers import JsonOutputParser
from ..filter.filter_response import filter_input,remove_anchor_tags

dotenv.load_dotenv()
planner_llm_groq = ChatGroq(
    model="llama-3.3-70b-versatile",
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
    inner_text: Optional[str] = Field(default=None, description="Inner text of the element")
class SearchAction(BaseModel):
    fill_element: SearchElement = Field(description="Element to fill")

def extract_fill_click(page_html: list[Dict[str,Any]],description: str,objective: str):
    prompt = ChatPromptTemplate.from_template(
        """
        You are a web automation agent. You are given the page html to select which element to fill. to fill the element you need to know the objective of the action.After filling the element, enter will be pressed to perform the search.
        Page HTML: {page_html}

        The description of the action is: {description}

        The objective of the action is: {objective}

        You must return a valid JSON object with all the original attributes of the element:
        
        "fill_element": {{
            id: str
            name: str 
            ....
        }}
        
        
        Instructions:
        - Do not include any comments or additional text in the JSON
        - The response must be a valid JSON object
        - The response must be a valid element from the page html
        """
    )
    chain = prompt | planner_llm_groq | JsonOutputParser(pydantic_object=SearchAction)
    input = [m.model_dump() for m in page_html]
    filtered_input = filter_input(input)
    filtered_input = remove_anchor_tags(filtered_input)

    try:
        response = chain.invoke({"page_html": filtered_input,"description":description, "objective":objective})
        return response
    except Exception as e:
        print(f"Error parsing response: {e}")
        # Return default structure with all null values
        return SearchAction(
            fill_element=SearchElement()
        )