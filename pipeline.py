__author__ = 'TalBY'
import urllib, json, nltk, json, cPickle, re, string, numpy
from grid import GS
from nltk.corpus import stopwords
stop = stopwords.words('english')
from model import LG,testing, NB, splitsets, add_singles, computeP, add_ngrams
from DF import build_data_frame, tokening

exclude = set(string.punctuation)
from pandas import DataFrame


def getdata(url):
    response = urllib.urlopen(url);
    data = json.loads(response.read())
    if isinstance(data.values()[0][0], dict):
        print len(data.values()[0])
        return data.values()[0]
    elif isinstance(data.values()[1][0], dict):
        print len(data.values()[1])
        return data.values()[1]
    else:
        print('error')


def GETkW(data):
    rdioshows = radioshows(data)
    Dkw5834 = {rdioshow: [] for rdioshow in rdioshows}
    for d in data:
        if d['showName'] in Dkw5834.keys(): # append the new number to the existing array at this slot
            Dkw5834[d['showName']].extend([i for i in d['keywords']])
        else:
            Dkw5834[d['showName']] = [i for i in d['keywords']]
    return Dkw5834


def reading(phrases, b,e,s, ids= []):
    data = []
    for phrase in phrases:
        url = "http://api.audioburst.com/Search?value="+phrase+"&filter=sourceKey%20eq%205843%20&top=1000"
        # print(phrase)
        data.extend(getdata(url))
        for d in data:
            if d['id'] is not None and d['id'] not in ids:
                ids.append(d['id'])
        for num in range(b,e,s):
            url = "http://api.audioburst.com/Search?value="+phrase+"&filter=sourceKey%20eq%205843%20&top=1000&skip="+str(num)
            try:
                data.extend(getdata(url))
            except:
                continue
    return data, ids


def radioshows(data):
    #get unique list of shows
    rdioshows = []
    for d in data:
        rdioshows.append(d['showName'])
    return set(rdioshows)


if __name__ == '__main__':
    phrases = ["Bloomberg%20travel%20weather",  "Bloomberg%20weather%20center", "Bloomberg%20meteorologist%20Gary%20Best",  "travel%20weather%20reports"]
    l, ids = [], []
    # li = ['Weather', 'Weather Channel', 'Forecast', 'Chilly', 'Wet', 'Snow', 'Rain', 'Temperature', 'Meteorologist', 'Storms', 'Dry', 'Clouds', 'Cold', 'Warms','Cloudy', 'Sunshine', 'Sunny', 'Showers', 'Cooler', 'Hurricane', 'Climate', 'Winter', 'Rainbow', 'Seasonal', 'Thunder', 'Atlantic', 'Breeze', 'Gusty', 'Fog', 'Snowfall', 'Colder', 'Chill', 'Skies', 'Lows', 'Breezy', 'Wind', 'Windy', 'Overnight']
    li = ['Weather Channel', 'Forecast', 'Temperature', 'Meteorologist']
    for st in li:
        l.append(st.replace(" ", "%20"))
    data, ids = reading(phrases+l, 1000, 3000, 1000, ids)
    c = len(ids)
    print(len(data))
    dataf, ids = build_data_frame(data, [1])

    workfile = 'C:\Users\TalBY\Downloads\List of IDs_10000v2.txt'
    data_frame = DataFrame({'text': [], 'cl': [], 'id': []})
    with open(workfile) as f:
        lines = f.readlines()
    for idx in lines[:(len(lines)/2-1)]:
        idxx = idx.replace('\r', '').replace('\n','')
        if idxx not in ids:
            ids.append(idxx)
            url = "".join(['http://storageaudiobursts.blob.core.windows.net/nlp/', idx.replace('\r', '').replace('\n',''),'.json' ])
            print(url)
            try:
                response = urllib.urlopen(url)
                data = json.loads(response.read())
                data_frame = data_frame.append(DataFrame({'text': data['text'], 'cl': [0], 'id':idxx}))
            except:
                continue
        else:
            continue
    # print((len(lines)-c) == len(data_frame))
    print('ids:', len(ids))
    print('dataf:', len(dataf))
    cPickle.dump(dataf, open("dataf_2.p", "wb" ))
    # dataf = dataf.append(build_data_frame(data2, [0]))
    dataf = dataf.append(data_frame)
    # dataf = dataf.append(dataf2)
    # dataf.index = [i for i in range(0, len(dataf))]
    # dataf = dataf.reindex(numpy.random.permutation(dataf.index))
    # dataf = cPickle.load(dataf, open("dataf.p", "rb"))

    train, test = splitsets(dataf, 0.8)
    # acc, predictions = LG(train, test)
    # print(acc)
    predictions, gs_logreg = GS(train, test)

    zipped = zip(test.text, predictions)
    with open('resultsfile.txt', 'w') as f:
        for i in zipped:
            f.writelines(str(i))
            f.writelines('\n')
            f.writelines('\n')
    f.close()
    cPickle.dump(gs_logreg, open("gs_logreg.p", "wb" ))


    print(testing(test.iloc[0], gs_logreg))
    print(testing('tal', gs_logreg))



