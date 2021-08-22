"""Using Pandas to work with databases"""
import sqlite3

import pandas as pd

conn = sqlite3.connect('rides.db', detect_types=sqlite3.PARSE_DECLTYPES)

# What's the average ride distance for VeriFone?
params = {
    'vendor': 'VeriFone',
}
sql = 'SELECT distance FROM rides WHERE vendor = :vendor'

df = pd.read_sql(sql, conn, params=params)
avg_distance = df['distance'].mean()
print(f'average distance: {avg_distance:.2f}miles')
