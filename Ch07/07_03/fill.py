"""Filling missing data"""
import numpy as np
import pandas as pd

values = pd.Series([1., 2., np.nan, 4., 5., np.nan, 7.0])

# fillna will fill na with a given value
# fillna will return a new Series (use inplace=True to mutate the object)
print(values.fillna(5.))  # [1, 2, 5, 4, 5, 5, 7]

# You can use computed value
avg = values.mean()  # mean is "nan aware"
print(values.fillna(avg))  # [1, 2, 3.8, 4, 5, 3.8, 7]

# interpolate will fill values with linear interpolation by default
# fillna will return a new Series (use inplace=True to mutate the object)
print(values.interpolate())  # [1, 2, 3, 4, 5, 6, 7]
