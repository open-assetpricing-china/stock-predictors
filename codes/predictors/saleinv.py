'''
@Author: Yuan Yang
@Email: yangy7@sustech.edu.cn
'''
# saleinv: Quarterly sales divided by total inventory
# 'C001001000' : Cash Received from Sales of Goods or Rendering of Services
# 'A001123000' : Net inventories

def equation(x):
    x['saleinv'] = (x['C001001000'] / x['A001123000']).shift()
    return x
#
def calculation(df_input):
    df_output = df_input['monthly'][['stkcd', 'month','C001001000', 'A001123000']]
    df_output = df_output.groupby('stkcd').apply(equation).reset_index(drop=True)
    df_output = df_output[['stkcd', 'month', 'saleinv']]
    return df_output