#from https://dev.mention.com/current/src/guides/twitter.html 
import os

from rauth import OAuth1Service

# API keys
# from dotenv import load_dotenv
# load_dotenv()
# consumer_key = os.getenv('CONSUMER_KEY')
# consumer_secret = os.getenv('CONSUMER_SECRET')
# access_token = os.getenv('ACCESS_TOKEN')
# access_token_secret = os.getenv('ACCESS_TOKEN_SECRET')

import sys
sys.path.insert(0, os.path.abspath('/Volumes/GoogleDrive-108526182429603786708/My Drive/keys'))
import keys
from keys import *

# Instantiate a client
# MUST INPUT YOUR OWN CONSUMER KEY AND ACCESS TOKEN INFO in keys.py
twitter_client = OAuth1Service(name='twitter',
                              consumer_key=keys.consumer_key,
                              consumer_secret=keys.consumer_secret,
                              base_url='https://api.twitter.com/1.1/')

twitter_session = twitter_client.get_session((keys.access_token, keys.access_token_secret))

# Rounding/simplifying numbers - will fix so as to not hard-code numbers
def simp(number):
    if number >= 1000000000:
        new_number = str(round(number / 10000000000, 1)) + "B"

    elif number >= 10000000: 
        new_number = str(round(number / 10000000, 1)) + "M"

    elif number >= 10000:
        new_number = str(round(number / 1000, 1)) + "K"

    else:
        new_number = number

    return new_number

# Request the metadata of a tweet
def get_metadata(link):
    
    #tweet URL (api) and id
    id = link.split('/')[-1]

    ID = [id]
    URL = 'https://api.twitter.com/1.1/statuses/lookup.json'
    
    #get request
    r = twitter_session.get(URL,
                            params={'id': ','.join(ID)})

    #retrieve metadata in JSON format
    h = r.json()
    #JSON dictionary of initial tweet
    dict = h[0]

    #data we want: Tweet URL, Retweets, Likes, Author handle, Author profile URL, Author bio, Followers
    #generate url for twitframe
    twitframe_url = "https://twitframe.com/show?url=" + link #urllib.parse.quote(meta_url, safe="")
    #retweets
    retweets = dict["retweet_count"]
    #likes
    likes = dict["favorite_count"]
    #author info
    author_dict = dict["user"]
    name = author_dict["name"]
    handle = author_dict["screen_name"]
    bio = author_dict["description"]
    #followers - write rounding formula with mod later (for K or M, or B?)
    followers = author_dict["followers_count"]

    #store in dictionary
    metadata = {
            "url": link, 
            "twitframe_url": twitframe_url,
            "retweets": simp(retweets), 
            "likes": simp(likes), 
            "author_name": name, 
            "handle": handle, 
            "bio": bio, 
            "followers": simp(followers)
        }

    print(metadata)
    
    return metadata
    
# switch to class/object-oriented, rather than dataframe?