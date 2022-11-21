# pchsaleinv : Quarterly percentage change in sales-to-inventory.
# D000113000 : Decrease of Inventories
#
import numpy as np
def equation(x):
    x['pchsaleinv'] = x['D000113000'].pct_change(periods=3)
    return x
#
def fill_0(x):
    x.replace([0,], np.nan, inplace = True)
    x.fillna(method='ffill', inplace=True)
    return x
#
def calculation(df_input):
    df_output = df_input['monthly'][['stkcd', 'month', 'D000113000']]
    df_output = df_output.groupby('stkcd').apply(equation).reset_index(drop=True)
    df_output = df_output.groupby('stkcd').apply(fill_0).reset_index(drop=True)
    df_output = df_output[['stkcd', 'month', 'pchsaleinv']]
    return df_output
