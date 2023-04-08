'''
@Author: Yuan Yang
@Email: messiyuan16@gmail.com
'''
# Natural log of market capitalization at end of month t-1
# 'Msmvttl': 'size'
import numpy as np
def equation(x):
    x['mve'] = np.log(x['Msmvttl']).shift(1) # lag one month
    return x
#
def calculation(df_input):
    df = df_input['monthly']
    df_output = df[['stkcd', 'month', 'Msmvttl']]
    df_output = df_output.groupby('stkcd').apply(equation).reset_index(drop=True)
    df_output = df_output[['stkcd', 'month', 'mve']]
    return df_output