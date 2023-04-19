'''
@Author: Yuan Yang
@Email: messiyuan16@gmail.com
'''
# Change in sales divided by average total assets
# 'B001100000' : Total operating revenue, ==> sales
# 'A001000000': Total Assets
import numpy as np
def equation(x):
    x = x.copy()
    x['chato'] = (x['B001100000'] / x['A001000000']).diff(periods=3)
    return x
#
def fill_0(x):
    x.replace([0,], np.nan, inplace = True)
    x.fillna(method='ffill', inplace=True)
    return x
#
def lag_one_month(x):
    x = x.copy()
    x['chato'] = x['chato'].shift()
    return x
#
def check_divisor(x): # if divisor equals 0, it can lead the inf value appears. 
    x.loc[(x['A001000000']==0),'A001000000'] = np.nan
    return x
#
def calculation(df_input):
    df = df_input['monthly']
    df_output = df[['stkcd', 'month', 'B001100000','A001000000' ]]
    df_output = check_divisor(df_output)
    df_output = df_output.groupby('stkcd').apply(lambda x: equation(x)).reset_index(drop=True)
    df_output = df_output.groupby('stkcd').apply(fill_0).reset_index(drop=True)
    df_output = df_output[['stkcd', 'month', 'chato']]
    df_output = df_output.groupby('stkcd').apply(lambda x: lag_one_month(x)).reset_index(drop=True)
    return df_output