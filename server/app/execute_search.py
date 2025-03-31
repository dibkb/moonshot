from typing import Dict
from playwright.async_api import Page
from .utils.html_electors import make_selector
from .actions.search import SearchAction

async def execute_search(page: Page, search_action: SearchAction, context: Dict[str, str]):
    input_element = search_action['fill_element']
    params = context['params']

    if input_element['tag']:
        print("\n")
        print("make_selector",make_selector(input_element))
        print("\n")
        input_element = await page.query_selector(make_selector(input_element))
    if input_element:
        await input_element.fill(params['value'])
        await input_element.press('Enter')


