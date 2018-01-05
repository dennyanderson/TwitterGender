import math
import pandas as pd
import re
import matplotlib as plt
from nltk.corpus import stopwords
import csv
#import nltk
import numpy as np
import itertools

filename = "genderCSV.csv"

# list of colors
colors = [["black",[0,0,0]],
          ["green",[0,128,0]],
          ["silver",[192,192,192]],
          ["lime",[0,255,0]],
          ["gray",[128,0,128]],
          ["olive",[128,128,0]],
          ["white",[255,255,255]],
          ["yellow",[255,255,0]],
          ["maroon",[128,0,0]],
          ["navy",[0,0,128]], 
          ["red",[255,0,0]],
          ["blue",[0,0,255]],
          ["purple",[128,0,128]],
          ["teal",[0,128,128]],
          ["fuchsia",[255,0,255]],
          ["aqua",[0,255,255]]]

# function to convert a hex value into rgb values
# returns an array in the form [r, g, b]
def hexToRGB(color):
    color = str(color)
    if (len(color) == 0):
        return ([0, 0, 0])
    if (color[0] == '#'):
        color = color[1:]
    if (len(color) == 0 or len(color) > 6):
        return ([0, 0, 0])
    while (len(color) != 6):
        color = '0' + color
    hexR = color[0:2]
    hexG = color[2:4]
    hexB = color[4:6]
    decR = int(hexR, 16)
    decG = int(hexG, 16)
    decB = int(hexB, 16)
    listRGB = [decR, decG, decB]
    return listRGB

# function to convert a hex value into a color
# returns the color closest to the given hex value
def returnColor(hexColor):
    decColor = hexToRGB(hexColor)
    minimum = 256
    bestIndex = 0
    index = 0
    for c in colors:
        distR = (decColor[0] - c[1][0])
        distG = (decColor[1] - c[1][1])
        distB = (decColor[2] - c[1][2])
        distance = math.sqrt(distR**2 + distG**2 + distB**2)
        if (distance < minimum):
            minimum = distance
            bestIndex = index;
        index = index + 1
    return colors[bestIndex][0]

# read in data
plt.get_backend()
data = pd.read_csv(filename, usecols= [0, 1, 2, 3, 4, 5, 6, 7, 8], encoding='latin1')

# function to clean the data
def cleaning(s):
    if(isinstance(s, str)):
        s = str(s)
        s = s.lower()
        s = s.replace("&amp;", "")
        s = re.sub('\s\W',' ',s)
        s = re.sub('\W,\s',' ',s)
        s = re.sub(r'[^\w]', ' ', s)
        s = re.sub("\d+", "", s)
        s = re.sub('\s+',' ',s)
        s = re.sub('[!@#$_]', '', s)
        s = s.replace(","," ")
        s = s.replace("[\w*"," ")
        s = s.replace("â","")
        s = s.replace("á", "")
        s = s.replace("å", "")
        s = s.replace("ä", "")
        s = s.replace("ã", "")
        s = s.replace("ê", "")
        s = s.replace("é", "")
        s = s.replace("ï", "")
        s = s.replace("î", "")
        s = s.replace("ì", "")
        s = s.replace("ô", "")
        s = s.replace("ò", "")
        s = s.replace("ö", "")
        s = s.replace("û","")
        s = s.replace("ü","")
        s = s.replace("ù", "")
        s = s.replace("ª", "")
        return s
    else:
        return ""

# clean tweets
data['Tweets'] = [cleaning(s) for s in data['text']]

# clean description
data['Description'] = [cleaning(s) for s in data['description']]

# define stopwords
stop = set(stopwords.words('english'))
stop.add("co")
stop.add("com")
stop.add("http")
stop.add("https")

# process tweets
data['Tweets'] = data['Tweets'].str.lower().str.split()
data['Tweets'] = data['Tweets'].apply(lambda x : [item for item in x if item not in stop])

# process descriptions
data['Description'] = data['Description'].str.lower().str.split()
data['Description'] = data['Description'].apply(lambda x : [item for item in x if item not in stop])

# process link_color and sidebar_color
data['link_colorGroup'] = [returnColor(i) for i in data['link_color']]
data['sidebar_colorGroup'] = [returnColor(i) for i in data['sidebar_color']]

# function for converting string array into a single string separated by spaces
def convertArrayToString(array):
    string = " "
    for word in array:
        string = string + word + " "
    return string

# 'descString' is the single-string version of 'Description'
# 'tweetString' is the single-string version of 'Tweets'
data['descString'] = [convertArrayToString(wordArray) for wordArray in data['Description']]
data['tweetString'] = [convertArrayToString(wordArray) for wordArray in data['Tweets']]

# these are the headers to put in the csv file
headers = ['fav_number', 'link_colorGroup', 'retweet_count', 'sidebar_colorGroup',
           'tweet_count', 'gender']

# function to write to csv file given the headers of the data file to write
def writeToFile(headers):
    file = open('genderCSVedit.csv', 'w')
    index = 0
    while (index < 20050):
        for header in headers:
            if (data['gender'][index] == 'brand' or data['gender'][index] == 'female' or data['gender'][index] == 'male'):
                file.write(str(data[header][index]))
                file.write(',')
        if (data['gender'][index] == 'brand' or data['gender'][index] == 'female' or data['gender'][index] == 'male'):
            file.write('\n')
        index = index + 1
    file.close()

brandLinkColors = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
femaleLinkColors = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
maleLinkColors = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
brandSidebarColors = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
femaleSidebarColors = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
maleSidebarColors = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
brands = 0
females = 0
males = 0

index = 0
while (index < 20050):
    if (data['gender'][index] == 'brand'):
        brands = brands + 1
        if (data['link_colorGroup'][index] == 'black'):
            brandLinkColors[0] = brandLinkColors[0] + 1
        elif (data['link_colorGroup'][index] == 'green'):
            brandLinkColors[1] = brandLinkColors[1] + 1
        elif (data['link_colorGroup'][index] == 'silver'):
            brandLinkColors[2] = brandLinkColors[2] + 1
        elif (data['link_colorGroup'][index] == 'lime'):
            brandLinkColors[3] = brandLinkColors[3] + 1
        elif (data['link_colorGroup'][index] == 'gray'):
            brandLinkColors[4] = brandLinkColors[4] + 1
        elif (data['link_colorGroup'][index] == 'olive'):
            brandLinkColors[5] = brandLinkColors[5] + 1
        elif (data['link_colorGroup'][index] == 'white'):
            brandLinkColors[6] = brandLinkColors[6] + 1
        elif (data['link_colorGroup'][index] == 'yellow'):
            brandLinkColors[7] = brandLinkColors[7] + 1
        elif (data['link_colorGroup'][index] == 'maroon'):
            brandLinkColors[8] = brandLinkColors[8] + 1
        elif (data['link_colorGroup'][index] == 'navy'):
            brandLinkColors[9] = brandLinkColors[9] + 1
        elif (data['link_colorGroup'][index] == 'red'):
            brandLinkColors[10] = brandLinkColors[10] + 1
        elif (data['link_colorGroup'][index] == 'blue'):
            brandLinkColors[11] = brandLinkColors[11] + 1
        elif (data['link_colorGroup'][index] == 'purple'):
            brandLinkColors[12] = brandLinkColors[12] + 1
        elif (data['link_colorGroup'][index] == 'teal'):
            brandLinkColors[13] = brandLinkColors[13] + 1
        elif (data['link_colorGroup'][index] == 'fuchsia'):
            brandLinkColors[14] = brandLinkColors[14] + 1
        elif (data['link_colorGroup'][index] == 'aqua'):
            brandLinkColors[15] = brandLinkColors[15] + 1
        if (data['sidebar_colorGroup'][index] == 'black'):
            brandSidebarColors[0] = brandSidebarColors[0] + 1
        elif (data['sidebar_colorGroup'][index] == 'green'):
            brandSidebarColors[1] = brandSidebarColors[1] + 1
        elif (data['sidebar_colorGroup'][index] == 'silver'):
            brandSidebarColors[2] = brandSidebarColors[2] + 1
        elif (data['sidebar_colorGroup'][index] == 'lime'):
            brandSidebarColors[3] = brandSidebarColors[3] + 1
        elif (data['sidebar_colorGroup'][index] == 'gray'):
            brandSidebarColors[4] = brandSidebarColors[4] + 1
        elif (data['sidebar_colorGroup'][index] == 'olive'):
            brandSidebarColors[5] = brandSidebarColors[5] + 1
        elif (data['sidebar_colorGroup'][index] == 'white'):
            brandSidebarColors[6] = brandSidebarColors[6] + 1
        elif (data['sidebar_colorGroup'][index] == 'yellow'):
            brandSidebarColors[7] = brandSidebarColors[7] + 1
        elif (data['sidebar_colorGroup'][index] == 'maroon'):
            brandSidebarColors[8] = brandSidebarColors[8] + 1
        elif (data['sidebar_colorGroup'][index] == 'navy'):
            brandSidebarColors[9] = brandSidebarColors[9] + 1
        elif (data['sidebar_colorGroup'][index] == 'red'):
            brandSidebarColors[10] = brandSidebarColors[10] + 1
        elif (data['sidebar_colorGroup'][index] == 'blue'):
            brandSidebarColors[11] = brandSidebarColors[11] + 1
        elif (data['sidebar_colorGroup'][index] == 'purple'):
            brandSidebarColors[12] = brandSidebarColors[12] + 1
        elif (data['sidebar_colorGroup'][index] == 'teal'):
            brandSidebarColors[13] = brandSidebarColors[13] + 1
        elif (data['sidebar_colorGroup'][index] == 'fuchsia'):
            brandSidebarColors[14] = brandSidebarColors[14] + 1
        elif (data['sidebar_colorGroup'][index] == 'aqua'):
            brandSidebarColors[15] = brandSidebarColors[15] + 1
    elif (data['gender'][index] == 'female'):
        females = females + 1
        if (data['link_colorGroup'][index] == 'black'):
            femaleLinkColors[0] = femaleLinkColors[0] + 1
        elif (data['link_colorGroup'][index] == 'green'):
            femaleLinkColors[1] = femaleLinkColors[1] + 1
        elif (data['link_colorGroup'][index] == 'silver'):
            femaleLinkColors[2] = femaleLinkColors[2] + 1
        elif (data['link_colorGroup'][index] == 'lime'):
            femaleLinkColors[3] = femaleLinkColors[3] + 1
        elif (data['link_colorGroup'][index] == 'gray'):
            femaleLinkColors[4] = femaleLinkColors[4] + 1
        elif (data['link_colorGroup'][index] == 'olive'):
            femaleLinkColors[5] = femaleLinkColors[5] + 1
        elif (data['link_colorGroup'][index] == 'white'):
            femaleLinkColors[6] = femaleLinkColors[6] + 1
        elif (data['link_colorGroup'][index] == 'yellow'):
            femaleLinkColors[7] = femaleLinkColors[7] + 1
        elif (data['link_colorGroup'][index] == 'maroon'):
            femaleLinkColors[8] = femaleLinkColors[8] + 1
        elif (data['link_colorGroup'][index] == 'navy'):
            femaleLinkColors[9] = femaleLinkColors[9] + 1
        elif (data['link_colorGroup'][index] == 'red'):
            femaleLinkColors[10] = femaleLinkColors[10] + 1
        elif (data['link_colorGroup'][index] == 'blue'):
            femaleLinkColors[11] = femaleLinkColors[11] + 1
        elif (data['link_colorGroup'][index] == 'purple'):
            femaleLinkColors[12] = femaleLinkColors[12] + 1
        elif (data['link_colorGroup'][index] == 'teal'):
            femaleLinkColors[13] = femaleLinkColors[13] + 1
        elif (data['link_colorGroup'][index] == 'fuchsia'):
            femaleLinkColors[14] = femaleLinkColors[14] + 1
        elif (data['link_colorGroup'][index] == 'aqua'):
            femaleLinkColors[15] = femaleLinkColors[15] + 1
        if (data['sidebar_colorGroup'][index] == 'black'):
            femaleSidebarColors[0] = femaleSidebarColors[0] + 1
        elif (data['sidebar_colorGroup'][index] == 'green'):
            femaleSidebarColors[1] = femaleSidebarColors[1] + 1
        elif (data['sidebar_colorGroup'][index] == 'silver'):
            femaleSidebarColors[2] = femaleSidebarColors[2] + 1
        elif (data['sidebar_colorGroup'][index] == 'lime'):
            femaleSidebarColors[3] = femaleSidebarColors[3] + 1
        elif (data['sidebar_colorGroup'][index] == 'gray'):
            femaleSidebarColors[4] = femaleSidebarColors[4] + 1
        elif (data['sidebar_colorGroup'][index] == 'olive'):
            femaleSidebarColors[5] = femaleSidebarColors[5] + 1
        elif (data['sidebar_colorGroup'][index] == 'white'):
            femaleSidebarColors[6] = femaleSidebarColors[6] + 1
        elif (data['sidebar_colorGroup'][index] == 'yellow'):
            femaleSidebarColors[7] = femaleSidebarColors[7] + 1
        elif (data['sidebar_colorGroup'][index] == 'maroon'):
            femaleSidebarColors[8] = femaleSidebarColors[8] + 1
        elif (data['sidebar_colorGroup'][index] == 'navy'):
            femaleSidebarColors[9] = femaleSidebarColors[9] + 1
        elif (data['sidebar_colorGroup'][index] == 'red'):
            femaleSidebarColors[10] = femaleSidebarColors[10] + 1
        elif (data['sidebar_colorGroup'][index] == 'blue'):
            femaleSidebarColors[11] = femaleSidebarColors[11] + 1
        elif (data['sidebar_colorGroup'][index] == 'purple'):
            femaleSidebarColors[12] = femaleSidebarColors[12] + 1
        elif (data['sidebar_colorGroup'][index] == 'teal'):
            femaleSidebarColors[13] = femaleSidebarColors[13] + 1
        elif (data['sidebar_colorGroup'][index] == 'fuchsia'):
            femaleSidebarColors[14] = femaleSidebarColors[14] + 1
        elif (data['sidebar_colorGroup'][index] == 'aqua'):
            femaleSidebarColors[15] = femaleSidebarColors[15] + 1
    elif (data['gender'][index] == 'male'):
        males = males + 1
        if (data['link_colorGroup'][index] == 'black'):
            maleLinkColors[0] = maleLinkColors[0] + 1
        elif (data['link_colorGroup'][index] == 'green'):
            maleLinkColors[1] = maleLinkColors[1] + 1
        elif (data['link_colorGroup'][index] == 'silver'):
            maleLinkColors[2] = maleLinkColors[2] + 1
        elif (data['link_colorGroup'][index] == 'lime'):
            maleLinkColors[3] = maleLinkColors[3] + 1
        elif (data['link_colorGroup'][index] == 'gray'):
            maleLinkColors[4] = maleLinkColors[4] + 1
        elif (data['link_colorGroup'][index] == 'olive'):
            maleLinkColors[5] = maleLinkColors[5] + 1
        elif (data['link_colorGroup'][index] == 'white'):
            maleLinkColors[6] = maleLinkColors[6] + 1
        elif (data['link_colorGroup'][index] == 'yellow'):
            maleLinkColors[7] = maleLinkColors[7] + 1
        elif (data['link_colorGroup'][index] == 'maroon'):
            maleLinkColors[8] = maleLinkColors[8] + 1
        elif (data['link_colorGroup'][index] == 'navy'):
            maleLinkColors[9] = maleLinkColors[9] + 1
        elif (data['link_colorGroup'][index] == 'red'):
            maleLinkColors[10] = maleLinkColors[10] + 1
        elif (data['link_colorGroup'][index] == 'blue'):
            maleLinkColors[11] = maleLinkColors[11] + 1
        elif (data['link_colorGroup'][index] == 'purple'):
            maleLinkColors[12] = maleLinkColors[12] + 1
        elif (data['link_colorGroup'][index] == 'teal'):
            maleLinkColors[13] = maleLinkColors[13] + 1
        elif (data['link_colorGroup'][index] == 'fuchsia'):
            maleLinkColors[14] = maleLinkColors[14] + 1
        elif (data['link_colorGroup'][index] == 'aqua'):
            maleLinkColors[15] = maleLinkColors[15] + 1
        if (data['sidebar_colorGroup'][index] == 'black'):
            maleSidebarColors[0] = maleSidebarColors[0] + 1
        elif (data['sidebar_colorGroup'][index] == 'green'):
            maleSidebarColors[1] = maleSidebarColors[1] + 1
        elif (data['sidebar_colorGroup'][index] == 'silver'):
            maleSidebarColors[2] = maleSidebarColors[2] + 1
        elif (data['sidebar_colorGroup'][index] == 'lime'):
            maleSidebarColors[3] = maleSidebarColors[3] + 1
        elif (data['sidebar_colorGroup'][index] == 'gray'):
            maleSidebarColors[4] = maleSidebarColors[4] + 1
        elif (data['sidebar_colorGroup'][index] == 'olive'):
            maleSidebarColors[5] = maleSidebarColors[5] + 1
        elif (data['sidebar_colorGroup'][index] == 'white'):
            maleSidebarColors[6] = maleSidebarColors[6] + 1
        elif (data['sidebar_colorGroup'][index] == 'yellow'):
            maleSidebarColors[7] = maleSidebarColors[7] + 1
        elif (data['sidebar_colorGroup'][index] == 'maroon'):
            maleSidebarColors[8] = maleSidebarColors[8] + 1
        elif (data['sidebar_colorGroup'][index] == 'navy'):
            maleSidebarColors[9] = maleSidebarColors[9] + 1
        elif (data['sidebar_colorGroup'][index] == 'red'):
            maleSidebarColors[10] = maleSidebarColors[10] + 1
        elif (data['sidebar_colorGroup'][index] == 'blue'):
            maleSidebarColors[11] = maleSidebarColors[11] + 1
        elif (data['sidebar_colorGroup'][index] == 'purple'):
            maleSidebarColors[12] = maleSidebarColors[12] + 1
        elif (data['sidebar_colorGroup'][index] == 'teal'):
            maleSidebarColors[13] = maleSidebarColors[13] + 1
        elif (data['sidebar_colorGroup'][index] == 'fuchsia'):
            maleSidebarColors[14] = maleSidebarColors[14] + 1
        elif (data['sidebar_colorGroup'][index] == 'aqua'):
            maleSidebarColors[15] = maleSidebarColors[15] + 1
    index = index + 1

index = 0
while (index < 16):
    blc = brandLinkColors[index]
    bsc = brandSidebarColors[index]
    flc = femaleLinkColors[index]
    fsc = femaleSidebarColors[index]
    mlc = maleLinkColors[index]
    msc = maleSidebarColors[index]
    blcPercent = (blc / brands) * 100
    bscPercent = (bsc / brands) * 100
    flcPercent = (flc / females) * 100
    fscPercent = (fsc / females) * 100
    mlcPercent = (mlc / males) * 100
    mscPercent = (msc / males) * 100
    winnerLCPercent = 0
    winnerSCPercent = 0
    winnerLC = ""
    winnerSC = ""
    if (blcPercent >= flcPercent and blcPercent >= mlcPercent):
        winnerLCPercent = blcPercent
        winnerLC = "brand"
    elif (flcPercent >= blcPercent and flcPercent >= mlcPercent):
        winnerLCPercent = flcPercent
        winnerLC = "female"
    elif (mlcPercent >= blcPercent and mlcPercent >= flcPercent):
        winnderLCPercent = mlcPercent
        winnerLC = "male"
    if (bscPercent >= fscPercent and bscPercent >= mscPercent):
        winnerSCPercent = bscPercent
        winnerSC = "brand"
    elif (fscPercent >= bscPercent and fscPercent >= mscPercent):
        winnerSCPercent = fscPercent
        winnerSC = "female"
    elif (mscPercent >= bscPercent and mscPercent >= fscPercent):
        winnderSCPercent = mscPercent
        winnerSC = "male"
    winnerColor = colors[index][0]
    print (winnerColor + ": link = " + winnerLC + " with " + str(winnerLCPercent) + "; sidebar = " + winnerSC + " with " +
           str(winnerSCPercent))
    index = index + 1
    
writeToFile(headers)

# data attributes:
#     gender
#     description -> Description -> descString
#     fav_number
#     link_color -> link_colorGroup
#     name
#     retweet_count
#     sidebar_color -> sidebar_colorGroup
#     text -> Tweets -> tweetString
#     tweet_count