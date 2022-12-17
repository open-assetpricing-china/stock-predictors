'''
@Author: Yuan Yang
@Email: yangy7@sustech.edu.cn
'''
# gma: Revenue minus cost of goods sold divided by lagged total assets.
# 'B001100000' : Total Revenue
# 'C001001000' : Cash Received from Sales of Goods or Rendering of Services
# df['A001000000'] -> Total Asset
#
def equation(x):
    x['gma'] = (x['B001100000'] - x['C001001000']) / x['A001000000'].shift(3)
    return x
#
def calculation(df_input):
    df = df_input['monthly']
    df_output = df[['stkcd', 'month', 'B001100000','C001001000','A001000000']]
    df_output = df_output.groupby('stkcd').apply(lambda x: equation(x)).reset_index(drop=True)
    df_output = df_output[['stkcd', 'month', 'gma']]
    return df_output