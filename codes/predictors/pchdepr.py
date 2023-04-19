'''
@Author: Yuan Yang
@Email: messiyuan16@gmail.com
'''
# pchdepr : Percentage change in depreciation
# 'D000103000' : Depreciation of Fixed Assets, Oil and Gas Assets, and Bearer Biological Assets.
#
import numpy as np
def equation(x):
    x['pchdepr'] = x['D000103000'].pct_change(periods=3)
    return x
#
def fill_0(x):
    x.replace([0,], np.nan, inplace = True)
    x.fillna(method='ffill', inplace=True)
    return x
#
def check_divisor(x): # if divisor equals 0, it can lead the inf value appears. 
    x.loc[(x['D000103000']==0),'D000103000'] = np.nan
    return x
#
def lag_one_month(x):
    x = x.copy()
    x['pchdepr'] = x['pchdepr'].shift()
    return x
#
def calculation(df_input):
    df_output = df_input['monthly'][['stkcd', 'month', 'D000103000']]
    df_output = check_divisor(df_output)
    df_output = df_output.groupby('stkcd').apply(equation).reset_index(drop=True)
    df_output = df_output.groupby('stkcd').apply(fill_0).reset_index(drop=True)
    df_output = df_output[['stkcd', 'month', 'pchdepr']]
    df_output = df_output.groupby('stkcd').apply(lag_one_month).reset_index(drop=True)
    return df_output