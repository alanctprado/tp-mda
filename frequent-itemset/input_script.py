import sys
import json


def print_accepted_submissions(path: str) -> None:
    accepted = set()
    with open(path) as f:
        data = json.load(f)
        for submission in data:
            if submission["verdict"] == "OK":
                try:
                    accepted.add(str(submission["contestId"]) + submission["index"])
                except:
                    continue
    print(','.join(accepted))



def main():
    if len(sys.argv) <= 1:
        raise RuntimeError("Wrong usage! User list should be passed as a parameter")
    submissions_path = sys.argv[1]
    print_accepted_submissions(submissions_path)


if __name__ == "__main__":
    main()
