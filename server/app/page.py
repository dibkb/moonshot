from playwright.async_api import Page
async def get_page_text(page: Page):
    page_text = set()
    elements = await page.query_selector_all("*")
    for element in elements:
        text = await element.inner_text()
        if text.strip():
            page_text.add(text.strip())
    return page_text