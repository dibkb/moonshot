from typing import Dict
from playwright.async_api import Page
from .actions.search import SearchAction

async def execute_search(page: Page, search_action: SearchAction, context: Dict[str, str]):
    print(search_action)
    input_element = search_action['search_query_element']
    submit_element = search_action['submit_element']
    
    # Use proper CSS selector syntax
    if input_element['id']:
        input_element = await page.query_selector(f"{input_element['tag']}[id='{input_element['id']}']")
    elif input_element['name']:
        input_element = await page.query_selector(f"{input_element['tag']}[name='{input_element['name']}']")
    
    # Fix the submit element selection logic
    if submit_element['id'] and submit_element['id'] != 'None':
        submit_element = await page.query_selector(f"{submit_element['tag']}[id='{submit_element['id']}']")
    elif submit_element['name'] and submit_element['name'] != 'None':
        submit_element = await page.query_selector(f"{submit_element['tag']}[name='{submit_element['name']}']")
    print(input_element, submit_element)
    if input_element:
        await input_element.fill(context['query'])
        # Add a small wait to ensure the input is processed
    
    if submit_element:
        print(submit_element)
        await submit_element.click()
        # Wait for navigation after click
        # await page.wait_for_load_state('networkidle')
