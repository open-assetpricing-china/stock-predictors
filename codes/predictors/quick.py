'''
@Author: Yuan Yang
@Email: messiyuan16@gmail.com
'''
# Quick ratio = (current assets - inventory) / current liabilities
# 'A001100000' : Total current Assets
# 'A002100000' : Total current Liabilities
# 'A001123000' : Net inventories
#
import numpy as np
def equation(x):
    x['quick'] = (x['A001100000'] - x['A001123000'])/ x['A002100000']
    return x
def check_divisor(x): # if divisor equals 0, it can lead the inf value appears. 
    x.loc[(x['A002100000']==0),'A002100000'] = np.nan
    return x
def lag_one_month(x):
    x = x.copy()
    x['quick'] = x['quick'].shift()
    return x

def calculation(df_input):
    df_output = df_input['monthly'][['stkcd', 'month', 'A001100000', 'A002100000', 'A001123000']]
    df_output = check_divisor(df_output)
    df_output = df_output.groupby('stkcd').apply(equation).reset_index(drop=True)
    df_output = df_output[['stkcd', 'month', 'quick']]
    df_output = df_output.groupby('stkcd').apply(lag_one_month).reset_index(drop=True)
    return df_output