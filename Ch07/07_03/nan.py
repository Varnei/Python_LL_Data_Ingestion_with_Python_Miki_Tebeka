"""Working with nan"""
import pandas as pd

val = float('nan')  # also np.nan
print(val)  # nan

print(val == float('nan'))  # False
print(val == val)  # False

print(pd.isnull(val))  # True

values = pd.Series([1.2, 2.3, float('nan'), 4.5])
# pd.isnull is a ufunc
print(pd.isnull(values))   # [False, False, True, False]
