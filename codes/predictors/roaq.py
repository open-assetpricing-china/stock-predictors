'''
@Author: Yuan Yang
@Email: messiyuan16@gmail.com
'''
# roaq = Income before extraordinary items/one quarter lagged total assets
# 'B001100000': Total Operating Revenue, The sum of all income arising from operating business of the company.
# A001000000: Total assets
#
import numpy as np
def equation(x):
    x['roaq'] = x['B001100000'] / x['A001000000'].shift(3)
    return x
#
def check_divisor(x): # if divisor equals 0, it can lead the inf value appears. 
    x.loc[(x['A001000000']==0),'A001000000'] = np.nan
    return x
#
def lag_one_month(x):
    x = x.copy()
    x['roaq'] = x['roaq'].shift()
    return x
#
def calculation(df_input):
    df_output = df_input['monthly'][['stkcd', 'month', 'B001100000', 'A001000000']]
    df_output = check_divisor(df_output)
    df_output = df_output.groupby('stkcd').apply(equation).reset_index(drop=True)
    df_output = df_output[['stkcd', 'month', 'roaq' ]]
    df_output = df_output.groupby('stkcd').apply(lag_one_month).reset_index(drop=True)
    return df_output
