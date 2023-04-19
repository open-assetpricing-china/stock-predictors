'''
@Author: Yuan Yang
@Email: messiyuan16@gmail.com
'''
# lev : Total liabilities divided by quarter-end market capitalization
# 'A002000000': Total Liabilities
# 'Msmvttl': 'size'
import numpy as np
def equation(x):
    x['lev'] = x['A002000000'] / x['Msmvttl']
    return x
#
def lag_one_month(x):
    x = x.copy()
    x['lev'] = x['lev'].shift()
    return x
#
def check_divisor(x): # if divisor equals 0, it can lead the inf value appears. 
    x.loc[(x['Msmvttl']==0),'Msmvttl'] = np.nan
    return x
#
def calculation(df_input):
    df = df_input['monthly']
    df_output = df[['stkcd', 'month', 'A002000000','Msmvttl']]
    df_output = check_divisor(df_output)
    df_output = df_output.groupby('stkcd').apply(equation).reset_index(drop=True)
    df_output = df_output[['stkcd', 'month', 'lev']]
    df_output = df_output.groupby('stkcd').apply(lag_one_month).reset_index(drop=True) # lag one month
    return df_output