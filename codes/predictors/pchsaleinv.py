'''
@Author: Yuan Yang
@Email: messiyuan16@gmail.com
'''
# pchsaleinv : Quarterly percentage change in sales-to-inventory.
# 'B001100000' : Total operating revenue, ==> sales
# 'A001123000' : Net Inventories
import numpy as np
def equation(x):
    x['pchsaleinv'] = (x['B001100000'] / x['A001123000']).pct_change(periods=3)
    return x
#
def fill_0(x):
    x.replace([0,], np.nan, inplace = True)
    x.fillna(method='ffill', inplace=True)
    return x
#
def lag_one_month(x):
    x = x.copy()
    x['pchsaleinv'] = x['pchsaleinv'].shift()
    return x
#
def calculation(df_input):
    df_output = df_input['monthly'][['stkcd', 'month', 'B001100000', 'A001123000']]
    df_output = df_output.groupby('stkcd').apply(equation).reset_index(drop=True)
    df_output = df_output.groupby('stkcd').apply(fill_0).reset_index(drop=True)
    df_output = df_output[['stkcd', 'month', 'pchsaleinv']]
    df_output = df_output.groupby('stkcd').apply(lag_one_month).reset_index(drop=True)
    return df_output
