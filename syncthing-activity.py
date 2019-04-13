#!/usr/bin/env python3

import requests
import time
import json
import sys
import os

__author__    = "Jan-Piet Mens <jp@mens.de>"
__copyright__ = "Copyright 2019 Jan-Piet Mens"
__license__   = "GNU General Public License"


global last_id
last_id = 0

folders = {}

def getfolders(data):

    global folders

    for f in data['folders']:
        folders[f["id"]] = f["label"]

def process(array):
    global last_id


    for event in array:
        if "type" in event and event["type"] == "ItemStarted":
            last_id = event["id"]

            folder_id = event["data"]["folder"]
            folder_label = folders[folder_id]

            e = {
                "time"          : event["time"],
                "action"        : event["data"]["action"],
                "type"          : event["data"]["type"],
                "item"          : event["data"]["item"],
                "folder_label"  : folder_label,
                "folder_id"     : folder_id,
            }

            # print(json.dumps(e, indent=4))
            print("{folder_label:>15} {type:<5s} {action:<10s} {item}".format(**e))

def main(apikey):
    headers = { "X-API-Key" : apikey }

    r = requests.get("http://localhost:8384/rest/system/config", headers=headers)
    getfolders(json.loads(r.text))

    while True:

        params = {
            "since" : last_id,
            "limit" : "10",
            "events" : "ItemStarted",
        }

        r = requests.get("http://localhost:8384/rest/events", headers=headers, params=params)
        if r.status_code == 200:
            process(json.loads(r.text))
        elif r.status_code != 304:
            time.sleep(60)
            continue
        time.sleep(10.0)

if __name__ == "__main__":

    apikey = os.getenv("SYNCTHING_APIKEY")
    if apikey is None:
        print("Missing SYNCTHING_APIKEY in environment", file=sys.stderr)
        exit(2)

    main(apikey)
