from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field
from ..llms.main import LLM
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
llm = LLM()


class ExtractInformation(BaseModel):
    information: str = Field(description="The information that satisfies the users objective")


def extract_information(text: str, description: str, objective: str)->ExtractInformation:

    parser = JsonOutputParser(pydantic_object=ExtractInformation)

    try:

        prompt = PromptTemplate(
            template= 
                    """
        You are an information extraction agent. Your task is to analyze webpage content and extract relevant information based on the given description and objective in a presentable way to the user.

        Webpage Content: {text}

        Description of what to extract: {description}

        Objective/Goal: {objective}

        Instructions:
        - Extract relevant information from the webpage content
        - Structure your response using proper markdown formatting:
          * Use # for main headings
          * Use ## for subheadings
          * Use bullet points (- or *) for lists
          * Use > for important quotes or highlights
          * Use **bold** for emphasis on key points
          * Use tables where appropriate using | syntax
        - Ensure the response is well-organized and follows a logical flow
        - Include a brief summary at the beginning
        - Group related information under appropriate headings
        - Conclude with key takeaways or insights
        - Make sure the response directly addresses the objective
        - Use markdown formatting for the response
        - spacing after each section

         {format_instructions}
        """,
            input_variables=["text","description","objective"],
            partial_variables={"format_instructions": parser.get_format_instructions()},
        )

        chain = prompt | llm.get_groq_llm() | parser

        response = chain.invoke({"text": text, "description": description, "objective": objective})
        
        return response
    except Exception as e:
        print(f"Error parsing response: {e}")
        return {"error": "Failed to extract information", "details": str(e)}