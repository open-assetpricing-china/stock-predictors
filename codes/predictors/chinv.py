# chinv: Change in inventory scaled by total assets
# 'A001123000' : Net Inventories 净存货
# 'A001000000' :  total asset
#
import numpy as np
def equation(x):
    x['chinv'] = (x['A001123000'] / x['A001000000']).diff(periods=3)
    return x
#
def fill_0(x):
    x.replace([0,], np.nan, inplace = True)
    x.fillna(method='ffill', inplace=True)
    return x

def calculation(df_input):
    df = df_input['monthly']
    df_output = df[['stkcd', 'month', 'A001123000','A001000000']]
    df_output = df_output.groupby('stkcd').apply(equation).reset_index(drop=True)
    df_output = df_output.groupby('stkcd').apply(fill_0).reset_index(drop=True)
    df_output = df_output[['stkcd', 'month', 'chinv']]
    return df_output