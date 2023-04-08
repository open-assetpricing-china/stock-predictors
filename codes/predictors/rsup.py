'''
@Author: Yuan Yang
@Email: messiyuan16@gmail.com
'''
# rsup: Sales from quarter t minus sales from quarter t − 1 divided by quarter-end market capitalization.
# 'B001100000' : Total operating revenue, ==> sales
# 'Msmvttl' : size
import numpy as np
def equation(x):
    x['rsup'] = (x['B001100000'] - x['B001100000'].shift(3)) / x['Msmvttl']
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
    df_output = df_input['monthly'][['stkcd','month', 'Msmvttl', 'B001100000']]
    df_output = df_output.groupby('stkcd').apply(equation).reset_index(drop=True)
    df_output = df_output.groupby('stkcd').apply(fill_0).reset_index(drop=True)
    df_output = df_output[['stkcd', 'month', 'rsup']]
    df_output = df_output.groupby('stkcd').apply(lag_one_month).reset_index(drop=True)
    return df_output