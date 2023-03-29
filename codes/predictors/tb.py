'''
@Author: Yuan Yang
@Email: yangy7@sustech.edu.cn
'''
# tb = (current tax expense / enterprise income tax rate in China(25%))/total income
# B002100000: Income Tax Expenses
# B006000000: Total Comprehensive Income #
def equation(x):
    x['tb'] = (x['B002100000'] / 0.25).shift() / x['B006000000'].shift() # lag one month
    return x
#
def calculation(df_input):
    df_output = df_input['monthly'][['stkcd', 'month', 'B006000000', 'B002100000']]
    df_output = df_output.groupby('stkcd').apply(equation).reset_index(drop=True)
    df_output = df_output[['stkcd', 'month', 'tb']]
    return df_output