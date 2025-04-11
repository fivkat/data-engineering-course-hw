import os
from typing import List, Dict, Any
import json


def read_json(path: str, json_file_name: str) -> List[Dict[str, Any]]:
    """
    The function to read the JSON file.

    :param path: the path to the JSON file
    :param json_file_name: the name of the JSON file
    :return: the JSON file
    """
    json_file_path = os.path.join(path, json_file_name)
    with open(json_file_path, 'r', encoding='utf-8') as json_file:
        return json.load(json_file)
