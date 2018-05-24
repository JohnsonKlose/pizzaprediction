# -*- coding: utf-8 -*-
import jieba
from data_clean import return_data
from collections import Counter
import numpy as np
import sys
import pandas as pd
from make_labels import *
from draw_plot import draw_word_cloud
import seaborn as sns
import matplotlib.pyplot as plt


reload(sys)
sys.setdefaultencoding('utf-8')

data_all = return_data()
words = []


def cut(name, des):
    to_cut = ''
    if des == ' ' or des is np.nan:
        to_cut = name
    else:
        to_cut = des
    se = jieba_cut(to_cut)
    words.extend(se)
    return ",".join(se)


def jieba_cut(word):
    s = jieba.cut(word)
    s = [word.encode('utf-8') for word in list(s)]
    stoplist = {}.fromkeys([line.strip() for line in open("./stopwords.txt")])
    segs = [word for word in list(s) if word not in stoplist]
    return segs


data_all['cut'] = data_all.apply(lambda row: cut(row['item_name'], row['item_description']), axis=1)
print data_all
labels_np, marker_np = make_labels(data_all['cut'], data_all['shop_food_score'], data_all['item_rating'])
print labels_np.shape, marker_np.shape
np.save("./train/labels.npy", labels_np)
np.save("./train/marker.npy", marker_np)

# value = dict(Counter(words))
# value_sorted = sorted(value.items(), lambda x, y: cmp(x[1], y[1]), reverse=True)
#
# draw_word_cloud(value)


# for i in range(0, len(value_sorted)):
#     k, v = value_sorted[i]
#     if v > 5:
#         print str(i+1) + ':' + str(k) + 'number is ' + str(v)
#     else:
#         break