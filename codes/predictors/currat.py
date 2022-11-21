# currrat: The ratio of current assets to current liabilities
# 'A001100000', current assets
# 'A002100000', current liabilities
import numpy as np
def equation(x):
    x['currat'] = x['A001100000'] / x['A002100000']
    return x
def fill_0(x):
    x.replace([0,], np.nan, inplace = True)
    x.fillna(method='ffill', inplace=True)
    return x
def calculation(df_input):
    df = df_input['monthly']
    df_output = df[['stkcd', 'month', 'A001100000', 'A002100000']]
    df_output = df_output.groupby('stkcd').apply(lambda x: equation(x)).reset_index(drop=True)
    df_output = df_output.groupby('stkcd').apply(fill_0).reset_index(drop=True)
    df_output = df_output[['stkcd', 'month', 'currat']]
    return df_output