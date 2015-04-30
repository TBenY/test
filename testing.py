__author__ = 'TalBY'

import urllib, json, nltk
url = "http://api.audioburst.com/search?value=Weather&top=10000"
url2 = "http://api.audioburst.com/Search/history?value=Weather&top=10000"
response = urllib.urlopen(url)
data = json.loads(response.read())
# print len(data.values()[0])
def getdata(url):
    response = urllib.urlopen(url);
    data = json.loads(response.read())
    print len(data.values()[1])
    return data.values()[1]

data = getdata(url)
d2 = getdata(url2)
# # data = data+d2


print(len(data))