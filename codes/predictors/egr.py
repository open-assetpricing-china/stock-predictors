'''
@Author: Yuan Yang
@Email: yangy7@sustech.edu.cn
'''
# egr: Quarterly percent change in book value of equity.
# 'A001000000' -> Total Asset
import numpy as np
def equation(x):
    x['egr'] = x['A001000000'].pct_change(periods=3)
    return x
#
def fill_0(x):
    x.replace([0,], np.nan, inplace = True)
    x.fillna(method='ffill', inplace=True)
    return x
#
def lag_one_month(x):
    x = x.copy()
    x['egr'] = x['egr'].shift()
    return x
#
def calculation(df_input):
    df = df_input['monthly']
    df_output = df[['stkcd', 'month', 'A001000000']]
    df_output = df_output.groupby('stkcd').apply(lambda x: equation(x)).reset_index(drop=True)
    df_output = df_output.groupby('stkcd').apply(fill_0).reset_index(drop=True)
    df_output =  df_output[['stkcd', 'month', 'egr']]
    df_output = df_output.groupby('stkcd').apply(lag_one_month).reset_index(drop=True) # lag one month
    return df_output