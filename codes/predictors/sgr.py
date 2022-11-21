# sgr: Quarterly percentage change in sales
# 'C001001000': Cash Received from Sales of Goods or Rendering of Services
#
import numpy as np
def equation(x):
    x['sgr'] = x['C001001000'].pct_change(periods=3)
    return x
#
#
def fill_0(x):
    x.replace([0,], np.nan, inplace = True)
    x.fillna(method='ffill', inplace=True)
    return x
def calculation(df_input):
    df_output = df_input['monthly'][['stkcd', 'month', 'C001001000']]
    df_output = df_output.groupby('stkcd').apply(equation).reset_index(drop=True)
    df_output = df_output.groupby('stkcd').apply(fill_0).reset_index(drop=True)
    df_output = df_output[['stkcd', 'month', 'sgr']]
    return df_output