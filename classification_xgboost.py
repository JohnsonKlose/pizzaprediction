import numpy as np
import xgboost as xgb
from pandas import DataFrame
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix
from sklearn.model_selection import train_test_split
import seaborn as sns


def precision_and_recall(preds, dtrain):
    lab = dtrain.get_label()
    preds = [int(i >= 0.5) for i in preds]
    conf = confusion_matrix(lab, preds)
    precision = float(conf[0][0]) / float(conf[1][0]+conf[0][0])
    recall = float(conf[0][0]) / float(conf[0][1]+conf[0][0])
    return 'precision', precision


labels = np.load("./train/labels.npy")
markers = np.load("./train/marker.npy")
df = DataFrame(markers)
print df[0].value_counts()
# print np.cov(labels)
# sns.heatmap(labels, center=0)
# plt.show()

xTrain, xTest, yTrain, yTest = train_test_split(labels, markers, test_size=0.2, random_state=0)
# xTrain = labels[:3000]
# yTrain = markers[:3000]
# xTest = labels[3001:]
# yTest = markers[3001:]

data_train = xgb.DMatrix(xTrain, label=yTrain)
data_test = xgb.DMatrix(xTest, label=yTest)

# params = {
#     'booster': 'gbtree',
#     'max_depth': 20,
#     'min_child_weight': 5,
#     'gamma': 2.5,
#     'subsample': 0.6,
#     'colsample_bytree': 0.85,
#     'objective': 'binary:logistic',
#     'eval_metric': ['error', 'auc']
# }
params = {
    'booster': 'gbtree',
    'max_depth': 6,
    'min_child_weight': 5,
    'gamma': 0.05,
    'eta': 0.5,
    'objective': 'binary:logistic',
    'eval_metric': ['error', 'auc']
}
watchlist = [(data_test, 'eval'), (data_train, 'train')]
num_round = 500
evaluation_result = {}
bst = xgb.train(params, data_train, num_round, watchlist, feval=precision_and_recall, evals_result=evaluation_result)

x = range(1, num_round+1)
y_error = evaluation_result['train']['error']
y_eval_error = evaluation_result['eval']['error']
y_precision = evaluation_result['train']['precision']
y_eval_precision = evaluation_result['eval']['precision']

plt.subplot(2, 1, 1)
plt.plot(x, y_precision)
plt.plot(x, y_eval_precision)
# plt.yticks(np.arange(0, 0.6, 0.1))
plt.ylabel("precision")

plt.subplot(2, 1, 2)
plt.plot(x, y_error)
plt.plot(x, y_eval_error)
plt.ylabel("error")
plt.show()


# print "test error: " + str(evaluation_result['eval']['error'])
# print "test auc:" + str(evaluation_result['eval']['auc'])
# print "train error:" + str(evaluation_result['train']['error'])
# print "train auc:" + str(evaluation_result['train']['auc'])

# clf = xgb.XGBModel(objective='binary:logistic')
# clf.fit(xTrain, yTrain,
#         eval_set=[(xTrain, yTrain), (xTest, yTest)],
#         eval_metric='error')
# evals_result = clf.evals_result()
#
# print 'Access error metric directly from validation_0:' + str(evals_result['validation_0']['error'])
#
# print ''
# print 'Access metrics through a loop:'
# for e_name, e_mtrs in evals_result.items():
#     print '- {}'.format(e_name)
#     for e_mtr_name, e_mtr_vals in e_mtrs.items():
#         print '  -{}'.format(e_mtr_name)
#         print '    -{}'.format(e_mtr_vals)
#
# print ''
# print 'Access complete dict:'
# print evals_result