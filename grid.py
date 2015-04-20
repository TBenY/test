__author__ = 'TalBY'

import nltk, cPickle, re, string, numpy
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression
from model import splitsets

def GS(train):
    from sklearn.pipeline import Pipeline
    text_lg = Pipeline([('count_vectorizer', CountVectorizer()),
                     ('logreg',  LogisticRegression())])

    targets = numpy.asarray(train['class'])
    text_lg.fit(numpy.asarray(train['text']), targets)


    from sklearn.grid_search import GridSearchCV
    parameters = {'count_vectorizer__ngram_range': [(1, 1), (1, 2), (1, 3)],
                  'count_vectorizer__min_df':[5,10,15],
                  'count_vectorizer__max_df':[0.5,.9,1],
                  'count_vectorizer__max_features':[3000,5000,7000] ,
                  'logreg__C': (1e-4, 1e4) }

    gs_logreg = GridSearchCV(text_lg, parameters, n_jobs=-1)
    gs_logreg.fit(numpy.asarray(train['text']), targets)

    best_parameters, score, _ = max(gs_logreg.grid_scores_, key=lambda x: x[1])
    for param_name in sorted(parameters.keys()):
        print("%s: %r" % (param_name, best_parameters[param_name]))


if __name__ == '__main__':
    dataf = cPickle.load(open("C:\Users\TalBY\PycharmProjects\AB\dataf.p", "rb"))
    train, test = splitsets(dataf, 0.99)
    GS(train)
