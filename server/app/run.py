from playwright.async_api import Playwright

async def run(browser,url:str):
    page = await browser.new_page()
    await page.goto(url)
    
    elements = await page.query_selector_all('input,button,a')
    
    element_metadata = []
    for element in elements:
        box = await element.bounding_box()
        if box:
            metadata = {
                "selector": await element.get_attribute("id") or await element.get_attribute("name"),
                "type": await element.get_attribute("type"),
                "value": await element.get_attribute("value"),
                "tag": await element.evaluate('element => element.tagName.toLowerCase()'), 
                "position": {
                    "x": box["x"],
                    "y": box["y"],
                    "width": box["width"],
                    "height": box["height"]
                },
                "text": await element.inner_text()
            }
            
                
            element_metadata.append(metadata)