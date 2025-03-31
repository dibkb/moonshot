from playwright.async_api import Page
from .actions.click import SearchAction
from typing import Dict

async def execute_click(page: Page, click_action: SearchAction):
    text = click_action['click_element']['inner_text']
    await page.get_by_text(text).first.click()