import pandas as pd
import os
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"   # see issue #152
import tensorflow as tf


df = pd.read_csv('data_gazering/data/DATASETS.csv')
print(df.columns)
df.drop('Unnamed: 0', inplace=True, axis=1)


for index, row in df.iterrows():
    df['features'][index] = [float(x) for x in row['features'][1:-1].split(', ')]
    df['predict'][index] = [float(x) for x in row['predict'][1:-1].split(', ')]

print(len(df['features'][0]))
print(len(df['predict'][0]))





