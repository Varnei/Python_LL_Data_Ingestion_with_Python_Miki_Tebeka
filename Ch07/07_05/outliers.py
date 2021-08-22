"""Using scikit-learn to detect ourliers"""
import pandas as pd
from sklearn.neighbors import LocalOutlierFactor

df = pd.read_csv('AAPL.csv')
print(df.columns)  # ['Symbol', 'Open', 'High', 'Low', 'Close', 'Volume']

# Find outliers in Volume

# Convert to numpy array in shape for LocalOutlierFactor
volume = df['Volume'].values.reshape(-1, 1)
print(volume)  # [[ 57327900] [100345700] [ 90862100] ...

# Create model & find outliers
clf = LocalOutlierFactor(contamination='auto')
vals = clf.fit_predict(volume)

# Get boolean mask
mask = (vals == -1)  # -1 is outlier

# Set values in outliers to mean Volume
df.loc[mask, 'Volume'] = df['Volume'].mean()
