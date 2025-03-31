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
    model="llama-3.3-70b-versatile",
    temperature=0.1,
    api_key=os.getenv("GROQ_API_KEY"),
    model_kwargs={"response_format": {"type": "json_object"}}
)

# Create prompt template
planner_prompt = ChatPromptTemplate.from_template(
    """
    You will analyze the command and return a JSON response with high-level objectives for web automation.
    In the command, withing | the actions need to performed on the same page.
    Command: {command}

    Consider:
    1. First navigate to the main domain
    2. Then perform interactions
    3. Finally extract data

    This should be the format of the objective always:
    
    Always give full url in the navigate objective

    For login/form filling actions:
    - Each field should be a separate action
    - For fill actions, always use this format in the JSON:
        "type": "INTERACT",
        "params": {{
            "action_type": "fill",
            "description": "Enter [field name]",
            "params": {{
                "value": "[actual value]"
            }}
        }}

    action_type options for JSON response:
        click
        fill
        fill-click
        scroll-click
    
    Return a JSON object in exactly this format:
    {{
        "steps": [
            {{
                "objective": "Navigate to login page",
                "type": "NAVIGATE",
                "params": {{"url": "https://www.example.com"}}
            }},
            {{
                "objective": "Enter email",
                "type": "INTERACT",
                "params": {{
                    "action_type": "fill",
                    "description": "Enter email in email field",
                    "params": {{
                        "value": "user@example.com"
                    }}
                }}
            }},
            {{
                "objective": "Enter password",
                "type": "INTERACT",
                "params": {{
                    "action_type": "fill",
                    "description": "Enter password in password field",
                    "params": {{
                        "value": "password123"
                    }}
                }}
            }},
            {{
                "objective": "Submit login",
                "type": "INTERACT",
                "params": {{
                    "action_type": "click",
                    "description": "Click login button"
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