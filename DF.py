import pandas as pd
from pandas import DataFrame
import nltk

def build_data_frame(data, classification):
    data_frame = DataFrame({'text': [], 'class': []})
    for d in data:
        # text = tokening(d['text'])
        # data_frame = data_frame.append(DataFrame({'text': [text], 'class': classification}))
        data_frame = data_frame.append(DataFrame({'text': d['text'], 'class': classification}))
    return data_frame

# dataf = DataFrame({'text': [], 'class': []})
# dataf = build_data_frame(data, [1])


def tokening(text = ['']):
    from nltk.corpus import stopwords
    stop = stopwords.words('english')
    from nltk.tokenize import RegexpTokenizer

    tokenizer = RegexpTokenizer(r'\w+')
    # tokenizer = RegexpTokenizer(r'((?<=[^\w\s])\w(?=[^\w\s])|(\W))+', gaps=True)
    tokens = tokenizer.tokenize(text)
    return [t.lower() for t in tokens if t not in stop if len(t) > 1]