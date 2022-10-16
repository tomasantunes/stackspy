import requests
import json
import os
import time
from datetime import datetime, timedelta

KEY = ""
USER_ID = ""
MAX_RETRIES = 20
BASEURL = "https://api.stackexchange.com/2.3"

s = requests.Session()
adapter = requests.adapters.HTTPAdapter(max_retries=MAX_RETRIES)
s.mount('https://', adapter)
s.mount('http://', adapter)

print("Starting.")

last_question = ""
last_answer = ""
last_post = ""

params = {
    "key" : KEY,
    "pagesize": 1,
    "sort": "creation",
    "site": "stackoverflow.com"
}

while(True):
    r = s.get(BASEURL + "/users/" + USER_ID + "/questions", params=params)
    question = json.loads(r.text)["items"][0]
    question_id = question["question_id"]
    url = "https://stackoverflow.com/q/" + str(question_id)
    if url != last_question:
        dt = datetime.now()
        print("["+str(dt)+"] Last question from this user is: " + url)
        last_question = url

    r = s.get(BASEURL + "/users/" + USER_ID + "/answers", params=params)
    answer = json.loads(r.text)["items"][0]
    question_id = answer["question_id"]
    url = "https://stackoverflow.com/q/" + str(question_id)
    if url != last_answer:
        dt = datetime.now()
        print("["+str(dt)+"] Last answer from this user is: " + url)
        last_answer = url

    r = s.get(BASEURL + "/users/" + USER_ID + "/comments", params=params)
    comment = json.loads(r.text)["items"][0]
    post_id = answer["post_id"]
    url = "https://stackoverflow.com/q/" + str(post_id)
    if url != last_post:
        print("["+str(dt)+"] Last comment from this user is: " + url)
        last_post = url
    time.sleep(300)
