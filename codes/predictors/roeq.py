'''
@Author: Yi Tian
@Email: 12232985@mail.sustech.edu.cn
'''
# roeq: Income before extraordinary items divided by lagged common shareholders’ equity
# Total Comprehensive Income: B006000000
# Total Shareholders’ Equity: A003000000
#
#
def equation(x):
    x['roeq'] = (x['B006000000'] / x['A003000000']).shift()
    return x
#
def calculation(df_input):
    df_output = df_input['monthly'][['stkcd', 'month', 'B006000000', 'A003000000']]
    df_output = df_output.groupby('stkcd').apply(equation).reset_index(drop=True)
    df_output = df_output[['stkcd', 'month', 'roeq']]
    return df_output
#
