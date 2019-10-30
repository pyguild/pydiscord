# Common properties
"""
AUTHORIZATION is a long string about 88 characters which can be found by inspecting network to discord
In the `Request Headers` -> `authorization`.

AUTHOR_ID and SERVER_ID can be easily copied if you enable the developer mode on discord.
To do that, go to `Settings` -> `Appearance` -> `Advanced` -> Enable `Developer Mode`.
You should now be able to right click on server and user icons and select `Copy ID`.
"""
AUTHOR_ID = "000000000000000000"  # It should be 18 digits in total
AUTHORIZATION = ""
SERVER = "000000000000000000"  # It should be 18 digits in total


# Delete message properties
TO_DELETE_PINNED = False
IS_DIRECT_MESSAGE = False
