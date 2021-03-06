# Common properties
"""
AUTHORIZATION is a long string about 88 characters which can be found by inspecting network to discord
In the `Request Headers` -> `authorization`.

AUTHOR_ID and SERVER_ID can be easily copied if you enable the developer mode on discord.
To do that, go to `Settings` -> `Appearance` -> `Advanced` -> Enable `Developer Mode`.
You should now be able to right click on server and user icons and select `Copy ID`.
"""
AUTHORIZATION = ""
TARGET_AUTHOR_ID = "000000000000000000"  # It should be 18 digits in total
TARGET_SERVER_ID = "000000000000000000"  # It should be 18 digits in total


# Delete message properties
TO_DELETE_PINNED = False  # To delete pinned messages

"""
To delete direct messages, set this to true.
TARGET_SERVER_ID is then required to set to the user id of the other party. 
"""
IS_DIRECT_MESSAGE = False
