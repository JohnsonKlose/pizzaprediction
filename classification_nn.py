# -*- coding: utf-8 -*-
import keras
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import Dropout
import numpy as np
import matplotlib.pyplot as plt


# 损失和精度的计算函数
class LossAccuracyHistory(keras.callbacks.Callback):
    # 训练开始时定义存储变量
    def on_train_begin(self, logs={}):
        self.loss = []
        self.acc = []
        self.val_loss = []
        self.val_acc = []

    #  每个训练epoch结束后将结果存入变量
    def on_epoch_end(self, epoch, logs={}):
        self.loss.append(logs.get('loss'))
        self.acc.append(logs.get('acc'))
        self.val_loss.append(logs.get('val_loss'))
        self.val_acc.append(logs.get('val_acc'))


X = np.load("train/labels.npy")
X_train = X[:3000]
X_test = X[3000:]

y = np.load("train/marker.npy")
y_train = y[:3000]
y_test = y[3000:]

model = Sequential()
model.add(Dense(64, activation='sigmoid', input_dim=X.shape[1]))
model.add(Dropout(0.8))
model.add(Dense(16, activation='sigmoid'))
model.add(Dense(8, activation='sigmoid'))
model.add(Dense(1, activation='sigmoid'))

sgd = keras.optimizers.SGD(lr=0.001)
model.compile(loss='mse',
              optimizer=sgd,
              metrics=['accuracy'])

history = LossAccuracyHistory()
epoch_num = 100
model.fit(x=X_train, y=y_train, validation_split=0.2, batch_size=32, epochs=epoch_num, callbacks=[history])
train_score = model.evaluate(X_train, y_train, batch_size=32)
validation_score = model.evaluate(X_test, y_test, batch_size=32)
print train_score, validation_score

x = range(1, epoch_num+1)
y_loss = history.loss
y_val_loss = history.val_loss
y_acc = history.acc
y_val_acc = history.val_acc

plt.subplot(2, 1, 1)
plt.plot(x, y_loss)
plt.plot(x, y_val_loss)
plt.ylabel("loss")

plt.subplot(2, 1, 2)
plt.plot(x, y_acc)
plt.plot(x, y_val_acc)
plt.ylabel("accuracy")
plt.show()

