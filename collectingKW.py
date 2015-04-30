__author__ = 'TalBY'

import urllib, json, nltk, re, cPickle
# print len(data.values()[0])

def getdata(url):
    response = urllib.urlopen(url);
    data = json.loads(response.read())
    try:
        if isinstance(data.values()[0][0], dict):
            print len(data.values()[0])
            return data.values()[0]
        elif isinstance(data.values()[1][0], dict):
            print len(data.values()[1])
            return data.values()[1]
    except:
        print('error')
        return


searchphrases = ["Bloomberg%20travel%20weather","Blomberg weather center","Blomber meteorologist Gary Best", "travel weather reports"]
data_t = []
for i in searchphrases:
    url = "http://api.audioburst.com/Search?value="+i.replace(" ", "%20")+"&filter=sourceKey%20eq%205843%20&top=10000"
    response = urllib.urlopen(url)
    data = json.loads(response.read())
    data = getdata(url)
    # length = data.__len__()
    if not data== None:
        data_t = data+data_t


#get unique list of shows
rdioshows = []
for d in data:
    rdioshows.append(d['showName'])
rdioshows5843 = set(rdioshows)
len(rdioshows5843)

#build the corpus for each station
def GETkW(data):
    Dkw5834 = {rdioshow:[] for rdioshow in rdioshows}
    for d in data:
        # rawtext = d['text']
        if d['showName'] in Dkw5834.keys(): # append the new number to the existing array at this slot
            Dkw5834[d['showName']].extend([i for i in d['keywords']])
        else:
            Dkw5834[d['showName']] = [i for i in d['keywords']]
        print(d['keywords'])
        print(d['text'])
    return Dkw5834

#     print(pattern)
weatherKW_5843 = GETkW(data_t)
cPickle.dump(weatherKW_5843, open( "weatherKW_5843.p", "wb" ) )