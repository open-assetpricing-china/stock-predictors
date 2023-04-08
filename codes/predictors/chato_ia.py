'''
@Author: Yuan Yang
@Email: messiyuan16@gmail.com
'''
# industry-adjusted chato
# 'B001100000' : Total operating revenue, ==> sales
# 'A001000000': Total Assets
import numpy as np
def equation(x):
    x = x.copy()
    x['chato'] = (x['B001100000'] / x['A001000000']).diff(periods=3)
    return x
#
def mean_value(x):
    x['chato_ind_mean'] = x['chato'].mean()
    return x
#
def fill_0(x):
    x.replace([0,], np.nan, inplace = True)
    x.fillna(method='ffill', inplace=True)
    return x
#
def lag_one_month(x):
    x = x.copy()
    x['chato_ia'] = x['chato_ia'].shift()
    return x
#
def calculation(df_input):
    df = df_input['monthly']
    df_output = df[['stkcd', 'month', 'B001100000','A001000000','ind_cd' ]]
    df_output = df_output.groupby('stkcd').apply(lambda x: equation(x)).reset_index(drop=True)
    df_output = df_output.groupby(['month','ind_cd']).apply(lambda x:mean_value(x)).reset_index(drop=True)
    df_output['chato_ia'] = df_output['chato'] - df_output['chato_ind_mean']
    df_output = df_output.groupby('stkcd').apply(fill_0).reset_index(drop=True)
    df_output = df_output[['stkcd', 'month', 'chato_ia']]
    df_output = df_output.groupby('stkcd').apply(lag_one_month).reset_index(drop=True)
    return df_output