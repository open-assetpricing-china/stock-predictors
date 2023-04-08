'''
@Author: Yuan Yang
@Email: messiyuan16@gmail.com
'''
# salerev: Quarterly sales divided by accounts receivable
# 'C001001000' : Cash Received from Sales of Goods or Rendering of Services
# 'B001100000' : Total operating revenue, ==> sales
# 'A001111000' : Net Accounts Receivable
#
def equation(x):
    x['salerev'] = (x['B001100000'] / x['A001111000']).shift() # lag one month
    return x
#
def calculation(df_input):
    df_output = df_input['monthly'][['stkcd', 'month', 'B001100000', 'A001111000']]
    df_output = df_output.groupby('stkcd').apply(equation).reset_index(drop=True)
    df_output = df_output[['stkcd', 'month', 'salerev']]
    return df_output