import time

import requests

# Using a separate file to hold the configurable fields.
from config import *

s = requests.Session()
s.headers = {'authorization': AUTHORIZATION}
offset = 0
current_timestamp = ""
while True:
    # the url for deleting direct message and channel message is different
    if IS_DIRECT_MESSAGE:
        url = "https://discordapp.com/api/v6/channels/%s/messages/search?author_id=%s&attempts=1&offset=%s"
    else:
        url = "https://discordapp.com/api/v6/guilds/%s/messages/search?author_id=%s&include_nsfw=true&offset=%s"

    full_url = url % (TARGET_SERVER_ID, TARGET_AUTHOR_ID, str(offset))
    print(full_url)
    p = s.get(full_url)

    if p.status_code is not 200:
        print("Error %d has occurred during get." % p.status_code)
        print(p.content)
        exit(0)

    # no more messages to delete
    if len(p.json()["messages"]) is 0:
        print("No messages to delete!")
        break

    acceptable_codes = [200, 204, 404]
    for messages in p.json()["messages"]:
        for message in messages:
            message_id = message["id"]
            message_timestamp = message["timestamp"]
            current_timestamp = message_timestamp if current_timestamp == "" else current_timestamp
            pinned = message["pinned"]

            # Ignore all the messages not authored by the target author
            if "hit" not in message or not message["hit"]:
                continue

            # This helps to keep your conversation going while the script deletes old messages
            if message_timestamp > current_timestamp:
                offset += 1
                continue

            if pinned and TO_DELETE_PINNED:
                print(message)
                print("PINNED!")
                offset += 1
                continue

            if message["author"]["id"] == TARGET_AUTHOR_ID:
                d = s.delete("https://discordapp.com/api/v6/channels/%s/messages/%s"
                             % (message["channel_id"], message["id"]))
                if d.status_code in acceptable_codes:
                    print("Deleted message: %s" % message)
                else:
                    print("Error %d has occurred during delete." % d.status_code)
                    print(d.content)
                    exit(0)

                time.sleep(0.1)
