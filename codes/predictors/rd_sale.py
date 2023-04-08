'''
@Author: Yuan Yang
@Email: messiyuan16@gmail.com
'''
# rd_sale: R&D expense divided by quarterly sales
# 'A001219000' : R&D expenses
# 'B001100000' : Total operating revenue, ==> sales
def equation(x):
    x['rd_sale'] = (x['A001219000'] / x['B001100000']).shift() # lag one month
    return x
#
def calculation(df_input):
    df_output = df_input['monthly'][['stkcd', 'month', 'B001100000', 'A001219000']]
    df_output = df_output.groupby('stkcd').apply(equation).reset_index(drop=True)
    df_output = df_output[['stkcd', 'month', 'rd_sale']]
    return df_output