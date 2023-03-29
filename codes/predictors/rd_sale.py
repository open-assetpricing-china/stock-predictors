'''
@Author: Yuan Yang
@Email: yangy7@sustech.edu.cn
'''
# rd_sale: R&D expense divided by quarterly sales
# 'A001219000' : R&D expenses
# 'C001001000': Cash Received from Sales of Goods or Rendering of Services
def equation(x):
    x['rd_sale'] = (x['A001219000'] / x['C001001000']).shift() # lag one month
    return x
#
def calculation(df_input):
    df_output = df_input['monthly'][['stkcd', 'month', 'C001001000', 'A001219000']]
    df_output = df_output.groupby('stkcd').apply(equation).reset_index(drop=True)
    df_output = df_output[['stkcd', 'month', 'rd_sale']]
    return df_output