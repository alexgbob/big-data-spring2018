## Set up performance data query
import jsonpickle
import pandas as pd
import requests
import csv
import json
import bs4
# Set up api for MBTA
MBTA_api = "wX9NwuHnZU2ToO7GmGR9uw"

# make sure I'm in the current directory
import os
os.chdir('/Users/abob/Desktop/github/big-data-spring2018/transit_delays/gtfs_scrape')


#read in origin_dest2 csv with cbd lines removed
origin_dest2 = pd.read_csv('origin_dest2.csv', sep=',')

#check it out
origin_dest2.head()



#check out my origin_dest2 df_columns
origin_dest2.columns

# set up a data frame to store api request addresses, created from the stops in the origin_dest2 file
#http://realtime.mbta.com/developer/api/v2.1/traveltimes?api_key=wX9NwuHnZU2ToO7GmGR9uw&format=json&from_stop=11384&to_stop=70061&from_datetime=1514419200&to_datetime=1514505600
# create a DataFrame
# pass the origin/ destination to the dataframe as unique rows
# with the url corresponding to that destination
# add another column(s) and iterate through the urls to query the data and put it in the
# columns according to the origin/ destination

#create the URL calling from the origin_dest2 df
def url_string(x,y):
    url = 'http://realtime.mbta.com/developer/api/v2.1/traveltimes?api_key=wX9NwuHnZU2ToO7GmGR9uw&format=json&from_stop={}&to_stop={}&from_datetime=1514419200&to_datetime=1514505600'.format(x,y)
    return url
#create input for url_string
# origin = [origin_dest2.origin_id]
# dest = [origin_dest2.dest_id]
# print(url_string(origin,dest))


## for loop for scraping all data from mbta gtfs performance api
from pandas.io.json import json_normalize

all_perf_df = pd.DataFrame()
for index, row in origin_dest2.iterrows():
    api_string = url_string(row["origin_id"], row["dest_id"])
    #or_d = pd.DataFrame(data = [,row["origin_id"], row["origin_name"], row["dest_id"], row["dest_name"]], columns = ['origin_id', 'origin_name', 'dest_id', 'dest_name'])
    resp = requests.get(api_string).json()
    pars_resp2 = json.dumps(resp)
    resp_pars = json.loads(pars_resp2)
    perf_df = json_normalize(resp_pars['travel_times'])
    perf_df = perf_df.assign(origin_id = row["origin_id"], origin_name = row["origin_name"], dest_id = row["dest_id"], dest_name = row["dest_name"])
    all_perf_df = all_perf_df.append(perf_df)

all_perf_df.to_csv('mbta_perf_v1.csv', encoding='utf-8')
