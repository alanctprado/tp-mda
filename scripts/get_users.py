import json
from os import makedirs
from os.path import exists
from api import call
import sys


DEFAULT_DIR = "data/users/"


def split_json_file(data: dict) -> None:
    for obj in data:
        if 'handle' not in obj:
            raise ValueError("One of the objects does not contain a 'handle' field")
        output_file = DEFAULT_DIR + f"{obj['handle']}.json"
        with open(output_file, 'w') as file:
            json.dump(obj, file, indent=4)


def main():
    if len(sys.argv) <= 1:
        raise RuntimeError("Wrong usage! User list should be passed as a parameter")
    users = sys.argv[1]
    data = call("user.info", {"handles": users})
    if not exists(DEFAULT_DIR):
        makedirs(DEFAULT_DIR)
    split_json_file(data)


if __name__ == "__main__":
    main()
