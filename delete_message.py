import time
import requests


def delete_direct_messages(auth, author_id, server_id, del_pinned):
    """
    :param auth: is a long string about 88 characters which can be found by inspecting network to discord
            In the `Request Headers` -> `authorization`.

    :param author_id:
    :param server_id:
            author_id and server_id can be easily copied if you enable the developer mode on discord.
            To do that, go to `Settings` -> `Appearance` -> `Advanced` -> Enable `Developer Mode`.
            You should now be able to right click on server and user icons and select `Copy ID`.

    :param del_pinned: Set it to True if you wish to delete the pinned messages as well.
    """
    delete_messages(auth, author_id, server_id, True, del_pinned)


def delete_messages(auth, author_id, server_id, dm=False, del_pinned=False):
    """
    :param auth: is a long string about 88 characters which can be found by inspecting network to discord
            In the `Request Headers` -> `authorization`.

    :param author_id:
    :param server_id:
            author_id and server_id can be easily copied if you enable the developer mode on discord.
            To do that, go to `Settings` -> `Appearance` -> `Advanced` -> Enable `Developer Mode`.
            You should now be able to right click on server and user icons and select `Copy ID`.

    :param dm: Set it to True if the target server is a direct message channel.
    :param del_pinned: Set it to True if you wish to delete the pinned messages as well.
    """
    s = requests.Session()
    s.headers = {'authorization': auth}
    offset = 0
    current_timestamp = ""
    while True:
        # the url for deleting direct message and channel message is different
        if dm:
            url = "https://discordapp.com/api/v6/channels/%s/messages/search?author_id=%s&attempts=1&offset=%s"
        else:
            url = "https://discordapp.com/api/v6/guilds/%s/messages/search?author_id=%s&include_nsfw=true&offset=%s"

        full_url = url % (server_id, author_id, str(offset))
        print(full_url)
        p = s.get(full_url)

        if p.status_code is not 200:
            print("Delete Messages: error %d has occurred during get." % p.status_code)
            print(p.content)
            return

        # no more messages to delete
        if len(p.json()["messages"]) is 0:
            print("No messages to delete!")
            break

        acceptable_codes = [200, 204, 404]
        for messages in p.json()["messages"]:
            for message in messages:
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

                if pinned and del_pinned:
                    print("Deleted pinned message: " + message)
                    offset += 1
                    continue

                if message["author"]["id"] == author_id:
                    d = s.delete("https://discordapp.com/api/v6/channels/%s/messages/%s"
                                 % (message["channel_id"], message["id"]))
                    if d.status_code in acceptable_codes:
                        print("Deleted message: %s" % message)
                    else:
                        print("Delete Messages: error %d has occurred during delete." % d.status_code)
                        print(d.content)
                        return

                    time.sleep(0.1)


if __name__ == "__main__":
    # Using a separate file to hold the configurable fields.
    from config import *
    delete_messages(AUTHORIZATION, TARGET_AUTHOR_ID, TARGET_SERVER_ID, IS_DIRECT_MESSAGE, TO_DELETE_PINNED)
