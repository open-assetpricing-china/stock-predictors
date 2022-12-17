'''
@Author: Yuan Yang
@Email: yangy7@sustech.edu.cn
'''
# pchquick: Percentage change in quick ratio.
# Quick Ratio = (Current assets - Inventory - Prepaid expenses) / Current Liabilities
# 'A001100000' : Total Current Assets
# 'A001123000' : Net inventories
# 'A001112000' : Net Prepayments
# 'A002100000' : Total Current Liabilities
#
import numpy as np
def equation(x):
    x['pchquick'] = ((x['A001100000'] - x['A001123000'] - x['A001112000'] ) / x['A002100000']
                           ).pct_change(periods=3)
    return x
#
def fill_0(x):
    x.replace([0,], np.nan, inplace = True)
    x.fillna(method='ffill', inplace=True)
    return x
#
def lag_one_month(x):
    x = x.copy()
    x['pchquick'] = x['pchquick'].shift()
    return x
#
def calculation(df_input):
    df_output = df_input['monthly'][['stkcd', 'month', 'A001100000', 'A001123000', 'A001112000', 'A002100000' ]]
    df_output = df_output.groupby('stkcd').apply(equation).reset_index(drop=True)
    df_output = df_output.groupby('stkcd').apply(fill_0).reset_index(drop=True)
    df_output = df_output[['stkcd', 'month', 'pchquick']]
    df_output = df_output.groupby('stkcd').apply(lag_one_month).reset_index(drop=True)
    return df_output
