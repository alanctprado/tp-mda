import json
from os import environ, makedirs
from os.path import exists
from api import call
import sys


USERS_DIR = environ["MDADATADIR"] + "/users/"


def split_json_file(data: dict) -> None:
    """
    Splits a dictionary containing several users into one JSON file for each
    user.
    """
    for obj in data:
        if 'handle' not in obj:
            raise ValueError("One of the objects does not contain a 'handle' field")
        output_file = USERS_DIR + f"{obj['handle']}.json"
        with open(output_file, 'w') as file:
            json.dump(obj, file, indent=4)


def main():
    if len(sys.argv) <= 1:
        raise RuntimeError("Wrong usage! User list should be passed as a parameter")
    users = sys.argv[1]
    data = call("user.info", {"handles": users})
    if not exists(USERS_DIR):
        makedirs(USERS_DIR)
    split_json_file(data)


if __name__ == "__main__":
    main()
