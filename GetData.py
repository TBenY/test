__author__ = 'TalBY'

import urllib, json, nltk, json, cPickle
from nltk import FreqDist
from nltk.corpus import stopwords
stop = stopwords.words('english')


def getdata(url):
    response = urllib.urlopen(url);
    data = json.loads(response.read())
    print len(data.values()[1])
    return data.values()[1]

#build the corpus for each station

def searchPat(data, word = 'weather'):
    patterns = {}
    for d in data:
        idx = d['text'].find(word)
        pattern =  d['text'][idx-50:idx+150]
        if d['sourceKey'] in patterns.keys():
        # append the new number to the existing array at this slot
            patterns[d['sourceKey']].append(pattern.split())
        else:
            # create a new array in this slot
            patterns[d['sourceKey']] = [pattern.split()]
        # list of list to a corpus
    sourceKeys = {d['sourceKey']: d['sourceName'] for d in data}
    for k, v in patterns.iteritems():
        patterns[k] = [item for sublist in v for item in sublist if item.lower() not in stop]
    return patterns


    def main():
        data = getdata(url)
        d2 = getdata(url2)
        print len(data)
        patterns = searchPat(data)
        fds = {k: FreqDist(v) for k, v in patterns.iteritems()}
        freqd = []
        for k_, f in fds:
            freqd[k_] = {k: f.freq(k) for k, w in f.items() if w > 1}
        # import operator
        # sorted_x = sorted(freqd.items(), key=operator.itemgetter(1), reverse=True)

        cPickle.dump(freqd, open( "freqd.p", "wb" ) )
        print(len(freqd))
