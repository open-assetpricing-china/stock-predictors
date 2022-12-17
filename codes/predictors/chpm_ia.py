'''
@Author: Yuan Yang
@Email: yangy7@sustech.edu.cn
'''
# chpm: Change in income before extraordinary items scaled by scales.
# 'C001001000': Cash Received from Sales of Goods or Rendering of Services
# 'B001400000': Non-operating Income
#
import numpy as np
def equation(x):
    x['chpm'] = (x['B001400000'] / x['C001001000']).diff(periods=3)
    return x
#
def mean_value(x):
    x['chpm_ind_mean'] = x['chpm'].mean()
    return x
#
def fill_0(x):
    x.replace([0,], np.nan, inplace = True)
    x.fillna(method='ffill', inplace=True)
    return x
#
def lag_one_month(x):
    x = x.copy()
    x['chpm_ia'] = x['chpm_ia'].shift()
    return x
#
def calculation(df_input):
    df = df_input['monthly']
    df_output = df[['stkcd', 'month', 'B001400000','C001001000', 'ind_cd']]
    df_output = df_output.groupby('stkcd').apply(lambda x: equation(x)).reset_index(drop=True)
    df_output = df_output.groupby(['month', 'ind_cd']).apply(lambda x: mean_value(x)).reset_index(drop=True)
    df_output['chpm_ia'] = df_output['chpm'] - df_output['chpm_ind_mean']
    df_output = df_output.groupby('stkcd').apply(fill_0).reset_index(drop=True)
    df_output = df_output[['stkcd', 'month', 'chpm_ia']]
    df_output = df_output.groupby('stkcd').apply(lag_one_month).reset_index(drop=True)
    return df_output