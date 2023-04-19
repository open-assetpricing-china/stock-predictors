'''
@Author: Yuan Yang
@Email: messiyuan16@gmail.com
'''
# cash: cash and cash equivalents divided by average total assets.
# 'A001101000' : cash and cash equivalents
# 'A001000000' : Total Asset
import numpy as np
def lag_one_month(x):
    x = x.copy()
    x['cash'] = x['cash'].shift()
    return x
#
def check_divisor(x): # if divisor equals 0, it can lead the inf value appears. 
    x.loc[(x['A001000000']==0),'A001000000'] = np.nan
    return x
#
def calculation(df_input):
    df = df_input['monthly']
    df_output = df[['stkcd', 'month', 'A001101000', 'A001000000']]
    df_output = df_output.copy()
    df_output = check_divisor(df_output)
    df_output['cash'] = (df_output['A001101000'] / df_output['A001000000'])
    df_output = df_output[['stkcd', 'month', 'cash']]
    df_output = df_output.groupby('stkcd').apply(lambda x: lag_one_month(x)).reset_index(drop=True)
    return df_output
