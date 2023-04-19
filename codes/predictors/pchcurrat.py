'''
@Author: Yuan Yang
@Email: messiyuan16@gmail.com
'''
# pchcurrat: Percentage change in current ratio (current liabilities divided by
# current asset)
# 'A001100000' : total current assets
# 'A002100000' : total current liabilities
import numpy as np
def equation(x):
    x['pchcurrat'] = (x['A002100000'] / x['A001100000']).pct_change(periods=3)
    return x
#
def fill_0(x):
    x.replace([0,], np.nan, inplace = True)
    x.fillna(method='ffill', inplace=True)
    return x
#
def check_divisor(x): # if divisor equals 0, it can lead the inf value appears. 
    x.loc[(x['A001100000']==0),'A001100000'] = np.nan
    return x
#
def lag_one_month(x):
    x = x.copy()
    x['pchcurrat'] = x['pchcurrat'].shift()
    return x
#
def calculation(df_input):
    df_output = df_input['monthly'][['stkcd', 'month', 'A002100000','A001100000']]
    df_output = check_divisor(df_output)
    df_output = df_output.groupby('stkcd').apply(equation).reset_index(drop=True)
    df_output = df_output.groupby('stkcd').apply(fill_0).reset_index(drop=True)
    df_output = df_output[['stkcd', 'month', 'pchcurrat']]
    df_output = df_output.groupby('stkcd').apply(lag_one_month).reset_index(drop=True)
    return df_output
#
