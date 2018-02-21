import pandas as pd
import numpy as np

new_list = []
df = pd.DataFrame()
print(df)

df['name'] = ['Bilbo', 'Frodo', 'Samwise']

df

df.assign(height = [0.5, 0.4, 0.6])

import os
os.chdir('week-03')
df = pd.read_csv('data/skyhook_2017-07.csv', sep = ',')

df.head()

df.shape[] # returns tuple of shape of DataFrame

df.columns

df['cat_name'].unique()

df['hour'] == 158 # creates mask where the truth of  the statement is tested for each row
one_fifty_eight = df[df['hour'] == 158] # pass a mask to the DataFrame to only get entries where the hour is 158

one_fifty_eight.shape

df[(df['hour'] == 158) & (df['count'] > 50)].shape #subsetting rows and columns -- this also won't overwrite the DataFrame

bastille = df[df['date'] == '2017-07-14']
bastille.head()

#greater than average cells
bastille['count'] > bastille['count'].mean() #mask for where the count is greater than the mean count

lovers_of_bastille = bastille[bastille['count'] > bastille['count'].mean()]

lovers_of_bastille['count'].describe()

#groupby statistics and plot

import matplotlib
%matplotlib inline


df.groupby('date')['count'].sum() # looks for all unique dates, aggregates them and then sums the counts for each day

df.groupby('date')['count'].sum().plot() # generate plot of groupby data

df.groupby('date')['count'].describe()

df['count'].max()
df['count'].min()
df['count'].mean()
df['count'].std()
df['count'].count()

df[df['count'] == df['count'].max()] #find the entry where the count is the maximum


df['hour'].unique()
Jul_02 = df[df['date'] == '2017-07-02']

Jul_02.groupby('hour')['count'].sum()

Jul_02.groupby('hour')['count'].sum().plot()

#use datetime function to specify to pandas that the data field is a date
df['date_new'] = pd.to_datetime(df['date'], format = '%Y-%m-%d')

#add weekday field that correspnds to the actual weekday
df['weekday'] = df['date_new'].apply(lambda x: x.weekday() + 1)
df['weekday'].replace(7, 0, inplace = True)

# extract and drop GPS pings that are outside the date that the entry was recorded on

for i in range(0, 168, 24):
    j = range()
    df.drop(df[df['weekday'] == (i/24) &
    (
    (df['hour']) < i | df['hour'] > j + 18)
    )
    ])
