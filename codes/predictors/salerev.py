'''
@Author: Yuan Yang
@Email: yangy7@sustech.edu.cn
'''
# salerev: Quarterly sales divided by accounts receivable
# 'C001001000' : Cash Received from Sales of Goods or Rendering of Services
# 'A001111000' : Net Accounts Receivable
#
def equation(x):
    x['salerev'] = (x['C001001000'] / x['A001111000']).shift() # lag one month
    return x
#
def calculation(df_input):
    df_output = df_input['monthly'][['stkcd', 'month', 'C001001000', 'A001111000']]
    df_output = df_output.groupby('stkcd').apply(equation).reset_index(drop=True)
    df_output = df_output[['stkcd', 'month', 'salerev']]
    return df_output