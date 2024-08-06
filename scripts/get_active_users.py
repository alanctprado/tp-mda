import json
from os import environ, makedirs
from os.path import exists
from api import call


ACTIVE_USERS_DIR = environ["MDADATADIR"] + "/active_users/"


def split_json_file(data: dict) -> None:
    for obj in data:
        if 'handle' not in obj:
            raise ValueError("One of the objects does not contain a 'handle' field")
        output_file = ACTIVE_USERS_DIR + f"{obj['handle']}.json"
        with open(output_file, 'w') as file:
            json.dump(obj, file, indent=4)


def main():
    data = call("user.ratedList", {"activeOnly": "true", "includeRetired": "false"})
    if not exists(ACTIVE_USERS_DIR):
        makedirs(ACTIVE_USERS_DIR)
    split_json_file(data)


if __name__ == "__main__":
    main()
