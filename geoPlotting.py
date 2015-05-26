import ast
import pandas as pd
import numpy as np
from twitter_helpers import DataFrame_from_tweets
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
import csv
import os
# countries.py needs to be in same dir as this script
# import countries


def get_coords_by_language(df, lang):
    # filter DataFrame to one language
    langDF = df[df['tweet_lang'] == lang]

    lats=[]
    lons=[]
    for pair in langDF['coords']:
        pair = ast.literal_eval(pair)
        lats.append(pair[1])
        lons.append(pair[0])

    return lats, lons



def plotMap(llcrnrlon, llcrnrlat, urcrnrlon, urcrnrlat, 
            lons, lats, color, title):
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
        if color == 'b':
            plt.hexbin(x, y, gridsize=40, cmap=plt.cm.Blues)        
        if color == 'g':
            plt.hexbin(x, y, gridsize=40, cmap=plt.cm.Greens)
        m.scatter(lons, lats, 1, marker='o',color=color, latlon=True)
        plt.show()



# def find_country_for_coords():
#     cc = countries.CountryChecker('/home/josh/google_drive/misc/TM_WORLD_BORDERS-0.3/TM_WORLD_BORDERS-0.3.shp')
#     country = []
#     i=0
#     for coords in df['coords']:
#         pair = ast.literal_eval(coords)
#         try:
#             label = cc.getCountry(countries.Point(pair[1], pair[0])).iso
#         except AttributeError:
#             label = "NaN"
#         country.append(label)
#         i+=1
#         print i

#     df['country'] = pd.Series(country)
#     print df['country'].value_counts()

#     df = df[df['country']=='NaN']



def main(myPath):
    # Ukraine coords
    llcrnrlon = 22.1357201
    llcrnrlat = 44.386383
    urcrnrlon = 40.227172
    urcrnrlat = 52.379475

    df = DataFrame_from_tweets(myPath)
    
    langsColors = [('ru', 'r'), ('uk', 'b'), ('en', 'g')]
    
    for lang, color in langsColors:
        lats, lons = get_coords_by_language(df, lang)
    
        plotMap(llcrnrlon, llcrnrlat, urcrnrlon, urcrnrlat, lons,
                lats, color, title=lang)


if __name__ == "__main__":
    import sys
    myPath = sys.argv[1]
    main(myPath)
        
