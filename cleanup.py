import pandas as pd
import re
import matplotlib as plt
from nltk.corpus import stopwords
import time

# Read in data
plt.get_backend()
data = pd.read_csv("./twitter-gender.csv",usecols= [0,5,19,17,21,10,11],encoding='latin1')

# Data Cleaning function
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
        s = s.replace("à", "")
        s = s.replace("ã", "")
        s = s.replace("ç", "")
        s = s.replace("ê", "")
        s = s.replace("ë", "")
        s = s.replace("è", "")
        s = s.replace("é", "")
        s = s.replace("ï", "")
        s = s.replace("î", "")
        s = s.replace("í", "")
        s = s.replace("ì", "")
        s = s.replace("ñ", "")
        s = s.replace("ô", "")
        s = s.replace("ò", "")
        s = s.replace("õ", "")
        s = s.replace("ð", "")
        s = s.replace("ø", "")
        s = s.replace("ó", "")
        s = s.replace("ö", "")
        s = s.replace("û","")
        s = s.replace("ü","")
        s = s.replace("µ", "")
        s = s.replace("ù", "")
        s = s.replace("ý", "")
        s = s.replace("ª", "")
        s = s.replace("æ", "")
        s = s.replace("¼", "")
        s = s.replace("¾", "")
        return s
    else:
        return ""

# how long does preprocessing take?
start = time.time()

#Clean tweets
data['Tweets'] = [cleaning(s) for s in data['text']]

#Clean Description
data['Description'] = [cleaning(s) for s in data['description']]

#Define Stopwords
stop = set(stopwords.words('english'))
stop.add("co")
stop.add("com")
stop.add("http")
stop.add("https")

#Process Tweets
data['Tweets'] = data['Tweets'].str.lower().str.split()
data['Tweets'] = data['Tweets'].apply(lambda x : [item for item in x if item not in stop])

#Process Descriptions
data['Description'] = data['Description'].str.lower().str.split()
data['Description'] = data['Description'].apply(lambda x : [item for item in x if item not in stop])

#Separate by Gender
Male = data[data['gender'] == 'male']
Female = data[data['gender'] == 'female']
Brand = data[data['gender'] == 'brand']

mwords = []
fwords = []
bwords = []
totalwords = set()
mbigrams = []
fbigrams = []
bbigrams = []

# get words and bigrams from male tweets
mtwords = []
mtbigrams = []
for tweet in Male['Tweets']:
    for i in range(len(tweet)):
        mtwords.append(tweet[i])
        mwords.append(tweet[i])
        totalwords.add(tweet[i])
        if (i < len(tweet)-1):
            mtbigrams.append(str(tweet[i]) + " " + str(tweet[i+1]))
            mbigrams.append(str(tweet[i]) + " " + str(tweet[i+1]))
        
# get words from female tweets
ftwords = []
ftbigrams = []
for tweet in Female['Tweets']:
    for i in range(len(tweet)):
        ftwords.append(tweet[i])
        fwords.append(tweet[i])
        totalwords.add(tweet[i])
        if (i < len(tweet)-1):
            ftbigrams.append(str(tweet[i]) + " " + str(tweet[i+1]))
            fbigrams.append(str(tweet[i]) + " " + str(tweet[i+1]))

# get words from brand tweets
btwords = []
btbigrams = []
for tweet in Brand['Tweets']:
    for i in range(len(tweet)):
        btwords.append(tweet[i])
        bwords.append(tweet[i])
        totalwords.add(tweet[i])
        if (i < len(tweet)-1):
            btbigrams.append(str(tweet[i]) + " " + str(tweet[i+1]))
            bbigrams.append(str(tweet[i]) + " " + str(tweet[i+1]))

# get words from male descriptions
mdwords = []
mdbigrams = []
for desc in Male['Description']:
    for i in range(len(desc)):
        mdwords.append(desc[i])
        mwords.append(desc[i])
        totalwords.add(desc[i])
        if (i < len(desc)-1):
            mdbigrams.append(str(desc[i]) + " " + str(desc[i+1]))
            mbigrams.append(str(desc[i]) + " " + str(desc[i+1]))
        
# get words from female descriptions
fdwords = []
fdbigrams = []
for desc in Female['Description']:
    for i in range(len(desc)):
        fdwords.append(desc[i])
        fwords.append(desc[i])
        totalwords.add(desc[i])
        if (i < len(desc)-1):
            fdbigrams.append(str(desc[i]) + " " + str(desc[i+1]))
            fbigrams.append(str(desc[i]) + " " + str(desc[i+1]))
        
# get words from brand descriptions
bdwords = []
bdbigrams = []
for desc in Brand['Description']:
    for i in range(len(desc)):
        bdwords.append(desc[i])
        bwords.append(desc[i])
        totalwords.add(desc[i])
        if (i < len(desc)-1):
            bdbigrams.append(str(desc[i]) + " " + str(desc[i+1]))
            bbigrams.append(str(desc[i]) + " " + str(desc[i+1]))

# find words that are exclusive to each gender
#xmwords = []
#xfwords = []
#xbwords = []
#i = 0
#for word in totalwords:
#    print(i)
#    i += 1
#    if not (word in fwords or word in bwords):
#        xmwords.append(word)
#    elif not (word in mwords or word in bwords):
#        xfwords.append(word)
#    elif not (word in mwords or word in fwords):
#        xbwords.append(word)
#    continue
#print("exclusive male words")
#print(xmwords)
#print("exclusive female words")
#print(xfwords)
#print("exclusive brand words")
#print(xbwords)

# define series of top 20 words
Male_Words = pd.Series(mwords).value_counts()[:20]
Female_Words = pd.Series(fwords).value_counts()[:20]
Brand_Words = pd.Series(bwords).value_counts()[:20]
Male_Words_T = pd.Series(mtwords).value_counts()[:20]
Female_Words_T = pd.Series(ftwords).value_counts()[:20]
Brand_Words_T = pd.Series(btwords).value_counts()[:20]
Male_Words_D = pd.Series(mdwords).value_counts()[:20]
Female_Words_D = pd.Series(fdwords).value_counts()[:20]
Brand_Words_D = pd.Series(bdwords).value_counts()[:20]

# define series of top 20 bigrams
Male_Bigrams_T = pd.Series(mtbigrams).value_counts()[:20]
Female_Bigrams_T = pd.Series(ftbigrams).value_counts()[:20]
Brand_Bigrams_T = pd.Series(btbigrams).value_counts()[:20]
Male_Bigrams_D = pd.Series(mdbigrams).value_counts()[:20]
Female_Bigrams_D = pd.Series(fdbigrams).value_counts()[:20]
Brand_Bigrams_D = pd.Series(bdbigrams).value_counts()[:20]
Male_Bigrams = pd.Series(mbigrams).value_counts()[:20]
Female_Bigrams = pd.Series(fbigrams).value_counts()[:20]
Brand_Bigrams = pd.Series(bbigrams).value_counts()[:20]

# identify top 2000 words for each gender
tMale_Words = pd.Series(mwords).value_counts()[:2000]
tFemale_Words = pd.Series(fwords).value_counts()[:2000]
tBrand_Words = pd.Series(bwords).value_counts()[:2000]
tMale_Words_T = pd.Series(mtwords).value_counts()[:2000]
tFemale_Words_T = pd.Series(ftwords).value_counts()[:2000]
tBrand_Words_T = pd.Series(btwords).value_counts()[:2000]
tMale_Words_D = pd.Series(mdwords).value_counts()[:2000]
tFemale_Words_D = pd.Series(fdwords).value_counts()[:2000]
tBrand_Words_D = pd.Series(bdwords).value_counts()[:2000]

f = open('words_yay.txt','w')
with pd.option_context('display.max_rows', None, 'display.max_columns', 3):
    f.write('------MALE WORDS--------\n')
    f.write(str(tMale_Words))
    f.write('\n')
    f.write('-------FEMALE WORDS-------\n')
    f.write(str(tFemale_Words))
    f.write('\n')
    f.write('---------BRAND WORDS----------\n')
    f.write(str(tBrand_Words))
    f.write('\n')
    f.close()
    
end = time.time()
print("Preprocessing time: " + str(end-start) + " seconds")

#Plot
#overall
Male_Words.plot(kind='bar',stacked=True, color='blue')
plt.pyplot.title('Male Words Overall')
plt.pyplot.ylabel('Occurrences')
plt.pyplot.show()

Female_Words.plot(kind='bar',stacked=True, color='magenta')
plt.pyplot.title('Female Words Overall')
plt.pyplot.ylabel('Occurrences')
plt.pyplot.show()

Brand_Words.plot(kind='bar',stacked=True, color='green')
plt.pyplot.title('Brand Words Overall')
plt.pyplot.ylabel('Occurrences')
plt.pyplot.show()

Male_Bigrams.plot(kind='bar',stacked=True, color='blue')
plt.pyplot.title('Male Bigrams Overall')
plt.pyplot.ylabel('Occurrences')
plt.pyplot.show()

Female_Bigrams.plot(kind='bar',stacked=True, color='magenta')
plt.pyplot.title('Female Bigrams Overall')
plt.pyplot.ylabel('Occurrences')
plt.pyplot.show()

Brand_Bigrams.plot(kind='bar',stacked=True, color='green')
plt.pyplot.title('Brand Bigrams Overall')
plt.pyplot.ylabel('Occurrences')
plt.pyplot.show()


#tweets
Male_Words_T.plot(kind='bar',stacked=True, color='blue')
plt.pyplot.title('Male Words in Tweets')
plt.pyplot.ylabel('Occurrences')
plt.pyplot.show()

Female_Words_T.plot(kind='bar',stacked=True, color='magenta')
plt.pyplot.title('Female Words in Tweets')
plt.pyplot.ylabel('Occurrences')
plt.pyplot.show()

Brand_Words_T.plot(kind='bar',stacked=True, color='green')
plt.pyplot.title('Brand Words in Tweets')
plt.pyplot.ylabel('Occurrences')
plt.pyplot.show()

Male_Bigrams_T.plot(kind='bar',stacked=True, color='blue')
plt.pyplot.title('Male Bigrams in Tweets')
plt.pyplot.ylabel('Occurrences')
plt.pyplot.show()

Female_Bigrams_T.plot(kind='bar',stacked=True, color='magenta')
plt.pyplot.title('Female Bigrams in Tweets')
plt.pyplot.ylabel('Occurrences')
plt.pyplot.show()

Brand_Bigrams_T.plot(kind='bar',stacked=True, color='green')
plt.pyplot.title('Brand Bigrams in Tweets')
plt.pyplot.ylabel('Occurrences')
plt.pyplot.show()


#description
Male_Words_D.plot(kind='bar',stacked=True, color='blue')
plt.pyplot.title('Male Words in Descriptions')
plt.pyplot.ylabel('Occurrences')
plt.pyplot.show()

Female_Words_D.plot(kind='bar',stacked=True, color='magenta')
plt.pyplot.title('Female Words in Descriptions')
plt.pyplot.ylabel('Occurrences')
plt.pyplot.show()

Brand_Words_D.plot(kind='bar',stacked=True, color='green')
plt.pyplot.title('Brand Words in Descriptions')
plt.pyplot.ylabel('Occurrences')
plt.pyplot.show()

Male_Bigrams_D.plot(kind='bar',stacked=True, color='blue')
plt.pyplot.title('Male Bigrams in Descriptions')
plt.pyplot.ylabel('Occurrences')
plt.pyplot.show()

Female_Bigrams_D.plot(kind='bar',stacked=True, color='magenta')
plt.pyplot.title('Female Bigrams in Descriptions')
plt.pyplot.ylabel('Occurrences')
plt.pyplot.show()

Brand_Bigrams_D.plot(kind='bar',stacked=True, color='green')
plt.pyplot.title('Brand Bigrams in Descriptions')
plt.pyplot.ylabel('Occurrences')
plt.pyplot.show()
