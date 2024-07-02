import json
from os import environ, makedirs
from os.path import exists
from api import call
import sys


DEFAULT_DIR = environ["MDABASEDIR"] + "data/submissions/"


def split_json_file(data: list, handle: str) -> None:
    useful_keys = ["id", "programmingLanguage", "verdict"]
    useless_keys = ["problemsetName", "name", "type"]
    final_data = []
    for obj in data:
        problem = obj["problem"]
        for key in useless_keys:
            if key in problem:
                problem.pop(key)
        for key in useful_keys:
            if key in obj:
                problem[key] = obj[key]
        final_data.append(problem)
    output_file = DEFAULT_DIR + f"{handle}.json"
    with open(output_file, 'w') as file:
        json.dump(final_data, file, indent=4)


def main():
    if len(sys.argv) <= 1:
        raise RuntimeError("Wrong usage! User handle should be passed as a parameter")
    user = sys.argv[1]
    data = call("user.status", {"handle": user})
    if not exists(DEFAULT_DIR):
        makedirs(DEFAULT_DIR)
    split_json_file(data, user)


if __name__ == "__main__":
    main()
