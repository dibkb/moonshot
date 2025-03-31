from typing import Dict
allowed_attributes = ['class_name', 'id', 'name', 'type', 'value', 'inner_text', 'placeholder', 'aria_label']
def make_selector(element: Dict[str, str]):
    attributes = []
    for k, v in element.items():
        if v is not None and v.strip() != '' and k in allowed_attributes:
            key = k
            if k == 'class_name':
                key = 'class'
            if k == 'inner_text':
                key = 'text'
            if k == 'aria_label':
                key = 'aria-label'
            attributes.append(f"[{key}='{v}']")
    
    selector = f"{element['tag']}{''.join(attributes)}"
    return selector