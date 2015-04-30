__author__ = 'TalBY'
import cPickle
from model import testing

dataf = cPickle.load(open("dataf.p", "rb"))
gs_logreg = cPickle.load(open("gs_logreg.p", "rb"))
print(testing('tal', gs_logreg))