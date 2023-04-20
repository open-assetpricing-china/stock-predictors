'''
@Author: Yuan Yang
@Email: messiyuan16@gmail.com
'''
import numpy as np
# roeq: Income before extraordinary items divided by lagged common shareholders’ equity
# 'B001100000': Total Operating Revenue, The sum of all income arising from operating business of the company.
# 'A003000000': Total Shareholders’ Equity
def equation(x):
    x['roeq'] = (x['B001100000'] / x['A003000000']).shift() # lag one month
    return x
#
def check_divisor(x): # if divisor equals 0, it can lead the inf value appears. 
    x.loc[(x['A003000000']==0),'A003000000'] = np.nan
    return x
#
def calculation(df_input):
    df_output = df_input['monthly'][['stkcd', 'month', 'B001100000', 'A003000000']]
    df_output = check_divisor(df_output)
    df_output = df_output.groupby('stkcd').apply(equation).reset_index(drop=True)
    df_output = df_output[['stkcd', 'month', 'roeq']]
    return df_output
#
