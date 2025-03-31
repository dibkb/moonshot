from typing import Dict
from playwright.async_api import Page
from .utils.html_electors import make_selector
from .actions.search import SearchAction

async def execute_search(page: Page, search_action: SearchAction, context: Dict[str, str]):
    input_element = search_action['search_query_element']
    submit_element = search_action['submit_element']
    params = context['params']

    if input_element['tag']:
        input_element = await page.query_selector(make_selector(input_element))
    if input_element:
        await input_element.fill(params['value'])
        await page.keyboard.press('Enter')

    if submit_element['tag']:
        submit_element = await page.query_selector(make_selector(submit_element))

    if submit_element:
        await submit_element.click()
        # Wait for navigation after click
        # await page.wait_for_load_state('networkidle')


