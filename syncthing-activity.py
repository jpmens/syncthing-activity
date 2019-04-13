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

def main(url, apikey):
    headers = { "X-API-Key" : apikey }

    r = requests.get("{0}/rest/system/config".format(url), headers=headers)
    getfolders(json.loads(r.text))

    while True:

        params = {
            "since" : last_id,
            "limit" : None,
            "events" : "ItemStarted",
        }

        r = requests.get("{0}/rest/events".format(url), headers=headers, params=params)
        if r.status_code == 200:
            process(json.loads(r.text))
        elif r.status_code != 304:
            time.sleep(60)
            continue
        time.sleep(10.0)

if __name__ == "__main__":

    url = os.getenv("SYNCTHING_URL", "http://localhost:8384")
    apikey = os.getenv("SYNCTHING_APIKEY")
    if apikey is None:
        print("Missing SYNCTHING_APIKEY in environment", file=sys.stderr)
        exit(2)

    try:
        main(url, apikey)
    except KeyboardInterrupt:
        exit(1)
    except:
        raise
