'''
@Author: Yuan Yang
@Email: yangy7@sustech.edu.cn
'''
# pchgm_pchsale : Percentage change in gross margin minus Percentage
# change in sales.
# 'C001001000' : Cash Received from Sales of Goods or Rendering of Services
# 'B001209000' : Selling Expenses
#
import numpy as  np
def equation(x):
    x['pchgm_pchsale'] = ((x['C001001000'] - x['B001209000']) / x['C001001000']
                           ).pct_change(periods=3) - x['C001001000'].pct_change(periods=3)
    return x
#
def fill_0(x):
    x.replace([0,], np.nan, inplace = True)
    x.fillna(method='ffill', inplace=True)
    return x
#
def lag_one_month(x):
    x = x.copy()
    x['pchgm_pchsale'] = x['pchgm_pchsale'].shift()
    return x
def calculation(df_input):
    df_output = df_input['monthly'][['stkcd', 'month', 'C001001000', 'B001209000']]
    df_output = df_output.groupby('stkcd').apply(equation).reset_index(drop=True)
    df_output = df_output.groupby('stkcd').apply(fill_0).reset_index(drop=True)
    df_output = df_output[['stkcd', 'month', 'pchgm_pchsale']]
    df_output = df_output.groupby('stkcd').apply(lag_one_month).reset_index(drop=True)
    return df_output