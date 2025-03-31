from playwright.async_api import Page
async def get_page_text(page: Page):
    await page.wait_for_load_state('networkidle',timeout=10000)
    await page.wait_for_load_state('domcontentloaded',timeout=10000)
    page_text = set()
    elements = await page.query_selector_all("*")
    for element in elements:
        print("element",element)
        text = await element.inner_text()
        if text.strip():
            page_text.add(text.strip())
    return page_text