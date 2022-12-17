'''
@Author: Yi Tian
@Email: 12232985@mail.sustech.edu.cn
'''
# Total Comprehensive Income: df['B006000000']
# Total assets: A001000000
# roaq = Income before extraordinary items/one quarter lagged total assets
#
def equation(x):
    x['roaq'] = x['B006000000'] / x['A001000000'].shift(3)
    return x
#
def calculation(df_input):
    df_output = df_input['monthly'][['stkcd', 'month', 'B006000000', 'A001000000']]
    df_output = df_output.groupby('stkcd').apply(equation).reset_index(drop=True)
    df_output = df_output[['stkcd', 'month', 'roaq' ]]
    return df_output
