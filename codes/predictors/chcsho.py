'''
@Author: Yuan Yang
@Email: messiyuan16@gmail.com
'''
#
# Monthly percent change in shares outstanding
# 'Msmvttl' : 'size'
import numpy as np
def equation(x):
    x = x.copy()
    x['chcsho'] = (x['Msmvttl'] / x['Mclsprc']).pct_change()
    return x
#
def lag_one_month(x):
    x = x.copy()
    x['chcsho'] = x['chcsho'].shift()
    return x
#
def check_divisor(x): # if divisor equals 0, it can lead the inf value appears. 
    x.loc[(x['Mclsprc']==0),'Mclsprc'] = np.nan
    return x
#
def calculation(df_input):
    df = df_input['monthly']
    df_output = df[['stkcd', 'month', 'Msmvttl', 'Mclsprc']]
    df_output = check_divisor(df_output)
    df_output = df_output.groupby('stkcd').apply(lambda x: equation(x)).reset_index(drop=True)
    df_output = df_output[['stkcd', 'month', 'chcsho']]
    df_output = df_output.groupby('stkcd').apply(lambda x: lag_one_month(x)).reset_index(drop=True)
    return df_output