import ast                                                                      # convert string to literal
import pandas as pd
import numpy as np
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
import csv
import os
# import countries                                                              # countries.py needs to be in same dir as this script


myDir = '/home/josh/google_drive/twitter/fetched_tweets/'

ukraine = 1
border = 0

# ukraine
llcrnrlon = 22.1357201
llcrnrlat = 44.386383
urcrnrlon = 40.227172
urcrnrlat = 52.379475

# # us-mexico border
# llcrnrlat = 14
# llcrnrlon = -124
# urcrnrlat = 38
# urcrnrlon = -86


fileNames = [f for f in os.listdir(myDir) if f.endswith('.txt')]

tweets=[]
for fileName in fileNames:
    print '====='
    print fileName

    fullpath = myDir+fileName
    with open(fullpath, 'rU') as csvfile:
         f = csv.reader(csvfile, delimiter='\t', quotechar='"')
         for row in f:
             tweets.append(row)

    df = pd.DataFrame(tweets, columns=['coords',
                                         'text',
                                         'hashtags',
                                         'time',
                                         'tweet_lang',
                                         'user_lang',
                                         'tweet_id',
                                         'user_id'])

    print "the df has the shape: " + str(df.shape)


# cc = countries.CountryChecker('/home/josh/google_drive/misc/TM_WORLD_BORDERS-0.3/TM_WORLD_BORDERS-0.3.shp')
# country = []
# i=0
# for coords in df['coords']:
#     pair = ast.literal_eval(coords)
#     try:
#         label = cc.getCountry(countries.Point(pair[1], pair[0])).iso
#     except AttributeError:
#         label = "NaN"
#     country.append(label)
#     i+=1
#     print i

# df['country'] = pd.Series(country)
# print df['country'].value_counts()

# df = df[df['country']=='NaN']

print df.shape
print df['tweet_lang'].value_counts()
print df['user_lang'].value_counts()


if ukraine:
    ru = df[df['tweet_lang'] == 'ru']
    uk = df[df['tweet_lang'] == 'uk']

    rulats=[]
    rulons=[]
    for pair in ru['coords']:
        pair = ast.literal_eval(pair)
        rulats.append(pair[1])
        rulons.append(pair[0])
    print "Russian tweets = " + str(len(rulats))

    uklats=[]
    uklons=[]
    for pair in uk['coords']:
        pair = ast.literal_eval(pair)
        uklats.append(pair[1])
        uklons.append(pair[0])
    print "Ukrainian tweets = " + str(len(uklats))

elif border:
    lats=[]
    lons=[]
    for pair in df['coords']:
        pair = ast.literal_eval(pair)
        lats.append(pair[1])
        lons.append(pair[0])
    print "Border tweets = " + str(len(lats))


def plotMap(llcrnrlon, llcrnrlat, urcrnrlon, urcrnrlat, title, 
            lons, lats, color):
        m = Basemap(projection='merc',
                    resolution='i', 
                    llcrnrlon = llcrnrlon,
                    llcrnrlat = llcrnrlat,
                    urcrnrlon = urcrnrlon,
                    urcrnrlat = urcrnrlat)

        m.drawcountries(linewidth=1)
        m.drawcoastlines(linewidth=1)
        m.drawlsmask()
        m.drawstates()
        m.drawrivers(linewidth=.1)

        plt.title((str(len(lats)))+ \
            title,
            fontsize=12)

        x,y = m(lons, lats)
        if color == 'r':
            plt.hexbin(x, y, gridsize=40, cmap=plt.cm.Reds)
        elif color == 'b':
            plt.hexbin(x, y, gridsize=40, cmap=plt.cm.Blues)
        m.scatter(lons, lats, 1, marker='o',color=color, latlon=True)
        plt.show()



if ukraine:
    plotMap(llcrnrlon, llcrnrlat, urcrnrlon, urcrnrlat, "Russian", 
            rulons, rulats, 'r')
    plotMap(llcrnrlon, llcrnrlat, urcrnrlon, urcrnrlat, "Ukrainian", 
            uklons, uklats, 'b')

elif border:
    plotMap(llcrnrlon, llcrnrlat, urcrnrlon, urcrnrlat, "Border", 
            lons, lats, 'r')



