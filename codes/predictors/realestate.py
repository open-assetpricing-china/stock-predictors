'''
@Author: Yuan Yang
@Email: messiyuan16@gmail.com
'''
# realestate: Investment real estates divided by fixed assets. Data are acquired from CSMAR
# 房地产：投资性房地产除以固定资产。从CSMAR获取数据
# Net Fixed Assets：df['A001212000']
# Net Investment Properties:df['A001211000']: 投资性房地产净额
# realestate = Net Investment Properties/Net Fixed Assets
# 'A001211000': Net Investment Properties
# 'A001212000': Net Fixed Assets
#
import numpy as np
def equation(x):
    x['realestate'] = (x['A001211000'] / x['A001212000']).shift() # lag one month
    return x
def check_divisor(x): # if divisor equals 0, it can lead the inf value appears. 
    x.loc[(x['A001212000']==0),'A001212000'] = np.nan
    return x
def calculation(df_input):
    df_output = df_input['monthly'][['stkcd', 'month', 'A001212000', 'A001211000' ]]
    df_output = check_divisor(df_output)
    df_output = df_output.groupby('stkcd').apply(equation).reset_index(drop=True)
    df_output = df_output[['stkcd', 'month', 'realestate']]
    return df_output
