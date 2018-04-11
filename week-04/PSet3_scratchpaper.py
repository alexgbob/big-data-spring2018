#Import my libraries for setting up the Scraper
import jsonpickle
import tweepy
import pandas as pd

#Set up my twitter keys
import os
from twitter_keys import api_key, api_secret

#Set up my function for twitter authentication
def auth(key, secret):
  auth = tweepy.AppAuthHandler(key, secret) #shouldn't these terms by the names set up in my twitter_keys doc? api_key and api_secret?
  api = tweepy.API(auth, wait_on_rate_limit = True, wait_on_rate_limit_notify = True)
  # Print error and exit if there is an authentication error
  if (not api):
      print ("Can't Authenticate")
      sys.exit(-1)
  else:
      return api

api = auth(api_key, api_secret)

# Set up my Scraper
def get_tweets(
    geo, ## allows to specify location, based on lat, long and search radius, pass to function using geo attribut
    out_file, ## output file, ie the json we're writing to
    search_term = '', ## search term, look for a specific word, particular term/phrase
    tweet_per_query = 100, ## 100 results per page return.
    tweet_max = 150,
    since_id = None,
    max_id = -1, ## means that
    write = False
  ):
  tweet_count = 0 ## how we're going to count up the total number of tweets we've accumulated
  all_tweets = pd.DataFrame()
  while tweet_count < tweet_max: ##while tweet count is 0, like it is now, this condition is true so it performs this operation, not the 'else' branch below
    try:
      if (max_id <= 0):
        if (not since_id):
          new_tweets = api.search(
            q = search_term, ## if above terms are true, run a search on the AP, with a rpp of tweets per query with a geographical location specified above
            rpp = tweet_per_query,
            geocode = geo
          ) ### basically, are there new tweets? if there are, do the next thing, if not, stop the function
        else:
          new_tweets = api.search(
            q = search_term,
            rpp = tweet_per_query,
            geocode = geo,
            since_id = since_id
          )
      else:  ### when max id is not <= to zero,
        if (not since_id):
          new_tweets = api.search(
            q = search_term,
            rpp = tweet_per_query,
            geocode = geo,
            max_id = str(max_id - 1)
          )
        else:
          new_tweets = api.search(
            q = search_term,
            rpp = tweet_per_query,
            geocode = geo,
            max_id = str(max_id - 1),
            since_id = since_id
          )
      if (not new_tweets):
        print("No more tweets found")
        break
      for tweet in new_tweets: ## if there are new tweets, write those new tweets to a json file
        all_tweets = all_tweets.append(parse_tweet(tweet), ignore_index = True)
        if write == True:
            with open(out_file, 'w') as f: ## while the given file is open, writable, pass it to the file (giving the file an alias)
                f.write(jsonpickle.encode(tweet._json, unpicklable=False) + '\n') ## parsing json and writing it to a json, \n indicates output subdirectory
      max_id = new_tweets[-1].id  ## identify new max id, max id was a unique identifier for the last tweet pulled, this negative indexes on the array and passes to the function to start us off,
      tweet_count += len(new_tweets) ## syntactically equivalent to tweet_count = tweet_count + len(new_tweets), these two lines indicate that the values for max id and tweet count have changed, max id is the id of the last tweet we've gathered and tweet count reverts to create a loop
    except tweepy.TweepError as e:
      # Just exit if any error
      print("Error : " + str(e))
      break
  print (f"Downloaded {tweet_count} tweets.")
  return all_tweets

# Set a Lat Lon
latlng = '42.359416,-71.093993' # Eric's office (ish)
# Set a search distance
radius = '5mi'
# See tweepy API reference for format specifications
geocode_query = latlng + ',' + radius
# set output file location
file_name = 'data/pset3_test2.json'
# set threshold number of Tweets. Note that it's possible
# to get more than one
t_max = 80000

get_tweets(
  geo = geocode_query,
  tweet_max = t_max,
  write = True,
  out_file = file_name
  )



def parse_tweet(tweet):
    p = pd.Series()
    if tweet.coordinates != None:
      p['lat'] = tweet.coordinates['coordinates'][0]
      p['lon'] = tweet.coordinates['coordinates'][1]
    else:
      p['lat'] = None
      p['lon'] = None
    p['location'] = tweet.user.location
    p['id'] = tweet.id_str
    p['content'] = tweet.text
    p['user'] = tweet.user.screen_name
    p['user_id'] = tweet.user.id_str
    p['time'] = str(tweet.created_at)
    return p