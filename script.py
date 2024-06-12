import hashlib
import json
import random
from datetime import datetime

import requests


API = "https://codeforces.com/api"
with open("credentials.json") as f:
    credentials = json.load(f)


def call(methodName: str, params: dict) -> dict:
    query = methodName

    params["apiKey"] = credentials["KEY"]
    params["time"] = int(round(datetime.now().timestamp()))

    sep = "?"
    for name, value in sorted(params.items()):
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


oi = call("blogEntry.comments", {"blogEntryId": "130381"})
print(oi)
