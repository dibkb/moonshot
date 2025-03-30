from typing import Dict
from playwright.async_api import Page
from .actions.search import SearchAction

async def execute_search(page: Page, search_action: SearchAction, context: Dict[str, str]):
    input_element = search_action['search_query_element']
    submit_element = search_action['submit_element']
    

    if input_element['tag']:
        input_element = await page.query_selector(make_selector(input_element))
    if submit_element['tag']:
        submit_element = await page.query_selector(make_selector(submit_element))
    if input_element:
        await input_element.fill(context['query'])
        # Add a small wait to ensure the input is processed
    
    if submit_element:
        print(submit_element)
        await submit_element.click()
        # Wait for navigation after click
        # await page.wait_for_load_state('networkidle')


def make_selector(element: Dict[str, str]):
    str_input_element = ""
    for k,v in element.items():
        if v != None and k != 'tag' and k != 'text':  # Skip tag and text attributes
            str_input_element += f"][{k}='{v}'"
    # Remove the first ][ and add closing bracket
    selector = f"{element['tag']}[{str_input_element[2:]}]"
    return selector