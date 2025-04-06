import os
from typing import List, Dict, Any
import json

def read_json(path: str, json_file_name: str) -> List[Dict[str, Any]]:
    """

    :param path:
    :param json_file_name:
    :return:
    """
    json_file_path = os.path.join(path, json_file_name)
    with open(json_file_path, 'r', encoding='utf-8') as json_file:
        return json.load(json_file)