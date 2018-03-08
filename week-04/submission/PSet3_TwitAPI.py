##Scraper
import jsonpickle
import tweepy
import pandas as pd

import os
os.chdir('week-04')
from twitter_keys import api_key, api_secret

def auth(key, secret):
  auth = tweepy.AppAuthHandler(api_key, api_secret)
  api = tweepy.API(auth, wait_on_rate_limit = True, wait_on_rate_limit_notify = True)
  # Print error and exit if there is an authentication error
  if (not api):
      print ("Can't Authenticate")
      sys.exit(-1)
  else:
      return api

api = auth(api_key, api_secret)



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

def get_tweets(
    geo,
    out_file,
    search_term = '',
    tweet_per_query = 100,
    tweet_max = 150,
    since_id = None,
    max_id = -1,
    write = False
  ):
  tweet_count = 0
  all_tweets = pd.DataFrame()
  while tweet_count < tweet_max:
    try:
      if (max_id <= 0):
        if (not since_id):
          new_tweets = api.search(
            q = search_term,
            rpp = tweet_per_query,
            geocode = geo
          )
        else:
          new_tweets = api.search(
            q = search_term,
            rpp = tweet_per_query,
            geocode = geo,
            since_id = since_id
          )
      else:
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
      for tweet in new_tweets:
        all_tweets = all_tweets.append(parse_tweet(tweet), ignore_index = True)
        max_id = new_tweets[-1].id
        tweet_count += len(new_tweets)
    except tweepy.TweepError as e:
      # Just exit if any error
        print("Error : " + str(e))
        break
        print (f"Downloaded {tweet_count} tweets.")
  if write == True:
      all_tweets.to_json(out_file)
      return all_tweets

##Step 1

latlng = '42.359416,-71.093993'
radius = '5mi'
geocode_query = latlng + ',' + radius
file_name = 'data/tweets_2.json'
t_max = 30000

tweets2 = get_tweets(
  geo = geocode_query,
  tweet_max = t_max,
  write = True,
  max_id = 0,
  out_file = file_name
)
len(tweets2)

## Step 2

import numpy as np
import matplotlib.pyplot as plt
%matplotlib inline

bos_list = tweets2[tweets2['location'].str.contains("Boston")]['location']
bos2_list = tweets2[tweets2['location'].str.contains("boston")]['location']
bos3_list = tweets2[tweets2['location'].str.contains("BOSTON")]['location']
camb_list = tweets2[tweets2['location'].str.contains("Cambridge")]['location']
camb2_list = tweets2[tweets2['location'].str.contains("cambridge")]['location']
Som_list = tweets2[tweets2['location'].str.contains("Somerville")]['location']
Brook_list = tweets2[tweets2['location'].str.contains("Brookline")]['location']
Dot_list = tweets2[tweets2['location'].str.contains("Dorchester")]['location']
Ca_list = tweets2[tweets2['location'].str.contains("California")]['location']
Ca2_list = tweets2[tweets2['location'].str.contains("CA")]['location']
MA_list = tweets2[tweets2['location'].str.contains("Massachusetts")]['location']
US_list = tweets2[tweets2['location'].str.contains("United States")]['location']
jp_list = tweets2[tweets2['location'].str.contains("Jamaica Plain")]['location']
jp2_list = tweets2[tweets2['location'].str.contains("JP")]['location']


tweets2['location'].replace(bos_list, 'Boston, MA', inplace = True)
tweets2['location'].replace(bos2_list, 'Boston, MA', inplace = True)
tweets2['location'].replace(bos3_list, 'Boston, MA', inplace = True)
tweets2['location'].replace(camb_list, 'Cambridge, MA', inplace = True)
tweets2['location'].replace(camb2_list, 'Cambridge, MA', inplace = True)
tweets2['location'].replace(Som_list, 'Somerville, MA', inplace = True)
tweets2['location'].replace(Brook_list, 'Brookline, MA', inplace = True)
tweets2['location'].replace(Dot_list, 'Dorchester, MA', inplace = True)
tweets2['location'].replace(Ca_list, 'California', inplace = True)
tweets2['location'].replace(Ca2_list, 'California', inplace = True)
tweets2['location'].replace(MA_list, 'Massachusetts', inplace = True)
tweets2['location'].replace(US_list, 'United States', inplace = True)
tweets2['location'].replace(jp_list, 'Jamaica Plain', inplace = True)

loc_tweets = tweets2[tweets2['location'] != '']
count_tweets = loc_tweets.groupby('location')['id'].count()
df_count_tweets = count_tweets.to_frame()
df_count_tweets.columns = ['count']
df_count_tweets
Maj_locs_counts = df_count_tweets[df_count_tweets['count'] > 6]

colors = ["#697dc6","#5faf4c","#7969de","#b5b246",
          "#cc54bc","#4bad89","#d84577","#4eacd7",
          "#cf4e33","#894ea8","#cf8c42","#d58cc9",
          "#737632","#9f4b75","#c36960"]

plt.pie(Maj_locs_counts['count'], labels=Maj_locs_counts.index.get_values(), shadow=False, colors=colors)
plt.axis('equal')
plt.title('Counts of User Provided Locations (locations provided by 6 or less users excluded)')
plt.tight_layout()
plt.show()

##Step 3

Geo_tweets = tweets2.dropna(subset=['lat','lon'])
len(Geo_tweets)
len(tweets2)

plt.scatter(Geo_tweets['lon'], Geo_tweets['lat'], s = 25)
plt.title("Longitude, Latitude Coordinates for Tweeters")
plt.xlabel("longitude")
plt.ylabel("latitude")
plt.show()

##Step 4

latlng = '42.359416,-71.093993'
radius = '5mi'
geocode_query = latlng + ',' + radius
search = 'housing'
file_name = 'data/tweets_2.json'
t_max = 20000

hous_tweets = get_tweets(
  geo = geocode_query,
  tweet_max = t_max,
  write = True,
  max_id = 0,
  out_file = file_name,
  search_term = search
)

len(hous_tweets)

##Step 5

bos_list = hous_tweets[hous_tweets['location'].str.contains("Boston|boston|BOSTON")]['location']
camb_list = hous_tweets[hous_tweets['location'].str.contains("Cambridge|cambridge|CAMBRIDGE")]['location']
som_list = hous_tweets[hous_tweets['location'].str.contains("Somerville|somerville|SOMERVILLE")]['location']
dot_list = hous_tweets[hous_tweets['location'].str.contains("Dorchester|dorchester|DORCHESTER")]['location']
mass_list = hous_tweets[hous_tweets['location'].str.contains("Massachusetts|massachusetts|MASSACHUSETTS")]['location']
ny_list = hous_tweets[hous_tweets['location'].str.contains("New York|new york|NY")]['location']

hous_tweets['location'].replace(bos_list, 'Boston, MA', inplace = True)
hous_tweets['location'].replace(camb_list, 'Cambridge, MA', inplace = True)
hous_tweets['location'].replace(som_list, 'Somerville, MA', inplace = True)
hous_tweets['location'].replace(dot_list, 'Dorchester, MA', inplace = True)
hous_tweets['location'].replace(mass_list, 'Massachusetts', inplace = True)
hous_tweets['location'].replace(ny_list, 'New York', inplace = True)

loc_h_tweets = hous_tweets[hous_tweets['location'] != '']
count_h_tweets = loc_h_tweets.groupby('location')['id'].count()
df_count_h_tweets = count_h_tweets.to_frame()
df_count_h_tweets.columns = ['count']
Maj_locs_h_counts = df_count_h_tweets[df_count_h_tweets['count'] > 7]

colors = ["#697dc6","#5faf4c","#7969de","#b5b246",
          "#cc54bc","#4bad89","#d84577","#4eacd7",
          "#cf4e33","#894ea8","#cf8c42","#d58cc9",
          "#737632","#9f4b75","#c36960"]

plt.pie(Maj_locs_h_counts['count'], labels=Maj_locs_h_counts.index.get_values(), shadow=False, colors=colors)
plt.axis('equal')
plt.title('Counts of Tweeters\' User Provided Locations (locations provided by 7 or less users excluded)')
#plt.tight_layout()
plt.show()

##Step 6

Geo_h_tweets = hous_tweets.dropna(subset=['lat','lon'])
len(Geo_h_tweets)

plt.scatter(Geo_h_tweets['lon'], Geo_h_tweets['lat'], s = 25)
plt.title("Longitude, Latitude Coordinates for housing Tweeters")
plt.xlabel("longitude")
plt.ylabel("latitude")
plt.show()

##Step 7

tweets2.to_csv("scraped_tweets.csv", encoding = 'utf-8')
hous_tweets.to_csv("scraped_tweets_srchd.csv", encoding = 'utf-8')
