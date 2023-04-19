'''
@Author: Yuan Yang
@Email: messiyuan16@gmail.com
'''
# dolvol : Natural logarithm of trading volume times price per share from month t-2
# 'Mnvaltrd':  'Value of Shares Traded in Month (MNVALTRD)'  # 当月交易的股票价值（MNVALTRD）
import numpy as np
#
def equation(x):
    x['dolvol'] = np.log(x['Mnvaltrd']).shift(2) # lag two month
    return x
#
def check_divisor(x): # if divisor equals 0, it can lead the inf value appears. 
    x.loc[(x['Mnvaltrd']==0),'Mnvaltrd'] = np.nan
    return x
#
def calculation(df_input):
    df = df_input['monthly']
    df_output = df[['stkcd', 'month', 'Mnvaltrd']]
    df_output = check_divisor(df_output)
    df_output = df_output.groupby('stkcd').apply(lambda x: equation(x)).reset_index(drop=True)
    df_output = df_output[['stkcd', 'month', 'dolvol']]
    return df_output
