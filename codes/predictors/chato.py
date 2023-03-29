'''
@Author: Yuan Yang
@Email: yangy7@sustech.edu.cn
'''
# Change in sales divided by average total assets
# 'C001001000': Cash Received from Sales of Goods or Rendering of Services
# 'A001000000': Total Assets
import numpy as np
def equation(x):
    x = x.copy()
    x['chato'] = (x['C001001000'] / x['A001000000']).diff(periods=3)
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
def calculation(df_input):
    df = df_input['monthly']
    df_output = df[['stkcd', 'month', 'C001001000','A001000000' ]]
    df_output = df_output.groupby('stkcd').apply(lambda x: equation(x)).reset_index(drop=True)
    df_output = df_output.groupby('stkcd').apply(fill_0).reset_index(drop=True)
    df_output = df_output[['stkcd', 'month', 'chato']]
    df_output = df_output.groupby('stkcd').apply(lambda x: lag_one_month(x)).reset_index(drop=True)
    return df_output