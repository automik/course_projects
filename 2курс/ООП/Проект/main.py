import pandas as pd
import os
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"   # Ограничение на использование графического процессора
from tensorflow import keras
from tensorflow.keras import layers
from sklearn.model_selection import train_test_split
import numpy as np


class Network:
    def __init__(self, dataframe):
        self.features = np.empty((0, len([float(x) for x in df['features'][0][1:-1].split(', ')])), int)
        self.predict = np.empty((0, len([float(x) for x in df['predict'][0][1:-1].split(', ')])), int)

        for index, row in dataframe.iterrows():
            self.features = np.vstack(
                (self.features, np.asarray([float(x) for x in row['features'][1:-1].split(', ')]).astype(np.float32)))
            self.predict = np.vstack(
                (self.predict, np.asarray([float(x) for x in row['predict'][1:-1].split(', ')]).astype(np.float32)))

        self.x_train, self.x_test, self.y_train, self.y_test = train_test_split(self.features, self.predict,
                                                                                test_size=0.1)
        self.model = None

    def initialise_model(self):
        self.model = keras.Sequential([
            layers.InputLayer(input_shape=(len(self.x_train[0]),)),
            layers.Dense(10, activation=keras.activations.tanh),
            layers.Dense(10, activation=keras.activations.tanh),
            layers.Dense(len(self.y_train[0]), activation=keras.activations.sigmoid)
        ])
        self.model.compile(loss='mse', optimizer=keras.optimizers.Adam(0.1),  metrics=['mse', 'mae', 'mape'])

    def fit_model(self):
        return self.model.fit(self.x_train, self.y_train, epochs=50, verbose=1)

    def test_model(self):
        return self.model.evaluate(self.x_test, self.y_test, verbose=1)


df = pd.read_csv('data_gazering/data/DATASETS.csv')

network = Network(df)
network.initialise_model()
history = network.fit_model()
result = network.test_model()
print(result)
print(f'Loss: {result[0]}, mse: {result[1]}, mae: {result[2]}, mape: {result[3]}')
