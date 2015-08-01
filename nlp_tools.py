def tokening(text = ['']):
    from nltk.corpus import stopwords
    stop = stopwords.words('english')
    from nltk.tokenize import RegexpTokenizer

    tokenizer = RegexpTokenizer(r'\w+')
    # tokenizer = RegexpTokenizer(r'((?<=[^\w\s])\w(?=[^\w\s])|(\W))+', gaps=True)
    tokens = tokenizer.tokenize(text)
    return [t.lower() for t in tokens if t not in stop if len(t) > 1]

#ADD TRI&BIGRAMS
def add_ngrams(text, n=2):
    sixgrams = ngrams(text.split(), n)
    l_ngrams = []
    for grams in sixgrams:
        l_ngrams.append(' '.join(grams))
    return [unicode(l) for l in l_ngrams if l.find(',') == -1]
