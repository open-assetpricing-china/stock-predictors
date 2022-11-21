# lgr : Quarterly percent change in total liabilities
# 'A002000000': Total Liabilities
#
import numpy as np
def equation(x):
    x['lgr'] = x['A002000000'].pct_change(periods=3)
    return x
#
def fill_0(x):
    x.replace([0,], np.nan, inplace = True)
    x.fillna(method='ffill', inplace=True)
    return x
#
def calculation(df_input):
    df = df_input['monthly']
    df_output = df[['stkcd', 'month', 'A002000000']]
    df_output = df_output.groupby('stkcd').apply(lambda x:equation(x)).reset_index(drop=True)
    df_output = df_output.groupby('stkcd').apply(fill_0).reset_index(drop=True)
    df_output = df_output[['stkcd', 'month', 'lgr']]
    return df_output