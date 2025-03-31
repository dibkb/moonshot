from playwright.async_api import Page

async def get_clean_text(page:Page):
    await page.wait_for_selector("body")
    raw_text = await page.locator("body").inner_text()
    
    # Basic cleaning
    cleaned_text = "\n".join([
        line.strip() for line in raw_text.split("\n")
        if line.strip()
    ])

    return cleaned_text