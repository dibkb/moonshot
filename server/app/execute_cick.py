from playwright.async_api import Page
from .actions.click import SearchAction
from typing import Dict
from .utils.html_electors import make_selector
async def execute_click(page: Page, click_action: SearchAction):
    if 'inner_text' in click_action['click_element']:
        text = click_action['click_element']['inner_text']
        await page.get_by_text(text).first.click()
    else:
        if click_action['click_element']['tag']:
            print("\n")
            print("make_selector",make_selector(click_action['click_element']))
            print("\n")
            click_element = await page.query_selector(make_selector(click_action['click_element']))
            await click_element.click()
