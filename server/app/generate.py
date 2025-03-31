from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_groq import ChatGroq
from langchain_core.output_parsers import JsonOutputParser
from pydantic import BaseModel, Field
from typing import List, Dict
import os
import dotenv
dotenv.load_dotenv()
# Define data models
class Step(BaseModel):
    type: str = Field(description="Action type: NAVIGATE, INTERACT, EXTRACT, etc.")
    params: Dict[str, str] = Field(description="Parameters needed for the action")

class AutomationPlan(BaseModel):
    steps: List[Step] = Field(description="List of automation steps")

# Set up planner LLM
planner_llm_gpt4o = ChatOpenAI(
    model="gpt-4o",
    temperature=0.1,
    api_key=os.getenv("OPENAI_API_KEY"),
    model_kwargs={"response_format": {"type": "json_object"}}
)
planner_llm_groq = ChatGroq(
    model="llama3-8b-8192",
    temperature=0.1,
    api_key=os.getenv("GROQ_API_KEY"),
    model_kwargs={"response_format": {"type": "json_object"}}
)

# Create prompt template
planner_prompt = ChatPromptTemplate.from_template(
    """
    Break this command into high-level objectives for web automation:
    Command: {command}

    Consider:
    1. First navigate to the main domain
    2. Then perform interactions
    3. Finally extract data

    action_type:
        click
        fill-click
        scroll-click
    
    Return JSON format:
    {{
        "steps": [
            {{
                "objective": "Navigate to domain",
                "type": "NAVIGATE",
                "params": {{"url": http://"..."}}
            }},
            {{
                "objective": "Perform search",
                "type": "INTERACT",
                "params": {{
                    "action_type": "fill-click",
                    "description": "Enter search query in main search box"
                }}
            }},
            {{
                "objective": "Get results",
                "type": "EXTRACT",
                "params": {{
                    "description": "Extract first search result information"
                }}
            }}
        ]
    }}
    """
)


# Create the processing chain
planner_chain = (
    planner_prompt 
    | planner_llm_groq
    | JsonOutputParser(pydantic_object=AutomationPlan)
)

def generate_plan(user_command: str) -> AutomationPlan:
    """
    Generate automation plan from natural language command
    """
    return planner_chain.invoke({"command": user_command})