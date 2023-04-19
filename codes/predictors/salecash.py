'''
@Author: Yuan Yang
@Email: messiyuan16@gmail.com
'''
# salecash: Quarterly sales divided by cash and cash equivalents
# 'B001100000' : Total operating revenue, ==> sales
# 'A001101000' : cash and cash equivalents
#
import numpy as np
def equation(x):
    x['salecash'] = (x['B001100000'] / x['A001101000']).shift() # lag one month
    return x
def check_divisor(x): # if divisor equals 0, it can lead the inf value appears. 
    x.loc[(x['A001101000']==0),'A001101000'] = np.nan
    return x
def calculation(df_input):
    df_output = df_input['monthly'][['stkcd', 'month','B001100000', 'A001101000']]
    df_output = check_divisor(df_output)
    df_output = df_output.groupby('stkcd').apply(equation).reset_index(drop=True)
    df_output = df_output[['stkcd', 'month', 'salecash']]
    return df_output