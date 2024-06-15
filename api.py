from datetime import datetime
import hashlib
import json
import random
import requests
import sys
from typing import Tuple


API = "https://codeforces.com/api"
with open("credentials.json") as f:
    credentials = json.load(f)


def parse_arguments() -> Tuple[str, str, dict]:
    parameters = {}
    file_path = sys.argv[1]
    method = sys.argv[2]
    args = sys.argv[3:]

    for arg in args:
        key_value = arg[2:].split('=', 1)
        if not arg.startswith('--') or len(key_value) != 2:
            raise Exception("Wrong usage!")
        key, value = key_value
        parameters[key] = value

    return file_path, method, parameters


def call(methodName: str, parameters: dict) -> dict:
    query = methodName

    parameters["apiKey"] = credentials["KEY"]
    parameters["time"] = int(round(datetime.now().timestamp()))

    sep = "?"
    for name, value in sorted(parameters.items()):
        query += sep + name + "=" + str(value)
        sep = "&"

    rand = str(random.randint(100000, 1000000))

    to_sig = rand + "/" + query + "#" + credentials["SECRET"]
    sig = hashlib.sha512(to_sig.encode("utf-8")).hexdigest()
    query += "&apiSig=" + rand + sig

    res = requests.get(API + "/" + query).json()
    if res["status"] != "OK":
        raise Exception(res["status"] + ": " + res["comment"])
    return res["result"]


def main():
    result_path, method_name, parameters = parse_arguments()
    data = call(method_name, parameters)
    with open(result_path, 'w') as file:
        json.dump(data, file, indent=4)


if __name__ == "__main__":
    main()
