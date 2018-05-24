import numpy as np
import xgboost as xgb
from pandas import DataFrame
import matplotlib.pyplot as plt
import seaborn as sns


labels = np.load("./train/labels.npy")
markers = np.load("./train/marker.npy")
# df = DataFrame(labels)
# print np.cov(labels)
# sns.heatmap(labels, center=0)
# plt.show()

xTrain = labels[:3000]
yTrain = markers[:3000]
xTest = labels[3001:]
yTest = markers[3001:]

data_train = xgb.DMatrix(xTrain, label=yTrain)
data_test = xgb.DMatrix(xTest, label=yTest)

params = {
    'booster': 'gbtree',
    'max_depth': 10,
    'eta': 1,
    'objective': 'binary:logistic',
    'eval_metric': ['error', 'auc']
}
watchlist = [(data_test, 'eval'), (data_train, 'train')]
num_round = 200
evaluation_result = {}
bst = xgb.train(params, data_train, num_round, watchlist, evals_result=evaluation_result)

print "test error: " + str(evaluation_result['eval']['error'])
print "test auc:" + str(evaluation_result['eval']['auc'])
print "train error:" + str(evaluation_result['train']['error'])
print "train auc:" + str(evaluation_result['train']['auc'])

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