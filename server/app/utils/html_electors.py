from typing import Dict

def make_selector(element: Dict[str, str]):
    attributes = []
    for k, v in element.items():
        if v is not None and v.strip() != '' and k != 'tag' and k != 'text':
            if k == 'class_name':
                key = 'class'
            else:
                key = k
            attributes.append(f"[{key}='{v}']")
    
    selector = f"{element['tag']}{''.join(attributes)}"
    return selector