import ast
import pandas as pd
import numpy as np
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
import csv
import os
# countries.py needs to be in same dir as this script
# import countries


def get_coords_by_language(myPath):

    if os.path.isdir(myPath):
        fileNames = [f for f in os.listdir(myPath) if f.endswith('.txt')]
        
    elif os.path.isfile(myPath):
        fileNames = [myPath]
        
    tweets=[]
    for fileName in fileNames:
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

    ru = df[df['tweet_lang'] == 'ru']
    uk = df[df['tweet_lang'] == 'uk']
    en = df[df['tweet_lang'] == 'en']

    rulats=[]
    rulons=[]
    for pair in ru['coords']:
        pair = ast.literal_eval(pair)
        rulats.append(pair[1])
        rulons.append(pair[0])

    uklats=[]
    uklons=[]
    for pair in uk['coords']:
        pair = ast.literal_eval(pair)
        uklats.append(pair[1])
        uklons.append(pair[0])

    enlats=[]
    enlons=[]
    for pair in en['coords']:
        pair = ast.literal_eval(pair)
        enlats.append(pair[1])
        enlons.append(pair[0])

    return rulats, rulons, uklats, uklons, enlats, enlons



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

    rulons,rulats, uklons,uklats, enlons,enlats = get_coords_by_language(myPath)
    
    plotMap(llcrnrlon, llcrnrlat, urcrnrlon, urcrnrlat, "Russian", 
            rulons, rulats, 'r')
    plotMap(llcrnrlon, llcrnrlat, urcrnrlon, urcrnrlat, "Ukrainian", 
            uklons, uklats, 'b')
    plotMap(llcrnrlon, llcrnrlat, urcrnrlon, urcrnrlat, "English", 
            enlons, enlats, 'g')


if __name__ == "__main__":
    import sys
    myPath = sys.argv[1]
    main(myPath)
        
