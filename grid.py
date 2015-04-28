__author__ = 'TalBY'

import nltk, cPickle, re, string, numpy
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.linear_model import LogisticRegressionCV
from model import splitsets, testing
from sklearn.metrics import classification_report
from sklearn.linear_model import PassiveAggressiveClassifier
from sklearn.feature_extraction.text import TfidfVectorizer


def GS(train, test):

    from sklearn.pipeline import Pipeline
    text_lg = Pipeline((
        ('count_vectorizer', CountVectorizer(min_df=1, max_df=0.8)),
        # ('logreg',  LogisticRegressionCV(Cs=10, fit_intercept=True, cv=5))
        #  ('clf', PassiveAggressiveClassifier(C=1)),
        ('logreg', LogisticRegression(C=1e4)),
    ))
    # pipeline = Pipeline((
    #     ('vec', TfidfVectorizer(min_df=1, max_df=0.8, use_idf=True)),
    #     ('clf', PassiveAggressiveClassifier(C=1)),
    # ))

    targets = numpy.asarray(train['cl'])
    # text_lg.fit(numpy.asarray(train['text']), targets)


    from sklearn.grid_search import GridSearchCV
    parameters = {'count_vectorizer__ngram_range': [(1, 3), (1, 2), (1, 1)],
                  # 'count_vectorizer__min_df': numpy.linspace(1, 3,2),
                  'count_vectorizer__max_df' : [0.6, 0.7, 0.8, 0.9], #numpy.linspace(.7, .95, 4),
                  'count_vectorizer__max_features': [5000, 10000, 15000],
                  'logreg__C': [1e-2, 1,1e4]}
    # }

    gs_logreg = GridSearchCV(text_lg, parameters, n_jobs=-1, verbose=2, refit=True)
    _ = gs_logreg.fit(numpy.asarray(train['text']), targets)
    print('score:', gs_logreg.best_score_)
    best_parameters, score, _ = max(gs_logreg.grid_scores_, key=lambda x: x[1])
    for param_name in sorted(parameters.keys()):
        print("%s: %r" % (param_name, best_parameters[param_name]))

    predictions = gs_logreg.predict(numpy.asarray(test['text']))

    from sklearn.metrics import accuracy_score
    acc = accuracy_score(predictions, test['cl'])
    print('acc:', acc)
    print(classification_report(test['cl'],predictions))
    clf_name, clf = text_lg.steps[1]

    return predictions, gs_logreg



if __name__ == '__main__':
    dataf = cPickle.load(open("C:\Users\TalBY\PycharmProjects\AB\dataf.p", "rb"))
    train, test = splitsets(dataf, 0.8)
    predictions, gs_logreg = GS(train, test)
    assert (not(set(train.id) & set(test.id))== True), "duplicates"
    assert (not set(train.text) & set(test.text)== True), "duplicates"
    from sklearn.metrics import classification_report
    zipped = zip(test.text, predictions)

    with open('resultsfile.txt', 'w') as f:
        for i in zipped:
            f.writelines(str(i))
            f.writelines('\n')
            f.writelines('\n')
    f.close()
    # predictions = text_lg.predict(numpy.asarray(test['text']))
    #
    # from sklearn.metrics import accuracy_score
    # acc = accuracy_score(predictions, test['cl'])
    # print('acc:', acc)
    # print(classification_report(test['cl'],predictions))
                            # target_names=twenty_test_small.target_names))