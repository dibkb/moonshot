from .actions.fill import SearchAction
from playwright.async_api import Page
from typing import Dict
from .utils.html_electors import make_selector
async def execute_fill(page: Page, fill_action: SearchAction, context: Dict[str, str]):
    input_element = fill_action['fill_element']
    params = context['params']

    if input_element['tag']:
        print("\n")
        print("make_selector",make_selector(input_element))
        print("\n")
        input_element = await page.query_selector(make_selector(input_element))
    if input_element:
        await input_element.fill(params['value'])

