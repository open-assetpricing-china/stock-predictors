'''
@Author: Yuan Yang
@Email: yangy7@sustech.edu.cn
'''
# Natural log of market capitalization at end of month t-1
# 'Msmvttl' : 'size
import numpy as np
#
def equation(x):
    x['mve'] = np.log(x['Msmvttl']).shift(1) # lag one month
    return x
#
def mean_value(x):
    x['mve_ind'] = x['mve'].mean()
    return x
#
def calculation(df_input):
    df = df_input['monthly']
    df_output = df[['stkcd', 'month', 'Msmvttl', 'ind_cd']]
    df_output = df_output.groupby('stkcd').apply(equation).reset_index(drop=True)
    df_output = df_output.groupby(['month', 'ind_cd']).apply(mean_value).reset_index(drop=True)
    df_output['mve_ia'] = df_output['mve'] - df_output['mve_ind']
    df_output = df_output[['stkcd', 'month', 'mve_ia']]
    return df_output