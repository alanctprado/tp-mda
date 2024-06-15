import json
from concurrent.futures import ProcessPoolExecutor
from script import call
from tqdm import tqdm
from time import sleep
from random import random
from os.path import exists


DEFAULT_DIR = "data/contests/"


def contest_path(id: str) -> str:
    return DEFAULT_DIR + f"{id}.json"


def users_path(id: str) -> str:
    return DEFAULT_DIR + f"{id}_users.txt"


def ratings_path(id: str) -> str:
    return DEFAULT_DIR + f"{id}_ratings.json"


def standings_path(id: str) -> str:
    return DEFAULT_DIR + f"{id}_standings.json"


def status_path(id: str) -> str:
    return DEFAULT_DIR + f"{id}_status.json"


def getContests() -> list:
    contest_list = call("contest.list", {"gym": "false"})
    for contest in contest_list:
        id = contest["id"]
        if not exists(contest_path(id)):
            with open(contest_path(id), 'w') as file:
                json.dump(contest, file, indent=4)
    return [contest["id"] for contest in contest_list]


def getContestUsers(id: str) -> int:
    if exists(users_path(id)) and exists(ratings_path(id)):
        return 1

    try:
        contest_ratings = call("contest.ratingChanges", {"contestId": id})
    except Exception as e:
        if str(e) == "FAILED: Call limit exceeded":
            sleep(5 * random())
            return getContestUsers(id)
        return 0

    with open(ratings_path(id), 'w') as file:
        json.dump(contest_ratings, file, indent=4)

    f = open(users_path(id), "w")
    for user_rating in contest_ratings:
        f.write(user_rating["handle"] + "\n")
    f.close()

    return 1


def getContestStandings(id: str) -> int:
    if exists(standings_path(id)):
        return 1

    try:
        contest_standings = call("contest.standings", {"contestId": id})
    except Exception as e:
        if str(e) == "FAILED: Call limit exceeded":
            sleep(5 * random())
            return getContestStandings(id)
        return 0

    with open(standings_path(id), 'w') as file:
        json.dump(contest_standings, file, indent=4)
    return 1


def getContestStatus(id: str) -> int:
    if exists(status_path(id)):
        return 1

    try:
        contest_status = call("contest.status", {"contestId": id})
    except Exception as e:
        if str(e) == "FAILED: Call limit exceeded":
            sleep(5 * random())
            return getContestStatus(id)
        return 0

    with open(status_path(id), 'w') as file:
        json.dump(contest_status, file, indent=4)
    return 1


def main():
    max_workers = 4
    ids = getContests()
    with ProcessPoolExecutor(max_workers=max_workers) as executor:
        result = list(tqdm(executor.map(getContestUsers, ids), total=len(ids)))
    print(f"Downloaded users and ratings for {sum(result)} / {len(result)} contests")
    with ProcessPoolExecutor(max_workers=max_workers) as executor:
        result = list(tqdm(executor.map(getContestStandings, ids), total=len(ids)))
    print(f"Downloaded standings for {sum(result)} / {len(result)} contests")
    with ProcessPoolExecutor(max_workers=max_workers) as executor:
        result = list(tqdm(executor.map(getContestStatus, ids), total=len(ids)))
    print(f"Downloaded status for {sum(result)} / {len(result)} contests")


if __name__ == "__main__":
    main()
