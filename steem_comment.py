from steem import Steem
import json
import datetime
import os
from dateutil import parser
import time
from random import randrange
# create Steem instance
s = Steem(keys=['5KYbuefVtjm8dvt37JLCo3fEp8Y7unnQacJ6KrdcWof3wYaDNE5','5JhPVV7bfYhBYj5r35ic5EaawMNjAYHfEH9i3mBGfuUXRcCezfj'])
accountHandle = "ksvvb"
messages_list = ['I really love your blog :)','Nice post, beautifully presented!!', "Loved it, !!", "keep up the good work!","thank you for sharing this with us"," Detail oriented with nice pics."]

latestPostId = s.get_feed(accountHandle, -1, 1)[0]['entry_id']

runMe = True


def upvoteAndResteem(postAuthor, link, postVotes,accountHandle,post_id):
    # upvote post
    s.vote("@" + postAuthor + "/" + link, 100.0,accountHandle)
    # resteem post
    #s.resteem("@" + postAuthor + "/" + link,accountHandle)
   # reply in comment
    message_index = randrange(0, len(messages_list))
    s.post("hey", str(messages_list[message_index])+", Upvoted :)\n\n Please follow me @"+accountHandle,accountHandle, reply_identifier="@" + postAuthor + "/" + link)
    
    # print out data
    message = "[+] Upvoted post: @" + postAuthor + "/" + link + " as voter #" + str(postVotes) + " at time: " + str(
        datetime.datetime.now()) + "\n"
    print(message)
    #open and write message to log file
    f = open("log.txt", "a")
    f.write(message)
    f.close()


# get current latest post id on feed
while runMe == True:

    # gets latest post on your feed
    feed = s.get_feed(accountHandle, -1, 1)
    latestPost = feed[0]['entry_id']
    #print(feed[0])
    if latestPost > latestPostId:
        # Get the author of the posts
        author = feed[0]['comment']['author']
        # Get the link to the post
        postLink = feed[0]['comment']['permlink']

        # Get the amount of upvotes on the post
        votes = feed[0]['comment']['net_votes']

        post_id = feed[0]['comment']['id']
        # We wan't to be in the top 10 first votes
        if votes < 11:
            upvoteAndResteem(author, postLink, votes,accountHandle,post_id)
            # Update the latest post value in log
            latestPostId = latestPost
        else:
            # If we're not in the first 10 votes we won't upvote and resteem
            print("votes too high")
            # Update latest post value in log
            latestPostId = latestPost


    else:
        print("[-] No new posts at time: " + str(datetime.datetime.now()))
        
    print('[-] Sleeping for 120 seconds')
    # sleep for for 120 seconds before cheecking for new posts
    time.sleep(120)
    print("[-] Done sleeping")
