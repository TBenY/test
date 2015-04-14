__author__ = 'TalBY'

import nltk, cPickle, re, string
from nltk.util import ngrams
from nltk import word_tokenize
from string import punctuation
from nltk.corpus import stopwords
from alchemyapi import AlchemyAPI

exclude = set(string.punctuation)
stop = stopwords.words('english')
alchemyapi = AlchemyAPI()


# cor = "Greater, taken they're spending make higher, it'll on one hand, to, people more if they go outside of their particular provider network putting, people that had no coverage, more affordable, population I think we're going to continue is going to be, to try and make people well obviously I'm what the weather healthcare cost go up rapidly or not is going to depend on how we can control cause going forward what strategies are out there that we're using or or should be using to keep spending growth low, well that's actually true in fact I think the way you phrase that is important."
# d = alchemyapi.taxonomy("text", cor)
# label = d['taxonomy'][0]['label']
# corwords = word_tokenize(cor)
# cor_KWrelevance = {x[u'text']: x[u'relevance'] for x in alchemyapi.keywords("text", cor)['keywords']}

# freqd = cPickle.load(open("freqd.p", "rb"))# freq is weather class for all
# def computeP(freqd, KWrelevance ):
# '''freqd is a dict of words freq for a given class
#     cor is a corpus text
#     '''
#     both = set(freqd.keys()) & set(KWrelevance.keys())
#     probs = [freqd[w] for w in both]
#     return sum(probs)

# computeP(freqd, cor_KWrelevance.keys() )
weatherKW_5843 = cPickle.load(open("weatherKW_5843.p", "rb"))


def add_singles(weatherKW_5843, showname):
    # showname = u'Bloomberg Surveillance'
    KW = [i for i in weatherKW_5843[showname] if i not in stop]
    KWl = []
    for i in KW:
        splitted = i.split()
        for j in range(0, len(splitted)):
            KWl.append(splitted[j])
    return KW.extend(KWl)


# KW = cor_KWrelevance.keys()
def computeP(KW, corlist, l_ngrams):
    '''weather is a list of words  for a given class
    cor is a corpus text
    '''

    both = set(corlist) & set(KW)
    bothn = set(l_ngrams) & set(KW)
    both.update(bothn)
    probs = [1 for w in both]
    if len(corlist) < 1:
        return -1
    elif sum(probs) / float(len(corlist)) > 1:
        print(len(corlist))
    else:
        return sum(probs) / float(len(corlist))


def computeP2(KW, cor):
    '''weather is a list of words  for a given class
    cor is a corpus text
    '''
    alchemyapi = AlchemyAPI()
    corKW = alchemyapi.keywords("text", cor)
    # corKW = corKW['keywords']
    both = set(corKW) & set(KW)
    if both==set([]):
        return 0, []
    probs = [1 for w in both]
    if len(corKW) < 1:
        return -1, []
    elif probs == []:
        return 0
    elif 1 < sum(probs) / float(len(corKW)):
        print('ERROR', len(corKW))
    else:
        return sum(probs) / float(len(corKW)), corKW


#ADD TRI&BIGRAMS
def add_ngrams(text, n=2):
    sixgrams = ngrams(text.split(), n)
    l_ngrams = []
    for grams in sixgrams:
        l_ngrams.append(' '.join(grams))
    return [unicode(l) for l in l_ngrams if l.find(',') == -1]


# corwords = ''.join(ch for ch in corwords if ch not in exclude)
# if __name__== '__main__':
#     # showname = d[u'showName']#ie u'Bloomberg Surveillance'
#     weatherKW_5843 = cPickle.load(open("weatherKW_5843.p", "rb"))
#
#     l_ngrams = add_ngrams(cor, n=2)# + add_ngrams(text, n=3)
#     p = computeP(KW, corwords, l_ngrams)
#     print(p)

### to run on a stream of words need to change the function







