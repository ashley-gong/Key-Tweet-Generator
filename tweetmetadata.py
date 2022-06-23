#from https://dev.mention.com/current/src/guides/twitter.html 
import json
from rauth import OAuth1Service

def get_keys(path):
    with open(path) as f:
        return json.load(f)

# Retrieve API keys
keys = get_keys("/Volumes/GoogleDrive-108526182429603786708/My Drive/key-tweet-gen/.secret/keys.json")
consumer_key = keys['consumer_key']
consumer_secret = keys['consumer_secret']
access_token = keys['access_token']
access_token_secret = keys['access_token_secret']


# Instantiate a client
twitter_client = OAuth1Service(name='twitter',
                              consumer_key=consumer_key,
                              consumer_secret=consumer_secret,
                              base_url='https://api.twitter.com/1.1/')

twitter_session = twitter_client.get_session((access_token, access_token_secret))

# Rounding/simplifying numbers - will fix so as to not hard-code numbers
def simplify(number):
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
    #text
    text = dict["text"]
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
            "text": text,
            "retweets": simplify(retweets),
            "likes": simplify(likes),
            "author_name": name,
            "handle": handle,
            "bio": bio,
            "followers": simplify(followers)
        }

    print(metadata)

    return metadata

