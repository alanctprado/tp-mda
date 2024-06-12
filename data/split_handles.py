import json


def split_json_file(input_file):
    with open(input_file, 'r') as file:
        data = json.load(file)

    for obj in data:
        if 'handle' not in obj:
            raise ValueError("One of the objects does not contain a 'handle' field")

        handle = obj['handle']
        output_file = f"users/{handle}.json"

        with open(output_file, 'w') as file:
            json.dump(obj, file, indent=4)


def main():
    input_file = 'active_users.json'
    split_json_file(input_file)


if __name__ == "__main__":
    main()
