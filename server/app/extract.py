from playwright.async_api import Page
from pydantic import BaseModel
from typing import Dict, List, Optional

class ElementMetadata(BaseModel):
    id: Optional[str] = None
    # name: Optional[str] = None
    tag: Optional[str] = None
    href: Optional[str] = None
    type: Optional[str] = None
    value: Optional[str] = None
    inner_text: Optional[str] = None
    placeholder: Optional[str] = None
    aria_label: Optional[str] = None
    class_name: Optional[str] = None
    def dict(self, *args, **kwargs):
        # Override dict method to exclude None values
        base_dict = super().dict(*args, **kwargs)
        return {k: v for k, v in base_dict.items() if v is not None}

async def extract_elements(page: Page):
    # Wait for network to be idle and DOM to be loaded
    await page.wait_for_load_state('networkidle',timeout=10000)
    await page.wait_for_load_state('domcontentloaded',timeout=10000)

    elements = await page.query_selector_all('input,button,textarea,a,form,label')
    element_metadata: List[ElementMetadata] = []

    for element in elements:
        box = await element.bounding_box()
        if box:
            metadata = {}
            
            # Only add fields if they're not None
            if (id := await element.get_attribute("id")):
                metadata["id"] = str(id)
            if (class_name := await element.get_attribute("class")):
                metadata["class_name"] = str(class_name)
            if (href := await element.get_attribute("href")):
                metadata["href"] = str(href)
            if (tag := await element.evaluate('element => element.tagName.toLowerCase()')):
                metadata["tag"] = str(tag)
            if (type := await element.get_attribute("type")):
                metadata["type"] = str(type)
            if (value := await element.get_attribute("value")):
                metadata["value"] = str(value)
            # if (title := await element.get_attribute('title')):
            #     metadata["title"] = str(title)
            if (text := await element.inner_text()):
                metadata["inner_text"] = str(text)
            
            # Check for placeholder and aria-label only for input/textarea
            if tag in ('input', 'textarea'):
                if (placeholder := await element.get_attribute("placeholder")):
                    metadata["placeholder"] = str(placeholder)
                if (aria_label := await element.get_attribute("aria-label")):
                    metadata["aria_label"] = str(aria_label)
            
            # Only add non-empty metadata
            if metadata:
                element_metadata.append(ElementMetadata(**metadata))
    
    return element_metadata