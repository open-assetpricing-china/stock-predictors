'''
@Author: Yuan Yang
@Email: messiyuan16@gmail.com
'''
# chpm: Change in income before extraordinary items scaled by scales.
# 'C001001000': Cash Received from Sales of Goods or Rendering of Services
# 'B001100000': Total Operating Revenue,
# The sum of all income arising from operating business of company.
#
import numpy as np
def equation(x):
    x['chpm'] = (x['C001001000'] / x['B001100000']).diff(periods=3)
    return x
def fill_0(x):
    x.replace([0,], np.nan, inplace = True)
    x.fillna(method='ffill', inplace=True)
    return x
def lag_one_month(x):
    x = x.copy()
    x['chpm'] = x['chpm'].shift()
    return x
#
def calculation(df_input):
    df = df_input['monthly']
    df_output = df[['stkcd', 'month', 'B001100000','C001001000']]
    df_output = df_output.groupby('stkcd').apply(lambda x: equation(x)).reset_index(drop=True)
    df_output = df_output.groupby('stkcd').apply(fill_0).reset_index(drop=True)
    df_output = df_output[['stkcd', 'month', 'chpm']]
    df_output = df_output.groupby('stkcd').apply(lag_one_month).reset_index(drop=True)
    return df_output