'''
@Author: Yuan Yang
@Email: messiyuan16@gmail.com
'''
# cashspr: Cash productivity, which is defined as quarter-end market capitalization plus
# long-term debt minus total assets divided by cash and equivalents.
#
# (size + long term debt - total assets) / (cash and cash equivalents)
# 'size': size
# 'A002201000': Long-term Debts
# 'A001000000': total assets
# 'A001101000': cash and cash equivalents
# 'Msmvttl' : size
import numpy as np
def equation(x):
    x = x.copy()
    x['cashspr'] = (x['Msmvttl'] + x['A002201000'] -x['A001000000']).shift() / x['A001101000'].shift() # lag one month
    return x
#
def check_divisor(x): # if divisor equals 0, it can lead the inf value appears. 
    x.loc[(x['A001101000']==0),'A001101000'] = np.nan
    return x
#
def calculation(df_input):
    df = df_input['monthly']
    df_output = df[['stkcd', 'month','Msmvttl','A002201000', 'A001000000', 'A001101000' ]]
    df_output = check_divisor(df_output)
    df_output = df_output.groupby('stkcd').apply(lambda x: equation(x)).reset_index(drop=True)
    df_output = df_output[['stkcd', 'month','cashspr']]
    return df_output