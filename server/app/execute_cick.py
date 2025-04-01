from playwright.async_api import Page
from .actions.click import SearchAction
from typing import Dict
from .utils.html_electors import make_selector
async def execute_click(page: Page, click_action: SearchAction):
    if 'href' in click_action['click_element'] and click_action['click_element']['href'] != "" and click_action['click_element']['href'] != "#":

        current_url = page.url
        href = click_action['click_element']['href']
        if href.startswith('http') or href.startswith('www'):
            await page.goto(href)
        else:
            if href.startswith('./'):
                href = href[2:] 
            if current_url.endswith('/'):
                full_url = current_url + href
            else:
                full_url = current_url + '/' + href
            await page.goto(full_url)
        return
    if 'inner_text' in click_action['click_element']:
        text = click_action['click_element']['inner_text']
        await page.get_by_text(text).first.click()
        return  
    if click_action['click_element']['tag']:
        click_element = await page.query_selector(make_selector(click_action['click_element']))
        await click_element.click()
        return
