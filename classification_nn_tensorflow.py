import numpy as np
import pandas as pd
import tensorflow as tf
import math
from sklearn import metrics
from matplotlib import pyplot as plt


def construct_feature_columns(input_features):
    return set([tf.feature_column.numeric_column(my_feature) for my_feature in input_features])


def my_input_fn(features, targets, batch_size=1, shuffle=True, num_epochs=None):
    features = {key: np.array(value) for key, value in dict(features).items()}

    ds = tf.data.Dataset.from_tensor_slices((features, targets))
    # ds = tf.python.data.Dataset.from_tensor_slices((features, targets))
    ds = ds.batch(batch_size).repeat(num_epochs)

    if shuffle:
        ds = ds.shuffle(10000)

    features, labels = ds.make_one_shot_iterator().get_next()
    return features, labels


def train_nn_classification_model(
        learning_rate,
        steps,
        batch_size,
        hidden_units,
        training_examples,
        training_targets,
        validation_examples,
        validation_targets):

    periods = 10
    steps_per_period = steps/periods
    feature_columns = []
    for i in range(0, 130):
        feature_columns.append(i)
    my_optimizer = tf.train.GradientDescentOptimizer(learning_rate=learning_rate)
    my_optimizer = tf.contrib.estimator.clip_gradients_by_norm(my_optimizer, 5.0)
    dnn_classification = tf.estimator.DNNClassifier(
        feature_columns=construct_feature_columns(training_examples),
        hidden_units=hidden_units,
        optimizer=my_optimizer
    )

    training_input_fn = lambda: my_input_fn(training_examples,
                                            training_targets,
                                            batch_size=batch_size)
    predict_training_input_fn = lambda: my_input_fn(training_examples,
                                                    training_targets,
                                                    num_epochs=1,
                                                    shuffle=False)
    predict_validation_input_fn = lambda: my_input_fn(validation_examples,
                                                      validation_targets,
                                                      num_epochs=1,
                                                      shuffle=False)

    print "Training model..."
    print "RMSE (on training data):"
    training_rmse = []
    validation_rmse = []
    for period in range(0, periods):
        dnn_classification.train(input_fn=training_input_fn,
                                 steps=steps_per_period)
        training_predictions = dnn_classification.predict(input_fn=predict_training_input_fn)
        training_predictions = np.array([item['predictions'][0] for item in training_predictions])

        validation_predictions = dnn_classification.predict(input_fn=predict_validation_input_fn)
        validation_predictions = np.array([item['predictions'][0] for item in validation_predictions])

        training_root_mean_squared_error = math.sqrt(
            metrics.mean_squared_error(training_predictions, training_targets))
        validation_root_mean_squared_error = math.sqrt(
            metrics.mean_squared_error(validation_predictions, validation_targets))
        print " period %02d : %0.2f" % (period, training_root_mean_squared_error)
        print "Model training finished."

        plt.ylabel("RMSE")
        plt.xlabel("Periods")
        plt.title("Root Mean Squared Error vs. Periods")
        plt.tight_layout()
        plt.plot(training_rmse, label="training")
        plt.plot(validation_rmse, label="validation")

        print "Final RMSE (on training data):    %0.2f" % training_root_mean_squared_error
        print "Final RMSE (on validation data):  %0.2f" % validation_root_mean_squared_error

        return dnn_classification


if __name__ == '__main__':
    X = np.load("labels.npy")
    X_train = X[:3000]
    X_validation = X[3000:]
    X_train = pd.DataFrame(X_train)
    X_validation = pd.DataFrame(X_validation)
    y = np.load("marker.npy")
    y_train = y[:3000]
    y_validation = y[3000:]
    y_train = pd.DataFrame(y_train)
    y_validation = pd.DataFrame(y_validation)
    _ = train_nn_classification_model(
        learning_rate=0.01,
        steps=500,
        batch_size=10,
        hidden_units=[10, 2],
        training_examples=X_train,
        training_targets=y_train,
        validation_examples=X_validation,
        validation_targets=y_validation)