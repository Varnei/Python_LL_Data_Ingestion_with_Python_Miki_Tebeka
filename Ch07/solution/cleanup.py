"""Clean ride times"""

import sqlite3

import pandas as pd


conn = sqlite3.connect('rides.db', detect_types=sqlite3.PARSE_DECLTYPES)
df = pd.read_sql('SELECT * FROM rides', conn)
df['duration'] = df['tpep_dropoff_datetime'] - df['tpep_pickup_datetime']
print('min:', df['duration'].min(), 'max:', df['duration'].max())

df = df[df['duration'] > pd.Timedelta('1m')]
mask = df['duration'] > pd.Timedelta('5h')
df.loc[mask, 'duration'] = df['duration'].median()
print('min:', df['duration'].min(), 'max:', df['duration'].max())
