'''
@Author: Yuan Yang
@Email: messiyuan16@gmail.com
'''
# rd_sale: R&D expense divided by quarterly sales
# 'A001219000' : R&D expenses
# 'B001100000' : Total operating revenue, ==> sales
import numpy as np
def equation(x):
    x['rd_sale'] = (x['A001219000'] / x['B001100000']).shift() # lag one month
    return x
#
def check_divisor(x): # if divisor equals 0, it can lead the inf value appears. 
    x.loc[(x['B001100000']==0),'B001100000'] = np.nan
    return x
#
def calculation(df_input):
    df_output = df_input['monthly'][['stkcd', 'month', 'B001100000', 'A001219000']]
    df_output = check_divisor(df_output)
    df_output = df_output.groupby('stkcd').apply(equation).reset_index(drop=True)
    df_output = df_output[['stkcd', 'month', 'rd_sale']]
    return df_output