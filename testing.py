__author__ = 'TalBY'
import cPickle
from model import testing

dataf = cPickle.load(open("dataf.p", "rb"))
gs_logreg = cPickle.load(open("gs_logreg.p", "rb"))

#type the string
string = 'the bloomberg  weather: today is rainy'
string2 = 'i played basketball'
print(testing(string, gs_logreg))
print(testing(string2, gs_logreg))