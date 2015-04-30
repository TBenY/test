__author__ = 'TalBY'

    # for d in data[:2]:
    #     # d = alchemyapi.taxonomy("text", cor)
    #     # label = d['taxonomy'][0]['label']
    #     #know the weatherKW_5843 by the label



    #     KW = weatherKW_5843[d['showName']]
    #
    #     cor = d['text']
    #     corKW = d['keywords']
    #     # cor_KWrelevance = {x[u'text']: x[u'relevance'] for x in alchemyapi.keywords("text", cor)['keywords']}
    #     corwords = word_tokenize(d['text'])
    #     l_ngrams = add_ngrams(d['text'], n=2)# + add_ngrams(text, n=3)
    #
    #     r = re.compile(r'[\s{}]+'.format(re.escape(punctuation)))
    #     corlist = [w.lower() for w in corwords if w not in stop if len(w) > 2 if w not in exclude]
    #     p_cumm = []
    #     for i in range(0, len(corlist)-1):
    # #       p_per_w.append(computeP(KW, corwords[i-1:i], l_ngrams))
    #         p = computeP(KW, corlist[0:i], l_ngrams)
    #         # p = computeP(KW, corlist[0:i], l_ngrams)
    #         p_cumm.append(p)
    #         # print(corlist[i], p)
    #
    #     for i in range(1, len(cor.split())-1):
    # #       p_per_w.append(computeP(KW, corwords[i-1:i], l_ngrams))
    #         text = ' '.join(cor.split()[0:i])
    #         p, corKW = computeP2(KW, text)
    #         print(' '.join(cor.split()[1:i]))
    #         # p = computeP(KW, corlist[0:i], l_ngrams)
    #         p_cumm.append(p)
    #         print(corKW, p)
    #
    #     p = computeP2(KW, cor)
    #     p_cumm.append(p)
    #     print(corlist[-1], p)
    #     print("Total prob for %s element is %s\n  " % (i, p))
    #     p_cumm_D[j] = DataFrame({'corlist':corlist,'p_cumm':p_cumm}, columns=['corlist', 'p_cumm'])
    #     j=+1
    # cPickle.dump(p_cumm_D, open(str(j)+"p_cumm.p", "wb"))