__author__ = 'TalBY'

import nltk, cPickle, re, string, pandas
import numpy as np
from pandas import DataFrame
from nltk.util import ngrams
from nltk import word_tokenize
from string import punctuation
from nltk.corpus import stopwords
# from alchemyapi import AlchemyAPI
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.pipeline import Pipeline
exclude = set(string.punctuation)
stop = stopwords.words('english')
from sklearn import linear_model
# alchemyapi = AlchemyAPI()


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
##NB
def NB(dataf, ratio):
    """
    :ratio train test ratio
    :param dataf: DATAFRAME of class and tokems to train
    :return: predictions for test data
        """
    import numpy
    from sklearn.naive_bayes import MultinomialNB
    idx = int(ratio*len(dataf))
    train = dataf[:idx]
    test = dataf[idx:]
    count_vectorizer = CountVectorizer()
    counts = count_vectorizer.fit_transform(numpy.asarray(train['text']))


    classifier = MultinomialNB()
    targets = numpy.asarray(train['cl'])
    classifier.fit(counts, targets)
    example_counts = count_vectorizer.transform(test['text'])
    predictions = classifier.predict(example_counts)

    from sklearn.metrics import accuracy_score
    accuracy_score(predictions, test['cl'])

    return accuracy_score(predictions, test['cl']), predictions


def splitsets(dataf, ratio):
    # idx = int(ratio*len(dataf))
    msk = np.random.rand(len(dataf)) < ratio
    # train = dataf[:idx]
    # test = dataf[idx:]
    train = dataf[msk]
    test = dataf[~msk]
    assert (not(set(train.id) & set(test.id))== True), "duplicates"
    assert (not set(train.text) & set(test.text)== True), "duplicates"

    return train, test



def LG(train, test):
    """
    :ratio train test ratio
    :param dataf: DATAFRAME of class and tokems to train
    :return: predictions for test data
        """

    pipeline = Pipeline((
        ('vec', CountVectorizer( min_df=5, max_df=.95, max_features=10000, ngram_range=(1, 1))),
        # ('clf', PassiveAggressiveClassifier(C=1)),
        ('clf', linear_model.LogisticRegression(C=1e4)),
    ))

    # counts = count_vectorizer.fit_transform(np.asarray(train['text']))
    targets = np.asarray(train['cl'])
    # vocab = np.array(count_vectorizer.get_feature_names())
    # logreg = linear_model.LogisticRegression(C=1e4)# the smaller the bigger the regularization
    pipeline.fit(np.asarray(train['text']), targets)
    predictions = pipeline.predict(np.asarray(test['text']))

    from sklearn.metrics import accuracy_score
    accuracy_score(predictions, test['cl'])

    return accuracy_score(predictions, test['cl']), predictions


def testing(test, pipeline):
    if type(test)== string:
        pipeline.predict(test)
    elif type(test)== DataFrame:
        return pipeline.predict(np.asarray(test['text']))


def LGcv(train, test):
#          """
    from sklearn.linear_model import LogisticRegressionCV
    from sklearn.metrics import log_loss
    from sklearn.cross_validation import cross_val_score
    from scipy.stats import sem

    # pipeline = Pipeline((
    #     ('vec', CountVectorizer( min_df=5, max_df=.95, max_features=5000, ngram_range=(1, 2)),
    #      ('lg', linear_model.LogisticRegression(C=1e4)))
    # ))
    pipeline = Pipeline((
    ('vec', CountVectorizer( min_df=5, max_df=.95, max_features=5000, ngram_range=(1, 2))),
    ('lg', linear_model.LogisticRegression(C=1e4)),
    ))

    targets = np.asarray(train['cl'])
    scores = cross_val_score(pipeline, np.asarray(train['text']),
                         targets, cv=3, n_jobs=-1)

    print(scores.mean(), 'std:' , sem(scores))
    return
    # model_regression = LogisticRegressionCV(Cs=10, fit_intercept=True, cv=5)
    # model_regression.fit()

#     from sklearn import LogisticRegression
#     count_vectorizer =  CountVectorizer( min_df=5, max_df=1, max_features=5000, ngram_range=(1, 2))
#     counts = count_vectorizer.fit_transform(np.asarray(train['text']))
#     targets = np.asarray(train['class'])
#
#     from sklearn.cross_validation import cross_val_score
#
#     logreg = LogisticRegression(C=1)
#     scores = cross_val_score(logreg, counts, targets, cv=5, scoring='accuracy')
#     print("Logistic Regression CV scores:")
#     print("min: {:.3f}, mean: {:.3f}, max: {:.3f}".format(scores.min(), scores.mean(), scores.max()))
#
#     testdata = count_vectorizer.transform(np.asarray(test['text']))
#     predictions = logreg.predict(testdata)
#
#     from sklearn.metrics import accuracy_score
#     accuracy_score(predictions, test['class'])
#
#     return accuracy_score(predictions, test['class']), predictions


# from __future__ import print_function
import sklearn
from sklearn import datasets
from sklearn.cross_validation import train_test_split
from sklearn.grid_search import GridSearchCV
from sklearn.metrics import classification_report
from sklearn.svm import SVC


# sklearn.linear_model.LogisticRegressionCV(Cs=10, fit_intercept=True, cv=None, dual=False, penalty='l2', scoring=None, solver='lbfgs', tol=0.0001, max_iter=100, class_weight=None, n_jobs=1, verbose=0, refit=True, intercept_scaling=1.0, multi_class='ovr'
# parameters = {'kernel':('linear', 'rbf'), 'C':[1, 10]}
# svr = svm.SVC()
# clf = grid_search.GridSearchCV(svr, parameters)
# param_grid = [
#   {'C': [1, 10, 100, 1000], 'kernel': ['linear']},
#   {'C': [1, 10, 100, 1000], 'gamma': [0.001, 0.0001], 'kernel': ['rbf']},
#  ]

#
# def computeP2(KW, cor):
#     '''weather is a list of words  for a given class
#     cor is a corpus text
#     '''
#     alchemyapi = AlchemyAPI()
#     corKW = alchemyapi.keywords("text", cor)
#     # corKW = corKW['keywords']
#     both = set(corKW) & set(KW)
#     if both==set([]):
#         return 0, []
#     probs = [1 for w in both]
#     if len(corKW) < 1:
#         return -1, []
#     elif probs == []:
#         return 0
#     elif 1 < sum(probs) / float(len(corKW)):
#         print('ERROR', len(corKW))
#     else:
#         return sum(probs) / float(len(corKW)), corKW
#


from sklearn.cross_validation import train_test_split


if __name__ == '__main__':
    dataf = cPickle.load(open("C:\Users\TalBY\PycharmProjects\AB\dataf.p", "rb"))
    train, test = splitsets(dataf, 0.8)
    # acc, pred = NB(dataf, 0.8)
    # for i in (test.split()):
    #     cur =
    # for i in range(0, len(test)):

    # acc, pred = LG(train, test)
    # print(acc)
    # LGcv(train, test)
    acc, predictions = LG(train, test)
    # acc, pred = testing(test, logreg)

    print(acc)

    zipped = zip(test.text, predictions)
    with open('resultsfile.txt', 'w') as f:
        for i in zipped:
            f.writelines(str(i))
            f.writelines('\n')
            f.writelines('\n')
    f.close()

