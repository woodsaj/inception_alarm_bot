#!/usr/bin/env python3

import requests
import datetime
import json
import sys
from time import sleep
from os import path, environ


apiKey=environ.get('INCEPTION_API_KEY')
inception_addr=environ.get('INCEPTION_ADDR')
telgram_bot_token=environ.get('TELEGRAM_BOT_TOKEN')
telegram_bot_name=environ.get('TELEGRAM_BOT_NAME')
poll_interval=int(environ.get('POLL_INTERVAL'))

state_file = "./run/state"
if not path.isfile(state_file):
    with open(state_file, "w") as f:
        json.dump({}, f, indent=4)

subscriber_file = "./run/subscribers"
if not path.isfile(subscriber_file):
    with open(subscriber_file, "w") as f:
        json.dump({}, f, indent=4)

def loadSubscribers():
    with open(subscriber_file, "r") as f:
        subscribers = json.loads(f.read())
        return subscribers

def saveSubscribers(subscribers):
    with open(subscriber_file, "w") as f:
        json.dump(subscribers, f, indent=4)

def getSubscribers():
    subscribers = loadSubscribers()
    url = f"https://api.telegram.org/bot{telgram_bot_token}/getUpdates"
    r = requests.get(url)
    if r.status_code != 200:
        print("failed to get telegram messages.", r.status_code, r.text)
        return
    
    messages = r.json()
    for m in messages['result']:
        if m['message']['text'] == "/subscribe":
            # new subscription.
            print("new subscription", m['message'])
            subscribers[m['message']['from']['username']] = m['message']['chat']['id']

    saveSubscribers(subscribers)
    return subscribers

def getLastEvent():
    with open(state_file, "r") as f:
        state = json.loads(f.read())

def run():
    query = {
        'messageTypeIdFilter': 6203,
        'dir': 'asc',
    }
    subscribers = getSubscribers()
    with open(state_file, "r") as f:
        state = json.loads(f.read())

        if 'ID' in state and 'ReferenceTime' in state:
            query['referenceId'] = state['ID']
            query['referenceTime'] = state['ReferenceTime']

    if not 'referenceId' in query:
        lastHourDateTime = datetime.datetime.now() - datetime.timedelta(hours = 720)
        query["start"] =  lastHourDateTime.isoformat()

    print("sending query: ", query)
    events = requests.get('http://'+inception_addr+'/api/v1/review', params=query, headers={'Accept':'Application/json', 'Authorization': 'ApiToken '+apiKey})

    if events.status_code == 200:
        print(events.text)
    else:
        print("failed to get events")
        print(events.text)
        return

    # check if any events returned
    e = events.json()
    count = e['Count']

    if count > 0:
        last_event = e['Data'][count - 1]
        # new event occurred. Send notifications
        for s in subscribers:
            chat_id = subscribers[s]
            message = last_event['Description'] + "  Open SkyCommand app for actions."
            url = f"https://api.telegram.org/bot{telgram_bot_token}/sendMessage?chat_id={chat_id}&text={message}"
            r = requests.get(url)
            if r.status_code != 200:
                print("failed to send message to subscriber", r.status_code, r.text)


        # persist this event to the state file so ack that we have seen it.
        with open(state_file, "w") as f:
            json.dump(last_event, f, indent=4)


while True:
    run()
    sleep(poll_interval)
