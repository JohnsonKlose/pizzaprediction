# -*- coding: utf-8 -*-
import numpy as np
from sklearn.linear_model import Ridge
from sklearn.ensemble import RandomForestClassifier

X = np.load("./train/labels.npy")
y = np.load("./train/marker.npy")

# ridge = Ridge(alpha=.3)
# ridge.fit(X, y)
# coefs = ridge.coef_
# coefs = coefs.T
# names = ["X%s" % x for x in range(len(coefs))]
# lst = zip(coefs, names)
# lst = sorted(lst,  key=lambda t: -np.abs(t[0]))
# print lst

rf = RandomForestClassifier()
rf.fit(X, y)
names = ["X%s" % x for x in range(0, 130)]
print "Features sorted by their score:"
print sorted(zip(map(lambda x: round(x, 4), rf.feature_importances_), names),
             reverse=True)