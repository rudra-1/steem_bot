from steem import Steem
import json
import datetime
import os
from dateutil import parser
import time
import requests
import random

s = Steem(keys=['5KQmqAv4xjh3NHGQqASBSyurxFYQuoRPmB2HTj8AjwZwyTtp1LU','5JZtFgeQpd6GbukkLV8oTAZ1NxYfoBARWwJTb65oC4W8owEUSZg'])
accountHandle = "sarcastic.man"


def fetch_reddit_meme():
	reddit_post = {}
	headers = {'User-agent': 'Chrome'}
	r = requests.get('https://www.reddit.com/r/memes/new.json?sort=new&limit=1',headers=headers)
	reddit_post_json = r.json()

	reddit_post['title'] = reddit_post_json['data']['children'][0]['data']['title']
	reddit_post['image'] = reddit_post_json['data']['children'][0]['data']['url']

	return reddit_post


def create_steam_post(title, image_url, accountHandle):
    # reply in comment
    content = "<img src='"+image_url+"'/>"
    tags = ['funny','meme','life','blog','joy']
    random.shuffle(tags)
    s.post(title, content,accountHandle,tags=tags)
    
fetched_post = fetch_reddit_meme()
create_post = False
if fetched_post['title'] != '' and fetched_post['image'] != '':
	try:
		#open and write message to log file
	    f = open("last_post_title.txt", "r")
	    if fetched_post['title'] != f.read():
	    	create_post = True
	    f.close()
	except Exception as e:
		print(str(datetime.datetime.now()) +str(e))
		create_post = True
		pass

	if create_post:
		create_steam_post(fetched_post['title'], fetched_post['image'], accountHandle)
		f = open("last_post_title.txt", "w")
		f.write(fetched_post['title'])
		f.close()		 
		print(str(datetime.datetime.now()) + " [+] Post created "+fetched_post['title']+"-"+fetched_post['image'])
	else:
		print(str(datetime.datetime.now()) + " [-] repeated post "+fetched_post['title'])
	