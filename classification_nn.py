import keras
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import Dropout
from keras import regularizers
import numpy as np
import matplotlib.pyplot as plt


class LossAccuracyHistory(keras.callbacks.Callback):
    def on_train_begin(self, logs={}):
        self.loss = []
        self.acc = []
        self.val_loss = []
        self.val_acc = []

    def on_epoch_end(self, epoch, logs={}):
        self.loss.append(logs.get('loss'))
        self.acc.append(logs.get('acc'))
        self.val_loss.append(logs.get('val_loss'))
        self.val_acc.append(logs.get('val_acc'))


X = np.load("labels.npy")
X_train = X[:3000]
X_validation = X[3000:]

y = np.load("marker.npy")
y_train = y[:3000]
y_validation = y[3000:]

model = Sequential()
# model.add(Dense(128, activation='sigmoid', input_dim=X.shape[1]))
# model.add(Dense(100, activation='sigmoid', input_dim=X.shape[1]))
# model.add(Dropout(0.5))
model.add(Dense(64, activation='sigmoid', input_dim=X.shape[1]))
model.add(Dropout(0.8))
model.add(Dense(16, activation='sigmoid'))
# model.add(Dropout(0.8))
# model.add(Dense(32, activation='sigmoid'))
model.add(Dense(8, activation='sigmoid'))
# model.add(Dense(5, activation='sigmoid'))
# model.add(Dense(3, activation='sigmoid', kernel_regularizer=regularizers.l1(0.01)))
model.add(Dense(1, activation='sigmoid'))

RMSprop = keras.optimizers.RMSprop(lr=0.01)
# sgd = keras.optimizers.SGD(lr=0.001)
model.compile(loss='mse',
              optimizer=RMSprop,
              metrics=['accuracy'])

history = LossAccuracyHistory()
epoch_num = 500
model.fit(x=X_train, y=y_train, validation_split=0.2, batch_size=32, epochs=epoch_num, callbacks=[history])
train_score = model.evaluate(X_train, y_train, batch_size=32)
validation_score = model.evaluate(X_validation, y_validation, batch_size=32)
print train_score, validation_score

x = range(1, epoch_num+1)
y_loss = history.loss
y_val_loss = history.val_loss
y_acc = history.acc
y_val_acc = history.val_acc

plt.subplot(2, 1, 1)
plt.plot(x, y_loss)
plt.plot(x, y_val_loss)
# plt.yticks(np.arange(0, 0.6, 0.1))
plt.ylabel("loss")

plt.subplot(2, 1, 2)
plt.plot(x, y_acc)
plt.plot(x, y_val_acc)
plt.ylabel("accuracy")
plt.show()

