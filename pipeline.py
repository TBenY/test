__author__ = 'TalBY'
import urllib, json, nltk, json, cPickle, re, string, numpy
from nltk import FreqDist
from nltk.corpus import stopwords
stop = stopwords.words('english')
from model import LG, NB, splitsets, add_singles, computeP, computeP2, add_ngrams
from DF import build_data_frame, tokening
from nltk.util import ngrams
from nltk import word_tokenize
from string import punctuation
from nltk.corpus import stopwords
from alchemyapi import AlchemyAPI
exclude = set(string.punctuation)
import pandas as pd
from pandas import DataFrame,Series

alchemyapi = AlchemyAPI()


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
    Dkw5834 = {rdioshow : [] for rdioshow in rdioshows}
    for d in data:
        if d['showName'] in Dkw5834.keys(): # append the new number to the existing array at this slot
            Dkw5834[d['showName']].extend([i for i in d['keywords']])
        else:
            Dkw5834[d['showName']] = [i for i in d['keywords']]
    return Dkw5834


def radioshows(data):
    #get unique list of shows
    rdioshows = []
    for d in data:
        rdioshows.append(d['showName'])
    return set(rdioshows)


if __name__ == '__main__':
    phrases = ["Bloomberg%20travel%20weather","weather", "Bloomberg%20weather%20center", "Bloomberg%20meteorologist%20Gary%20Best",  "travel%20weather%20reports"]
    data = []
    for phrase in phrases:
        url = "http://api.audioburst.com/Search?value="+phrase+"&filter=sourceKey%20eq%205843%20&top=1000"
        # print(phrase)
        data.extend(getdata(url))
        for num in range(1000, 2000, 1000):
            url = "http://api.audioburst.com/Search?value="+phrase+"&filter=sourceKey%20eq%205843%20&top=1000&skip="+str(num)
            try:
                data.extend(getdata(url))
            except:
                continue


    print(len(data))

# print len(data.values()[0])

    phrases = ["finance"]

    for phrase in phrases:
        url = "http://api.audioburst.com/Search?value="+phrase+"&filter=sourceKey%20eq%205843%20&top=1000"
        print(phrase)
        data2 = getdata(url)
        for num in range(1000, 2000, 1000):
            url = "http://api.audioburst.com/Search?value="+phrase+"&filter=sourceKey%20eq%205843%20&top=1000&skip="+str(num)
            try:
                data.extend(getdata(url))
            except:
                continue

    # weatherKW_5843 = GETkW(data)
    # financeKW_5843 = GETkW(data2)
    # weatherKW_5843 = cPickle.load(open("weatherKW_5843.p", "rb"))

    # cPickle.dump(weatherKW_5843, open( "weatherKW_5843.p", "wb" ) )
    # p_cumm_D, j = {}, 0
    #
    #
    # #build dataframe

    dataf = build_data_frame(data, [1])
    dataf = dataf.append(build_data_frame(data2, [0]))
    dataf.index = [i for i in range(0, len(dataf))]
    dataf = dataf.reindex(numpy.random.permutation(dataf.index))
    # cPickle.dump(dataf, open("dataf.p", "wb"))
    print(len(dataf))
    train, test = splitsets(dataf, 0.8)
    # acc, pred = NB(dataf, 0.8)
    # for i in (test.split()):
    #     cur =
    # for i in range(0, len(test)):
    acc, pred = LG(train, test)
    print(acc)

    # for d in data[:2]:
    #     # d = alchemyapi.taxonomy("text", cor)
    #     # label = d['taxonomy'][0]['label']
    #     #know the weatherKW_5843 by the label
    #     # will be extraxted in real timE - TODO
    #
    #
    #
    #
    #
    #     KW = weatherKW_5843[d['showName']]
    #
    #     cor = d['text']
    #     corKW = d['keywords']
    #     # cor_KWrelevance = {x[u'text']: x[u'relevance'] for x in alchemyapi.keywords("text", cor)['keywords']}
    #     corwords = word_tokenize(d['text'])
    #     l_ngrams = add_ngrams(d['text'], n=2)# + add_ngrams(text, n=3)
    #
    #     r = re.compile(r'[\s{}]+'.format(re.escape(punctuation)))
    #     corlist = [w.lower() for w in corwords if w not in stop if len(w) > 2 if w not in exclude]
    #     p_cumm = []
    #     for i in range(0, len(corlist)-1):
    # #       p_per_w.append(computeP(KW, corwords[i-1:i], l_ngrams))
    #         p = computeP(KW, corlist[0:i], l_ngrams)
    #         # p = computeP(KW, corlist[0:i], l_ngrams)
    #         p_cumm.append(p)
    #         # print(corlist[i], p)
    #
    #     for i in range(1, len(cor.split())-1):
    # #       p_per_w.append(computeP(KW, corwords[i-1:i], l_ngrams))
    #         text = ' '.join(cor.split()[0:i])
    #         p, corKW = computeP2(KW, text)
    #         print(' '.join(cor.split()[1:i]))
    #         # p = computeP(KW, corlist[0:i], l_ngrams)
    #         p_cumm.append(p)
    #         print(corKW, p)
    #
    #     p = computeP2(KW, cor)
    #     p_cumm.append(p)
    #     print(corlist[-1], p)
    #     print("Total prob for %s element is %s\n  " % (i, p))
    #     p_cumm_D[j] = DataFrame({'corlist':corlist,'p_cumm':p_cumm}, columns=['corlist', 'p_cumm'])
    #     j=+1
    # cPickle.dump(p_cumm_D, open(str(j)+"p_cumm.p", "wb"))
    #
    #
    #
