"""
This file contains the controller that accepts command via HTTP
and trigger business logic layer to get JSON files from the local disk and write them in the avro format
"""
from flask import Flask, request
from flask import typing as flask_typing

from lec02.hw.job2.bll.reformat import convert_to_avro

app = Flask(__name__)


@app.route('/', methods=['POST'])
def main() -> flask_typing.ResponseReturnValue:
    """
    Controller that accepts command via HTTP and
    trigger business logic layer

    The POST body in JSON:
    {
      "raw_dir": "/path/to/my_dir/raw/sales/2022-08-09",
      "stg_dir": "/path/to/my_dir/stg/sales/2022-08-09"
    }
    """
    input_data: dict = request.json

    raw_dir = input_data.get('raw_dir')
    if not raw_dir:
        return {
            "message": "raw_dir parameter missed",
        }, 400

    stg_dir = input_data.get('stg_dir')
    if not stg_dir:
        return {
            "message": "stg_dir parameter missed",
        }, 400

    convert_to_avro(raw_dir, stg_dir)

    return {
        "message": "Files converted to the AVRO format successfully",
    }, 201


if __name__ == "__main__":
    app.run(debug=True, host="localhost", port=8082)
