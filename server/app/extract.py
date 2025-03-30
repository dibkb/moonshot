from playwright.async_api import Page
from pydantic import BaseModel
from typing import Dict, List, Optional

class ElementMetadata(BaseModel):
    id: Optional[str] = None
    name: Optional[str] = None
    tag: Optional[str] = None
    title: Optional[str] = None
    type: Optional[str] = None
    value: Optional[str] = None
    text: Optional[str] = None
    placeholder: Optional[str] = None
    aria_label: Optional[str] = None

    def dict(self, *args, **kwargs):
        # Override dict method to exclude None values
        base_dict = super().dict(*args, **kwargs)
        return {k: v for k, v in base_dict.items() if v is not None}

async def extract_elements(page: Page):
    elements = await page.query_selector_all('input,button,textarea')
    element_metadata: List[ElementMetadata] = []
    
    for element in elements:
        box = await element.bounding_box()
        if box:
            metadata = {}
            
            # Only add fields if they're not None
            if (id := await element.get_attribute("id")):
                metadata["id"] = str(id)
            if (name := await element.get_attribute("name")):
                metadata["name"] = str(name)
            if (tag := await element.evaluate('element => element.tagName.toLowerCase()')):
                metadata["tag"] = str(tag)
            if (type := await element.get_attribute("type")):
                metadata["type"] = str(type)
            if (value := await element.get_attribute("value")):
                metadata["value"] = str(value)
            if (title := await element.get_attribute('title')):
                metadata["title"] = str(title)
            if (text := await element.inner_text()):
                metadata["text"] = str(text)
            
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