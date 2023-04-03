'''
@Author: Yuan Yang
@Email: yangy7@sustech.edu.cn
'''
# rsup: Sales from quarter t minus sales from quarter t − 1 divided by quarter-end market capitalization.
# 'C001001000': Cash Received from Sales of Goods or Rendering of Services
# 'Msmvttl' : size
import numpy as np
def equation(x):
    x['rsup'] = (x['C001001000'] - x['C001001000'].shift(3)) / x['Msmvttl']
    return x
#
def fill_0(x):
    x.replace([0,], np.nan, inplace = True)
    x.fillna(method='ffill', inplace=True)
    return x
#
def lag_one_month(x):
    x = x.copy()
    x['rsup'] = x['rsup'].shift()
    return x

def calculation(df_input):
    df_output = df_input['monthly'][['stkcd','month', 'Msmvttl', 'C001001000']]
    df_output = df_output.groupby('stkcd').apply(equation).reset_index(drop=True)
    df_output = df_output.groupby('stkcd').apply(fill_0).reset_index(drop=True)
    df_output = df_output[['stkcd', 'month', 'rsup']]
    df_output = df_output.groupby('stkcd').apply(lag_one_month).reset_index(drop=True)
    return df_output