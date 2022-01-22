#!/usr/bin/env python3

import requests


API_BASE = "https://bad-api-assignment.reaktor.com/rps"

def fetch_one(key: str):
    if key:
        url = API_BASE + "/history?cursor=" + key
    else:
        url = API_BASE + "/history"
    
    res = requests.get(url)
    if 'cursor' in (json := res.json()):
        print(f"next: {json['cursor']}")
        print(f"        {res.text[:100]}")
        if json['cursor']:
            return json['cursor'].split("=")[1]

if __name__ == "__main__":
    cursor = fetch_one("")
    while cursor:
        cursor = fetch_one(cursor)

    print(cursor)