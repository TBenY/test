__author__ = 'TalBY'

import nltk, cPickle, re, string, numpy
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.linear_model import LogisticRegressionCV
from model import splitsets
from sklearn.linear_model import PassiveAggressiveClassifier
from sklearn.feature_extraction.text import TfidfVectorizer


def GS(train, test):
    from sklearn.pipeline import Pipeline
    text_lg = Pipeline([('count_vectorizer', CountVectorizer()),
                        ('logreg',  LogisticRegressionCV(Cs=10, fit_intercept=True, cv=5))])
    pipeline = Pipeline((
        ('vec', TfidfVectorizer(min_df=1, max_df=0.8, use_idf=True)),
        ('clf', PassiveAggressiveClassifier(C=1)),
    ))

    targets = numpy.asarray(train['cl'])
    # text_lg.fit(numpy.asarray(train['text']), targets)


    from sklearn.grid_search import GridSearchCV
    parameters = {'count_vectorizer__ngram_range': [(1, 3), (1, 2), (1, 1)],
                  'count_vectorizer__min_df': numpy.linspace(1, 9, 4),
                  'count_vectorizer__max_df' : numpy.linspace(.7, .95,4),
                  'count_vectorizer__max_features': [10000, 15000, 17000],
                  # 'logreg__C': [1e4]}
    }


#
#     parameters = {
#     #'vec__min_df': [1, 2],
#     'vec__max_df': [0.8, 1.0],
#     'vec__ngram_range': [(1, 1), (1, 2)],
#     'vec__use_idf': [True, False],
# }

    # gs = GridSearchCV(pipeline, parameters, verbose=2, refit=False)
    # _ = gs.fit(twenty_train_small.data, twenty_train_small.target)

    gs_logreg = GridSearchCV(text_lg, parameters, n_jobs=-1)
    _ = gs_logreg.fit(numpy.asarray(train['text']), targets)
    print(gs_logreg.best_score_)
    print(gs_logreg.best_params_)

    best_parameters, score, _ = max(gs_logreg.grid_scores_, key=lambda x: x[1])
    for param_name in sorted(parameters.keys()):
        print("%s: %r" % (param_name, best_parameters[param_name]))

    predictions = gs_logreg.predict(numpy.asarray(test['text']))

    from sklearn.metrics import accuracy_score
    acc = accuracy_score(predictions, test['cl'])
    print(acc)
    return accuracy_score(predictions, test['cl']), predictions



if __name__ == '__main__':
    dataf = cPickle.load(open("C:\Users\TalBY\PycharmProjects\AB\dataf.p", "rb"))
    train, test = splitsets(dataf, 0.9)
    GS(train)
