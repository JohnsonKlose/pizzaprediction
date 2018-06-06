# -*- coding: utf-8 -*-
import numpy as np
import xgboost as xgb
from pandas import DataFrame
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix
from sklearn.model_selection import train_test_split


# 计算精度和召回率
def precision_and_recall(preds, dtrain):
    lab = dtrain.get_label()
    preds = [int(i >= 0.5) for i in preds]
    conf = confusion_matrix(lab, preds)
    precision = float(conf[0][0]) / float(conf[1][0]+conf[0][0])
    recall = float(conf[0][0]) / float(conf[0][1]+conf[0][0])
    return 'precision', precision


labels = np.load("./train/labels.npy")
labels_train = labels[:3000]
labels_test = labels[3000:]
markers = np.load("./train/marker.npy")
marker_train = markers[:3000]
marker_test = markers[3000:]

df = DataFrame(markers)
print df[0].value_counts()

# 交叉验证分割数据
xTrain, xValidation, yTrain, yValidation = train_test_split(labels_train, marker_train, test_size=0.2, random_state=0)
data_train = xgb.DMatrix(xTrain, label=yTrain)
data_validation = xgb.DMatrix(xValidation, label=yValidation)
data_test = xgb.DMatrix(labels_test, label=marker_test)

params = {
    'booster': 'gbtree',
    'max_depth': 18,
    'scale_pos_weight': 0.8,
    # 'min_child_weight': 1,
    # 'gamma': 0.05,
    'eta': 0.5,
    'objective': 'binary:logistic',
    'eval_metric': ['error', 'auc']
}
watchlist = [(data_validation, 'eval'), (data_train, 'train')]
num_round = 500
evaluation_result = {}
bst = xgb.train(params, data_train, num_round, watchlist, feval=precision_and_recall, evals_result=evaluation_result)
marker_predict = bst.predict(data_test)
marker_predict = np.where(marker_predict > 0.5, 1, 0)
conf = confusion_matrix(marker_test, marker_predict)
precision_test = float(conf[0][0]) / float(conf[1][0] + conf[0][0])
recall_test = float(conf[0][0]) / float(conf[0][1]+conf[0][0])
print precision_test, recall_test
f_score = bst.get_fscore()
print sorted(f_score.iteritems(), key=lambda d: d[1], reverse=True)

x = range(1, num_round+1)
y_error = evaluation_result['train']['error']
y_eval_error = evaluation_result['eval']['error']
y_precision = evaluation_result['train']['precision']
y_eval_precision = evaluation_result['eval']['precision']

plt.subplot(2, 1, 1)
plt.plot(x, y_precision)
plt.plot(x, y_eval_precision)
plt.ylabel("precision")

plt.subplot(2, 1, 2)
plt.plot(x, y_error)
plt.plot(x, y_eval_error)
plt.ylabel("error")
plt.show()