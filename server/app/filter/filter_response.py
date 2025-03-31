from typing import Dict, Any, List

def filter_input(input: List[Dict[Any,Any]]):
   
    filtered_input = []
    for x in input:
        new_dict = {}
        for k,v in x.items():
            if v is not None:
                new_dict[k] = v
        filtered_input.append(new_dict)
    return filtered_input


def remove_anchor_tags(input: List[Dict[Any,Any]]):
    filtered_input = []
    for x in input:
        if x['tag'] != 'a' and x['tag'] != 'button':
            filtered_input.append(x)
    return filtered_input

def remove_input_tags(input: List[Dict[Any,Any]]):
    filtered_input = []
    for x in input:
        if x['tag'] != 'input' and x['tag'] != 'textarea':
            filtered_input.append(x)
    return filtered_input

def get_only_inner_text(input: List[Dict[Any,Any]]):
    filtered_input = []
    for x in input:
        if 'inner_text' in x:
            if x['inner_text'] is not None:
                filtered_input.append(x['inner_text'])
    return filtered_input
