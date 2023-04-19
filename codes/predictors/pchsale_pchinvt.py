'''
@Author: Yuan Yang
@Email: messiyuan16@gmail.com
'''
# Quarterly percentage change in sales minus quarterly percentage change in inventory.
# 'A001123000' : Net inventories
# 'B001100000' : Total operating revenue, ==> sales
import numpy as np
def equation(x):
    x['pchsale_pchinvt'] = x['B001100000'].pct_change(periods=3) - x['A001123000'].pct_change(periods=3)
    return x
#
def check_divisor(x): # if divisor equals 0, it can lead the inf value appears. 
    x.loc[(x['B001100000']==0),'B001100000'] = np.nan
    x.loc[(x['A001123000']==0),'A001123000'] = np.nan
    return x
#
def fill_0(x):
    x.replace([0,], np.nan, inplace = True)
    x.fillna(method='ffill', inplace=True)
    return x
#
def lag_one_month(x):
    x = x.copy()
    x['pchsale_pchinvt'] = x['pchsale_pchinvt'].shift()
    return x
#
def calculation(df_input):
    df_output = df_input['monthly'][['stkcd', 'month', 'B001100000', 'A001123000']]
    df_output = check_divisor(df_output)
    df_output = df_output.groupby('stkcd').apply(equation).reset_index(drop=True)
    df_output = df_output.groupby('stkcd').apply(fill_0).reset_index(drop=True)
    df_output = df_output[['stkcd', 'month', 'pchsale_pchinvt']]
    df_output = df_output.groupby('stkcd').apply(lag_one_month).reset_index(drop=True)
    return df_output