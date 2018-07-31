from steem import Steem
import json
import datetime
import os
from dateutil import parser
import time

try :
    # create Steem instance
    s = Steem(keys=['private-posting-key','private-active-key'])
    accountHandle = "account-handle"

    # gets latest post on your feed
    feed = s.get_feed(accountHandle, -1, 1)
    # Get the author of the posts
    author = feed[0]['comment']['author']
    # Get the link to the post
    postLink = feed[0]['comment']['permlink']

    s.vote("@" + author + "/" + postLink, 100.0,accountHandle)

    print(str(datetime.datetime.now()) + " [+] Voted @" + author + "/" + postLink)

except Exception as e:
    print(str(datetime.datetime.now()) +str(e))
