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