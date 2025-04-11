import os
from typing import List, Dict, Any
import json

def save_json_to_disk(json_content: List[Dict[str, Any]], path: str, json_file_name: str) -> None:
    """
        Write the JSON returned from the API into the local directory.

        :param json_content: list of records returned from the API in the JSON format
        :param path: the path to write to
        :param json_file_name: the name of the JSON file
        :return: None
    """

    json_file_path = os.path.join(path, json_file_name)
    with open(json_file_path, 'w') as json_file:
        json.dump(json_content, json_file, indent=4)
        print(f"JSON data written to {json_file_path}")
