__author__ = 'TalBY'
import pandas as pd
from pandas import DataFrame

###reading from text file:
import urllib, json

workfile = 'C:\Users\TalBY\Downloads\ListofIDs.txt'
classification = [0]
data_frame = DataFrame({'text': [], 'class': []})
with open(workfile) as f:
    lines = f.readlines()
for id in lines:
    url = "".join(['http://storageaudiobursts.blob.core.windows.net/nlp/',id.replace('\r','').replace('\n',''),'.json' ])
    # print(url)
    response = urllib.urlopen(url)
    data = json.loads(response.read())
    data_frame = data_frame.append(DataFrame({'text': data['text'], 'class': classification, 'id':id}))
print(len(lines))
print(len(data_frame))

